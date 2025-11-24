"""Test cases for tools"""
import pytest
from app.tools.flight_search import search_flights
from app.tools.booking import book_flight
from app.tools.calendar import add_to_calendar


class TestFlightSearch:
    """Test flight search tool"""
    
    def test_search_flights_success(self):
        """Test successful flight search"""
        result = search_flights.invoke({
            "departure": "Delhi",
            "destination": "Mumbai",
            "max_price": 5000,
            "booking_date": "25-11-2025"
        })
        
        assert "status" in result or "success" in result
        assert "Mumbai" in result
    
    def test_search_flights_invalid_date(self):
        """Test flight search with invalid date"""
        result = search_flights.invoke({
            "departure": "Delhi",
            "destination": "Mumbai",
            "max_price": 5000,
            "booking_date": "invalid-date"
        })
        
        assert "Error" in result or "error" in result.lower()
    
    def test_search_flights_no_results(self):
        """Test flight search with very low budget"""
        result = search_flights.invoke({
            "departure": "Delhi",
            "destination": "Mumbai",
            "max_price": 100,
            "booking_date": "25-11-2025"
        })
        
        assert "No flights found" in result or "success" in result


class TestBookFlight:
    """Test booking tool"""
    
    def test_book_flight_success(self):
        """Test successful flight booking (may sometimes fail due to random 5% failure rate)"""
        result = book_flight.invoke({
            "flight_number": "AI101",
            "passenger_name": "John Doe",
            "price": 4500,
            "date": "25-11-2025"
        })
        
        # Should either succeed with booking_id or fail with seat unavailability
        assert ("booking_id" in result or "BK" in result) or ("seat unavailability" in result.lower())
    
    def test_book_flight_invalid_date(self):
        """Test booking with invalid date"""
        result = book_flight.invoke({
            "flight_number": "AI101",
            "passenger_name": "John Doe",
            "price": 4500,
            "date": "invalid-date"
        })
        
        assert "Error" in result or "error" in result.lower()
    
    def test_book_flight_missing_data(self):
        """Test booking with missing data"""
        result = book_flight.invoke({
            "flight_number": "",
            "passenger_name": "John Doe",
            "price": 4500,
            "date": "25-11-2025"
        })
        
        assert "Error" in result or "required" in result.lower()


class TestCalendar:
    """Test calendar tool"""
    
    def test_add_to_calendar_success(self):
        """Test successful calendar addition"""
        result = add_to_calendar.invoke({
            "event_title": "Flight to Mumbai",
            "event_date": "25-11-2025",
            "event_time": "10:00",
            "description": "Flight AI101"
        })
        
        assert "event_id" in result or "CAL" in result
    
    def test_add_to_calendar_invalid_date(self):
        """Test calendar with invalid date"""
        result = add_to_calendar.invoke({
            "event_title": "Flight to Mumbai",
            "event_date": "invalid-date",
            "event_time": "10:00",
            "description": "Flight AI101"
        })
        
        assert "Error" in result or "error" in result.lower()
    
    def test_add_to_calendar_missing_data(self):
        """Test calendar with missing data"""
        result = add_to_calendar.invoke({
            "event_title": "",
            "event_date": "25-11-2025",
            "event_time": "10:00"
        })
        
        assert "Error" in result or "required" in result.lower()
