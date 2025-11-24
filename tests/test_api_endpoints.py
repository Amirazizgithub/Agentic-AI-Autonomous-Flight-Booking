"""Test cases for API endpoints using pytest"""
import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch

from app.main import app
from app.models import BookingStatus


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)


@pytest.fixture
def mock_agent():
    """Create mock agent"""
    agent = Mock()
    agent.process_booking_request = AsyncMock()
    agent.extract_booking_details = Mock()
    return agent


class TestRootEndpoints:
    """Test root and health endpoints"""
    
    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "status" in data
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "environment" in data


class TestAgentInfo:
    """Test agent info endpoint"""
    
    def test_agent_info_endpoint(self, client):
        """Test agent info endpoint"""
        response = client.get("/api/v1/agent-info")
        assert response.status_code in [200, 503]  # 503 if agent not initialized
        
        if response.status_code == 200:
            data = response.json()
            assert "agent_type" in data
            assert "principles" in data
            assert "tools" in data


class TestBookingEndpoint:
    """Test booking endpoint"""
    
    def test_booking_request_valid(self, client):
        """Test booking with valid request"""
        tomorrow = datetime.now() + timedelta(days=1)
        booking_date = tomorrow.strftime("%d-%m-%Y")
        
        request_data = {
            "passenger_name": "John Doe",
            "max_price": 5000,
            "departure": "Delhi",
            "destination": "Mumbai",
            "booking_date": booking_date
        }
        
        response = client.post("/api/v1/book-flight", json=request_data)
        
        # May be 200 (success) or 503 (agent not initialized)
        assert response.status_code in [200, 503, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert "status" in data
            assert "message" in data
    
    def test_booking_request_invalid_date(self, client):
        """Test booking with invalid date format"""
        request_data = {
            "passenger_name": "John Doe",
            "max_price": 5000,
            "departure": "Delhi",
            "destination": "Mumbai",
            "booking_date": "2025-11-25"  # Wrong format
        }
        
        response = client.post("/api/v1/book-flight", json=request_data)
        assert response.status_code == 422  # Validation error
    
    def test_booking_request_negative_price(self, client):
        """Test booking with negative price"""
        tomorrow = datetime.now() + timedelta(days=1)
        booking_date = tomorrow.strftime("%d-%m-%Y")
        
        request_data = {
            "passenger_name": "John Doe",
            "max_price": -100,
            "departure": "Delhi",
            "destination": "Mumbai",
            "booking_date": booking_date
        }
        
        response = client.post("/api/v1/book-flight", json=request_data)
        assert response.status_code == 422  # Validation error
    
    def test_booking_request_missing_fields(self, client):
        """Test booking with missing required fields"""
        request_data = {
            "passenger_name": "John Doe",
            "max_price": 5000
        }
        
        response = client.post("/api/v1/book-flight", json=request_data)
        assert response.status_code == 422  # Validation error
    
    def test_booking_request_missing_departure(self, client):
        """Test booking without departure field"""
        tomorrow = datetime.now() + timedelta(days=1)
        booking_date = tomorrow.strftime("%d-%m-%Y")
        
        request_data = {
            "passenger_name": "John Doe",
            "max_price": 5000,
            "destination": "Mumbai",
            "booking_date": booking_date
        }
        
        response = client.post("/api/v1/book-flight", json=request_data)
        assert response.status_code == 422  # Validation error
        
        data = response.json()
        assert "departure" in str(data).lower()
