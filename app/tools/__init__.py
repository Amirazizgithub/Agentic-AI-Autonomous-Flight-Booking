"""Tools module - Mock implementations of flight booking tools"""
from .flight_search import search_flights
from .booking import book_flight
from .calendar import add_to_calendar

__all__ = ["search_flights", "book_flight", "add_to_calendar"]
