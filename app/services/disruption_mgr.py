from apscheduler.schedulers.background import BackgroundScheduler
from typing import List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DisruptionMgr")

class DisruptionManager:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.scheduler = BackgroundScheduler()

    def start(self):
        # Poll weather/traffic every 5 minutes for all active itineraries
        self.scheduler.add_job(self.check_disruptions, "interval", minutes=5)
        self.scheduler.start()
        logger.info("Disruption Manager started: Polling every 5 mins")

    def check_disruptions(self):
        logger.info("Checking for environmental disruptions...")
        # Logic: 
        # 1. Query DB for itineraries with status='active'
        # 2. For each itinerary:
        #    a. Fetch OpenWeatherMap for current location
        #    b. Fetch Google Maps Traffic for next segment
        #    c. If precipitation > 60% or traffic speed < threshold -> Trigger Event
        pass

    def trigger_disruption_event(self, itinerary_id: int, event_type: str, details: Dict[str, Any]):
        logger.warning(f"DISRUPTION DETECTED for {itinerary_id}: {event_type}")
        # Push to Redis Queue for the Re-Optimizer to pick up
        event = {"itinerary_id": itinerary_id, "type": event_type, "details": details}
        self.redis.rpush("disruption_queue", str(event))
