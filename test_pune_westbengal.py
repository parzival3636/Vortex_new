"""Test Pune → West Bengal driver with Mumbai → West Bengal load"""
import requests
import time

BASE_URL = "http://localhost:8000/api/v1"

print("\n" + "="*70)
print("  TESTING: Pune → West Bengal Driver")
print("  LOAD: Mumbai → West Bengal")
print("="*70 + "\n")

# Step 1: Create demo data
print("1. Creating demo driver...")
response = requests.post(f"{BASE_URL}/demo/init")
demo = response.json()
driver_id = demo['driver_id']
truck_id = demo['truck_id']
print(f"✓ Driver ID: {driver_id[:8]}...")

# Step 2: Create trip Pune → West Bengal
print("\n2. Creating trip: Pune → West Bengal...")
trip_data = {
    "driver_id": driver_id,
    "truck_id": truck_id,
    "origin": {
        "lat": 18.5204,
        "lng": 73.8567,
        "address": "Pune, Maharashtra"
    },
    "destination": {
        "lat": 22.9868,
        "lng": 87.8550,
        "address": "West Bengal, India"
    },
    "outbound_load": "Electronics"
}

response = requests.post(f"{BASE_URL}/trips/", json=trip_data)
trip = response.json()
trip_id = trip['trip_id']
print(f"✓ Trip created: {trip_id[:8]}...")
print(f"  Route: Pune → West Bengal")

# Step 3: Mark as deadheading
print("\n3. Marking as deadheading...")
response = requests.patch(f"{BASE_URL}/trips/{trip_id}/deadhead")
print(f"✓ Marked as deadheading")

# Step 4: Get available loads (what driver sees)
print("\n4. Getting available loads (manual view)...")
response = requests.get(f"{BASE_URL}/loads/available")
loads = response.json()
print(f"✓ Total available loads: {len(loads)}")

# Find Mumbai → West Bengal load
mumbai_load = None
for load in loads:
    if 'Mumbai' in load['pickup_location']['address'] and 'West Bengal' in load['destination']['address']:
        mumbai_load = load
        break

if mumbai_load:
    print(f"\n✅ MUMBAI → WEST BENGAL LOAD FOUND IN AVAILABLE LOADS!")
    print(f"   Load ID: {mumbai_load['load_id'][:8]}...")
    print(f"   Pickup: {mumbai_load['pickup_location']['address'][:50]}...")
    print(f"   Delivery: {mumbai_load['destination']['address'][:50]}...")
    print(f"   Price: ₹{mumbai_load['price_offered']}")
    print(f"   Status: {mumbai_load['status']}")
else:
    print(f"\n❌ MUMBAI → WEST BENGAL LOAD NOT IN AVAILABLE LOADS")
    print(f"\nShowing first 3 available loads:")
    for i, load in enumerate(loads[:3], 1):
        print(f"\n{i}. {load['pickup_location']['address'][:40]} → {load['destination']['address'][:40]}")

# Step 5: Trigger auto-scheduler
print("\n5. Triggering AI auto-scheduler...")
response = requests.post(f"{BASE_URL}/scheduler/force-run")
result = response.json()
print(f"✓ Scheduler completed")
print(f"   Matches found: {result['stats']['last_run_matches']}")

# Step 6: Check if load was auto-assigned
print("\n6. Checking for auto-assignment...")
time.sleep(1)
response = requests.get(f"{BASE_URL}/trips/{trip_id}/assigned-load")
assignment = response.json()

if assignment['has_assigned_load']:
    load = assignment['load']
    print(f"\n✅ LOAD AUTO-ASSIGNED!")
    print(f"   Load ID: {load['load_id'][:8]}...")
    print(f"   Pickup: {load['pickup_location']['address'][:50]}...")
    print(f"   Delivery: {load['destination']['address'][:50]}...")
    print(f"   Price: ₹{load['price_offered']}")
    
    # Check if it's the Mumbai load
    if 'Mumbai' in load['pickup_location']['address']:
        print(f"\n🎉 YES! It's the Mumbai → West Bengal load!")
    else:
        print(f"\n⚠️  Different load was assigned")
else:
    print(f"\n❌ NO LOAD AUTO-ASSIGNED")
    print(f"   Checking why...")
    
    # Check if Mumbai load is still available
    from db_chromadb import db
    all_loads = db.loads.get()
    
    for load_meta in all_loads['metadatas']:
        if 'Mumbai' in load_meta.get('pickup_address', '') and 'West Bengal' in load_meta.get('destination_address', ''):
            print(f"\n   Mumbai load status: {load_meta['status']}")
            if load_meta['status'] == 'assigned':
                print(f"   Already assigned to: {load_meta['assigned_trip_id'][:8]}...")
            break

print("\n" + "="*70 + "\n")
