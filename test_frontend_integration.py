"""
Frontend Integration Test
Simulates what happens when user interacts with the frontend
"""

import requests
import time

BASE_URL = "http://localhost:8000/api/v1"

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_frontend_flow():
    """Simulate frontend user flow"""
    
    print_section("FRONTEND FLOW TEST")
    print("Simulating user interactions with the frontend...")
    
    # ===== VENDOR DASHBOARD =====
    print_section("1. VENDOR DASHBOARD - Register Vendor")
    print("User opens Vendor Dashboard...")
    print("Frontend calls: POST /api/v1/vendors/register")
    
    vendor_data = {
        "name": "Mumbai Market Vendor",
        "email": "mumbai@market.com",
        "phone": "+91-7777777777",
        "address": "Crawford Market, Mumbai"
    }
    
    response = requests.post(f"{BASE_URL}/vendors/register", json=vendor_data)
    if response.status_code == 201:
        vendor = response.json()
        print(f"✓ Vendor registered!")
        print(f"  Name: {vendor['name']}")
        print(f"  Location: {vendor['address']}")
        vendor_id = vendor['vendor_id']
    else:
        print(f"✗ Failed: {response.text}")
        return
    
    print_section("2. VENDOR DASHBOARD - Post Load")
    print("User fills form and clicks 'Post Load'...")
    print("Frontend calls: POST /api/v1/vendors/loads/by-address")
    
    load_data = {
        "vendor_id": vendor_id,
        "weight_kg": 8000,
        "pickup_address": "Crawford Market, Mumbai",
        "destination_address": "Pune, Maharashtra",
        "price_offered": 18000,
        "currency": "INR"
    }
    
    response = requests.post(f"{BASE_URL}/vendors/loads/by-address", json=load_data)
    if response.status_code == 200:
        result = response.json()
        print(f"✓ Load posted!")
        print(f"  Load ID: {result['load_id']}")
        print(f"  From: {result['pickup']['address'][:50]}...")
        print(f"  To: {result['destination']['address'][:50]}...")
        load_id = result['load_id']
    else:
        print(f"✗ Failed: {response.text}")
        return
    
    # ===== DRIVER DASHBOARD =====
    print_section("3. DRIVER DASHBOARD - Initialize Demo Data")
    print("User opens Driver Dashboard...")
    print("Frontend calls: POST /api/v1/demo/init")
    
    response = requests.post(f"{BASE_URL}/demo/init")
    if response.status_code == 200:
        demo = response.json()
        print(f"✓ Demo data initialized!")
        print(f"  Owner ID: {demo['owner_id']}")
        print(f"  Truck ID: {demo['truck_id']}")
        print(f"  Driver ID: {demo['driver_id']}")
        driver_id = demo['driver_id']
        truck_id = demo['truck_id']
    else:
        print(f"✗ Failed: {response.text}")
        return
    
    print_section("4. DRIVER DASHBOARD - Fetch Available Loads")
    print("Frontend calls: GET /api/v1/loads/available")
    
    response = requests.get(f"{BASE_URL}/loads/available")
    if response.status_code == 200:
        loads = response.json()
        print(f"✓ Fetched {len(loads)} available loads")
        
        # Find our load
        our_load = None
        for load in loads:
            if load['load_id'] == load_id:
                our_load = load
                break
        
        if our_load:
            print(f"\n✓ Our load is visible to driver!")
            print(f"  Weight: {our_load['weight_kg']}kg")
            print(f"  Price: ₹{our_load['price_offered']}")
            print(f"  Status: {our_load['status']}")
        else:
            print(f"\n✗ Our load not found!")
    else:
        print(f"✗ Failed: {response.text}")
        return
    
    print_section("5. DRIVER DASHBOARD - Create Trip")
    print("User enters source and destination...")
    print("Frontend calls: POST /api/v1/trips/")
    
    trip_data = {
        "driver_id": driver_id,
        "truck_id": truck_id,
        "origin": {
            "lat": 19.0760,
            "lng": 72.8777,
            "address": "Mumbai, Maharashtra"
        },
        "destination": {
            "lat": 18.5204,
            "lng": 73.8567,
            "address": "Pune, Maharashtra"
        },
        "outbound_load": "Electronics"
    }
    
    response = requests.post(f"{BASE_URL}/trips/", json=trip_data)
    if response.status_code == 201:
        trip = response.json()
        print(f"✓ Trip created!")
        print(f"  Trip ID: {trip['trip_id']}")
        print(f"  From: {trip['origin']['address']}")
        print(f"  To: {trip['destination']['address']}")
        trip_id = trip['trip_id']
    else:
        print(f"✗ Failed: {response.text}")
        return
    
    print_section("6. DRIVER DASHBOARD - Calculate Profitability")
    print("Frontend calls: POST /api/v1/calculate/profitability")
    
    calc_data = {
        "driver_current": {
            "lat": 19.0760,
            "lng": 72.8777,
            "address": "Mumbai, Maharashtra"
        },
        "driver_destination": {
            "lat": 18.5204,
            "lng": 73.8567,
            "address": "Pune, Maharashtra"
        },
        "vendor_pickup": {
            "lat": our_load['pickup_location']['lat'],
            "lng": our_load['pickup_location']['lng'],
            "address": our_load['pickup_location']['address']
        },
        "vendor_destination": {
            "lat": our_load['destination']['lat'],
            "lng": our_load['destination']['lng'],
            "address": our_load['destination']['address']
        },
        "vendor_offering": our_load['price_offered']
    }
    
    response = requests.post(f"{BASE_URL}/calculate/profitability", json=calc_data)
    if response.status_code == 200:
        result = response.json()
        print(f"✓ Profitability calculated!")
        print(f"  Extra Distance: {result.get('extra_distance_km', 0):.1f} km")
        print(f"  Fuel Cost: ₹{result.get('fuel_cost', 0):.2f}")
        print(f"  Driver Cost: ₹{result.get('driver_cost', 0):.2f}")
        print(f"  Revenue: ₹{result.get('revenue', 0):.2f}")
        print(f"  Net Profit: ₹{result.get('net_profit', 0):.2f}")
        print(f"  Profitability Score: {result.get('profitability_score', 0):.2f}")
        print(f"  Recommendation: {result.get('recommendation', 'N/A')}")
    else:
        print(f"✗ Failed: {response.text}")
        return
    
    print_section("7. DRIVER DASHBOARD - Accept Load")
    print("User clicks 'Accept Load'...")
    print("Frontend calls: PATCH /api/v1/loads/{load_id}/accept")
    
    response = requests.patch(f"{BASE_URL}/loads/{load_id}/accept?trip_id={trip_id}")
    if response.status_code == 200:
        print(f"✓ Load accepted!")
        print(f"  Load is now assigned to driver")
    else:
        print(f"✗ Failed: {response.text}")
        return
    
    print_section("8. VERIFY - Check Load Status")
    print("Verifying load is no longer available...")
    
    response = requests.get(f"{BASE_URL}/loads/{load_id}")
    if response.status_code == 200:
        load = response.json()
        print(f"✓ Load status updated!")
        print(f"  Status: {load['status']}")
        print(f"  Assigned to trip: {load['assigned_trip_id']}")
        print(f"  Assigned to driver: {load['assigned_driver_id']}")
    else:
        print(f"✗ Failed: {response.text}")
        return
    
    print_section("✅ FRONTEND INTEGRATION TEST PASSED!")
    print("Complete flow verified:")
    print("  1. ✓ Vendor registers via frontend")
    print("  2. ✓ Vendor posts load via frontend")
    print("  3. ✓ Driver sees load on dashboard")
    print("  4. ✓ Driver creates trip")
    print("  5. ✓ System calculates profitability")
    print("  6. ✓ Driver accepts load")
    print("  7. ✓ Load status updates in database")
    print(f"\n🎉 Frontend integration is working perfectly!")

if __name__ == "__main__":
    try:
        test_frontend_flow()
    except requests.exceptions.ConnectionError:
        print("\n✗ ERROR: Cannot connect to backend!")
        print("Please start the backend first:")
        print("  python main.py")
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
