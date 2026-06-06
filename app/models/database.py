from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, Session
from datetime import datetime
import json

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    # Stores encrypted JSON blob: {"preferences": {...}, "behavior": {...}}
    encrypted_profile = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    preferences = relationship("Preference", back_populates="user")

class Itinerary(Base):
    __tablename__ = "itineraries"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    status = Column(String, default="planned") # planned, active, completed, archived, disrupted
    created_at = Column(DateTime, default=datetime.utcnow)
    
    stops = relationship("ItineraryStop", back_populates="itinerary", cascade="all, delete-orphan")

class ItineraryStop(Base):
    __tablename__ = "itinerary_stops"
    id = Column(Integer, primary_key=True, index=True)
    itinerary_id = Column(Integer, ForeignKey("itineraries.id"), nullable=False)
    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=False)
    sequence_order = Column(Integer, nullable=False)
    planned_arrival = Column(DateTime)
    planned_departure = Column(DateTime)
    actual_arrival = Column(DateTime, nullable=True)
    actual_departure = Column(DateTime, nullable=True)
    is_substituted = Column(Integer, default=0) # 0: original, 1: substituted
    
    itinerary = relationship("Itinerary", back_populates="stops")
    venue = relationship("Venue")

class Venue(Base):
    __tablename__ = "venues"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    category = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    address = Column(String)
    opening_hours = Column(JSON) # format: {"mon": "09:00-17:00", ...}
    embedding = Column(JSON) # float list of the venue's semantic embedding
    metadata_json = Column(JSON) # extended details
    
    stops = relationship("ItineraryStop", back_populates="venue")

class Preference(Base):
    __tablename__ = "preferences"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    key = Column(String, nullable=False) # e.g., "dietary", "mobility", "vibe"
    value = Column(String, nullable=False)
    weight = Column(Float, default=1.0)
    
    user = relationship("User", back_populates="preferences")

# DB Connection helper
class DatabaseManager:
    def __init__(self, db_url: str = "sqlite:///./travel_agent.db"):
        self.engine = create_engine(db_url, connect_args={"check_same_thread": False})
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

db_manager = DatabaseManager()
