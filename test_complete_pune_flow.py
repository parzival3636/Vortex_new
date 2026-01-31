"""Complete test: Create load, then create Pune driver, should auto-assign"""
import requests
import time

BASE_URL = "http://localhost:8000/api/v1"

print("\n" + "="*70)
print("  COMPLETE FLOW: Fresh Load → Pune Driver → Auto-Assign")
print("="*70 + "\n")

# Step 1: Create fresh Mumbai → Kolkata load
print("1. Creating FRESH Mumbai → Kolkata load...")
vendor_response = requests.post(f"{BASE_URL}/vendors/register", json={
    "name": "Fresh Mumbai Vendor",
    "email": "fresh@mumbai.com",
    "phone": "+91-8888888888",
    "address": "Mumbai, Maharashtra"
})
vendor_id = vendor_response.json()['vendor_id']

load_response = requests.post(f"{BASE_URL}/vendors/loads/by-address", json={
    "vendor_id": vendor_id,
    "weight_kg": 6000,
    "pickup_address": "Mumbai, Maharashtra",
    "destination_address": "Kolkata, West Bengal",
    "price_offered": 80000,
    "currency": "INR"
})
load_result = load_response.json()
load_id = load_result['load_id']

print(f"✓ Fresh load created!")
print(f"  Load ID: {load_id[:8]}...")
print(f"  Pickup: Mumbai")
print(f"  Delivery: Kolkata")
print(f"  Price: ₹80,000")

# Step 2: Create Pune → West Bengal driver
print("\n2. Creating Pune → West Bengal driver...")
demo_response = requests.post(f"{BASE_URL}/demo/init")
demo = demo_response.json()
driver_id = demo['driver_id']
truck_id = demo['truck_id']

trip_response = requests.post(f"{BASE_URL}/trips/", json={
    "driver_id": driver_id,
    "truck_id": truck_id,
    "origin": {
        "lat": 18.5204,
        "lng": 73.8567,
        "address": "Pune, Maharashtra"
    },
    "destination": {
        "lat": 22.5726,
        "lng": 88.3639,
        "address": "Kolkata, West Bengal"
    },
    "outbound_load": "Electronics"
})
trip = trip_response.json()
trip_id = trip['trip_id']

print(f"✓ Driver created!")
print(f"  Driver ID: {driver_id[:8]}...")
print(f"  Route: Pune → Kolkata")

# Step 3: Mark as deadheading
print("\n3. Marking as deadheading...")
requests.patch(f"{BASE_URL}/trips/{trip_id}/deadhead")
print(f"✓ Marked as deadheading")

# Step 4: Trigger scheduler
print("\n4. Triggering AI auto-scheduler...")
print("   🤖 AI is finding the best load...")
scheduler_response = requests.post(f"{BASE_URL}/scheduler/force-run")
result = scheduler_response.json()
print(f"✓ Scheduler completed")
print(f"   Matches found: {result['stats']['last_run_matches']}")

# Step 5: Check assignment
print("\n5. Checking if Mumbai load was assigned to Pune driver...")
time.sleep(1)
assignment_response = requests.get(f"{BASE_URL}/trips/{trip_id}/assigned-load")
assignment = assignment_response.json()

if assignment['has_assigned_load']:
    assigned_load = assignment['load']
    print(f"\n✅ LOAD AUTO-ASSIGNED!")
    print(f"   Load ID: {assigned_load['load_id'][:8]}...")
    print(f"   Pickup: {assigned_load['pickup_location']['address'][:50]}...")
    print(f"   Delivery: {assigned_load['destination']['address'][:50]}...")
    print(f"   Price: ₹{assigned_load['price_offered']}")
    
    if assigned_load['load_id'] == load_id:
        print(f"\n🎉 YES! The fresh Mumbai → Kolkata load was assigned!")
        print(f"🎉 Pune → Kolkata driver got the Mumbai load!")
    else:
        print(f"\n⚠️  Different load was assigned")
        print(f"   Expected: {load_id[:8]}...")
        print(f"   Got: {assigned_load['load_id'][:8]}...")
else:
    print(f"\n❌ NO LOAD AUTO-ASSIGNED")

print("\n" + "="*70)
print("  SUMMARY")
print("="*70)
print(f"Fresh Mumbai load created: ✅")
print(f"Pune → Kolkata driver created: ✅")
print(f"Auto-scheduler triggered: ✅")
print(f"Load assigned: {'✅' if assignment['has_assigned_load'] else '❌'}")
print("="*70 + "\n")
