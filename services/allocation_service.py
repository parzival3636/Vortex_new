"""
Manual Allocation Service
Handles vehicle-to-load allocation logic
"""

from typing import List, Dict, Optional, Tuple
from datetime import datetime
import math

from db_chromadb import db
from services.math_engine import calculate_distance


class AllocationService:
    """Service for managing manual vehicle-load allocations"""
    
    MAX_ALLOCATION_DISTANCE_KM = 500  # Maximum distance for allocation
    
    def get_owner_statistics(self, owner_id: str) -> Dict:
        """Calculate owner dashboard statistics"""
        # Get all trucks for this owner
        all_trucks = self._get_all_trucks()
        owner_trucks = [t for t in all_trucks if t.get('owner_id') == owner_id]
        
        # Get all loads
        all_loads_result = db.loads.get()
        all_loads = all_loads_result['metadatas'] if all_loads_result['ids'] else []
        
        # Get all allocations
        all_allocations_result = db.allocations.get()
        all_allocations = all_allocations_result['metadatas'] if all_allocations_result['ids'] else []
        
        # Calculate statistics
        total_active_vehicles = len([t for t in owner_trucks if t.get('status') != 'inactive'])
        total_pending_loads = len([l for l in all_loads if l.get('status') == 'available'])
        total_allocated_loads = len([a for a in all_allocations if a.get('status') == 'active'])
        total_completed_loads = len([l for l in all_loads if l.get('status') == 'delivered'])
        
        allocation_rate = (total_allocated_loads / total_pending_loads * 100) if total_pending_loads > 0 else 0
        
        # Calculate vehicle utilization (simplified)
        vehicle_utilization = (total_allocated_loads / total_active_vehicles * 100) if total_active_vehicles > 0 else 0
        
        return {
            "totalActiveVehicles": total_active_vehicles,
            "totalPendingLoads": total_pending_loads,
            "totalAllocatedLoads": total_allocated_loads,
            "totalCompletedLoads": total_completed_loads,
            "allocationRate": round(allocation_rate, 2),
            "averageVehicleUtilization": round(min(vehicle_utilization, 100), 2),
            "lastUpdated": datetime.utcnow().isoformat()
        }
    
    def get_available_vehicles(self, owner_id: str) -> List[Dict]:
        """Get all available vehicles for allocation"""
        all_trucks = self._get_all_trucks()
        owner_trucks = [t for t in all_trucks if t.get('owner_id') == owner_id]
        
        available_vehicles = []
        for truck in owner_trucks:
            # Skip if truck is already allocated or deadheading
            if truck.get('status') in ['allocated', 'deadheading']:
                continue
            
            # Get latest location
            location = db.get_latest_location(truck['truck_id'])
            if not location:
                # Default location if no GPS data
                location = {
                    'latitude': 28.6139,  # Delhi default
                    'longitude': 77.2090,
                    'accuracy': 100
                }
            
            # Calculate distance to nearest load
            nearest_distance = self._calculate_distance_to_nearest_load(
                location['latitude'], 
                location['longitude']
            )
            
            available_vehicles.append({
                "id": truck['truck_id'],
                "name": truck.get('license_plate', 'Unknown'),
                "currentLocation": {
                    "latitude": location['latitude'],
                    "longitude": location['longitude'],
                    "address": "Current Location"
                },
                "status": truck.get('status', 'idle'),
                "distanceToNearestLoad": round(nearest_distance, 2)
            })
        
        return available_vehicles
    
    def get_unallocated_loads(self) -> List[Dict]:
        """Get all unallocated loads"""
        available_loads = db.get_available_loads()
        
        unallocated = []
        for load in available_loads:
            # Skip if load is deadheading or already allocated
            if load.get('status') not in ['available']:
                continue
            
            unallocated.append({
                "id": load['load_id'],
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
                "status": load['status'],
                "specialInstructions": load.get('special_instructions', None)
            })
        
        return unallocated
    
    def get_compatible_loads(self, vehicle_id: str) -> List[Dict]:
        """Get loads compatible with a vehicle, sorted by distance"""
        # Get vehicle location
        location = db.get_latest_location(vehicle_id)
        if not location:
            return []
        
        # Get all unallocated loads
        loads = self.get_unallocated_loads()
        
        # Calculate distance to each load and filter
        compatible = []
        for load in loads:
            distance = calculate_distance(
                location['latitude'],
                location['longitude'],
                load['pickupLocation']['lat'],
                load['pickupLocation']['lng']
            )
            
            if distance <= self.MAX_ALLOCATION_DISTANCE_KM:
                load['distanceFromVehicle'] = round(distance, 2)
                compatible.append(load)
        
        # Sort by distance
        compatible.sort(key=lambda x: x['distanceFromVehicle'])
        return compatible
    
    def get_compatible_vehicles(self, load_id: str, owner_id: str) -> List[Dict]:
        """Get vehicles compatible with a load, sorted by distance"""
        # Get load
        load = db.get_load(load_id)
        if not load:
            return []
        
        # Get all available vehicles
        vehicles = self.get_available_vehicles(owner_id)
        
        # Calculate distance to load pickup and filter
        compatible = []
        for vehicle in vehicles:
            distance = calculate_distance(
                vehicle['currentLocation']['latitude'],
                vehicle['currentLocation']['longitude'],
                load['pickup_lat'],
                load['pickup_lng']
            )
            
            if distance <= self.MAX_ALLOCATION_DISTANCE_KM:
                vehicle['distanceToLoad'] = round(distance, 2)
                compatible.append(vehicle)
        
        # Sort by distance
        compatible.sort(key=lambda x: x['distanceToLoad'])
        return compatible
    
    def validate_allocation(self, vehicle_id: str, load_id: str) -> Tuple[bool, str]:
        """Validate if allocation is possible"""
        # Check vehicle exists and is available
        truck = db.get_truck(vehicle_id)
        if not truck:
            return False, "Vehicle not found"
        
        if truck.get('status') in ['allocated', 'deadheading']:
            return False, f"Vehicle is not available (status: {truck.get('status')})"
        
        # Check load exists and is available
        load = db.get_load(load_id)
        if not load:
            return False, "Load not found"
        
        if load.get('status') != 'available':
            return False, f"Load is not available (status: {load.get('status')})"
        
        # Check distance
        location = db.get_latest_location(vehicle_id)
        if location:
            distance = calculate_distance(
                location['latitude'],
                location['longitude'],
                load['pickup_lat'],
                load['pickup_lng']
            )
            
            if distance > self.MAX_ALLOCATION_DISTANCE_KM:
                return False, f"Vehicle is too far from pickup location ({round(distance, 2)}km, max: {self.MAX_ALLOCATION_DISTANCE_KM}km)"
        
        return True, "Validation passed"
    
    def create_allocation(self, vehicle_id: str, load_id: str, owner_id: str) -> Dict:
        """Create a new allocation"""
        # Validate
        is_valid, message = self.validate_allocation(vehicle_id, load_id)
        if not is_valid:
            raise ValueError(message)
        
        # Create allocation
        allocation = db.create_allocation(vehicle_id, load_id, owner_id)
        
        # Update truck status
        truck = db.get_truck(vehicle_id)
        if truck:
            db.trucks.update(
                ids=[vehicle_id],
                metadatas=[{**truck, 'status': 'allocated'}]
            )
        
        # Update load status
        db.update_load(load_id, {'status': 'allocated'})
        
        # Get driver for this truck
        driver = self._get_driver_for_truck(vehicle_id)
        
        # Send notification to driver
        if driver:
            load = db.get_load(load_id)
            db.create_notification(
                driver_id=driver['driver_id'],
                notification_type='allocation',
                title='New Load Allocated',
                message=f"You have been assigned a new load from {load.get('pickup_address', 'pickup')} to {load.get('destination_address', 'destination')}",
                load_id=load_id
            )
        
        return allocation
    
    def cancel_allocation(self, allocation_id: str) -> Dict:
        """Cancel an allocation"""
        allocation = db.get_allocation(allocation_id)
        if not allocation:
            raise ValueError("Allocation not found")
        
        # Cancel allocation
        db.cancel_allocation(allocation_id)
        
        # Revert truck status
        truck = db.get_truck(allocation['vehicle_id'])
        if truck:
            db.trucks.update(
                ids=[allocation['vehicle_id']],
                metadatas=[{**truck, 'status': 'idle'}]
            )
        
        # Revert load status
        db.update_load(allocation['load_id'], {'status': 'available'})
        
        return allocation
    
    def _get_all_trucks(self) -> List[Dict]:
        """Get all trucks from database"""
        try:
            result = db.trucks.get()
            return result['metadatas'] if result['ids'] else []
        except:
            return []
    
    def _get_driver_for_truck(self, truck_id: str) -> Optional[Dict]:
        """Get driver assigned to a truck"""
        try:
            result = db.drivers.get()
            if result['ids']:
                for driver in result['metadatas']:
                    if driver.get('truck_id') == truck_id:
                        return driver
        except:
            pass
        return None
    
    def _calculate_distance_to_nearest_load(self, lat: float, lng: float) -> float:
        """Calculate distance to nearest available load"""
        loads = db.get_available_loads()
        if not loads:
            return 0.0
        
        min_distance = float('inf')
        for load in loads:
            distance = calculate_distance(
                lat, lng,
                load['pickup_lat'],
                load['pickup_lng']
            )
            min_distance = min(min_distance, distance)
        
        return min_distance if min_distance != float('inf') else 0.0


# Global service instance
allocation_service = AllocationService()
