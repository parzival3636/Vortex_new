from fastapi import APIRouter, HTTPException, status
from uuid import UUID
from datetime import datetime

from db_chromadb import db
from models.domain import TripCreate, TripResponse, Coordinate

router = APIRouter(prefix="/api/v1/trips", tags=["trips"])


@router.post("/", response_model=TripResponse, status_code=status.HTTP_201_CREATED)
def create_trip(trip_data: TripCreate):
    """
    Create a new trip
    
    - **driver_id**: UUID of the driver
    - **truck_id**: UUID of the truck
    - **origin**: Starting location with coordinates
    - **destination**: Ending location with coordinates
    - **outbound_load**: Description of the load being carried
    """
    # Validate driver exists
    driver = db.get_driver(str(trip_data.driver_id))
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Driver with ID {trip_data.driver_id} not found"
        )
    
    # Validate truck exists
    truck = db.get_truck(str(trip_data.truck_id))
    if not truck:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Truck with ID {trip_data.truck_id} not found"
        )
    
    # Create trip
    trip = db.create_trip(
        driver_id=str(trip_data.driver_id),
        truck_id=str(trip_data.truck_id),
        origin_lat=trip_data.origin.lat,
        origin_lng=trip_data.origin.lng,
        origin_address=trip_data.origin.address,
        destination_lat=trip_data.destination.lat,
        destination_lng=trip_data.destination.lng,
        destination_address=trip_data.destination.address,
        outbound_load=trip_data.outbound_load
    )
    
    # Build response
    return TripResponse(
        trip_id=UUID(trip['trip_id']),
        driver_id=UUID(trip['driver_id']),
        truck_id=UUID(trip['truck_id']),
        origin=Coordinate(
            lat=trip['origin_lat'],
            lng=trip['origin_lng'],
            address=trip['origin_address']
        ),
        destination=Coordinate(
            lat=trip['destination_lat'],
            lng=trip['destination_lng'],
            address=trip['destination_address']
        ),
        outbound_load=trip['outbound_load'],
        is_deadheading=trip['is_deadheading'],
        status=trip['status'],
        created_at=datetime.fromisoformat(trip['created_at']),
        completed_at=datetime.fromisoformat(trip['completed_at']) if trip['completed_at'] else None
    )


@router.get("/{trip_id}", response_model=TripResponse)
def get_trip(trip_id: UUID):
    """Get trip details by ID"""
    trip = db.get_trip(str(trip_id))
    
    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trip with ID {trip_id} not found"
        )
    
    return TripResponse(
        trip_id=UUID(trip['trip_id']),
        driver_id=UUID(trip['driver_id']),
        truck_id=UUID(trip['truck_id']),
        origin=Coordinate(
            lat=trip['origin_lat'],
            lng=trip['origin_lng'],
            address=trip['origin_address']
        ),
        destination=Coordinate(
            lat=trip['destination_lat'],
            lng=trip['destination_lng'],
            address=trip['destination_address']
        ),
        outbound_load=trip['outbound_load'],
        is_deadheading=trip['is_deadheading'],
        status=trip['status'],
        created_at=datetime.fromisoformat(trip['created_at']),
        completed_at=datetime.fromisoformat(trip['completed_at']) if trip['completed_at'] else None
    )


@router.get("/{trip_id}/assigned-load")
def get_assigned_load(trip_id: UUID):
    """Get load assigned to this trip (if any)"""
    trip = db.get_trip(str(trip_id))
    
    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trip with ID {trip_id} not found"
        )
    
    # Find load assigned to this trip
    all_loads = db.loads.get()
    
    if all_loads['ids']:
        for load_meta in all_loads['metadatas']:
            if load_meta.get('assigned_trip_id') == str(trip_id):
                return {
                    "has_assigned_load": True,
                    "load": {
                        "load_id": load_meta['load_id'],
                        "vendor_id": load_meta['vendor_id'],
                        "weight_kg": load_meta['weight_kg'],
                        "pickup_location": {
                            "lat": load_meta['pickup_lat'],
                            "lng": load_meta['pickup_lng'],
                            "address": load_meta['pickup_address']
                        },
                        "destination": {
                            "lat": load_meta['destination_lat'],
                            "lng": load_meta['destination_lng'],
                            "address": load_meta['destination_address']
                        },
                        "price_offered": load_meta['price_offered'],
                        "currency": load_meta['currency'],
                        "status": load_meta['status'],
                        "assigned_at": load_meta.get('assigned_at', '')
                    }
                }
    
    return {
        "has_assigned_load": False,
        "load": None
    }


@router.patch("/{trip_id}/deadhead", response_model=TripResponse)
def mark_deadheading(trip_id: UUID):
    """Mark trip as deadheading (returning empty)"""
    trip = db.mark_deadheading(str(trip_id))
    
    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trip with ID {trip_id} not found"
        )
    
    # TODO: Trigger load matching workflow
    
    return TripResponse(
        trip_id=UUID(trip['trip_id']),
        driver_id=UUID(trip['driver_id']),
        truck_id=UUID(trip['truck_id']),
        origin=Coordinate(
            lat=trip['origin_lat'],
            lng=trip['origin_lng'],
            address=trip['origin_address']
        ),
        destination=Coordinate(
            lat=trip['destination_lat'],
            lng=trip['destination_lng'],
            address=trip['destination_address']
        ),
        outbound_load=trip['outbound_load'],
        is_deadheading=trip['is_deadheading'],
        status=trip['status'],
        created_at=datetime.fromisoformat(trip['created_at']),
        completed_at=datetime.fromisoformat(trip['completed_at']) if trip['completed_at'] else None
    )


@router.patch("/{trip_id}/pickup")
def confirm_pickup(trip_id: UUID):
    """Confirm load pickup"""
    trip = db.get_trip(str(trip_id))
    
    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trip with ID {trip_id} not found"
        )
    
    # Find the load assigned to this trip
    all_loads = db.loads.get()
    assigned_load = None
    
    if all_loads['ids']:
        for load_meta in all_loads['metadatas']:
            if load_meta.get('assigned_trip_id') == str(trip_id):
                assigned_load = load_meta
                break
    
    # Update load status to picked_up
    if assigned_load:
        db.update_load(assigned_load['load_id'], {
            "status": "picked_up",
            "picked_up_at": datetime.utcnow().isoformat()
        })
        
        return {
            "message": "Pickup confirmed",
            "trip_id": str(trip_id),
            "load_id": assigned_load['load_id'],
            "status": "picked_up"
        }
    
    return {
        "message": "Pickup confirmed (no load assigned)",
        "trip_id": str(trip_id)
    }


@router.patch("/{trip_id}/delivery")
def confirm_delivery(trip_id: UUID):
    """Confirm delivery completion"""
    trip = db.update_trip(str(trip_id), {
        "status": "completed",
        "completed_at": datetime.utcnow().isoformat()
    })
    
    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trip with ID {trip_id} not found"
        )
    
    # Find the load assigned to this trip
    all_loads = db.loads.get()
    assigned_load = None
    
    if all_loads['ids']:
        for load_meta in all_loads['metadatas']:
            if load_meta.get('assigned_trip_id') == str(trip_id):
                assigned_load = load_meta
                break
    
    # Update load status to delivered
    if assigned_load:
        db.update_load(assigned_load['load_id'], {
            "status": "delivered",
            "delivered_at": datetime.utcnow().isoformat()
        })
        
        return {
            "message": "Delivery confirmed",
            "trip_id": str(trip_id),
            "load_id": assigned_load['load_id'],
            "status": "delivered"
        }
    
    return {
        "message": "Delivery confirmed (no load assigned)",
        "trip_id": str(trip_id)
    }
