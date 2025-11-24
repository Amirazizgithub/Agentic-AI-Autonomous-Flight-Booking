# Agentic AI - Autonomous Flight Booking System

A production-level FastAPI application demonstrating **Agentic AI principles** (Perception, Planning, Action) by automating the entire flight booking workflow. Uses LangChain as the reasoning engine to autonomously sequence calls to mock FlightSearch, Booking, and Calendar tools.

## 🎯 Features

- **Autonomous Agent**: LangChain-powered agent that understands, plans, and executes booking workflows
- **Three Core Principles**:
  - **Perception**: Understands user booking requirements
  - **Planning**: Determines optimal action sequence
  - **Action**: Executes tools autonomously (search → book → calendar)
- **FastAPI Backend**: Production-ready REST API with async support
- **Mock Tools**: Realistic flight search, booking, and calendar integration simulations
- **Full Validation**: Pydantic models for request/response validation
- **Docker Support**: Containerized deployment ready
- **Comprehensive Testing**: Unit and integration tests included

## 🏗️ Architecture

```
┌─────────────────┐
│   FastAPI API   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  LangChain      │
│  Agent Engine   │
└────────┬────────┘
         │
    ┌────┴────┬──────────┬───────────┐
    ▼         ▼          ▼           ▼
┌────────┐ ┌──────┐ ┌─────────┐ ┌──────────┐
│ Search │ │ Book │ │Calendar │ │  More... │
│ Flights│ │Flight│ │         │ │          │
└────────┘ └──────┘ └─────────┘ └──────────┘
```

## 📁 Project Structure

```
Agentic-AI-Autonomous-Flight-Booking/
├── app/                     # Main application
│   ├── agents/              # LangChain agent
│   ├── config/              # Settings
│   ├── models/              # Pydantic schemas
│   └── tools/               # Mock tools
├── tests/                   # Pytest test suite
│   ├── test_api_endpoints.py
│   ├── test_models.py
│   ├── test_tools.py
│   └── README.md
├── .env                     # Environment variables
├── .gitignore               # Git ignore rules
├── conftest.py              # Pytest configuration
├── docker-compose.yml       # Docker compose
├── Dockerfile               # Docker image
├── EXAMPLES.md              # API examples
├── LICENSE                  # MIT license
├── pytest.ini               # Pytest settings
├── QUICKSTART.md            # Quick start guide
├── README.md                # Main documentation
└── requirements.txt         # Python dependencies
```

## 📋 Prerequisites

- Python 3.11+
- OpenAI API Key
- pip or poetry

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone [<repository-url>](https://github.com/Amirazizgithub/Agentic-AI-Autonomous-Flight-Booking.git)
cd Agentic-AI-Autonomous-Flight-Booking
```

### 2. Set Up Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
# Copy env file
copy .env

# Edit .env and add your OpenAI API key
OPENAI_API_KEY=your_actual_api_key_here
ENVIRONMENT=main
LOG_LEVEL=INFO
```

### 4. Run the Application

```bash
# Start the FastAPI server
python -m uvicorn app.main:app --reload

# Or use:
python app/main.py
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once the server is running, access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### API Endpoints

#### 1. Book Flight (Main Endpoint)

**POST** `/api/v1/book-flight`

Request body:
```json
{
  "passenger_name": "John Doe",
  "max_price": 5000,
  "departure": "Delhi",
  "destination": "Mumbai",
  "booking_date": "25-11-2025"
}
```

Response:
```json
{
  "status": "confirmed",
  "message": "Flight booked successfully and added to calendar",
  "booking_id": "BK123456",
  "flight_details": {
    "flight_number": "AI101",
    "airline": "Air India",
    "departure": "Delhi",
    "destination": "Mumbai",
    "departure_time": "10:00",
    "arrival_time": "12:30",
    "price": 4500,
    "duration": "2h 30m"
  },
  "calendar_event_id": "CAL789",
  "timestamp": "2025-11-24T10:00:00Z",
  "agent_reasoning": [
    "search_flights: Searching for flights...",
    "book_flight: Booking selected flight...",
    "add_to_calendar: Adding to calendar..."
  ]
}
```

#### 2. Health Check

**GET** `/health`

Returns API health status and agent initialization state.

#### 3. Agent Info

**GET** `/api/v1/agent-info`

Returns information about the agent's capabilities and tools.

## 🧪 Testing

### Automated Tests (Recommended)

Run the full pytest test suite:

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_models.py -v
pytest tests/test_tools.py -v
pytest tests/test_api_endpoints.py -v

# Run with coverage
pip install pytest-cov
pytest --cov=app --cov-report=html
```

**Test Coverage:**
- ✅ 23 automated tests
- ✅ Model validation tests
- ✅ Tool functionality tests
- ✅ API endpoint tests
- ✅ Error handling tests

### Manual Tests

```bash
# Test the agent directly (no API needed)
python test_agent.py

# Manual API tests (requires running server)
# Terminal 1: Start server
python -m uvicorn app.main:app --reload

# Terminal 2: Run manual tests
python manual_test_api.py
```

### Example cURL Request

```bash
curl -X POST "http://localhost:8000/api/v1/book-flight" \
  -H "Content-Type: application/json" \
  -d '{
    "passenger_name": "John Doe",
    "max_price": 5000,
    "departure": "Delhi",
    "destination": "Mumbai",
    "booking_date": "25-11-2025"
  }'
```

## 🐳 Docker Deployment

### Build and Run with Docker

```bash
# Build image
docker build -t agentic-flight-booking .

# Run container
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your_api_key_here \
  agentic-flight-booking
```

### Using Docker Compose

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🔧 Configuration

Edit `.env` file to customize:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4

# Application Settings
ENVIRONMENT=development
LOG_LEVEL=INFO

# Agent Configuration
MAX_ITERATIONS=10
AGENT_TEMPERATURE=0.7
```

## 🎓 How the Agent Works

The agent demonstrates three key principles of Agentic AI:

### 1. **Perception** 👁️
The agent understands the user's intent from the booking request:
- Passenger name
- Budget constraints
- Destination
- Travel date

### 2. **Planning** 🧠
The agent creates an execution plan:
1. Search for available flights within budget
2. Select the best option (usually cheapest)
3. Book the selected flight
4. Add booking to calendar

### 3. **Action** 🎬
The agent autonomously executes the plan:
- Calls `search_flights` tool
- Analyzes results
- Calls `book_flight` tool
- Calls `add_to_calendar` tool
- Returns comprehensive results

## 🛠️ Available Tools

### 1. search_flights
Searches for available flights matching criteria.

### 2. book_flight
Books a specific flight for a passenger.

### 3. add_to_calendar
Adds the booked flight to the passenger's calendar.

## 📊 Sample Agent Reasoning

```
Step 1: search_flights
Input: {destination: "Mumbai", max_price: 5000, date: "25-11-2025"}
Output: Found 3 flights, cheapest is AI101 at ₹4500

Step 2: book_flight
Input: {flight_number: "AI101", passenger: "John Doe", price: 4500}
Output: Booking confirmed with ID BK123456

Step 3: add_to_calendar
Input: {title: "Flight to Mumbai", date: "25-11-2025", time: "10:00"}
Output: Calendar event created with ID CAL789
```

## 🚨 Error Handling

The application includes comprehensive error handling:
- Input validation errors (400)
- Service unavailable (503)
- Internal server errors (500)
- Agent execution failures

## 🔐 Security Considerations

For production deployment:
- Store API keys securely (environment variables, secrets manager)
- Add authentication/authorization
- Implement rate limiting
- Use HTTPS
- Add input sanitization
- Implement logging and monitoring

## 📈 Future Enhancements

- [ ] Real flight API integration (Amadeus, Skyscanner)
- [ ] User authentication and authorization
- [ ] Database for booking persistence
- [ ] Payment gateway integration
- [ ] Email/SMS notifications
- [ ] Multi-city and round-trip support
- [ ] Price alerts and monitoring
- [ ] Advanced filtering (airlines, stops, times)

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file[LICENSE] for details.

## 👨‍💻 Author

Built with ❤️ using LangChain, FastAPI, and Agentic AI principles

## 📞 Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Note**: This is a demonstration project using mock APIs. Replace mock tools with real flight booking APIs for production use.
