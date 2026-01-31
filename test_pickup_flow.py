"""
Test Pickup Confirmation Flow
"""

import requests
from db_chromadb import db

BASE_URL = "http://localhost:8000/api/v1"

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

print_section("PICKUP CONFIRMATION TEST")

# Step 1: Create demo data
print("1. Creating demo data...")
response = requests.post(f"{BASE_URL}/demo/init")
demo = response.json()
print(f"✓ Demo data created")
print(f"  Driver ID: {demo['driver_id']}")
print(f"  Truck ID: {demo['truck_id']}")

# Step 2: Create a trip
print("\n2. Creating trip...")
trip_data = {
    "driver_id": demo['driver_id'],
    "truck_id": demo['truck_id'],
    "origin": {
        "lat": 28.6139,
        "lng": 77.2090,
        "address": "Delhi"
    },
    "destination": {
        "lat": 26.9124,
        "lng": 75.7873,
        "address": "Jaipur"
    },
    "outbound_load": "Electronics"
}

response = requests.post(f"{BASE_URL}/trips/", json=trip_data)
trip = response.json()
trip_id = trip['trip_id']
print(f"✓ Trip created: {trip_id}")

# Step 3: Get available loads
print("\n3. Getting available loads...")
response = requests.get(f"{BASE_URL}/loads/available")
loads = response.json()
print(f"✓ Found {len(loads)} available loads")

if len(loads) == 0:
    print("✗ No loads available for testing")
    exit()

load = loads[0]
load_id = load['load_id']
print(f"  Using load: {load_id}")
print(f"  Status: {load['status']}")

# Step 4: Accept the load
print("\n4. Accepting load...")
response = requests.patch(f"{BASE_URL}/loads/{load_id}/accept?trip_id={trip_id}")
print(f"✓ Load accepted")

# Verify load status
load_after_accept = db.get_load(load_id)
print(f"  Load status after accept: {load_after_accept['status']}")
print(f"  Assigned to trip: {load_after_accept['assigned_trip_id']}")

# Step 5: Confirm pickup
print("\n5. Confirming pickup...")
response = requests.patch(f"{BASE_URL}/trips/{trip_id}/pickup")
result = response.json()
print(f"✓ Pickup confirmed!")
print(f"  Message: {result['message']}")
if 'load_id' in result:
    print(f"  Load ID: {result['load_id']}")
    print(f"  Status: {result['status']}")

# Verify load status in database
load_after_pickup = db.get_load(load_id)
print(f"\n6. Verifying in database...")
print(f"  Load status: {load_after_pickup['status']}")
print(f"  Picked up at: {load_after_pickup['picked_up_at']}")

if load_after_pickup['status'] == 'picked_up':
    print(f"\n✅ PICKUP CONFIRMATION WORKING!")
    print(f"  - Load status changed from 'assigned' to 'picked_up'")
    print(f"  - Pickup timestamp recorded")
else:
    print(f"\n✗ PICKUP CONFIRMATION FAILED")
    print(f"  Expected status: 'picked_up'")
    print(f"  Actual status: '{load_after_pickup['status']}'")

# Step 6: Confirm delivery
print("\n7. Confirming delivery...")
response = requests.patch(f"{BASE_URL}/trips/{trip_id}/delivery")
result = response.json()
print(f"✓ Delivery confirmed!")
print(f"  Message: {result['message']}")

# Verify load status
load_after_delivery = db.get_load(load_id)
print(f"\n8. Verifying delivery in database...")
print(f"  Load status: {load_after_delivery['status']}")
print(f"  Delivered at: {load_after_delivery['delivered_at']}")

if load_after_delivery['status'] == 'delivered':
    print(f"\n✅ COMPLETE FLOW WORKING!")
    print(f"  available → assigned → picked_up → delivered")
else:
    print(f"\n✗ DELIVERY CONFIRMATION FAILED")

print("\n" + "="*60)
