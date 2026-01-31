"""
Vendor API Endpoints
Allows vendors to register and post loads
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional

from db_chromadb import db
from services.geocoding import geocoding_service
from models.domain import Coordinate

router = APIRouter(prefix="/api/v1/vendors", tags=["vendors"])


class VendorCreate(BaseModel):
    """Vendor registration request"""
    name: str
    email: EmailStr
    phone: str
    address: str  # Will be geocoded to get GPS coordinates


class VendorResponse(BaseModel):
    """Vendor response"""
    vendor_id: str
    name: str
    email: str
    phone: str
    location_lat: float
    location_lng: float
    address: str


class LoadCreateByAddress(BaseModel):
    """Create load using addresses (will be geocoded)"""
    vendor_id: UUID
    weight_kg: float
    pickup_address: str
    destination_address: str
    price_offered: float
    currency: str = "INR"


@router.post("/register", response_model=VendorResponse, status_code=status.HTTP_201_CREATED)
def register_vendor(vendor_data: VendorCreate):
    """
    Register a new vendor
    
    The address will be geocoded using OpenStreetMap to get GPS coordinates.
    
    Example:
    ```json
    {
        "name": "Azadpur Fruits Co.",
        "email": "fruits@azadpur.com",
        "phone": "+91-9876543210",
        "address": "Azadpur Mandi, Delhi"
    }
    ```
    """
    # Geocode the address
    location = geocoding_service.geocode(vendor_data.address)
    
    if not location:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not find GPS coordinates for address: {vendor_data.address}"
        )
    
    # Create vendor
    vendor = db.create_vendor(
        name=vendor_data.name,
        email=vendor_data.email,
        phone=vendor_data.phone,
        location_lat=location.lat,
        location_lng=location.lng
    )
    
    return VendorResponse(
        vendor_id=vendor['vendor_id'],
        name=vendor['name'],
        email=vendor['email'],
        phone=vendor['phone'],
        location_lat=location.lat,
        location_lng=location.lng,
        address=location.address
    )


@router.get("/{vendor_id}", response_model=VendorResponse)
def get_vendor(vendor_id: UUID):
    """Get vendor details by ID"""
    vendor = db.get_vendor(str(vendor_id))
    
    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vendor with ID {vendor_id} not found"
        )
    
    # Get address from coordinates
    address = geocoding_service.reverse_geocode(
        vendor['location_lat'],
        vendor['location_lng']
    )
    
    return VendorResponse(
        vendor_id=vendor['vendor_id'],
        name=vendor['name'],
        email=vendor['email'],
        phone=vendor['phone'],
        location_lat=vendor['location_lat'],
        location_lng=vendor['location_lng'],
        address=address
    )


@router.post("/loads/by-address")
def create_load_by_address(load_data: LoadCreateByAddress):
    """
    Create a load using addresses (will be geocoded automatically)
    
    This is easier for vendors - they just enter addresses, not GPS coordinates.
    
    Example:
    ```json
    {
        "vendor_id": "123e4567-e89b-12d3-a456-426614174000",
        "weight_kg": 5000,
        "pickup_address": "Azadpur Mandi, Delhi",
        "destination_address": "Jaipur, Rajasthan",
        "price_offered": 12000,
        "currency": "INR"
    }
    ```
    """
    # Verify vendor exists
    vendor = db.get_vendor(str(load_data.vendor_id))
    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vendor with ID {load_data.vendor_id} not found"
        )
    
    # Geocode pickup address
    pickup_location = geocoding_service.geocode(load_data.pickup_address)
    if not pickup_location:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not find GPS coordinates for pickup address: {load_data.pickup_address}"
        )
    
    # Geocode destination address
    destination_location = geocoding_service.geocode(load_data.destination_address)
    if not destination_location:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not find GPS coordinates for destination address: {load_data.destination_address}"
        )
    
    # Create load
    load = db.create_load(
        vendor_id=str(load_data.vendor_id),
        weight_kg=load_data.weight_kg,
        pickup_lat=pickup_location.lat,
        pickup_lng=pickup_location.lng,
        pickup_address=pickup_location.address,
        destination_lat=destination_location.lat,
        destination_lng=destination_location.lng,
        destination_address=destination_location.address,
        price_offered=load_data.price_offered,
        currency=load_data.currency
    )
    
    return {
        "message": "Load created successfully",
        "load_id": load['load_id'],
        "pickup": {
            "address": pickup_location.address,
            "gps": f"{pickup_location.lat}, {pickup_location.lng}"
        },
        "destination": {
            "address": destination_location.address,
            "gps": f"{destination_location.lat}, {destination_location.lng}"
        }
    }


@router.get("/geocode/search")
def search_places(query: str, limit: int = 5):
    """
    Search for places using OpenStreetMap
    
    Useful for autocomplete in frontend forms.
    
    Example: /api/v1/vendors/geocode/search?query=market%20yard%20mumbai
    """
    results = geocoding_service.search_places(query, limit=limit)
    
    return {
        "query": query,
        "count": len(results),
        "results": [
            {
                "address": r.address,
                "lat": r.lat,
                "lng": r.lng
            }
            for r in results
        ]
    }


@router.get("/geocode/address")
def geocode_address(address: str):
    """
    Convert address to GPS coordinates
    
    Example: /api/v1/vendors/geocode/address?address=Azadpur%20Mandi,%20Delhi
    """
    location = geocoding_service.geocode(address)
    
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find GPS coordinates for: {address}"
        )
    
    return {
        "input_address": address,
        "found_address": location.address,
        "lat": location.lat,
        "lng": location.lng
    }


@router.get("/geocode/reverse")
def reverse_geocode(lat: float, lng: float):
    """
    Convert GPS coordinates to address
    
    Example: /api/v1/vendors/geocode/reverse?lat=28.6139&lng=77.2090
    """
    address = geocoding_service.reverse_geocode(lat, lng)
    
    return {
        "lat": lat,
        "lng": lng,
        "address": address
    }
