from crewai import Agent, Task
from crewai.tools import tool
from typing import Dict

from agents.base import create_agent
from models.domain import Coordinate
from services.math_engine import math_engine


@tool("calculate_route_distance")
def calculate_route_distance_tool(origin: Dict, destination: Dict) -> float:
    """Calculate distance between two points"""
    origin_coord = Coordinate(**origin)
    dest_coord = Coordinate(**destination)
    return math_engine.calculate_distance(origin_coord, dest_coord)


@tool("calculate_route_time")
def calculate_route_time_tool(distance_km: float) -> float:
    """Calculate estimated travel time based on distance"""
    return math_engine.calculate_estimated_time(distance_km)


class RouteOptimizerAgent:
    """Agent responsible for calculating optimal routes and distances"""
    
    def __init__(self):
        self.agent = create_agent(
            role="Route Optimization Specialist",
            goal="Calculate optimal routes and accurate distance metrics for load opportunities, minimizing travel time and distance",
            backstory="""You are an expert in route planning and logistics optimization. 
            You calculate precise distances and travel times, considering road networks and 
            traffic patterns. You help drivers understand the true cost of detours and 
            ensure they make informed decisions about load opportunities.""",
            tools=[calculate_route_distance_tool, calculate_route_time_tool],
            verbose=True
        )
    
    def calculate_route_metrics(
        self,
        driver_current: Coordinate,
        driver_destination: Coordinate,
        vendor_pickup: Coordinate,
        vendor_destination: Coordinate
    ) -> Dict:
        """
        Calculate complete route metrics for a load opportunity
        
        Args:
            driver_current: Driver's current location
            driver_destination: Driver's intended destination
            vendor_pickup: Vendor's pickup location
            vendor_destination: Vendor's delivery destination
            
        Returns:
            Dictionary with route metrics
        """
        # Calculate direct route (without load)
        direct_distance = math_engine.calculate_distance(driver_current, driver_destination)
        direct_time = math_engine.calculate_estimated_time(direct_distance)
        
        # Calculate detour route (with load)
        dist_to_vendor = math_engine.calculate_distance(driver_current, vendor_pickup)
        dist_vendor_delivery = math_engine.calculate_distance(vendor_pickup, vendor_destination)
        dist_delivery_to_home = math_engine.calculate_distance(vendor_destination, driver_destination)
        
        detour_distance = dist_to_vendor + dist_vendor_delivery + dist_delivery_to_home
        detour_time = math_engine.calculate_estimated_time(detour_distance)
        
        # Calculate extra distance and time
        extra_distance = detour_distance - direct_distance
        extra_time = detour_time - direct_time
        
        return {
            "direct_distance_km": direct_distance,
            "direct_time_hours": direct_time,
            "detour_distance_km": detour_distance,
            "detour_time_hours": detour_time,
            "extra_distance_km": extra_distance,
            "extra_time_hours": extra_time,
            "distance_to_vendor_km": dist_to_vendor,
            "vendor_delivery_distance_km": dist_vendor_delivery,
            "delivery_to_home_km": dist_delivery_to_home
        }


# Global instance
route_optimizer_agent = RouteOptimizerAgent()
