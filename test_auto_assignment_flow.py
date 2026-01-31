"""
Test Auto-Assignment Flow
Simulates what happens when driver creates a trip in frontend
"""

import requests
import time

BASE_URL = "http://localhost:8000/api/v1"

print("\n" + "="*70)
print("  AUTO-ASSIGNMENT FLOW TEST")
print("="*70 + "\n")

# Step 1: Create demo data
print("1. Creating demo data...")
response = requests.post(f"{BASE_URL}/demo/init")
demo = response.json()
driver_id = demo['driver_id']
truck_id = demo['truck_id']
print(f"✓ Driver: {driver_id[:8]}...")
print(f"✓ Truck: {truck_id[:8]}...")

# Step 2: Create trip (like frontend does)
print("\n2. Driver creates trip...")
trip_data = {
    "driver_id": driver_id,
    "truck_id": truck_id,
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
print(f"✓ Trip created: {trip_id[:8]}...")

# Step 3: Mark as deadheading (like frontend does)
print("\n3. Marking trip as deadheading...")
response = requests.patch(f"{BASE_URL}/trips/{trip_id}/deadhead")
print(f"✓ Trip marked as deadheading")

# Step 4: Trigger auto-scheduler (like frontend does)
print("\n4. Triggering AI auto-scheduler...")
print("   🤖 AI is finding the best load...")
response = requests.post(f"{BASE_URL}/scheduler/force-run")
result = response.json()
print(f"✓ Scheduler completed")
print(f"   Matches found: {result['stats']['last_run_matches']}")

# Step 5: Check if load was auto-assigned
print("\n5. Checking for auto-assigned load...")
time.sleep(1)  # Give it a moment
response = requests.get(f"{BASE_URL}/trips/{trip_id}/assigned-load")
assignment = response.json()

if assignment['has_assigned_load']:
    load = assignment['load']
    print(f"\n✅ LOAD AUTO-ASSIGNED!")
    print(f"\n   Load Details:")
    print(f"   Load ID: {load['load_id'][:8]}...")
    print(f"   Weight: {load['weight_kg']}kg")
    print(f"   Price: ₹{load['price_offered']}")
    print(f"   Status: {load['status']}")
    print(f"   Pickup: {load['pickup_location']['address'][:50]}...")
    print(f"   Delivery: {load['destination']['address'][:50]}...")
    print(f"\n   🎉 Driver doesn't need to manually accept!")
    print(f"   🎉 AI automatically found and assigned the best load!")
else:
    print(f"\n   ℹ️  No load auto-assigned")
    print(f"   Driver will need to manually select from available loads")

print("\n" + "="*70)
print("  FLOW COMPLETE")
print("="*70 + "\n")

print("Summary:")
print("  1. Driver creates trip ✅")
print("  2. Trip marked as deadheading ✅")
print("  3. AI scheduler triggered ✅")
print("  4. Best load found and assigned ✅" if assignment['has_assigned_load'] else "  4. No optimal load found ℹ️")
print("  5. Driver sees assigned load automatically ✅" if assignment['has_assigned_load'] else "  5. Driver selects manually ℹ️")

print("\n" + "="*70 + "\n")
