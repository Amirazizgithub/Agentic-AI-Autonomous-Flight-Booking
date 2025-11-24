# Agentic AI - Autonomous Flight Booking

A production-ready LangChain Structured Agent (GPT-4) that automates flight booking workflows with robust guardrails and error handling.

## Features

### 🛠️ Three Powerful Tools

1. **search_flights(dest: str, price: int)** - Search for available flights
   - Returns flight options with IDs, prices, airlines, and departure times
   - Validates destination and price inputs
   - Handles errors gracefully

2. **book_flight(id: str, name: str)** - Book a flight with safety checks
   - ⚠️ **HIGH-STAKES ACTION** with explicit warnings
   - Budget verification before booking
   - Clear confirmation with tracking numbers
   - Prevents accidental bookings

3. **add_to_calendar(date: str, details: str)** - Add bookings to calendar
   - Date format validation (YYYY-MM-DD)
   - Event tracking with unique IDs
   - Integration-ready for real calendar APIs

### 🛡️ Production Guardrails

- **Try/Except Error Handling**: All tools wrapped in comprehensive error handling
- **Budget Check**: Prevents spending over $1,000 limit
- **High-Stakes Warning**: Clear warnings before financial transactions
- **Input Validation**: Pydantic schemas ensure data integrity
- **Graceful Degradation**: Informative error messages for users

### 📐 Pydantic Schemas

All tool inputs use Pydantic for strong typing and validation:
- `SearchFlightsInput`: Validates destination and price
- `BookFlightInput`: Validates flight ID and passenger name
- `AddToCalendarInput`: Validates date format and details

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key
export OPENAI_API_KEY='your-api-key-here'
```

## Usage

### Run the Agent

```bash
# Make executable (optional)
chmod +x booking_agent.py

# Run with Python
python3 booking_agent.py

# Or run directly (if executable)
./booking_agent.py
```

### Use as a Module

```python
from booking_agent import create_flight_booking_agent

# Initialize the agent
agent = create_flight_booking_agent()

# Query the agent
result = agent.invoke({
    "messages": [{
        "role": "user", 
        "content": "Search for flights to Paris under $800"
    }]
})

# Access response
print(result["messages"][-1].content)
```

### Use Individual Tools

```python
from booking_agent import search_flights, book_flight, add_to_calendar

# Search for flights
flights = search_flights("London", 700)
print(flights)

# Book a flight
confirmation = book_flight("FL123", "John Doe")
print(confirmation)

# Add to calendar
calendar_event = add_to_calendar("2024-12-25", "Flight to London")
print(calendar_event)
```

## Example Workflow

```python
# 1. Search for flights
agent.invoke({"messages": [{"role": "user", "content": "Find flights to Tokyo under $900"}]})

# 2. Book a specific flight
agent.invoke({"messages": [{"role": "user", "content": "Book flight FL456 for Alice Cooper"}]})

# 3. Add to calendar
agent.invoke({"messages": [{"role": "user", "content": "Add the Tokyo flight to my calendar for 2024-12-20"}]})
```

## Budget Management

The agent tracks spending and prevents over-budget bookings:

- **Budget Limit**: $1,000 (configurable in `booking_agent.py`)
- **Budget Check**: Automatic verification before each booking
- **Budget Status**: Displayed after operations

```python
from booking_agent import BUDGET_LIMIT, total_spending
print(f"Remaining budget: ${BUDGET_LIMIT - total_spending}")
```

## Safety Features

### High-Stakes Action Warnings

When booking flights, users see:
```
============================================================
⚠️  HIGH-STAKES ACTION: BOOKING FLIGHT
============================================================
Flight ID: FL123
Passenger: John Doe
Cost: $500
This action will charge your account!
============================================================
```

### Budget Protection

Bookings are blocked when budget is exceeded:
```
⛔ BOOKING BLOCKED: Budget exceeded!
Current spending: $1000
Flight cost: $500
Budget limit: $1000
```

### Error Handling

All errors are caught and reported clearly:
```
Search error: Invalid input - Destination cannot be empty
Booking error: Invalid input - Passenger name cannot be empty
Calendar error: Invalid input - Date must be in YYYY-MM-DD format
```

## Architecture

### Agent Components

- **Model**: GPT-4 (temperature=0 for deterministic behavior)
- **Tools**: 3 structured tools with Pydantic schemas
- **Prompt**: System prompt with clear guidelines
- **Framework**: LangChain 1.0 with `create_agent` API

### Tool Structure

Each tool follows this pattern:
1. **Input Validation**: Pydantic schema + runtime checks
2. **Business Logic**: Mock implementation (ready for real APIs)
3. **Error Handling**: Try/except with informative messages
4. **Return Format**: Clear, formatted strings

## Customization

### Modify Budget Limit

```python
# In booking_agent.py
BUDGET_LIMIT = 2000  # Change to your desired limit
```

### Add New Tools

```python
from pydantic import BaseModel, Field
from langchain_core.tools import StructuredTool

class MyToolInput(BaseModel):
    param: str = Field(description="Parameter description")

def my_tool(param: str) -> str:
    try:
        # Your logic here
        return "Success"
    except Exception as e:
        return f"Error: {str(e)}"

# Add to tools list in create_flight_booking_agent()
```

### Connect Real APIs

Replace mock implementations with real API calls:
- Flight search: Amadeus, Skyscanner, etc.
- Booking: Airline APIs
- Calendar: Google Calendar, Outlook, etc.

## Testing

```bash
# Test imports
python3 -c "import booking_agent; print('✅ Import successful')"

# Test individual tools
python3 -c "from booking_agent import search_flights; print(search_flights('NYC', 500))"

# Test budget guardrail
python3 -c "from booking_agent import book_flight; book_flight('FL1', 'Alice'); book_flight('FL2', 'Bob'); book_flight('FL3', 'Charlie')"
```

## Requirements

- Python 3.8+
- LangChain 1.0+
- LangChain OpenAI
- Pydantic 2.0+
- OpenAI API key

## License

MIT License (see LICENSE file)

## Contributing

Contributions welcome! Please ensure:
- Error handling in all tools
- Pydantic schemas for new tools
- Documentation for new features
- Tests for critical functionality

## Support

For issues or questions, please open an issue on GitHub.

---

**⚡ Built with LangChain | 🤖 Powered by GPT-4 | 🛡️ Production-Ready**
