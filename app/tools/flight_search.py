"""Mock Flight Search Tool - Simulates flight search API"""
import random
from typing import Dict, List, Any
from datetime import datetime, timedelta
from langchain.tools import tool


# Mock flight database
MOCK_FLIGHTS = [
    {"airline": "Air India", "base_price": 4500, "flight_prefix": "AI", "duration": "2h 30m"},
    {"airline": "IndiGo", "base_price": 4200, "flight_prefix": "6E", "duration": "2h 25m"},
    {"airline": "SpiceJet", "base_price": 3800, "flight_prefix": "SG", "duration": "2h 35m"},
    {"airline": "Vistara", "base_price": 5200, "flight_prefix": "UK", "duration": "2h 20m"},
    {"airline": "Go First", "base_price": 3600, "flight_prefix": "G8", "duration": "2h 40m"},
]

CITIES = {
    "mumbai": "Mumbai (BOM)",
    "delhi": "Delhi (DEL)",
    "bangalore": "Bangalore (BLR)",
    "chennai": "Chennai (MAA)",
    "kolkata": "Kolkata (CCU)",
    "hyderabad": "Hyderabad (HYD)",
}


@tool
def search_flights(departure: str, destination: str, max_price: float, booking_date: str) -> str:
    """
    Search for available flights from departure to destination within a price range.
    
    Args:
        departure: The departure city
        destination: The destination city
        max_price: Maximum price willing to pay
        booking_date: Date of travel in DD-MM-YYYY format
        
    Returns:
        JSON string with available flights or error message
    """
    try:
        # Parse the date
        travel_date = datetime.strptime(booking_date, '%d-%m-%Y')
        
        # Normalize departure and destination
        dep_normalized = departure.lower().strip()
        dep_display = CITIES.get(dep_normalized, departure)
        
        dest_normalized = destination.lower().strip()
        dest_display = CITIES.get(dest_normalized, destination)
        
        # Generate mock flights
        available_flights = []
        for flight_data in MOCK_FLIGHTS:
            # Add some price variance
            price = flight_data["base_price"] + random.randint(-500, 500)
            
            if price <= max_price:
                flight_num = f"{flight_data['flight_prefix']}{random.randint(100, 999)}"
                
                # Generate departure/arrival times
                departure_hour = random.randint(6, 20)
                departure_minute = random.choice([0, 15, 30, 45])
                departure_time = f"{departure_hour:02d}:{departure_minute:02d}"
                
                # Calculate arrival time
                duration_parts = flight_data['duration'].split('h')
                hours = int(duration_parts[0].strip())
                minutes = int(duration_parts[1].strip().replace('m', ''))
                
                departure_dt = datetime.strptime(f"{departure_hour:02d}:{departure_minute:02d}", "%H:%M")
                arrival_dt = departure_dt + timedelta(hours=hours, minutes=minutes)
                arrival_time = arrival_dt.strftime("%H:%M")
                
                flight = {
                    "flight_number": flight_num,
                    "airline": flight_data["airline"],
                    "departure": dep_display,
                    "destination": dest_display,
                    "departure_time": departure_time,
                    "arrival_time": arrival_time,
                    "price": price,
                    "duration": flight_data["duration"],
                    "date": booking_date
                }
                available_flights.append(flight)
        
        if not available_flights:
            return f"No flights found from {dep_display} to {dest_display} within budget of ₹{max_price}"
        
        # Sort by price
        available_flights.sort(key=lambda x: x['price'])
        
        # Return top 3 flights
        result = {
            "status": "success",
            "flights_found": len(available_flights),
            "flights": available_flights[:3],
            "message": f"Found {len(available_flights)} flights from {dep_display} to {dest_display} on {booking_date}"
        }
        
        return str(result)
        
    except ValueError as e:
        return f"Error: Invalid date format. Please use DD-MM-YYYY format. Details: {str(e)}"
    except Exception as e:
        return f"Error searching flights: {str(e)}"
