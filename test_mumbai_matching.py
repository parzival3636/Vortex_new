"""Test if Mumbai → West Bengal load matches with different driver routes"""
from services.math_engine import math_engine
from models.domain import Coordinate
from db_chromadb import db

print("\n=== TESTING MUMBAI → WEST BENGAL LOAD MATCHING ===\n")

# Get the Mumbai → West Bengal load
all_loads = db.loads.get()
mumbai_load = None

for load_meta in all_loads['metadatas']:
    if 'Mumbai' in load_meta.get('pickup_address', '') and 'West Bengal' in load_meta.get('destination_address', ''):
        mumbai_load = load_meta
        break

if not mumbai_load:
    print("❌ Mumbai → West Bengal load not found!")
    exit()

print(f"✅ Found load:")
print(f"   Load ID: {mumbai_load['load_id'][:8]}...")
print(f"   Pickup: {mumbai_load['pickup_address']}")
print(f"   Delivery: {mumbai_load['destination_address']}")
print(f"   Price: ₹{mumbai_load['price_offered']}")
print(f"   Status: {mumbai_load['status']}")

# Test with different driver routes
test_routes = [
    {
        "name": "Delhi → Kolkata",
        "origin": Coordinate(lat=28.6139, lng=77.2090, address="Delhi"),
        "destination": Coordinate(lat=22.5726, lng=88.3639, address="Kolkata")
    },
    {
        "name": "Mumbai → Kolkata",
        "origin": Coordinate(lat=19.0760, lng=72.8777, address="Mumbai"),
        "destination": Coordinate(lat=22.5726, lng=88.3639, address="Kolkata")
    },
    {
        "name": "Pune → West Bengal",
        "origin": Coordinate(lat=18.5204, lng=73.8567, address="Pune"),
        "destination": Coordinate(lat=22.9868, lng=87.8550, address="West Bengal")
    },
    {
        "name": "Mumbai → West Bengal",
        "origin": Coordinate(lat=19.0760, lng=72.8777, address="Mumbai"),
        "destination": Coordinate(lat=22.9868, lng=87.8550, address="West Bengal")
    }
]

load_pickup = Coordinate(
    lat=mumbai_load['pickup_lat'],
    lng=mumbai_load['pickup_lng'],
    address=mumbai_load['pickup_address']
)

load_destination = Coordinate(
    lat=mumbai_load['destination_lat'],
    lng=mumbai_load['destination_lng'],
    address=mumbai_load['destination_address']
)

print(f"\n{'='*70}")
print("TESTING DIFFERENT DRIVER ROUTES")
print(f"{'='*70}\n")

for route in test_routes:
    print(f"Driver Route: {route['name']}")
    print(f"  Origin: {route['origin'].address}")
    print(f"  Destination: {route['destination'].address}")
    
    # Calculate profitability
    profitability = math_engine.calculate_full_profitability(
        driver_current=route['origin'],
        driver_destination=route['destination'],
        vendor_pickup=load_pickup,
        vendor_destination=load_destination,
        vendor_offering=mumbai_load['price_offered']
    )
    
    print(f"\n  Profitability Analysis:")
    print(f"    Extra Distance: {profitability['extra_distance_km']} km")
    print(f"    Fuel Cost: ₹{profitability['fuel_cost']}")
    print(f"    Time Cost: ₹{profitability['time_cost']}")
    print(f"    Net Profit: ₹{profitability['net_profit']}")
    print(f"    Profitability Score: {profitability['profitability_score']}")
    
    if profitability['net_profit'] > 0:
        print(f"    ✅ PROFITABLE - Would be shown to driver")
    else:
        print(f"    ❌ NOT PROFITABLE - Would be filtered out")
    
    # Check distance to pickup
    distance_to_pickup = math_engine.calculate_distance(route['origin'], load_pickup)
    print(f"    Distance to Pickup: {distance_to_pickup} km")
    
    from config import settings
    if distance_to_pickup <= settings.max_route_deviation_km:
        print(f"    ✅ Within max deviation ({settings.max_route_deviation_km} km)")
    else:
        print(f"    ❌ Too far (max: {settings.max_route_deviation_km} km)")
    
    print()

print(f"{'='*70}\n")
