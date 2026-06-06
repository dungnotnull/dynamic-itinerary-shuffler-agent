import asyncio
import logging
import json
from datetime import datetime
from typing import Dict, Any, List
from app.core.config import settings
from app.models.database import db_manager, Itinerary, ItineraryStop, Venue
from sqlalchemy.orm import Session
import httpx

logger = logging.getLogger("DisruptionEngine")

class DisruptionEngine:
    """
    Core logic for detecting environmental disruptions and triggering re-optimization.
    """
    def __init__(self, redis_client):
        self.redis = redis_client
        self.http_client = httpx.AsyncClient()

    async def poll_weather(self, lat: float, lon: float) -> Dict[str, Any]:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={settings.openweathermap_api_key}"
        try:
            response = await self.http_client.get(url)
            data = response.json()
            rain = data.get("rain", {}).get("1h", 0)
            weather_main = data.get("weather", [{}])[0].get("main", "")
            if rain > 5.0 or weather_main in ["Storm", "Rain", "Snow"]:
                return {"disrupted": True, "reason": f"Weather condition: {weather_main}", "type": "weather"}
            return {"disrupted": False}
        except Exception as e:
            logger.error(f"Weather poll failed: {e}")
            return {"disrupted": False, "error": str(e)}

    async def poll_traffic(self, origin: str, destination: str) -> Dict[str, Any]:
        url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}&destinations={destination}&key={settings.google_maps_api_key}"
        try:
            response = await self.http_client.get(url)
            data = response.json()
            status = data.get("rows", [{}])[0].get("elements", [{}])[0]
            duration_in_traffic = status.get("duration_in_traffic", {}).get("value", 0)
            duration_normal = status.get("duration", {}).get("value", 0)
            if duration_in_traffic > duration_normal * 1.5:
                return {"disrupted": True, "reason": "Heavy traffic congestion", "type": "traffic"}
            return {"disrupted": False}
        except Exception as e:
            logger.error(f"Traffic poll failed: {e}")
            return {"disrupted": False, "error": str(e)}

    async def monitor_active_itineraries(self):
        db: Session = next(db_manager.get_db())
        active_trips = db.query(Itinerary).filter(Itinerary.status == "active").all()
        for trip in active_trips:
            current_stop = db.query(ItineraryStop).filter(
                ItineraryStop.itinerary_id == trip.id, 
                ItineraryStop.sequence_order == 0
            ).first()
            if not current_stop: continue
            venue = current_stop.venue
            weather_res = await self.poll_weather(venue.latitude, venue.longitude)
            if weather_res.get("disexecuted"): # Changed from disrupted to avoided typo
                await self.trigger_reoptimization(trip.id, weather_res)

    async def trigger_reoptimization(self, itinerary_id: int, reason: Dict[str, Any]):
        event = {
            "itinerary_id": itinerary_id,
            "timestamp": datetime.utcnow().isoformat(),
            "reason": reason.get("reason"),
            "type": reason.get("type")
        }
        logger.warning(f"SENSING DISRUPTION for Trip {itinerary_id}: {reason.get('reason')}")
        self.redis.rpush("disruption_queue", json.dumps(event))
