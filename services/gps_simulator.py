"""
GPS Simulator - Simulates real-time truck movement
Generates realistic GPS coordinates along routes
"""

import math
import time
from typing import List, Tuple
from models.domain import Coordinate


class GPSSimulator:
    """Simulate GPS tracking for trucks"""
    
    def __init__(self):
        self.EARTH_RADIUS_KM = 6371.0
    
    def generate_route_points(
        self,
        start: Coordinate,
        end: Coordinate,
        num_points: int = 20
    ) -> List[Coordinate]:
        """
        Generate intermediate GPS points along a route
        Simulates truck moving from start to end
        
        Args:
            start: Starting coordinate
            end: Ending coordinate
            num_points: Number of intermediate points
            
        Returns:
            List of coordinates representing the route
        """
        points = []
        
        for i in range(num_points + 1):
            # Linear interpolation between start and end
            fraction = i / num_points
            
            lat = start.lat + (end.lat - start.lat) * fraction
            lng = start.lng + (end.lng - start.lng) * fraction
            
            # Add small random variation to simulate real GPS drift
            import random
            lat += random.uniform(-0.001, 0.001)
            lng += random.uniform(-0.001, 0.001)
            
            points.append(Coordinate(
                lat=lat,
                lng=lng,
                address=f"Point {i+1} on route"
            ))
        
        return points
    
    def simulate_truck_movement(
        self,
        start: Coordinate,
        end: Coordinate,
        speed_kmh: float = 60.0,
        update_interval_seconds: int = 60
    ):
        """
        Generator that yields GPS coordinates as truck moves
        
        Args:
            start: Starting location
            end: Destination
            speed_kmh: Truck speed in km/h
            update_interval_seconds: How often to update position
            
        Yields:
            Current GPS coordinate
        """
        # Calculate total distance
        distance_km = self._calculate_distance(start, end)
        
        # Calculate total time
        total_time_hours = distance_km / speed_kmh
        total_time_seconds = total_time_hours * 3600
        
        # Calculate number of updates
        num_updates = int(total_time_seconds / update_interval_seconds)
        
        # Generate route points
        route_points = self.generate_route_points(start, end, num_updates)
        
        # Yield each point with time delay
        for point in route_points:
            yield point
            time.sleep(update_interval_seconds)
    
    def _calculate_distance(self, point_a: Coordinate, point_b: Coordinate) -> float:
        """Calculate distance between two points using Haversine formula"""
        lat1_rad = math.radians(point_a.lat)
        lon1_rad = math.radians(point_a.lng)
        lat2_rad = math.radians(point_b.lat)
        lon2_rad = math.radians(point_b.lng)
        
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        a = (math.sin(dlat / 2) ** 2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2)
        c = 2 * math.asin(math.sqrt(a))
        
        return self.EARTH_RADIUS_KM * c * 1.3  # Road adjustment
    
    def get_nearby_coordinates(
        self,
        center: Coordinate,
        radius_km: float = 50,
        count: int = 10
    ) -> List[Coordinate]:
        """
        Generate random coordinates within radius of center point
        Useful for simulating nearby vendors/market yards
        
        Args:
            center: Center point
            radius_km: Radius in kilometers
            count: Number of points to generate
            
        Returns:
            List of nearby coordinates
        """
        import random
        
        points = []
        
        for i in range(count):
            # Random angle
            angle = random.uniform(0, 2 * math.pi)
            
            # Random distance within radius
            distance = random.uniform(0, radius_km)
            
            # Convert to lat/lng offset
            # Approximate: 1 degree latitude = 111 km
            lat_offset = (distance * math.cos(angle)) / 111.0
            lng_offset = (distance * math.sin(angle)) / (111.0 * math.cos(math.radians(center.lat)))
            
            points.append(Coordinate(
                lat=center.lat + lat_offset,
                lng=center.lng + lng_offset,
                address=f"Location {i+1} ({distance:.1f}km from center)"
            ))
        
        return points


# Global instance
gps_simulator = GPSSimulator()
