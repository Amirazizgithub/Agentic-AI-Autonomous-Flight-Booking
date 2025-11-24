#!/usr/bin/env python3
"""
LangChain Structured Agent for Autonomous Flight Booking.

This module implements a production-ready agent with guardrails for:
- Searching flights
- Booking flights (with high-stakes warnings)
- Adding bookings to calendar

Includes robust error handling, budget checks, and safety mechanisms.
"""

import os
from typing import Optional
from pydantic import BaseModel, Field
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import StructuredTool

# ============================================================================
# CONFIGURATION
# ============================================================================

# Budget limit for bookings (in USD)
BUDGET_LIMIT = 1000

# Track total spending
total_spending = 0


# ============================================================================
# PYDANTIC SCHEMAS FOR TOOL INPUTS
# ============================================================================

class SearchFlightsInput(BaseModel):
    """Input schema for searching flights."""
    dest: str = Field(description="Destination city or airport code")
    price: int = Field(description="Maximum price in USD for the flight")


class BookFlightInput(BaseModel):
    """Input schema for booking a flight."""
    id: str = Field(description="Unique flight ID to book")
    name: str = Field(description="Passenger name for the booking")


class AddToCalendarInput(BaseModel):
    """Input schema for adding events to calendar."""
    date: str = Field(description="Date of the flight in YYYY-MM-DD format")
    details: str = Field(description="Flight details to add to calendar")


# ============================================================================
# TOOL IMPLEMENTATIONS
# ============================================================================

def search_flights(dest: str, price: int) -> str:
    """
    Search for available flights to a destination within a price range.
    
    Args:
        dest: Destination city or airport code
        price: Maximum price in USD
        
    Returns:
        Search results as a formatted string
        
    Raises:
        ValueError: If inputs are invalid
        Exception: For other search errors
    """
    try:
        # Input validation
        if not dest or not dest.strip():
            raise ValueError("Destination cannot be empty")
        if price <= 0:
            raise ValueError("Price must be greater than 0")
            
        # Mock flight search (in production, this would call a real API)
        flights = [
            {
                "id": f"FL{hash(dest) % 1000:03d}",
                "destination": dest.upper(),
                "price": min(price - 50, price * 0.9),
                "departure": "10:00 AM",
                "airline": "Mock Airlines"
            },
            {
                "id": f"FL{hash(dest) % 1000 + 100:03d}",
                "destination": dest.upper(),
                "price": min(price - 20, price * 0.95),
                "departure": "2:00 PM",
                "airline": "Budget Air"
            }
        ]
        
        result = f"Found {len(flights)} flights to {dest}:\n"
        for flight in flights:
            result += (
                f"- Flight {flight['id']}: ${flight['price']} "
                f"({flight['airline']}, Departs: {flight['departure']})\n"
            )
        
        return result
        
    except ValueError as e:
        return f"Search error: Invalid input - {str(e)}"
    except Exception as e:
        return f"Search error: Unexpected error occurred - {str(e)}"


def book_flight(id: str, name: str) -> str:
    """
    Book a flight with production guardrails.
    
    This is a HIGH-STAKES action that includes:
    - Budget verification
    - Explicit warnings
    - Error handling
    
    Args:
        id: Unique flight ID
        name: Passenger name
        
    Returns:
        Booking confirmation or error message
    """
    global total_spending
    
    try:
        # Input validation
        if not id or not id.strip():
            raise ValueError("Flight ID cannot be empty")
        if not name or not name.strip():
            raise ValueError("Passenger name cannot be empty")
            
        # Extract mock price from flight ID (in production, fetch from database)
        # For demo purposes, we'll use a mock price
        mock_price = 500  # Mock flight price
        
        # ⚠️ BUDGET CHECK - Production Guardrail #1
        if total_spending + mock_price > BUDGET_LIMIT:
            return (
                f"⛔ BOOKING BLOCKED: Budget exceeded! "
                f"Current spending: ${total_spending}, "
                f"Flight cost: ${mock_price}, "
                f"Budget limit: ${BUDGET_LIMIT}"
            )
        
        # ⚠️ HIGH-STAKES ACTION WARNING - Production Guardrail #2
        warning_message = (
            f"\n{'='*60}\n"
            f"⚠️  HIGH-STAKES ACTION: BOOKING FLIGHT\n"
            f"{'='*60}\n"
            f"Flight ID: {id}\n"
            f"Passenger: {name}\n"
            f"Cost: ${mock_price}\n"
            f"This action will charge your account!\n"
            f"{'='*60}\n"
        )
        
        # Mock booking process (in production, this would call a booking API)
        confirmation_number = f"CONF-{hash(f'{id}{name}') % 100000:05d}"
        
        # Update spending tracker
        total_spending += mock_price
        
        result = (
            f"{warning_message}"
            f"✅ BOOKING CONFIRMED\n"
            f"Confirmation Number: {confirmation_number}\n"
            f"Flight: {id}\n"
            f"Passenger: {name}\n"
            f"Amount Charged: ${mock_price}\n"
            f"Total Spending: ${total_spending} / ${BUDGET_LIMIT}\n"
        )
        
        return result
        
    except ValueError as e:
        return f"Booking error: Invalid input - {str(e)}"
    except Exception as e:
        return f"Booking error: Unexpected error occurred - {str(e)}"


def add_to_calendar(date: str, details: str) -> str:
    """
    Add a flight booking to the calendar.
    
    Args:
        date: Flight date in YYYY-MM-DD format
        details: Flight details
        
    Returns:
        Calendar entry confirmation or error message
    """
    try:
        # Input validation
        if not date or not date.strip():
            raise ValueError("Date cannot be empty")
        if not details or not details.strip():
            raise ValueError("Details cannot be empty")
            
        # Basic date format validation
        date_parts = date.split('-')
        if len(date_parts) != 3:
            raise ValueError("Date must be in YYYY-MM-DD format")
            
        # Mock calendar addition (in production, this would use a calendar API)
        event_id = f"EVENT-{hash(f'{date}{details}') % 10000:04d}"
        
        result = (
            f"📅 Calendar Event Created\n"
            f"Event ID: {event_id}\n"
            f"Date: {date}\n"
            f"Details: {details}\n"
            f"Status: Successfully added to calendar\n"
        )
        
        return result
        
    except ValueError as e:
        return f"Calendar error: Invalid input - {str(e)}"
    except Exception as e:
        return f"Calendar error: Unexpected error occurred - {str(e)}"


# ============================================================================
# AGENT SETUP
# ============================================================================

def create_flight_booking_agent():
    """
    Create a LangChain structured agent with flight booking tools.
    
    Returns:
        Configured agent ready to use
        
    Raises:
        ValueError: If OPENAI_API_KEY is not set
    """
    # Verify API key is available
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError(
            "OPENAI_API_KEY environment variable not set. "
            "Please set it with: export OPENAI_API_KEY='your-key-here'"
        )
    
    # Initialize GPT-4 model
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0,  # Deterministic for production use
    )
    
    # Create structured tools with Pydantic schemas
    tools = [
        StructuredTool(
            name="search_flights",
            description=(
                "Search for available flights to a destination. "
                "Use this to find flights within a price range. "
                "Returns a list of available flights with IDs, prices, and times."
            ),
            func=search_flights,
            args_schema=SearchFlightsInput,
        ),
        StructuredTool(
            name="book_flight",
            description=(
                "Book a specific flight by ID. WARNING: This is a high-stakes action "
                "that will charge money. Includes budget checks and safety warnings. "
                "Use only after confirming flight details with the user."
            ),
            func=book_flight,
            args_schema=BookFlightInput,
        ),
        StructuredTool(
            name="add_to_calendar",
            description=(
                "Add a flight booking to the calendar. "
                "Use this after successfully booking a flight to keep track of travel plans. "
                "Requires date in YYYY-MM-DD format and flight details."
            ),
            func=add_to_calendar,
            args_schema=AddToCalendarInput,
        ),
    ]
    
    # System prompt for the agent
    system_prompt = """You are a helpful flight booking assistant with access to tools for:
1. Searching flights
2. Booking flights (with safety checks)
3. Adding bookings to calendar

Always follow these guidelines:
- Search for flights before booking
- Verify flight details before booking
- Be cautious with booking actions (they charge money!)
- Add successful bookings to the calendar
- Handle errors gracefully and inform the user

When using tools, provide clear explanations of what you're doing."""
    
    # Create the structured agent using LangChain 1.0 API
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt,
    )
    
    return agent


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """
    Main entry point for the flight booking agent.
    Demonstrates the agent with example queries.
    """
    print("="*70)
    print("🛫 LangChain Flight Booking Agent (GPT-4)")
    print("="*70)
    print()
    
    try:
        # Create the agent
        print("Initializing agent...")
        agent = create_flight_booking_agent()
        print("✅ Agent initialized successfully!")
        print()
        
        # Example queries to demonstrate functionality
        example_queries = [
            "Search for flights to New York under $600",
            "Book flight FL421 for John Smith",
            "Add the booking to my calendar for 2024-12-15 with details 'Flight to NYC'",
        ]
        
        print("Running example queries:")
        print("-" * 70)
        
        for i, query in enumerate(example_queries, 1):
            print(f"\n[Query {i}]: {query}")
            print("-" * 70)
            
            try:
                result = agent.invoke({"messages": [{"role": "user", "content": query}]})
                print(f"\n[Response {i}]:")
                # Extract the last message from the agent
                if result and "messages" in result:
                    last_message = result["messages"][-1]
                    if hasattr(last_message, "content"):
                        print(last_message.content)
                    else:
                        print(last_message)
                else:
                    print("No output received")
                
            except Exception as e:
                print(f"❌ Error executing query: {str(e)}")
            
            print("-" * 70)
        
        # Show final budget status
        print(f"\n💰 Final Budget Status: ${total_spending} / ${BUDGET_LIMIT}")
        print()
        
    except ValueError as e:
        print(f"\n❌ Configuration Error: {str(e)}")
        print("\nTo run this agent, you need to set your OpenAI API key:")
        print("  export OPENAI_API_KEY='your-api-key-here'")
        print()
        return 1
        
    except Exception as e:
        print(f"\n❌ Unexpected Error: {str(e)}")
        print("\nPlease check your configuration and try again.")
        return 1
    
    print("="*70)
    print("✅ Agent demonstration completed successfully!")
    print("="*70)
    return 0


if __name__ == "__main__":
    exit(main())
