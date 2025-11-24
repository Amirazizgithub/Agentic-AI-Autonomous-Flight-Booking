# API Examples

## Using Python Requests

```python
import requests
import json

url = "http://localhost:8000/api/v1/book-flight"
payload = {
    "passenger_name": "Jane Smith",
    "max_price": 6000,
    "departure": "Delhi",
    "destination": "Mumbai",
    "booking_date": "30-11-2025"
}

response = requests.post(url, json=payload)
print(json.dumps(response.json(), indent=2))
```

## Using JavaScript/Fetch

```javascript
const url = 'http://localhost:8000/api/v1/book-flight';
const data = {
  passenger_name: 'Jane Smith',
  max_price: 6000,
  departure: 'Delhi',
  destination: 'Mumbai',
  booking_date: '25-11-2025'
};

fetch(url, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(data)
})
.then(response => response.json())
.then(data => console.log(data));
```

## Using PowerShell

```powershell
$body = @{
    passenger_name = "Jane Smith"
    max_price = 6000,
    departure = 'Delhi',
    destination = "Mumbai"
    booking_date = "30-11-2025"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/book-flight" `
    -Method Post `
    -Body $body `
    -ContentType "application/json"
```

## Response Example

```json
{
  "status": "confirmed",
  "message": "Flight AI456 booked successfully for Jane Smith to Mumbai on 30-11-2025. Added to calendar.",
  "booking_id": "BK789012",
  "flight_details": {
    "flight_number": "AI456",
    "airline": "Air India",
    "departure": "Delhi",
    "destination": "Mumbai",
    "departure_time": "14:30",
    "arrival_time": "17:00",
    "price": 4800,
    "duration": "2h 30m"
  },
  "calendar_event_id": "CAL345678",
  "timestamp": "2025-11-24T12:00:00Z",
  "agent_reasoning": [
    "search_flights: Found 3 available flights to Mumbai",
    "book_flight: Booked flight AI456 for ₹4800",
    "add_to_calendar: Added event to calendar"
  ]
}
```
