"""Pydantic models for request/response validation"""
from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field, validator


class BookingStatus(str, Enum):
    """Booking status enumeration"""
    PENDING = "pending"
    SEARCHING = "searching"
    FOUND = "found"
    BOOKED = "booked"
    CONFIRMED = "confirmed"
    FAILED = "failed"


class BookingRequest(BaseModel):
    """Request model for flight booking"""
    passenger_name: str = Field(..., min_length=2, max_length=100, description="Name of the passenger")
    max_price: float = Field(..., gt=0, description="Maximum price willing to pay")
    departure: str = Field(..., min_length=2, max_length=100, description="Departure city")
    destination: str = Field(..., min_length=2, max_length=100, description="Destination city")
    booking_date: str = Field(..., description="Booking date in DD-MM-YYYY format")
    
    @validator('booking_date')
    def validate_date(cls, v):
        """Validate date format"""
        try:
            datetime.strptime(v, '%d-%m-%Y')
            return v
        except ValueError:
            raise ValueError('Date must be in DD-MM-YYYY format')
    
    class Config:
        json_schema_extra = {
            "example": {
                "passenger_name": "John Doe",
                "max_price": 5000,
                "departure": "Delhi",
                "destination": "Mumbai",
                "booking_date": "25-11-2025"
            }
        }


class FlightDetails(BaseModel):
    """Flight information model"""
    flight_number: str
    airline: str
    departure: str
    destination: str
    departure_time: str
    arrival_time: str
    price: float
    duration: str


class BookingResponse(BaseModel):
    """Response model for booking operations"""
    status: BookingStatus
    message: str
    booking_id: Optional[str] = None
    flight_details: Optional[FlightDetails] = None
    calendar_event_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    agent_reasoning: Optional[List[str]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "confirmed",
                "message": "Flight booked successfully and added to calendar",
                "booking_id": "BK123456",
                "flight_details": {
                    "flight_number": "AI101",
                    "airline": "Air India",
                    "departure": "Delhi",
                    "destination": "Mumbai",
                    "departure_time": "10:00",
                    "arrival_time": "12:30",
                    "price": 4500,
                    "duration": "2h 30m"
                },
                "calendar_event_id": "CAL789",
                "timestamp": "2025-11-24T10:00:00Z"
            }
        }
