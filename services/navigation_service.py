"""
Navigation Service
Handles live navigation and route calculation
"""

from typing import Dict, List, Optional
from datetime import datetime
import math

from db_chromadb import db
from services.math_engine import calculate_distance


class NavigationService:
    """Service for navigation and route tracking"""
    
    AVERAGE_SPEED_KMH = 60
    WAYPOINT_THRESHOLD_METERS = 100  # 100 meters to consider waypoint reached
    
    def update_location(self, vehicle_id: str, latitude: float, longitude: float, accuracy: float) -> Dict:
        """Update vehicle location"""
        location = db.add_location_update(vehicle_id, latitude, longitude, accuracy)
        return {"success": True, "location": location}
    
    def get_current_location(self, vehicle_id: str) -> Optional[Dict]:
        """Get current location for a vehicle"""
        location = db.get_latest_location(vehicle_id)
        if not location:
            return None
        
        return {
            "latitude": location['latitude'],
            "longitude": location['longitude'],
            "accuracy": location['accuracy'],
            "timestamp": location['recorded_at']
        }
    
    def calculate_route(self, current_lat: float, current_lng: float,
                       pickup_lat: float, pickup_lng: float,
                       dest_lat: float, dest_lng: float) -> Dict:
        """Calculate route from current location through pickup to destination"""
        
        # Calculate distances
        distance_to_pickup = calculate_distance(current_lat, current_lng, pickup_lat, pickup_lng)
        distance_pickup_to_dest = calculate_distance(pickup_lat, pickup_lng, dest_lat, dest_lng)
        total_distance = distance_to_pickup + distance_pickup_to_dest
        
        # Calculate times
        time_to_pickup = (distance_to_pickup / self.AVERAGE_SPEED_KMH) * 60  # minutes
        time_pickup_to_dest = (distance_pickup_to_dest / self.AVERAGE_SPEED_KMH) * 60
        total_time = time_to_pickup + time_pickup_to_dest
        
        # Determine next waypoint
        next_waypoint = 'pickup' if distance_to_pickup > 0.1 else 'destination'
        
        return {
            "currentLocation": {
                "lat": current_lat,
                "lng": current_lng,
                "address": "Current Location"
            },
            "pickupPoint": {
                "lat": pickup_lat,
                "lng": pickup_lng,
                "address": "Pickup Point"
            },
            "destination": {
                "lat": dest_lat,
                "lng": dest_lng,
                "address": "Destination"
            },
            "route": {
                "waypoints": [
                    {"latitude": current_lat, "longitude": current_lng},
                    {"latitude": pickup_lat, "longitude": pickup_lng},
                    {"latitude": dest_lat, "longitude": dest_lng}
                ],
                "totalDistance": round(total_distance, 2),
                "totalTime": round(total_time, 2)
            },
            "nextWaypoint": next_waypoint,
            "distanceToNextWaypoint": round(distance_to_pickup if next_waypoint == 'pickup' else distance_pickup_to_dest, 2),
            "timeToNextWaypoint": round(time_to_pickup if next_waypoint == 'pickup' else time_pickup_to_dest, 2)
        }
    
    def check_waypoint_reached(self, current_lat: float, current_lng: float,
                              waypoint_lat: float, waypoint_lng: float) -> bool:
        """Check if driver has reached a waypoint"""
        distance_meters = calculate_distance(current_lat, current_lng, waypoint_lat, waypoint_lng) * 1000
        return distance_meters <= self.WAYPOINT_THRESHOLD_METERS
    
    def trigger_waypoint_notification(self, driver_id: str, waypoint_type: str, load_id: str) -> Dict:
        """Trigger notification when waypoint is reached"""
        title = "Pickup Point Reached" if waypoint_type == 'pickup' else "Destination Reached"
        message = "You have arrived at the pickup point" if waypoint_type == 'pickup' else "You have arrived at the destination"
        
        notification = db.create_notification(
            driver_id=driver_id,
            notification_type='waypoint',
            title=title,
            message=message,
            load_id=load_id,
            waypoint_type=waypoint_type
        )
        
        return {
            "success": True,
            "notification": notification
        }


# Global service instance
navigation_service = NavigationService()
