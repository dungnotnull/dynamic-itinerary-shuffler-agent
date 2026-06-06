import asyncio
import logging
import json
from app.core.mock_gateway import mock_gateway
from app.services.disruption_engine import DisruptionEngine
from app.services.venue_ranker import VenueRanker
from app.services.optimizer import VRPTWSolver
from app.models.database import db_manager, Itinerary, ItineraryStop, Venue
from unittest.mock import MagicMock

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SImulator")

class FullSystemSimulator:
    def __init__(self):
        self.redis_mock = MagicMockRedis()
        self.engine = DisruptionEngine(self.redis_mock)
        self.ranker = VenueRanker()
        
    async def run_scenario(self):
        logger.info("🚀 STARTING FAST SIMULATION")
        db = next(db_manager.get_db())
        trip = db.query(Itinerary).filter(Itinerary.status == "active").first()
        if not trip: return
        
        logger.info(f"Sensing... 🌧️  DISRUPTION DETECTED: Heavy Rain!")
        outdoor_stop = db.query(ItineraryStop).join(Venue).filter(
            ItineraryStop.itinerary_id == trip.id, Venue.category == "Nature"
        ).first()
        
        if outdoor_stop:
            candidates = await mock_gateway.get_foursquare_alternatives("Art", 10.7, 106.6)
            for c in candidates: c['embedding'] = [0.1] * 384 
            
            user_profile = {"vibe": "artsy", "interests": "galleries"}
            selection = await self.ranker.rank_alternatives(user_profile, candidates)
            logger.info(f"AI Selection: {selection['selected_venue']['name']}")
            
            new_dist_matrix = [[0, 10, 15, 20], [10, 0, 25, 30], [15, 25, 0, 10], [20, 30, 10, 0]]
            solver = VRPTWSolver(new_dist_matrix, [(0,100)]*4, [0]*4)
            result = solver.solve()
            logger.info(f"✅ ITINERARY HEALED. New Optimal Route: {result['route']}")

class MagicMockRedis:
    def __init__(self): self.data = {}
    def rpush(self, key, val): 
        if key not in self.data: self.data[key] = []
        self.data[key].append(val)

if __name__ == "__main__":
    sim = FullSystemSimulator()
    asyncio.run(sim.run_scenario())
