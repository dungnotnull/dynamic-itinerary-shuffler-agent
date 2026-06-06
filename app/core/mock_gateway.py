import random
from datetime import datetime, timedelta
from typing import Dict, Any, List

class MockAPIGateway:
    """
    Simulates all external API dependencies to allow the system to run 
    without real API keys.
    """
    def __init__(self):
        self.weather_scenarios = ["Clear", "Rain", "Storm", "Cloudy"]
        self.traffic_scenarios = [1.0, 1.2, 1.5, 2.5] # Multipliers for travel time

    async def get_weather(self, lat: float, lon: float) -> Dict[str, Any]:
        # Simulate a random weather condition
        condition = random.choice(self.weather_scenarios)
        return {
            "weather": [{"main": condition}],
            "rain": {"1h": 10.0 if condition == "Rain" else 0.0},
            "main": {"temp": 22.5}
        }

    async def get_distance_matrix(self, origins: List[str], destinations: List[str]) -> Dict[str, Any]:
        # Generate a random but consistent distance matrix
        matrix = []
        for o in origins:
            row = []
            for d in destinations:
                # Use a simple deterministic "distance" based on string length to keep it stable
                dist = abs(len(o) - len(d)) * 10 + random.randint(1, 5)
                row.append(dist)
            matrix.append(row)
        
        return {
            "rows": [
                {"elements": [{"distance": {"value": v}, "duration": {"value": v * 2}} for v in row]}
                for row in matrix
            ]
        }

    async def get_llm_response(self, prompt: str) -> str:
        # Simulate an LLM reasoning about venues
        return "Based on the user's preference for indoor artsy spaces, I recommend the 'Modern Art Gallery' because it is rain-proof and matches the vibe."

    async def get_foursquare_alternatives(self, category: str, lat: float, lon: float) -> List[Dict[str, Any]]:
        # Return a list of mock venues
        return [
            {"id": 101, "name": "Indoor Art Gallery", "category": "Art", "lat": lat+0.01, "lon": lon+0.01, "embedding": [0.1, 0.9, 0.1]},
            {"id": 102, "name": "City Museum", "category": "Museum", "lat": lat+0.02, "lon": lon+0.02, "embedding": [0.2, 0.7, 0.2]},
            {"id": 103, "name": "Outdoor Park", "category": "Nature", "lat": lat+0.03, "lon": lon+0.03, "embedding": [0.9, 0.1, 0.1]},
        ]

mock_gateway = MockAPIGateway()
