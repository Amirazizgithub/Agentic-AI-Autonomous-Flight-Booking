"""Mock Calendar Tool - Simulates calendar integration"""
import random
import string
from datetime import datetime
from typing import Dict, Any
from langchain.tools import tool


def generate_event_id() -> str:
    """Generate a random calendar event ID"""
    prefix = "CAL"
    numbers = ''.join(random.choices(string.digits, k=6))
    return f"{prefix}{numbers}"


@tool
def add_to_calendar(
    event_title: str,
    event_date: str,
    event_time: str,
    description: str = ""
) -> str:
    """
    Add a flight booking to calendar.
    
    Args:
        event_title: Title of the calendar event (e.g., "Flight to Mumbai")
        event_date: Date in DD-MM-YYYY format
        event_time: Time in HH:MM format
        description: Optional event description
        
    Returns:
        JSON string with calendar event confirmation or error message
    """
    try:
        # Validate inputs
        if not event_title or not event_date or not event_time:
            return "Error: Event title, date, and time are required"
        
        # Parse date and time
        event_datetime = datetime.strptime(f"{event_date} {event_time}", '%d-%m-%Y %H:%M')
        
        # Simulate calendar API call with 98% success rate
        if random.random() < 0.98:
            event_id = generate_event_id()
            
            result = {
                "status": "success",
                "event_id": event_id,
                "title": event_title,
                "date": event_date,
                "time": event_time,
                "description": description,
                "created_at": datetime.utcnow().isoformat(),
                "calendar": "Primary Calendar",
                "reminder_set": True,
                "reminder_time": "2 hours before",
                "message": f"Event '{event_title}' added to calendar successfully",
                "sync_status": "synced"
            }
            
            return str(result)
        else:
            return "Error: Failed to add event to calendar. Please try again."
        
    except ValueError as e:
        return f"Error: Invalid date/time format. Use DD-MM-YYYY for date and HH:MM for time. Details: {str(e)}"
    except Exception as e:
        return f"Error adding to calendar: {str(e)}"
