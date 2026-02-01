"""
Manual Allocation API Endpoints
Owner can manually allocate vehicles to loads
"""

from fastapi import APIRouter, HTTPException, status, Query
from typing import List
from uuid import UUID

from models.domain import (
    OwnerStatistics, VehicleInfo, LoadInfo, AllocationRequest, 
    AllocationRecord, DriverAllocatedLoadsSummary, NavigationState,
    LocationUpdate, Notification
)
from services.allocation_service import allocation_service
from services.driver_loads_service import driver_loads_service
from services.navigation_service import navigation_service
from db_chromadb import db

router = APIRouter(prefix="/api", tags=["allocations"])


# ==================== ADMIN ENDPOINTS ====================

@router.post("/admin/seed-demo-data")
def seed_demo_data():
    """Seed database with demo data for testing"""
    try:
        # Create Owner
        owner = db.create_owner("Demo Transport Co.", "owner@demo.com")
        owner_id = owner['owner_id']
        
        # Create Trucks
        trucks = []
        truck_plates = ["DL-01-AB-1234", "MH-02-CD-5678", "KA-03-EF-9012", "RJ-04-GH-3456", "UP-05-IJ-7890"]
        for plate in truck_plates:
            truck = db.create_truck(owner_id, plate, fuel_consumption_rate=0.35)
            trucks.append(truck)
        
        # Create Drivers
        drivers = []
        driver_names = [
            ("Rajesh Kumar", "+91-9876543210"),
            ("Amit Singh", "+91-9876543211"),
            ("Suresh Reddy", "+91-9876543212"),
            ("Vijay Sharma", "+91-9876543213"),
            ("Ravi Patel", "+91-9876543214")
        ]
        for i, (name, phone) in enumerate(driver_names):
            driver = db.create_driver(name, phone, trucks[i]['truck_id'], hourly_rate=25.0)
            drivers.append(driver)
        
        # Add Vehicle Locations
        locations = [
            (28.6139, 77.2090),  # Delhi
            (19.0760, 72.8777),  # Mumbai
            (12.9716, 77.5946),  # Bangalore
            (26.9124, 75.7873),  # Jaipur
            (22.5726, 88.3639)   # Kolkata
        ]
        for i, (lat, lng) in enumerate(locations):
            db.add_location_update(trucks[i]['truck_id'], lat, lng, 10.0)
        
        # Create Vendors
        vendors = []
        vendor_data = [
            ("Azadpur Fruits Co.", "fruits@azadpur.com", "+91-9876540001", 28.7041, 77.1025),
            ("Mumbai Textiles Ltd.", "textiles@mumbai.com", "+91-9876540002", 19.0176, 72.8562),
            ("Bangalore Electronics", "electronics@blr.com", "+91-9876540003", 12.9716, 77.5946),
            ("Jaipur Handicrafts", "handicrafts@jaipur.com", "+91-9876540004", 26.9124, 75.7873),
        ]
        for name, email, phone, lat, lng in vendor_data:
            vendor = db.create_vendor(name, email, phone, lat, lng)
            vendors.append(vendor)
        
        # Create Loads
        loads_data = [
            (0, 5000, 28.7041, 77.1025, "Azadpur Mandi, Delhi", 26.9124, 75.7873, "Jaipur, Rajasthan", 15000),
            (1, 3000, 19.0176, 72.8562, "Mumbai Port, Mumbai", 18.5204, 73.8567, "Pune, Maharashtra", 12000),
            (2, 4000, 12.9716, 77.5946, "Electronic City, Bangalore", 13.0827, 80.2707, "Chennai, Tamil Nadu", 18000),
            (3, 2500, 26.9124, 75.7873, "Jaipur Market, Jaipur", 28.6139, 77.2090, "Delhi", 10000),
            (0, 6000, 28.6139, 77.2090, "Connaught Place, Delhi", 19.0760, 72.8777, "Mumbai, Maharashtra", 25000),
            (1, 3500, 19.0760, 72.8777, "Andheri, Mumbai", 23.0225, 72.5714, "Ahmedabad, Gujarat", 14000),
            (2, 4500, 12.9716, 77.5946, "Whitefield, Bangalore", 17.3850, 78.4867, "Hyderabad, Telangana", 16000),
        ]
        
        for vendor_idx, weight, p_lat, p_lng, p_addr, d_lat, d_lng, d_addr, price in loads_data:
            db.create_load(
                vendor_id=vendors[vendor_idx]['vendor_id'],
                weight_kg=weight,
                pickup_lat=p_lat,
                pickup_lng=p_lng,
                pickup_address=p_addr,
                destination_lat=d_lat,
                destination_lng=d_lng,
                destination_address=d_addr,
                price_offered=price,
                currency="INR"
            )
        
        return {
            "success": True,
            "message": "Demo data created successfully",
            "owner_id": owner_id,
            "trucks_count": len(trucks),
            "drivers_count": len(drivers),
            "vendors_count": len(vendors),
            "loads_count": len(loads_data)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to seed demo data: {str(e)}"
        )


@router.post("/admin/clear-all-data")
def clear_all_data():
    """Clear all data from database"""
    try:
        db.clear_all_data()
        return {"success": True, "message": "All data cleared"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear data: {str(e)}"
        )


# ==================== VEHICLE REGISTRATION ====================

@router.post("/vehicles/register")
def register_vehicle(request: dict):
    """Register a new vehicle with driver"""
    try:
        owner_id = request.get('ownerId')
        license_plate = request.get('licensePlate')
        driver_name = request.get('driverName')
        driver_phone = request.get('driverPhone')
        fuel_rate = request.get('fuelConsumptionRate', 0.35)
        current_location = request.get('currentLocation')
        
        if not all([owner_id, license_plate, driver_name, driver_phone]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing required fields"
            )
        
        # Create truck
        truck = db.create_truck(owner_id, license_plate, fuel_consumption_rate=fuel_rate)
        
        # Create driver
        driver = db.create_driver(driver_name, driver_phone, truck['truck_id'], hourly_rate=25.0)
        
        # Add location if provided
        if current_location:
            db.add_location_update(
                truck['truck_id'],
                current_location['latitude'],
                current_location['longitude'],
                10.0
            )
        else:
            # Default location (Delhi)
            db.add_location_update(truck['truck_id'], 28.6139, 77.2090, 10.0)
        
        return {
            "success": True,
            "message": "Vehicle registered successfully",
            "truck": truck,
            "driver": driver
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to register vehicle: {str(e)}"
        )


# ==================== OWNER ENDPOINTS ====================

@router.get("/owner/statistics", response_model=OwnerStatistics)
def get_owner_statistics(owner_id: str = Query(..., description="Owner ID")):
    """Get owner dashboard statistics"""
    try:
        stats = allocation_service.get_owner_statistics(owner_id)
        return OwnerStatistics(**stats)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to calculate statistics: {str(e)}"
        )


@router.get("/allocations/available-vehicles", response_model=List[VehicleInfo])
def get_available_vehicles(owner_id: str = Query(..., description="Owner ID")):
    """Get all available vehicles for allocation"""
    try:
        vehicles = allocation_service.get_available_vehicles(owner_id)
        return [VehicleInfo(**v) for v in vehicles]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get available vehicles: {str(e)}"
        )


@router.get("/allocations/unallocated-loads", response_model=List[LoadInfo])
def get_unallocated_loads():
    """Get all unallocated loads"""
    try:
        loads = allocation_service.get_unallocated_loads()
        return [LoadInfo(**l) for l in loads]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get unallocated loads: {str(e)}"
        )


@router.get("/allocations/compatible-loads", response_model=List[LoadInfo])
def get_compatible_loads(vehicleId: str = Query(..., description="Vehicle ID")):
    """Get loads compatible with a vehicle, sorted by distance"""
    try:
        loads = allocation_service.get_compatible_loads(vehicleId)
        return [LoadInfo(**l) for l in loads]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get compatible loads: {str(e)}"
        )


@router.get("/allocations/compatible-vehicles", response_model=List[VehicleInfo])
def get_compatible_vehicles(
    loadId: str = Query(..., description="Load ID"),
    ownerId: str = Query(..., description="Owner ID")
):
    """Get vehicles compatible with a load, sorted by distance"""
    try:
        vehicles = allocation_service.get_compatible_vehicles(loadId, ownerId)
        return [VehicleInfo(**v) for v in vehicles]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get compatible vehicles: {str(e)}"
        )


@router.post("/allocations", response_model=AllocationRecord, status_code=status.HTTP_201_CREATED)
def create_allocation(request: AllocationRequest):
    """Create a new manual allocation"""
    try:
        allocation = allocation_service.create_allocation(
            request.vehicleId,
            request.loadId,
            request.ownerId
        )
        
        return AllocationRecord(
            id=allocation['allocation_id'],
            vehicleId=allocation['vehicle_id'],
            loadId=allocation['load_id'],
            status=allocation['status'],
            allocatedAt=allocation['allocated_at'],
            completedAt=allocation.get('completed_at') or None,
            cancelledAt=allocation.get('cancelled_at') or None
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create allocation: {str(e)}"
        )


@router.delete("/allocations/{allocation_id}")
def cancel_allocation(allocation_id: str):
    """Cancel an allocation"""
    try:
        allocation_service.cancel_allocation(allocation_id)
        return {"success": True, "message": "Allocation cancelled"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to cancel allocation: {str(e)}"
        )


# ==================== DRIVER ENDPOINTS ====================

@router.get("/driver/allocated-loads", response_model=DriverAllocatedLoadsSummary)
def get_driver_allocated_loads(driver_id: str = Query(..., description="Driver ID")):
    """Get all allocated loads for a driver"""
    try:
        summary = driver_loads_service.get_allocated_loads(driver_id)
        return DriverAllocatedLoadsSummary(**summary)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get allocated loads: {str(e)}"
        )


@router.get("/driver/allocated-loads/{load_id}/details")
def get_load_details(load_id: str):
    """Get detailed information for a specific load"""
    try:
        details = driver_loads_service.get_load_details(load_id)
        if not details:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Load not found"
            )
        return details
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get load details: {str(e)}"
        )


@router.post("/driver/allocated-loads/{load_id}/pickup")
def mark_load_picked_up(load_id: str):
    """Mark a load as picked up"""
    try:
        result = driver_loads_service.mark_load_picked_up(load_id)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to mark load as picked up: {str(e)}"
        )


@router.post("/driver/allocated-loads/{load_id}/complete")
def mark_load_completed(load_id: str):
    """Mark a load as completed"""
    try:
        result = driver_loads_service.mark_load_completed(load_id)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to mark load as completed: {str(e)}"
        )


# ==================== NAVIGATION ENDPOINTS ====================

@router.post("/navigation/location-update")
def update_location(update: LocationUpdate):
    """Update vehicle location"""
    try:
        result = navigation_service.update_location(
            update.vehicleId,
            update.latitude,
            update.longitude,
            update.accuracy
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update location: {str(e)}"
        )


@router.get("/navigation/current-location")
def get_current_location(vehicle_id: str = Query(..., description="Vehicle ID")):
    """Get current location for a vehicle"""
    try:
        location = navigation_service.get_current_location(vehicle_id)
        if not location:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No location data found for vehicle"
            )
        return location
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get current location: {str(e)}"
        )


@router.get("/navigation/route", response_model=NavigationState)
def get_navigation_route(
    currentLat: float = Query(..., description="Current latitude"),
    currentLng: float = Query(..., description="Current longitude"),
    pickupLat: float = Query(..., description="Pickup latitude"),
    pickupLng: float = Query(..., description="Pickup longitude"),
    destLat: float = Query(..., description="Destination latitude"),
    destLng: float = Query(..., description="Destination longitude")
):
    """Calculate navigation route"""
    try:
        route = navigation_service.calculate_route(
            currentLat, currentLng,
            pickupLat, pickupLng,
            destLat, destLng
        )
        return NavigationState(**route)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to calculate route: {str(e)}"
        )


@router.post("/navigation/waypoint-reached")
def waypoint_reached(
    driver_id: str = Query(..., description="Driver ID"),
    load_id: str = Query(..., description="Load ID"),
    waypoint_type: str = Query(..., description="Waypoint type (pickup/destination)")
):
    """Trigger notification when waypoint is reached"""
    try:
        result = navigation_service.trigger_waypoint_notification(
            driver_id,
            waypoint_type,
            load_id
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to trigger waypoint notification: {str(e)}"
        )


# ==================== NOTIFICATION ENDPOINTS ====================

@router.get("/notifications", response_model=List[Notification])
def get_notifications(driver_id: str = Query(..., description="Driver ID")):
    """Get all notifications for a driver"""
    try:
        notifications = db.get_driver_notifications(driver_id)
        return [Notification(**n) for n in notifications]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get notifications: {str(e)}"
        )


@router.get("/notifications/unread-count")
def get_unread_count(driver_id: str = Query(..., description="Driver ID")):
    """Get count of unread notifications"""
    try:
        count = db.get_unread_count(driver_id)
        return {"count": count}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get unread count: {str(e)}"
        )


@router.post("/notifications/{notification_id}/read")
def mark_notification_read(notification_id: str):
    """Mark a notification as read"""
    try:
        notification = db.mark_notification_read(notification_id)
        if not notification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found"
            )
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to mark notification as read: {str(e)}"
        )
