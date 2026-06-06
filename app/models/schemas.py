from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class VenueCreate(BaseModel):
    name: str
    category: str
    latitude: float
    longitude: float
    address: Optional[str] = None
    opening_hours: dict = Field(default={}, description="Format: {'mon': '09:00-17:00'}")
    metadata_json: Optional[dict] = None

class PreferenceCreate(BaseModel):
    key: str
    value: str
    weight: float = 1.0

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
    arrival_times: List[int]

class UserCreate(BaseModel):
    username: str
    email: str
    profile_data: dict
