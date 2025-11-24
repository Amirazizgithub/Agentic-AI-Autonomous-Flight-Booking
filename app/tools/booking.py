"""Mock Booking Tool - Simulates flight booking API"""
import random
import string
from datetime import datetime
from typing import Dict, Any
from langchain.tools import tool


def generate_booking_id() -> str:
    """Generate a random booking ID"""
    prefix = "BK"
    numbers = ''.join(random.choices(string.digits, k=6))
    return f"{prefix}{numbers}"


def generate_pnr() -> str:
    """Generate a random PNR number"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


@tool
def book_flight(flight_number: str, passenger_name: str, price: float, date: str) -> str:
    """
    Book a flight for a passenger.
    
    Args:
        flight_number: The flight number to book
        passenger_name: Name of the passenger
        price: Flight price
        date: Travel date in DD-MM-YYYY format
        
    Returns:
        JSON string with booking confirmation or error message
    """
    try:
        # Validate inputs
        if not flight_number or not passenger_name:
            return "Error: Flight number and passenger name are required"
        
        if price <= 0:
            return "Error: Invalid price"
        
        # Parse date
        travel_date = datetime.strptime(date, '%d-%m-%Y')
        
        # Simulate booking process with 95% success rate
        if random.random() < 0.95:
            booking_id = generate_booking_id()
            pnr = generate_pnr()
            
            result = {
                "status": "success",
                "booking_id": booking_id,
                "pnr": pnr,
                "flight_number": flight_number,
                "passenger_name": passenger_name,
                "price": price,
                "travel_date": date,
                "booking_time": datetime.utcnow().isoformat(),
                "message": f"Flight {flight_number} successfully booked for {passenger_name}",
                "payment_status": "confirmed",
                "ticket_sent": True
            }
            
            return str(result)
        else:
            return "Error: Booking failed due to seat unavailability. Please try another flight."
        
    except ValueError as e:
        return f"Error: Invalid date format. Please use DD-MM-YYYY format. Details: {str(e)}"
    except Exception as e:
        return f"Error booking flight: {str(e)}"
