from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from uuid import UUID

from db_chromadb import db
from models.domain import Coordinate, ProfitabilityCalculation, LoadOpportunity
from agents.coordinator import coordinator_agent

router = APIRouter(prefix="/api/v1/calculate", tags=["calculations"])


class ProfitabilityRequest(BaseModel):
    """Request for profitability calculation"""
    driver_current: Coordinate
    driver_destination: Coordinate
    vendor_pickup: Coordinate
    vendor_destination: Coordinate
    vendor_offering: float


@router.post("/profitability", response_model=ProfitabilityCalculation)
def calculate_profitability(request: ProfitabilityRequest):
    """
    Calculate profitability for a specific load opportunity
    
    Returns detailed breakdown of:
    - Extra distance required
    - Fuel cost
    - Time cost
    - Net profit
    - Profitability score
    - Estimated time
    """
    from services.math_engine import math_engine
    
    result = math_engine.calculate_full_profitability(
        driver_current=request.driver_current,
        driver_destination=request.driver_destination,
        vendor_pickup=request.vendor_pickup,
        vendor_destination=request.vendor_destination,
        vendor_offering=request.vendor_offering
    )
    
    return ProfitabilityCalculation(**result)


@router.get("/opportunities/{trip_id}")
def get_load_opportunities(trip_id: UUID):
    """
    Get ranked load opportunities for a deadheading trip
    
    Uses AI agents to:
    1. Match loads compatible with the route
    2. Calculate optimal routes
    3. Analyze profitability
    4. Rank by profitability score
    """
    # Get trip details
    trip = db.get_trip(str(trip_id))
    
    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trip with ID {trip_id} not found"
        )
    
    if not trip['is_deadheading']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Trip is not marked as deadheading"
        )
    
    # Get driver's current location and destination
    driver_current = Coordinate(
        lat=trip['origin_lat'],
        lng=trip['origin_lng']
    )
    driver_destination = Coordinate(
        lat=trip['destination_lat'],
        lng=trip['destination_lng']
    )
    
    # Get available loads
    available_loads = db.get_available_loads()
    
    # Use coordinator agent to get recommendations
    opportunities = coordinator_agent.get_load_recommendations(
        driver_current, driver_destination, available_loads
    )
    
    return {
        "trip_id": str(trip_id),
        "opportunities": opportunities,
        "count": len(opportunities)
    }
