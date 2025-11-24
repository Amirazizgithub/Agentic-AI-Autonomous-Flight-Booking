"""
Agentic AI Autonomous Flight Booking API

FastAPI application demonstrating Agentic AI principles:
- Perception: Understanding user booking requirements
- Planning: Sequencing flight search, booking, and calendar actions
- Action: Autonomous execution of booking workflow
"""
import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Dict, Any

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.models import BookingRequest, BookingResponse, FlightDetails, BookingStatus
from app.agents import create_flight_booking_agent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global agent instance
agent = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global agent
    settings = get_settings()
    
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Environment: {settings.environment}")
    
    # Initialize agent
    try:
        agent = create_flight_booking_agent()
        logger.info("Flight booking agent initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize agent: {e}")
        raise
    
    yield
    
    logger.info("Shutting down application")


# Create FastAPI app
settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Autonomous flight booking system using Agentic AI principles",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def root() -> Dict[str, str]:
    """Root endpoint"""
    return {
        "message": "Agentic AI Autonomous Flight Booking API",
        "version": settings.app_version,
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health", tags=["Health"])
async def health_check() -> Dict[str, Any]:
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": settings.environment,
        "agent_initialized": agent is not None
    }


@app.post(
    "/api/v1/book-flight",
    response_model=BookingResponse,
    status_code=status.HTTP_200_OK,
    tags=["Booking"]
)
async def book_flight_endpoint(request: BookingRequest) -> BookingResponse:
    """
    Book a flight autonomously using Agentic AI
    
    The agent will:
    1. **Perceive**: Understand booking requirements
    2. **Plan**: Determine optimal action sequence
    3. **Act**: Execute search_flights -> book_flight -> add_to_calendar
    
    Args:
        request: Booking request with passenger details, destination, budget, and date
        
    Returns:
        BookingResponse with booking confirmation and agent reasoning
        
    Raises:
        HTTPException: If booking fails or validation errors occur
    """
    global agent
    
    if agent is None:
        logger.error("Agent not initialized")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Booking service not available. Agent not initialized."
        )
    
    logger.info(f"Processing booking request for {request.passenger_name} from {request.departure} to {request.destination}")
    
    try:
        # Execute agent workflow
        result = await agent.process_booking_request(
            passenger_name=request.passenger_name,
            max_price=request.max_price,
            departure=request.departure,
            destination=request.destination,
            booking_date=request.booking_date
        )
        
        if not result.get("success"):
            logger.error(f"Booking failed: {result.get('message')}")
            return BookingResponse(
                status=BookingStatus.FAILED,
                message=result.get("message", "Booking failed"),
                agent_reasoning=[step.get("action", "") for step in result.get("reasoning_steps", [])]
            )
        
        # Extract booking details
        details = agent.extract_booking_details(result)
        
        # Build response
        response = BookingResponse(
            status=BookingStatus(details.get("status", "failed")),
            message=result.get("message", "Booking processed"),
            booking_id=details.get("booking_id"),
            calendar_event_id=details.get("calendar_event_id"),
            agent_reasoning=[
                f"{step.get('action')}: {step.get('input')}" 
                for step in result.get("reasoning_steps", [])
            ]
        )
        
        # Add flight details if available
        if details.get("flight_number") and details.get("price"):
            response.flight_details = FlightDetails(
                flight_number=details["flight_number"],
                airline="",  # Extracted from flight number if needed
                departure=request.departure,
                destination=request.destination,
                departure_time="",
                arrival_time="",
                price=details["price"],
                duration=""
            )
        
        logger.info(f"Booking completed: {details.get('booking_id')} - Status: {response.status}")
        
        return response
        
    except Exception as e:
        logger.error(f"Error processing booking: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing booking request: {str(e)}"
        )


@app.get("/api/v1/agent-info", tags=["Agent"])
async def get_agent_info() -> Dict[str, Any]:
    """
    Get information about the Agentic AI system
    
    Returns:
        Information about agent capabilities and tools
    """
    global agent
    
    if agent is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Agent not initialized"
        )
    
    return {
        "agent_type": "Autonomous Flight Booking Agent",
        "principles": {
            "perception": "Understands user booking requirements and context",
            "planning": "Sequences actions: search -> book -> calendar",
            "action": "Executes tools autonomously without user intervention"
        },
        "tools": [
            {
                "name": "search_flights",
                "description": "Search for available flights to destination within budget"
            },
            {
                "name": "book_flight",
                "description": "Book a selected flight for the passenger"
            },
            {
                "name": "add_to_calendar",
                "description": "Add booked flight to passenger's calendar"
            }
        ],
        "model": settings.openai_model,
        "max_iterations": settings.max_iterations
    }


# Exception handlers
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Handle validation errors"""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle unexpected errors"""
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.environment == "main"
    )
