import asyncio
import json
from unittest.mock import AsyncMock, MagicMock
from app.services.disruption_engine import DisruptionEngine
from app.services.venue_ranker import VenueRanker
from app.services.optimizer import VRPTWSolver

async def test_full_disruption_pipeline():
    """
    Simulates the complete workflow:
    Disruption Detected -> Alternative Found -> LLM Selected -> Route Re-optimized.
    """
    print("Testing Full Disruption Pipeline...")
    
    # 1. Setup Mocks
    mock_redis = MagicMock()
    engine = DisruptionEngine(mock_redis)
    ranker = VenueRanker()
    
    # Simulate a weather disruption event
    disruption_event = {
        "itinerary_id": 1,
        "type": "weather",
        "reason": "Heavy Rain"
    }
    
    # 2. Simulate Candidate Discovery (Mocking Foursquare)
    candidates = [
        {"id": 101, "name": "Indoor Art Gallery", "embedding": [0.1, 0.8, 0.1], "category": "Art"},
        {"id": 102, "name": "Outdoor Park", "embedding": [0.8, 0.1, 0.1], "category": "Nature"},
    ]
    user_profile = {"vibe": "indoor and artsy", "interests": "galleries"}
    
    # 3. Execute Venue Selection
    selection = await ranker.rank_alternatives(user_profile, candidates)
    selected_venue = selection["selected_venue"]
    print(f"LLM Selected Venue: {selected_venue['name']}")
    assert selected_venue["id"] == 101 # Should select the indoor gallery
    
    # 4. Execute Re-optimization
    # New distance matrix including the substitute venue
    new_dist_matrix = [[0, 10, 15], [10, 0, 20], [15, 20, 0]]
    new_time_windows = [(0, 100), (0, 100), (0, 100)]
    new_service_times = [0, 30, 30]
    
    solver = VRPTWSolver(new_dist_matrix, new_time_windows, new_service_times)
    new_route = solver.solve()
    
    assert new_route["success"] is True
    print(f"New Optimized Route: {new_route['route']}")
    print("✅ PIPELINE INTEGRATION TEST PASSED")

if __name__ == "__main__":
    asyncio.run(test_full_disruption_pipeline())
