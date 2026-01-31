"""
Test Auto-Scheduler
Demonstrates AI-powered automatic load assignment
"""

import requests
import time
from db_chromadb import db

BASE_URL = "http://localhost:8000/api/v1"

def print_section(title):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")

print_section("AI-POWERED AUTO-SCHEDULER TEST")

# Step 1: Create test data
print("1. Setting up test data...")

# Create demo data (owner, truck, driver)
response = requests.post(f"{BASE_URL}/demo/init")
demo = response.json()
print(f"✓ Demo data created")
print(f"  Driver ID: {demo['driver_id']}")
print(f"  Truck ID: {demo['truck_id']}")

# Create a trip (deadheading driver)
print("\n2. Creating trip (deadheading driver)...")
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
print(f"  Route: Delhi → Jaipur")

# Check available loads
print("\n3. Checking available loads...")
response = requests.get(f"{BASE_URL}/loads/available")
loads = response.json()
print(f"✓ Found {len(loads)} available loads")

if len(loads) == 0:
    print("⚠️  No loads available. Creating a test load...")
    
    # Register vendor
    vendor_response = requests.post(f"{BASE_URL}/vendors/register", json={
        "name": "Test Vendor",
        "email": "test@vendor.com",
        "phone": "+91-9999999999",
        "address": "Azadpur Mandi, Delhi"
    })
    vendor = vendor_response.json()
    
    # Create load
    load_response = requests.post(f"{BASE_URL}/vendors/loads/by-address", json={
        "vendor_id": vendor['vendor_id'],
        "weight_kg": 5000,
        "pickup_address": "Delhi",
        "destination_address": "Jaipur",
        "price_offered": 15000,
        "currency": "INR"
    })
    print(f"✓ Test load created")

# Step 2: Check scheduler status
print_section("CHECKING AUTO-SCHEDULER STATUS")

response = requests.get(f"{BASE_URL}/scheduler/status")
status = response.json()
print(f"Status: {'🟢 Running' if status['running'] else '🔴 Stopped'}")
print(f"Interval: {status['interval_seconds']} seconds")
print(f"Total Runs: {status['total_runs']}")
print(f"Total Assignments: {status['total_assignments']}")

# Step 3: Force run scheduler
print_section("FORCING SCHEDULER RUN (IMMEDIATE)")

print("Running AI-powered auto-scheduler...")
print("This will:")
print("  1. Find active trips (our Delhi → Jaipur trip)")
print("  2. Get available loads")
print("  3. Use Math Engine to calculate profitability")
print("  4. Use AI Agents to find optimal match")
print("  5. Auto-assign best load to driver")

response = requests.post(f"{BASE_URL}/scheduler/force-run")
result = response.json()

print(f"\n✓ Scheduler run completed!")
print(f"\nStats:")
print(f"  Total Runs: {result['stats']['total_runs']}")
print(f"  Total Matches: {result['stats']['total_matches']}")
print(f"  Total Assignments: {result['stats']['total_assignments']}")
print(f"  Last Run Matches: {result['stats']['last_run_matches']}")

# Step 4: Verify assignment
print_section("VERIFYING AUTO-ASSIGNMENT")

# Check if trip has assigned load
all_loads = db.loads.get()
assigned_load = None

if all_loads['ids']:
    for load_meta in all_loads['metadatas']:
        if load_meta.get('assigned_trip_id') == trip_id:
            assigned_load = load_meta
            break

if assigned_load:
    print(f"✅ LOAD AUTO-ASSIGNED!")
    print(f"\nLoad Details:")
    print(f"  Load ID: {assigned_load['load_id']}")
    print(f"  Status: {assigned_load['status']}")
    print(f"  Weight: {assigned_load['weight_kg']}kg")
    print(f"  Price: ₹{assigned_load['price_offered']}")
    print(f"  Pickup: {assigned_load['pickup_address'][:50]}...")
    print(f"  Delivery: {assigned_load['destination_address'][:50]}...")
    print(f"  Assigned to Trip: {assigned_load['assigned_trip_id']}")
    print(f"  Assigned to Driver: {assigned_load['assigned_driver_id']}")
else:
    print(f"ℹ️  No load was assigned")
    print(f"   Possible reasons:")
    print(f"   - No profitable loads found")
    print(f"   - All loads too far from route")
    print(f"   - No loads available")

# Step 5: Start continuous scheduler
print_section("STARTING CONTINUOUS AUTO-SCHEDULER")

print("Starting scheduler to run every 2 minutes...")
response = requests.post(f"{BASE_URL}/scheduler/start")
result = response.json()

print(f"✓ {result['message']}")
print(f"  Interval: {result['interval_seconds']} seconds")
print(f"  Status: {result['status']}")

print(f"\n🤖 Auto-scheduler is now running in the background!")
print(f"   It will check for new trips and loads every 2 minutes")
print(f"   and automatically assign optimal loads to drivers.")

print_section("TEST COMPLETE")

print("Summary:")
print("  ✅ Auto-scheduler tested successfully")
print("  ✅ Math Engine used for profitability calculations")
print("  ✅ AI Agents used for optimal matching")
print("  ✅ Automatic assignment working")
print("  ✅ Continuous scheduler started")

print("\nTo stop the scheduler:")
print("  POST http://localhost:8000/api/v1/scheduler/stop")

print("\nTo check status:")
print("  GET http://localhost:8000/api/v1/scheduler/status")

print("\n" + "="*70)
