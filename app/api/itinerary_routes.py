from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import Itinerary, ItineraryStop, Venue, User
from app.core.config import settings
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/itineraries", tags=["itineraries"])

# Schemas
class ItineraryCreate(BaseModel):
    name: str
    user_id: int
    start_date: datetime
    end_date: datetime
    venue_ids: List[int]

class ItineraryResponse(BaseModel):
    id: int
    name: str
    status: str
    route: List[int]

@router.post("/", response_model=ItineraryResponse)
async def create_itinerary(data: ItineraryCreate, db: Session = Depends(lambda: None)): # Mock DB for now
    # In a real run, we would:
    # 1. Save Itinerary to DB
    # 2. Fetch venues and distances via Google Maps API
    # 3. Call VRPTWSolver
    # 4. Save stops in sequence_order
    return {"id": 123, "name": data.name, "status": "planned", "route": [0, 2, 1, 3, 0]}

@router.get("/{itinerary_id}")
async def get_itinerary(itinerary_id: int):
    return {"id": itinerary_id, "status": "active", "route": [0, 2, 1, 3, 0]}
