from fastapi import APIRouter, HTTPException, status
from uuid import UUID
from typing import List
from datetime import datetime

from db_chromadb import db
from models.domain import LoadCreate, LoadResponse, Coordinate

router = APIRouter(prefix="/api/v1/loads", tags=["loads"])


@router.post("/", response_model=LoadResponse, status_code=status.HTTP_201_CREATED)
def create_load(load_data: LoadCreate):
    """
    Create a new load posting
    
    - **vendor_id**: UUID of the vendor
    - **weight_kg**: Load weight in kilograms (must be positive)
    - **pickup_location**: Pickup location with coordinates
    - **destination**: Delivery destination with coordinates
    - **price_offered**: Price offered for transport (must be positive)
    - **currency**: Currency code (default: USD)
    """
    # Validate vendor exists
    vendor = db.get_vendor(str(load_data.vendor_id))
    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vendor with ID {load_data.vendor_id} not found"
        )
    
    # Create load
    load = db.create_load(
        vendor_id=str(load_data.vendor_id),
        weight_kg=load_data.weight_kg,
        pickup_lat=load_data.pickup_location.lat,
        pickup_lng=load_data.pickup_location.lng,
        pickup_address=load_data.pickup_location.address,
        destination_lat=load_data.destination.lat,
        destination_lng=load_data.destination.lng,
        destination_address=load_data.destination.address,
        price_offered=load_data.price_offered,
        currency=load_data.currency
    )
    
    # Build response
    return LoadResponse(
        load_id=UUID(load['load_id']),
        vendor_id=UUID(load['vendor_id']),
        weight_kg=load['weight_kg'],
        pickup_location=Coordinate(
            lat=load['pickup_lat'],
            lng=load['pickup_lng'],
            address=load['pickup_address']
        ),
        destination=Coordinate(
            lat=load['destination_lat'],
            lng=load['destination_lng'],
            address=load['destination_address']
        ),
        price_offered=load['price_offered'],
        currency=load['currency'],
        status=load['status'],
        assigned_driver_id=UUID(load['assigned_driver_id']) if load['assigned_driver_id'] else None,
        assigned_trip_id=UUID(load['assigned_trip_id']) if load['assigned_trip_id'] else None,
        created_at=datetime.fromisoformat(load['created_at']),
        assigned_at=datetime.fromisoformat(load['assigned_at']) if load['assigned_at'] else None,
        picked_up_at=datetime.fromisoformat(load['picked_up_at']) if load['picked_up_at'] else None,
        delivered_at=datetime.fromisoformat(load['delivered_at']) if load['delivered_at'] else None
    )


@router.get("/available", response_model=List[LoadResponse])
def get_available_loads():
    """Get all available loads"""
    loads = db.get_available_loads()
    
    return [
        LoadResponse(
            load_id=UUID(load['load_id']),
            vendor_id=UUID(load['vendor_id']),
            weight_kg=load['weight_kg'],
            pickup_location=Coordinate(
                lat=load['pickup_lat'],
                lng=load['pickup_lng'],
                address=load['pickup_address']
            ),
            destination=Coordinate(
                lat=load['destination_lat'],
                lng=load['destination_lng'],
                address=load['destination_address']
            ),
            price_offered=load['price_offered'],
            currency=load['currency'],
            status=load['status'],
            assigned_driver_id=UUID(load['assigned_driver_id']) if load['assigned_driver_id'] else None,
            assigned_trip_id=UUID(load['assigned_trip_id']) if load['assigned_trip_id'] else None,
            created_at=datetime.fromisoformat(load['created_at']),
            assigned_at=datetime.fromisoformat(load['assigned_at']) if load['assigned_at'] else None,
            picked_up_at=datetime.fromisoformat(load['picked_up_at']) if load['picked_up_at'] else None,
            delivered_at=datetime.fromisoformat(load['delivered_at']) if load['delivered_at'] else None
        )
        for load in loads
    ]


@router.get("/{load_id}", response_model=LoadResponse)
def get_load(load_id: UUID):
    """Get load details by ID"""
    load = db.get_load(str(load_id))
    
    if not load:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Load with ID {load_id} not found"
        )
    
    return LoadResponse(
        load_id=UUID(load['load_id']),
        vendor_id=UUID(load['vendor_id']),
        weight_kg=load['weight_kg'],
        pickup_location=Coordinate(
            lat=load['pickup_lat'],
            lng=load['pickup_lng'],
            address=load['pickup_address']
        ),
        destination=Coordinate(
            lat=load['destination_lat'],
            lng=load['destination_lng'],
            address=load['destination_address']
        ),
        price_offered=load['price_offered'],
        currency=load['currency'],
        status=load['status'],
        assigned_driver_id=UUID(load['assigned_driver_id']) if load['assigned_driver_id'] else None,
        assigned_trip_id=UUID(load['assigned_trip_id']) if load['assigned_trip_id'] else None,
        created_at=datetime.fromisoformat(load['created_at']),
        assigned_at=datetime.fromisoformat(load['assigned_at']) if load['assigned_at'] else None,
        picked_up_at=datetime.fromisoformat(load['picked_up_at']) if load['picked_up_at'] else None,
        delivered_at=datetime.fromisoformat(load['delivered_at']) if load['delivered_at'] else None
    )


@router.patch("/{load_id}/accept")
def accept_load(load_id: UUID, trip_id: UUID):
    """Accept a load opportunity"""
    load = db.get_load(str(load_id))
    
    if not load:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Load with ID {load_id} not found"
        )
    
    # Allow accepting loads that are "available" or already "assigned" (by auto-scheduler)
    if load['status'] not in ["available", "assigned"]:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Load cannot be accepted (current status: {load['status']})"
        )
    
    # Get trip to find driver
    trip = db.get_trip(str(trip_id))
    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trip with ID {trip_id} not found"
        )
    
    # Update load status to assigned (if not already)
    if load['status'] != "assigned":
        db.accept_load(str(load_id), str(trip_id), trip['driver_id'])
    
    # TODO: Create LoadAssignment record and provide navigation
    
    return {"message": "Load accepted", "load_id": str(load_id)}


@router.patch("/{load_id}/reject")
def reject_load(load_id: UUID):
    """Reject a load opportunity"""
    load = db.get_load(str(load_id))
    
    if not load:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Load with ID {load_id} not found"
        )
    
    # Log rejection but keep load available
    # TODO: Log rejection event
    
    return {"message": "Load rejected", "load_id": str(load_id)}
