import math
from typing import Tuple
from models.domain import Coordinate
from config import settings


class MathEngine:
    """Core calculation service for distance, cost, and profitability computations"""
    
    def __init__(self):
        self.fuel_consumption_rate = settings.default_fuel_consumption_rate
        self.fuel_price = settings.default_fuel_price
        self.driver_hourly_rate = settings.default_driver_hourly_rate
        self.average_truck_speed = settings.average_truck_speed
        self.max_route_deviation_km = settings.max_route_deviation_km
        self.distance_accuracy_tolerance = settings.distance_accuracy_tolerance
        
        # Earth radius in kilometers
        self.EARTH_RADIUS_KM = 6371.0
        # Road network adjustment factor (straight line * 1.3 ≈ road distance)
        self.ROAD_ADJUSTMENT_FACTOR = 1.3
    
    def calculate_distance(self, point_a: Coordinate, point_b: Coordinate) -> float:
        """
        Calculate road distance between two geographic points in kilometers
        Uses Haversine formula with road network adjustment factor
        
        Args:
            point_a: Starting coordinate
            point_b: Ending coordinate
            
        Returns:
            Distance in kilometers
        """
        # Convert latitude and longitude from degrees to radians
        lat1_rad = math.radians(point_a.lat)
        lon1_rad = math.radians(point_a.lng)
        lat2_rad = math.radians(point_b.lat)
        lon2_rad = math.radians(point_b.lng)
        
        # Haversine formula
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        a = (math.sin(dlat / 2) ** 2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2)
        c = 2 * math.asin(math.sqrt(a))
        
        # Calculate straight-line distance
        straight_distance = self.EARTH_RADIUS_KM * c
        
        # Apply road network adjustment factor
        road_distance = straight_distance * self.ROAD_ADJUSTMENT_FACTOR
        
        return round(road_distance, 2)
    
    def calculate_extra_distance(
        self,
        driver_current: Coordinate,
        driver_destination: Coordinate,
        vendor_pickup: Coordinate,
        vendor_destination: Coordinate
    ) -> float:
        """
        Calculate extra distance for taking a load opportunity
        
        Formula:
        extra_distance = distance(driver_current → vendor_pickup) +
                        distance(vendor_pickup → vendor_destination) +
                        distance(vendor_destination → driver_destination) -
                        distance(driver_current → driver_destination)
        
        Args:
            driver_current: Driver's current location
            driver_destination: Driver's intended destination
            vendor_pickup: Vendor's pickup location
            vendor_destination: Vendor's delivery destination
            
        Returns:
            Extra distance in kilometers
        """
        # Calculate detour route
        dist_to_vendor = self.calculate_distance(driver_current, vendor_pickup)
        dist_vendor_delivery = self.calculate_distance(vendor_pickup, vendor_destination)
        dist_delivery_to_home = self.calculate_distance(vendor_destination, driver_destination)
        
        # Calculate direct route
        dist_direct = self.calculate_distance(driver_current, driver_destination)
        
        # Calculate extra distance
        extra_distance = (dist_to_vendor + dist_vendor_delivery + 
                         dist_delivery_to_home - dist_direct)
        
        return round(extra_distance, 2)
    
    def calculate_fuel_cost(
        self,
        distance_km: float,
        fuel_consumption_rate: float = None,
        fuel_price_per_liter: float = None
    ) -> float:
        """
        Calculate fuel cost for a given distance
        
        Formula:
        fuel_cost = distance_km * fuel_consumption_rate * fuel_price_per_liter
        
        Args:
            distance_km: Distance in kilometers
            fuel_consumption_rate: Liters per km (defaults to config value)
            fuel_price_per_liter: Price per liter (defaults to config value)
            
        Returns:
            Fuel cost in currency units
        """
        if fuel_consumption_rate is None:
            fuel_consumption_rate = self.fuel_consumption_rate
        if fuel_price_per_liter is None:
            fuel_price_per_liter = self.fuel_price
        
        fuel_cost = distance_km * fuel_consumption_rate * fuel_price_per_liter
        return round(fuel_cost, 2)
    
    def calculate_time_cost(
        self,
        time_hours: float,
        driver_hourly_rate: float = None
    ) -> float:
        """
        Calculate time cost for driver
        
        Formula:
        time_cost = time_hours * driver_hourly_rate
        
        Args:
            time_hours: Time in hours
            driver_hourly_rate: Driver's hourly rate (defaults to config value)
            
        Returns:
            Time cost in currency units
        """
        if driver_hourly_rate is None:
            driver_hourly_rate = self.driver_hourly_rate
        
        time_cost = time_hours * driver_hourly_rate
        return round(time_cost, 2)
    
    def calculate_net_profit(
        self,
        vendor_offering: float,
        fuel_cost: float,
        time_cost: float
    ) -> float:
        """
        Calculate net profit for load opportunity
        
        Formula:
        net_profit = vendor_offering - fuel_cost - time_cost
        
        Args:
            vendor_offering: Price offered by vendor
            fuel_cost: Calculated fuel cost
            time_cost: Calculated time cost
            
        Returns:
            Net profit in currency units
        """
        net_profit = vendor_offering - fuel_cost - time_cost
        return round(net_profit, 2)
    
    def calculate_profitability_score(
        self,
        net_profit: float,
        total_time_hours: float
    ) -> float:
        """
        Calculate profitability score for ranking
        
        Formula:
        profitability_score = net_profit / total_time_hours
        
        Args:
            net_profit: Net profit amount
            total_time_hours: Total time required
            
        Returns:
            Profitability score (profit per hour)
        """
        if total_time_hours == 0:
            return 0.0
        
        profitability_score = net_profit / total_time_hours
        return round(profitability_score, 4)
    
    def calculate_estimated_time(self, distance_km: float) -> float:
        """
        Calculate estimated travel time based on distance
        
        Args:
            distance_km: Distance in kilometers
            
        Returns:
            Estimated time in hours
        """
        time_hours = distance_km / self.average_truck_speed
        return round(time_hours, 2)
    
    def calculate_full_profitability(
        self,
        driver_current: Coordinate,
        driver_destination: Coordinate,
        vendor_pickup: Coordinate,
        vendor_destination: Coordinate,
        vendor_offering: float,
        fuel_consumption_rate: float = None,
        fuel_price_per_liter: float = None,
        driver_hourly_rate: float = None
    ) -> dict:
        """
        Calculate complete profitability analysis for a load opportunity
        
        Returns:
            Dictionary with all calculation components
        """
        # Calculate extra distance
        extra_distance = self.calculate_extra_distance(
            driver_current, driver_destination, vendor_pickup, vendor_destination
        )
        
        # Calculate estimated time
        estimated_time = self.calculate_estimated_time(extra_distance)
        
        # Calculate costs
        fuel_cost = self.calculate_fuel_cost(
            extra_distance, fuel_consumption_rate, fuel_price_per_liter
        )
        time_cost = self.calculate_time_cost(estimated_time, driver_hourly_rate)
        
        # Calculate profit
        net_profit = self.calculate_net_profit(vendor_offering, fuel_cost, time_cost)
        profitability_score = self.calculate_profitability_score(net_profit, estimated_time)
        
        return {
            "extra_distance_km": extra_distance,
            "estimated_time_hours": estimated_time,
            "fuel_cost": fuel_cost,
            "time_cost": time_cost,
            "net_profit": net_profit,
            "profitability_score": profitability_score
        }


# Global instance
math_engine = MathEngine()
