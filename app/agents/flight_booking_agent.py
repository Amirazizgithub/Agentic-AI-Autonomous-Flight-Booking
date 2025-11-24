"""LangChain Agent for Autonomous Flight Booking
Implements Agentic AI principles: Perception, Planning, and Action
"""
import json
import re
from typing import Dict, Any, List, Optional
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage, HumanMessage

from app.tools.flight_search import search_flights
from app.tools.booking import book_flight
from app.tools.calendar import add_to_calendar
from app.config import get_settings


class FlightBookingAgent:
    """
    Agentic AI Flight Booking System
    
    Demonstrates three core principles:
    1. Perception: Understanding user requirements and context
    2. Planning: Sequencing actions to achieve the goal
    3. Action: Executing tools in the correct order
    """
    
    def __init__(self, llm: ChatOpenAI, tools: List, agent_executor: AgentExecutor):
        self.llm = llm
        self.tools = tools
        self.agent_executor = agent_executor
        self.reasoning_steps = []
    
    async def process_booking_request(
        self,
        passenger_name: str,
        max_price: float,
        departure: str,
        destination: str,
        booking_date: str
    ) -> Dict[str, Any]:
        """
        Process a flight booking request autonomously
        
        This method demonstrates the agent's ability to:
        - Perceive: Understand the booking requirements
        - Plan: Determine the sequence of actions needed
        - Act: Execute search, booking, and calendar tools
        
        Args:
            passenger_name: Name of the passenger
            max_price: Maximum price budget
            departure: Departure city
            destination: Destination city
            booking_date: Travel date
            
        Returns:
            Dictionary containing booking results and agent reasoning
        """
        self.reasoning_steps = []
        
        # Create the prompt for the agent
        prompt = f"""You are an autonomous flight booking assistant. Your task is to help book a flight.

User Requirements:
- Passenger Name: {passenger_name}
- Maximum Price: ₹{max_price}
- Departure: {departure}
- Destination: {destination}
- Travel Date: {booking_date}

Your goal is to:
1. SEARCH for available flights using search_flights tool
2. SELECT the best flight option (cheapest or best value)
3. BOOK the selected flight using book_flight tool
4. ADD the flight to calendar using add_to_calendar tool

Important Instructions:
- Always search for flights first
- Parse the search results carefully to extract flight details
- Book the cheapest available flight that fits the criteria
- Create a clear calendar event with flight details
- Provide a summary of actions taken

Begin the booking process now."""

        try:
            # Execute the agent
            result = await self.agent_executor.ainvoke({
                "input": prompt
            })
            
            # Extract reasoning from intermediate steps
            if "intermediate_steps" in result:
                for step in result["intermediate_steps"]:
                    action, observation = step
                    self.reasoning_steps.append({
                        "action": action.tool,
                        "input": action.tool_input,
                        "observation": str(observation)[:200]  # Truncate for readability
                    })
            
            # Parse the final output
            output = result.get("output", "")
            
            return {
                "success": True,
                "message": output,
                "reasoning_steps": self.reasoning_steps,
                "raw_result": result
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error processing booking: {str(e)}",
                "reasoning_steps": self.reasoning_steps,
                "error": str(e)
            }
    
    def extract_booking_details(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract structured booking details from agent output
        
        Args:
            result: Agent execution result
            
        Returns:
            Structured booking information
        """
        details = {
            "booking_id": None,
            "flight_number": None,
            "price": None,
            "calendar_event_id": None,
            "status": "unknown"
        }
        
        try:
            # Extract from reasoning steps
            for step in self.reasoning_steps:
                observation = step.get("observation", "")
                
                # Extract booking ID
                booking_match = re.search(r"'booking_id':\s*'([^']+)'", observation)
                if booking_match:
                    details["booking_id"] = booking_match.group(1)
                
                # Extract flight number
                flight_match = re.search(r"'flight_number':\s*'([^']+)'", observation)
                if flight_match:
                    details["flight_number"] = flight_match.group(1)
                
                # Extract price
                price_match = re.search(r"'price':\s*(\d+(?:\.\d+)?)", observation)
                if price_match:
                    details["price"] = float(price_match.group(1))
                
                # Extract calendar event ID
                event_match = re.search(r"'event_id':\s*'([^']+)'", observation)
                if event_match:
                    details["calendar_event_id"] = event_match.group(1)
            
            # Determine status
            if details["booking_id"] and details["calendar_event_id"]:
                details["status"] = "confirmed"
            elif details["booking_id"]:
                details["status"] = "booked"
            elif any("flights_found" in step.get("observation", "") for step in self.reasoning_steps):
                details["status"] = "found"
            else:
                details["status"] = "failed"
            
        except Exception as e:
            print(f"Error extracting details: {e}")
        
        return details


def create_flight_booking_agent(api_key: Optional[str] = None) -> FlightBookingAgent:
    """
    Factory function to create a FlightBookingAgent
    
    Args:
        api_key: Optional OpenAI API key (uses config if not provided)
        
    Returns:
        Configured FlightBookingAgent instance
    """
    settings = get_settings()
    
    # Initialize LLM
    llm = ChatOpenAI(
        model=settings.openai_model,
        temperature=settings.agent_temperature,
        api_key=api_key or settings.openai_api_key
    )
    
    # Define tools
    tools = [search_flights, book_flight, add_to_calendar]
    
    # Create system prompt
    system_message = """You are an expert autonomous flight booking agent. You have access to three tools:

1. search_flights: Search for available flights to a destination
2. book_flight: Book a specific flight for a passenger
3. add_to_calendar: Add the booked flight to the passenger's calendar

Your approach should follow these principles:

**PERCEPTION**: Understand the user's requirements (destination, budget, date, passenger name)

**PLANNING**: 
- First, search for available flights
- Analyze the results and select the best option (usually cheapest within budget)
- Book the selected flight
- Add the booking to the calendar

**ACTION**: Execute each step systematically and handle any errors gracefully

Always provide clear feedback about what you're doing and the results of each action.
Be autonomous - make decisions and take actions without asking for confirmation.
"""
    
    # Create prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    # Create agent
    agent = create_openai_functions_agent(llm, tools, prompt)
    
    # Create agent executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=settings.max_iterations,
        return_intermediate_steps=True,
        handle_parsing_errors=True
    )
    
    return FlightBookingAgent(llm, tools, agent_executor)
