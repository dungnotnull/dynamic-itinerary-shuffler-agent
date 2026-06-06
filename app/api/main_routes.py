from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.database import db_manager, User, Itinerary, ItineraryStop, Venue, Preference
from app.models.schemas import UserCreate, ItineraryCreate, ItineraryResponse, VenueCreate, PreferenceCreate
from app.core.encryption import encryption_manager
from typing import List
from datetime import datetime

router = APIRouter()

def get_db():
    db = next(db_manager.get_db())
    try:
        yield db
    finally:
        db.close()

@router.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    # Encrypt profile before storing
    encrypted_blob = encryption_manager.encrypt_data(user_in.profile_data)
    db_user = User(
        username=user_in.username, 
        email=user_in.email, 
        encrypted_profile=encrypted_blob
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"id": db_user.id, "username": db_user.username}

@router.post("/venues", status_code=status.HTTP_201_CREATED)
async def create_venue(venue_in: VenueCreate, db: Session = Depends(get_db)):
    db_venue = Venue(**venue_in.dict())
    db.add(db_venue)
    db.commit()
    db.refresh(db_venue)
    return db_venue

@router.post("/itineraries", response_model=ItineraryResponse)
async def create_itinerary(itinerary_in: ItineraryCreate, db: Session = Depends(get_db)):
    # 1. Create the Itinerary record
    itinerary = Itinerary(
        name=itinerary_in.name,
        user_id=itinerary_in.user_id,
        start_date=itinerary_in.start_date,
        end_date=itinerary_in.end_date,
        status="planned"
    )
    db.add(itinerary)
    db.commit()
    db.refresh(itinerary)
    
    # 2. Solver logic would go here (Calling VRPTWSolver)
    # For now, we assume a solver mock that returns a valid route
    # In a real run, this involves fetching Distance Matrix API and calling solver.solve()
    mock_route = [0] + itinerary_in.venue_ids + [0] 
    mock_arrivals = [0] * len(mock_route)
    
    # 3. Save the stops in sequence_order
    for idx, v_id in enumerate(mock_route):
        stop = ItineraryStop(
            itinerary_id=itinerary.id,
            venue_id=v_id if v_id != 0 else 1, # Mock venue for depot
            sequence_order=idx,
            planned_arrival=datetime.utcnow()
        )
        db.add(stop)
        
    db.commit()
    
    return {
        "id": itinerary.id, 
        "name": itinerary.name, 
        "status": itinerary.status, 
        "route": mock_route, 
        "arrival_times": mock_arrivals
    }

@router.get("/users/{user_id}/profile")
async def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Decrypt on the fly
    profile = encryption_manager.decrypt_data(user.encrypted_profile)
    return profile
