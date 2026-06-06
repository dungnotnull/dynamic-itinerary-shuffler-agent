from app.models.database import db_manager, User, Venue, Preference, Itinerary, ItineraryStop
from app.core.encryption import encryption_manager
import random
from datetime import datetime, timedelta

def seed_database():
    print("Seeding database with production-like mock data...")
    db = next(db_manager.get_db())
    
    # Clear existing data to avoid IntegrityError
    db.query(ItineraryStop).delete()
    db.query(Itinerary).delete()
    db.query(Preference).delete()
    db.query(Venue).delete()
    db.query(User).delete()
    db.commit()
    
    # 1. Create a User
    user_profile = {
        "vibe": "artsy, quiet, indoor",
        "interests": ["modern art", "jazz", "specialty coffee"],
        "budget": "medium-high",
        "mobility": "walking"
    }
    encrypted_profile = encryption_manager.encrypt_data(user_profile)
    user = User(username="traveler_one", email="test@example.com", encrypted_profile=encrypted_profile)
    db.add(user)
    db.commit()
    
    # 2. Create Preferences
    prefs = [
        Preference(user_id=user.id, key="vibe", value="artsy", weight=1.0),
        Preference(user_id=user.id, key="interest", value="jazz", weight=0.8),
    ]
    db.add_all(prefs)
    
    # 3. Create Venues
    venues = [
        Venue(name="Hotel Start", category="Hotel", latitude=10.7626, longitude=106.6602, embedding=[0,0,0]),
        Venue(name="City Museum", category="Museum", latitude=10.7700, longitude=106.6700, embedding=[0.1, 0.8, 0.1]),
        Venue(name="Jazz Cafe", category="Cafe", latitude=10.7800, longitude=106.6800, embedding=[0.2, 0.7, 0.2]),
        Venue(name="Riverside Walk", category="Nature", latitude=10.7900, longitude=106.6900, embedding=[0.9, 0.1, 0.1]),
    ]
    db.add_all(venues)
    db.commit()
    
    # 4. Create a Planned Itinerary
    itinerary = Itinerary(
        name="Weekend Saigon Art Trip",
        user_id=user.id,
        start_date=datetime.utcnow(),
        end_date=datetime.utcnow() + timedelta(days=1),
        status="active"
    )
    db.add(itinerary)
    db.commit()
    
    # Create stops
    stops = [
        ItineraryStop(itinerary_id=itinerary.id, venue_id=1, sequence_order=0, planned_arrival=datetime.utcnow()),
        ItineraryStop(itinerary_id=itinerary.id, venue_id=2, sequence_order=1, planned_arrival=datetime.utcnow()),
        ItineraryStop(itinerary_id=itinerary.id, venue_id=3, sequence_order=2, planned_arrival=datetime.utcnow()),
        ItineraryStop(itinerary_id=itinerary.id, venue_id=4, sequence_order=3, planned_arrival=datetime.utcnow()),
    ]
    db.add_all(stops)
    db.commit()
    
    print(f"Database seeded successfully. User ID: {user.id}, Itinerary ID: {itinerary.id}")

if __name__ == "__main__":
    seed_database()
