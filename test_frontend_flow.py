"""
Simulate Frontend Flow - Test if data persists
This simulates exactly what happens when vendor posts load via frontend
"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

print("\n" + "="*70)
print("🧪 TESTING FRONTEND FLOW - VENDOR POSTS LOAD")
print("="*70)

# Step 1: Register Vendor (what frontend does)
print("\n📝 Step 1: Registering vendor...")
vendor_data = {
    "name": "Test Vendor from Frontend",
    "email": "frontend@test.com",
    "phone": "+91-8888888888",
    "address": "Azadpur Mandi, Delhi"
}

try:
    response = requests.post(f"{BASE_URL}/vendors/register", json=vendor_data)
    if response.status_code == 201:
        vendor = response.json()
        print(f"✅ Vendor registered!")
        print(f"   Vendor ID: {vendor['vendor_id']}")
        print(f"   GPS: {vendor['location_lat']}, {vendor['location_lng']}")
        print(f"   Address: {vendor['address']}")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)
        exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

# Step 2: Post Load (what frontend does)
print("\n📦 Step 2: Posting load...")
load_data = {
    "vendor_id": vendor['vendor_id'],
    "weight_kg": 8000,
    "pickup_address": "Azadpur Mandi, Delhi",
    "destination_address": "Jaipur, Rajasthan",
    "price_offered": 15000,
    "currency": "INR"
}

try:
    response = requests.post(f"{BASE_URL}/vendors/loads/by-address", json=load_data)
    if response.status_code == 200:
        load = response.json()
        print(f"✅ Load posted!")
        print(f"   Load ID: {load['load_id']}")
        print(f"   Pickup: {load['pickup']['address']}")
        print(f"   Pickup GPS: {load['pickup']['gps']}")
        print(f"   Destination: {load['destination']['address']}")
        print(f"   Destination GPS: {load['destination']['gps']}")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)
        exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

# Step 3: Verify load is in database
print("\n🔍 Step 3: Checking if load is in database...")
try:
    response = requests.get(f"{BASE_URL}/loads/available")
    if response.status_code == 200:
        loads = response.json()
        print(f"✅ Found {len(loads)} available loads in database")
        
        # Find our load
        our_load = None
        for l in loads:
            if l['vendor_id'] == vendor['vendor_id']:
                our_load = l
                break
        
        if our_load:
            print(f"\n✅ OUR LOAD IS IN DATABASE!")
            print(f"   Load ID: {our_load['load_id']}")
            print(f"   Pickup: {our_load['pickup_location']['address']}")
            print(f"   Destination: {our_load['destination']['address']}")
            print(f"   Weight: {our_load['weight_kg']}kg")
            print(f"   Price: ₹{our_load['price_offered']}")
            print(f"   Status: {our_load['status']}")
        else:
            print("❌ Our load NOT found in database!")
    else:
        print(f"❌ Failed to get loads: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*70)
print("✅ TEST COMPLETE!")
print("="*70)
print("\n💡 Now run: python check_db.py")
print("   You should see 5 loads (4 original + 1 new)")
print("\n")
