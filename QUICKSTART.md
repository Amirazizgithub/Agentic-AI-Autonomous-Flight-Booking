# Quick Start Guide

## Installation

1. **Clone and navigate to project**
   ```bash
   cd Agentic-AI-Autonomous-Flight-Booking
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   copy .env.example .env
   # Edit .env and add your OpenAI API key
   ```

5. **Run the application**
   ```bash
   python -m uvicorn app.main:app --reload
   ```

6. **Access the API**
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs

## Quick Test

```bash
# Test with curl
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

Or run the test script:
```bash
python test_api.py
```

## Docker Quick Start

```bash
docker-compose up -d
```

That's it! The API is now running at http://localhost:8000
