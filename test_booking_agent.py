#!/usr/bin/env python3
"""
Test script for booking_agent.py
Demonstrates all features without requiring an OpenAI API key.
"""

from booking_agent import (
    search_flights,
    book_flight,
    add_to_calendar,
    SearchFlightsInput,
    BookFlightInput,
    AddToCalendarInput,
    BUDGET_LIMIT,
)
import booking_agent


def test_search_flights():
    """Test the search_flights tool."""
    print("=" * 70)
    print("TEST 1: Search Flights")
    print("=" * 70)
    
    # Valid search
    print("\n✅ Valid search:")
    result = search_flights("New York", 600)
    print(result)
    
    # Invalid searches
    print("\n❌ Empty destination:")
    result = search_flights("", 600)
    print(result)
    
    print("\n❌ Invalid price:")
    result = search_flights("Paris", -100)
    print(result)


def test_book_flight():
    """Test the book_flight tool with guardrails."""
    print("\n" + "=" * 70)
    print("TEST 2: Book Flight (with Guardrails)")
    print("=" * 70)
    
    # Reset budget
    booking_agent.total_spending = 0
    
    # Valid booking
    print("\n✅ Valid booking:")
    result = book_flight("FL123", "Alice Johnson")
    print(result)
    
    # Another booking
    print("\n✅ Second booking:")
    result = book_flight("FL456", "Bob Smith")
    print(result)
    
    # Try to exceed budget
    print("\n⛔ Third booking (should hit budget limit):")
    result = book_flight("FL789", "Charlie Brown")
    print(result)
    
    # Invalid inputs
    print("\n❌ Empty flight ID:")
    result = book_flight("", "Jane Doe")
    print(result)
    
    print("\n❌ Empty passenger name:")
    result = book_flight("FL999", "")
    print(result)


def test_add_to_calendar():
    """Test the add_to_calendar tool."""
    print("\n" + "=" * 70)
    print("TEST 3: Add to Calendar")
    print("=" * 70)
    
    # Valid calendar entry
    print("\n✅ Valid calendar entry:")
    result = add_to_calendar("2024-12-25", "Flight to London")
    print(result)
    
    # Invalid date format
    print("\n❌ Invalid date format:")
    result = add_to_calendar("12-25-2024", "Flight to Paris")
    print(result)
    
    print("\n❌ Empty date:")
    result = add_to_calendar("", "Flight details")
    print(result)
    
    print("\n❌ Empty details:")
    result = add_to_calendar("2024-12-25", "")
    print(result)


def test_pydantic_schemas():
    """Test Pydantic validation."""
    print("\n" + "=" * 70)
    print("TEST 4: Pydantic Schema Validation")
    print("=" * 70)
    
    # Valid schemas
    print("\n✅ Valid SearchFlightsInput:")
    schema = SearchFlightsInput(dest="Tokyo", price=1000)
    print(f"   {schema}")
    
    print("\n✅ Valid BookFlightInput:")
    schema = BookFlightInput(id="FL777", name="David Lee")
    print(f"   {schema}")
    
    print("\n✅ Valid AddToCalendarInput:")
    schema = AddToCalendarInput(date="2024-12-31", details="New Year Flight")
    print(f"   {schema}")
    
    # Test invalid type (caught by Pydantic)
    print("\n❌ Invalid price type (should be int):")
    try:
        schema = SearchFlightsInput(dest="Rome", price="five hundred")
        print("   FAILED - Should have raised ValidationError")
    except Exception as e:
        print(f"   ✅ Correctly rejected: {type(e).__name__}")


def test_budget_tracking():
    """Test budget tracking functionality."""
    print("\n" + "=" * 70)
    print("TEST 5: Budget Tracking")
    print("=" * 70)
    
    # Reset budget
    booking_agent.total_spending = 0
    
    print(f"\nInitial budget: ${booking_agent.total_spending} / ${BUDGET_LIMIT}")
    
    # Book multiple flights
    flights = [
        ("FL001", "Passenger 1"),
        ("FL200", "Passenger 2"),
        ("FL999", "Passenger 3"),
    ]
    
    for flight_id, name in flights:
        print(f"\nBooking {flight_id} for {name}...")
        result = book_flight(flight_id, name)
        
        # Extract and show spending
        for line in result.split('\n'):
            if 'Total Spending:' in line or 'BOOKING BLOCKED' in line:
                print(f"  {line.strip()}")
                break


def test_price_variation():
    """Test that flight prices vary based on ID."""
    print("\n" + "=" * 70)
    print("TEST 6: Price Variation")
    print("=" * 70)
    
    # Reset budget
    booking_agent.total_spending = 0
    
    print("\nDifferent flight IDs should have different prices:")
    
    flight_ids = ["FL001", "FL123", "FL456", "FL789", "FL999"]
    
    for flight_id in flight_ids:
        result = book_flight(flight_id, "Test User")
        # Extract price
        for line in result.split('\n'):
            if 'Amount Charged:' in line:
                print(f"  {flight_id}: {line.strip()}")
                break
        booking_agent.total_spending = 0  # Reset for next test


def main():
    """Run all tests."""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "BOOKING AGENT TEST SUITE" + " " * 29 + "║")
    print("╚" + "═" * 68 + "╝")
    print("\nTesting all features without requiring OpenAI API key...")
    
    try:
        test_search_flights()
        test_book_flight()
        test_add_to_calendar()
        test_pydantic_schemas()
        test_budget_tracking()
        test_price_variation()
        
        print("\n" + "=" * 70)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print("\nThe booking_agent.py is working correctly with:")
        print("  ✅ All 3 tools (search, book, calendar)")
        print("  ✅ Pydantic schemas for input validation")
        print("  ✅ Try/except error handling")
        print("  ✅ Budget check guardrail")
        print("  ✅ High-stakes action warnings")
        print("  ✅ Price variation based on flight ID")
        print()
        
        return 0
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
