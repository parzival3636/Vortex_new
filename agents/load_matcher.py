from crewai import Agent, Task
from crewai.tools import tool
from typing import List, Dict

from agents.base import create_agent
from models.domain import Coordinate
from services.math_engine import math_engine
from config import settings


@tool("calculate_route_deviation")
def calculate_route_deviation_tool(
    driver_lat: float,
    driver_lng: float,
    driver_dest_lat: float,
    driver_dest_lng: float,
    vendor_lat: float,
    vendor_lng: float
) -> float:
    """Calculate how far the vendor pickup location deviates from driver's direct route"""
    driver_loc = Coordinate(lat=driver_lat, lng=driver_lng)
    driver_dest = Coordinate(lat=driver_dest_lat, lng=driver_dest_lng)
    vendor_loc = Coordinate(lat=vendor_lat, lng=vendor_lng)
    
    # Calculate direct distance
    direct_distance = math_engine.calculate_distance(driver_loc, driver_dest)
    
    # Calculate distance via vendor
    to_vendor = math_engine.calculate_distance(driver_loc, vendor_loc)
    vendor_to_dest = math_engine.calculate_distance(vendor_loc, driver_dest)
    
    # Deviation is the extra distance
    deviation = (to_vendor + vendor_to_dest) - direct_distance
    
    return deviation


class LoadMatcherAgent:
    """Agent responsible for finding compatible loads for deadheading trucks"""
    
    def __init__(self):
        self.agent = create_agent(
            role="Load Matcher Specialist",
            goal="Find vendor loads that are compatible with driver return routes based on geographic proximity and route deviation",
            backstory="""You are an expert in geographic matching and route compatibility. 
            You analyze driver routes and vendor load locations to find optimal matches that 
            minimize detours while maximizing load opportunities. You understand that drivers 
            want to avoid significant deviations from their planned routes.""",
            tools=[calculate_route_deviation_tool],
            verbose=True
        )
    
    def create_matching_task(
        self,
        driver_current: Coordinate,
        driver_destination: Coordinate,
        available_loads: List[Dict]
    ) -> Task:
        """
        Create a task to match loads with the driver's route
        
        Args:
            driver_current: Driver's current location
            driver_destination: Driver's intended destination
            available_loads: List of available load dictionaries
            
        Returns:
            CrewAI Task for load matching
        """
        task_description = f"""
        Analyze the driver's route and find compatible loads:
        
        Driver Current Location: {driver_current.lat}, {driver_current.lng}
        Driver Destination: {driver_destination.lat}, {driver_destination.lng}
        
        Available Loads: {len(available_loads)} loads to analyze
        
        For each load:
        1. Calculate the route deviation from the driver's direct path
        2. Filter loads where deviation is within {settings.max_route_deviation_km}km
        3. Return matched loads with their deviation metrics
        
        Focus on loads that require minimal detours while still being profitable.
        """
        
        return Task(
            description=task_description,
            agent=self.agent,
            expected_output="List of compatible loads with deviation metrics, filtered by maximum acceptable deviation"
        )
    
    def match_loads(
        self,
        driver_current: Coordinate,
        driver_destination: Coordinate,
        available_loads: List[Dict]
    ) -> List[Dict]:
        """
        Match available loads with driver's route
        
        Args:
            driver_current: Driver's current location
            driver_destination: Driver's destination
            available_loads: List of available loads from ChromaDB
            
        Returns:
            List of matched loads with deviation metrics
        """
        matched_loads = []
        
        for load in available_loads:
            vendor_pickup = Coordinate(
                lat=float(load['pickup_lat']),
                lng=float(load['pickup_lng'])
            )
            
            # Calculate deviation (distance to vendor pickup)
            deviation = math_engine.calculate_distance(driver_current, vendor_pickup)
            
            # Filter by max deviation
            if deviation <= settings.max_route_deviation_km:
                matched_loads.append({
                    "load_id": str(load['load_id']),
                    "vendor_id": str(load['vendor_id']),
                    "weight_kg": float(load['weight_kg']),
                    "pickup_location": {
                        "lat": float(load['pickup_lat']),
                        "lng": float(load['pickup_lng']),
                        "address": load['pickup_address']
                    },
                    "destination": {
                        "lat": float(load['destination_lat']),
                        "lng": float(load['destination_lng']),
                        "address": load['destination_address']
                    },
                    "price_offered": float(load['price_offered']),
                    "deviation_km": deviation
                })
        
        return matched_loads


# Global instance
load_matcher_agent = LoadMatcherAgent()
