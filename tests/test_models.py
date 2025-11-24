"""Test cases for data models"""
import pytest
from datetime import datetime
from pydantic import ValidationError

from app.models.schemas import BookingRequest, BookingResponse, BookingStatus, FlightDetails


class TestBookingRequest:
    """Test BookingRequest model"""
    
    def test_valid_booking_request(self):
        """Test valid booking request"""
        request = BookingRequest(
            passenger_name="John Doe",
            max_price=5000,
            departure="Delhi",
            destination="Mumbai",
            booking_date="25-11-2025"
        )
        assert request.passenger_name == "John Doe"
        assert request.max_price == 5000
        assert request.departure == "Delhi"
        assert request.destination == "Mumbai"
        assert request.booking_date == "25-11-2025"
    
    def test_invalid_date_format(self):
        """Test invalid date format"""
        with pytest.raises(ValidationError) as exc_info:
            BookingRequest(
                passenger_name="John Doe",
                max_price=5000,
                departure="Delhi",
                destination="Mumbai",
                booking_date="2025-11-25"  # Wrong format
            )
        assert "Date must be in DD-MM-YYYY format" in str(exc_info.value)
    
    def test_negative_price(self):
        """Test negative price validation"""
        with pytest.raises(ValidationError):
            BookingRequest(
                passenger_name="John Doe",
                max_price=-100,
                departure="Delhi",
                destination="Mumbai",
                booking_date="25-11-2025"
            )
    
    def test_missing_required_fields(self):
        """Test missing required fields"""
        with pytest.raises(ValidationError):
            BookingRequest(
                passenger_name="John Doe",
                max_price=5000
            )


class TestFlightDetails:
    """Test FlightDetails model"""
    
    def test_valid_flight_details(self):
        """Test valid flight details"""
        flight = FlightDetails(
            flight_number="AI101",
            airline="Air India",
            departure="Delhi",
            destination="Mumbai",
            departure_time="10:00",
            arrival_time="12:30",
            price=4500,
            duration="2h 30m"
        )
        assert flight.flight_number == "AI101"
        assert flight.price == 4500


class TestBookingResponse:
    """Test BookingResponse model"""
    
    def test_valid_booking_response(self):
        """Test valid booking response"""
        response = BookingResponse(
            status=BookingStatus.CONFIRMED,
            message="Booking confirmed",
            booking_id="BK123456"
        )
        assert response.status == BookingStatus.CONFIRMED
        assert response.booking_id == "BK123456"
        assert isinstance(response.timestamp, datetime)
