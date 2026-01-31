"""
Test load ranking to verify Mumbai load ranks higher than Noida load
for Pune → Delhi driver route
"""

from services.math_engine import math_engine
from models.domain import Coordinate

# Driver route: Pune → Delhi
driver_current = Coordinate(lat=18.5204, lng=73.8567, address="Pune, Maharashtra")
driver_destination = Coordinate(lat=28.6139, lng=77.2090, address="Delhi, Delhi")

# Load 1: Mumbai → Delhi (should be TOP PICK)
load1_pickup = Coordinate(lat=19.0760, lng=72.8777, address="Mumbai, Maharashtra")
load1_delivery = Coordinate(lat=28.6139, lng=77.2090, address="Delhi, Delhi")
load1_payment = 12000

# Load 2: Noida → Delhi (should be lower ranked)
load2_pickup = Coordinate(lat=28.5355, lng=77.3910, address="Noida, Uttar Pradesh")
load2_delivery = Coordinate(lat=28.6139, lng=77.2090, address="Delhi, Delhi")
load2_payment = 4000

print("="*60)
print("LOAD RANKING TEST")
print("="*60)
print(f"\nDriver Route: {driver_current.address} → {driver_destination.address}")
print()

# Calculate profitability for Load 1 (Mumbai)
print("LOAD 1: Mumbai → Delhi")
print("-" * 40)
result1 = math_engine.calculate_full_profitability(
    driver_current=driver_current,
    driver_destination=driver_destination,
    vendor_pickup=load1_pickup,
    vendor_destination=load1_delivery,
    vendor_offering=load1_payment
)

print(f"Pickup: {load1_pickup.address}")
print(f"Delivery: {load1_delivery.address}")
print(f"Payment: ₹{load1_payment:,}")
print(f"Extra Distance: {result1['extra_distance_km']} km")
print(f"Fuel Cost: ₹{result1['fuel_cost']}")
print(f"Net Profit: ₹{result1['net_profit']}")
print(f"Profitability Score: {result1['profitability_score']}")
print()

# Calculate profitability for Load 2 (Noida)
print("LOAD 2: Noida → Delhi")
print("-" * 40)
result2 = math_engine.calculate_full_profitability(
    driver_current=driver_current,
    driver_destination=driver_destination,
    vendor_pickup=load2_pickup,
    vendor_destination=load2_delivery,
    vendor_offering=load2_payment
)

print(f"Pickup: {load2_pickup.address}")
print(f"Delivery: {load2_delivery.address}")
print(f"Payment: ₹{load2_payment:,}")
print(f"Extra Distance: {result2['extra_distance_km']} km")
print(f"Fuel Cost: ₹{result2['fuel_cost']}")
print(f"Net Profit: ₹{result2['net_profit']}")
print(f"Profitability Score: {result2['profitability_score']}")
print()

# Compare
print("="*60)
print("COMPARISON")
print("="*60)
print(f"\nLoad 1 (Mumbai) Score: {result1['profitability_score']}")
print(f"Load 2 (Noida) Score: {result2['profitability_score']}")
print()

if result1['profitability_score'] > result2['profitability_score']:
    print("✅ CORRECT: Mumbai load ranks HIGHER (as expected)")
    print(f"   Mumbai is on the way from Pune to Delhi")
    print(f"   Extra distance: {result1['extra_distance_km']}km vs {result2['extra_distance_km']}km")
else:
    print("❌ ERROR: Noida load ranks HIGHER (unexpected!)")
    print(f"   This is wrong - Mumbai should be top pick")
    print(f"   Extra distance: {result1['extra_distance_km']}km vs {result2['extra_distance_km']}km")

print()
print("="*60)
