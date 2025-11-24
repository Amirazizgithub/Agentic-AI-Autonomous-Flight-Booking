# Testing Guide

## Automated Tests (pytest)

### Installation
```bash
pip install -r requirements.txt
```

### Run All Tests
```bash
pytest
```

### Run Specific Test Files
```bash
# Test models
pytest tests/test_models.py -v

# Test tools
pytest tests/test_tools.py -v

# Test API endpoints
pytest tests/test_api_endpoints.py -v
```

### Run with Coverage
```bash
pip install pytest-cov
pytest --cov=app --cov-report=html
```

### Test Structure
```
tests/
├── __init__.py
├── test_models.py         # Pydantic model validation tests
├── test_tools.py          # Tool function tests (search, book, calendar)
└── test_api_endpoints.py  # FastAPI endpoint tests
```

## Manual Testing

### Agent Test (No API needed)
```bash
python test_agent.py
```

### Manual API Test (Requires running server)
```bash
# Terminal 1: Start the server
python -m uvicorn app.main:app --reload

# Terminal 2: Run manual tests
python manual_test_api.py
```

## Test Coverage

### Unit Tests
- ✅ BookingRequest validation
- ✅ Date format validation
- ✅ Price validation
- ✅ Required field validation
- ✅ Flight search tool
- ✅ Booking tool
- ✅ Calendar tool

### Integration Tests
- ✅ API endpoints (root, health, agent-info)
- ✅ Booking endpoint validation
- ✅ Error handling

### End-to-End Tests
- 🔧 Manual test script for full booking workflow

## Example Test Run

```bash
$ pytest -v

tests/test_models.py::TestBookingRequest::test_valid_booking_request PASSED
tests/test_models.py::TestBookingRequest::test_invalid_date_format PASSED
tests/test_models.py::TestBookingRequest::test_negative_price PASSED
tests/test_tools.py::TestFlightSearch::test_search_flights_success PASSED
tests/test_tools.py::TestBookFlight::test_book_flight_success PASSED
tests/test_api_endpoints.py::TestRootEndpoints::test_root_endpoint PASSED
tests/test_api_endpoints.py::TestBookingEndpoint::test_booking_request_valid PASSED

========================= 23 passed in 2.5s =========================
```

## Troubleshooting

### Tests fail with import errors
```bash
# Make sure you're in the project root
cd Agentic-AI-Autonomous-Flight-Booking

# Install dependencies
pip install -r requirements.txt
```

### Agent initialization fails
- Check `.env` file has valid `OPENAI_API_KEY`
- Some tests may skip agent tests if not initialized

### Manual tests can't connect
- Make sure API server is running: `python -m uvicorn app.main:app --reload`
- Check server is on http://localhost:8000
