"""
Demo API - Helper endpoints for demo/testing
"""

from fastapi import APIRouter
from db_chromadb import db

router = APIRouter(prefix="/api/v1/demo", tags=["demo"])


@router.post("/init")
def initialize_demo_data():
    """
    Initialize demo data (owner, truck, driver)
    Returns IDs that can be used for testing
    """
    # Create demo owner
    owner = db.create_owner(
        name="Demo Transport Co.",
        email="demo@transport.com"
    )
    
    # Create demo truck
    truck = db.create_truck(
        owner_id=owner["owner_id"],
        license_plate="DEMO-1234"
    )
    
    # Create demo driver
    driver = db.create_driver(
        name="Demo Driver",
        phone="+91-9999999999",
        truck_id=truck["truck_id"]
    )
    
    return {
        "owner_id": owner["owner_id"],
        "truck_id": truck["truck_id"],
        "driver_id": driver["driver_id"],
        "message": "Demo data initialized successfully"
    }


@router.get("/data")
def get_demo_data():
    """Get existing demo data or create if doesn't exist"""
    try:
        # Try to get existing demo data
        # For now, just create new ones
        return initialize_demo_data()
    except Exception as e:
        return {"error": str(e)}
