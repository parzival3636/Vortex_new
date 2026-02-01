"""
Driver Allocated Loads Service
Handles driver-facing load management
"""

from typing import List, Dict, Optional
from datetime import datetime

from db_chromadb import db
from services.math_engine import calculate_distance


class DriverLoadsService:
    """Service for managing driver allocated loads"""
    
    AVERAGE_SPEED_KMH = 60  # Average truck speed
    
    def get_allocated_loads(self, driver_id: str) -> Dict:
        """Get all allocated loads for a driver"""
        # Get driver
        driver = db.get_driver(driver_id)
        if not driver:
            return {
                "totalLoads": 0,
                "totalDistance": 0,
                "totalTime": 0,
                "loads": []
            }
        
        # Get truck for driver
        truck_id = driver.get('truck_id')
        if not truck_id:
            return {
                "totalLoads": 0,
                "totalDistance": 0,
                "totalTime": 0,
                "loads": []
            }
        
        # Get allocations for this truck
        allocations = db.get_driver_allocations(driver_id)
        
        loads = []
        total_distance = 0
        total_time = 0
        
        for allocation in allocations:
            if allocation.get('status') != 'active':
                continue
            
            # Get load details
            load = db.get_load(allocation['load_id'])
            if not load:
                continue
            
            # Get current vehicle location
            location = db.get_latest_location(truck_id)
            if not location:
                location = {
                    'latitude': 28.6139,
                    'longitude': 77.2090
                }
            
            # Calculate distance and time to pickup
            distance_to_pickup = calculate_distance(
                location['latitude'],
                location['longitude'],
                load['pickup_lat'],
                load['pickup_lng']
            )
            
            time_to_pickup = (distance_to_pickup / self.AVERAGE_SPEED_KMH) * 60  # minutes
            
            # Calculate total distance (pickup to destination)
            total_load_distance = calculate_distance(
                load['pickup_lat'],
                load['pickup_lng'],
                load['destination_lat'],
                load['destination_lng']
            )
            
            total_load_time = (total_load_distance / self.AVERAGE_SPEED_KMH) * 60  # minutes
            
            loads.append({
                "id": allocation['allocation_id'],
                "loadId": load['load_id'],
                "pickupLocation": {
                    "lat": load['pickup_lat'],
                    "lng": load['pickup_lng'],
                    "address": load.get('pickup_address', 'Pickup Location')
                },
                "destination": {
                    "lat": load['destination_lat'],
                    "lng": load['destination_lng'],
                    "address": load.get('destination_address', 'Destination')
                },
                "status": load.get('status', 'allocated'),
                "estimatedDistanceToPickup": round(distance_to_pickup, 2),
                "estimatedTimeToPickup": round(time_to_pickup, 2),
                "totalEstimatedDistance": round(total_load_distance, 2),
                "totalEstimatedTime": round(total_load_time, 2),
                "specialInstructions": load.get('special_instructions', None)
            })
            
            total_distance += distance_to_pickup + total_load_distance
            total_time += time_to_pickup + total_load_time
        
        return {
            "totalLoads": len(loads),
            "totalDistance": round(total_distance, 2),
            "totalTime": round(total_time, 2),
            "loads": loads
        }
    
    def get_load_details(self, load_id: str) -> Optional[Dict]:
        """Get detailed information for a specific load"""
        load = db.get_load(load_id)
        if not load:
            return None
        
        return {
            "loadId": load['load_id'],
            "pickupLocation": {
                "lat": load['pickup_lat'],
                "lng": load['pickup_lng'],
                "address": load.get('pickup_address', 'Pickup Location')
            },
            "destination": {
                "lat": load['destination_lat'],
                "lng": load['destination_lng'],
                "address": load.get('destination_address', 'Destination')
            },
            "status": load.get('status', 'allocated'),
            "specialInstructions": load.get('special_instructions', None),
            "weight": load.get('weight_kg', 0),
            "priceOffered": load.get('price_offered', 0),
            "currency": load.get('currency', 'INR')
        }
    
    def mark_load_picked_up(self, load_id: str) -> Dict:
        """Mark a load as picked up"""
        load = db.get_load(load_id)
        if not load:
            raise ValueError("Load not found")
        
        # Update load status
        db.update_load(load_id, {
            'status': 'picked_up',
            'picked_up_at': datetime.utcnow().isoformat()
        })
        
        return {"success": True, "message": "Load marked as picked up"}
    
    def mark_load_completed(self, load_id: str) -> Dict:
        """Mark a load as completed"""
        load = db.get_load(load_id)
        if not load:
            raise ValueError("Load not found")
        
        # Update load status
        db.update_load(load_id, {
            'status': 'delivered',
            'delivered_at': datetime.utcnow().isoformat()
        })
        
        # Find and complete allocation
        allocations = db.get_active_allocations()
        for allocation in allocations:
            if allocation.get('load_id') == load_id:
                db.update_allocation(allocation['allocation_id'], {
                    'status': 'completed',
                    'completed_at': datetime.utcnow().isoformat()
                })
                
                # Update truck status back to idle
                truck_id = allocation.get('vehicle_id')
                if truck_id:
                    truck = db.get_truck(truck_id)
                    if truck:
                        db.trucks.update(
                            ids=[truck_id],
                            metadatas=[{**truck, 'status': 'idle'}]
                        )
                break
        
        return {"success": True, "message": "Load marked as completed"}


# Global service instance
driver_loads_service = DriverLoadsService()
