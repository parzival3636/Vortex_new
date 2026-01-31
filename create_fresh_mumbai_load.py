"""Create a fresh Mumbai → West Bengal load"""
import requests

BASE_URL = "http://localhost:8000/api/v1"

print("\n=== CREATING FRESH MUMBAI → WEST BENGAL LOAD ===\n")

# Register vendor
print("1. Registering vendor...")
vendor_data = {
    "name": "Mumbai Cargo Services",
    "email": "mumbai@cargo.com",
    "phone": "+91-9876543210",
    "address": "Mumbai, Maharashtra"
}

response = requests.post(f"{BASE_URL}/vendors/register", json=vendor_data)
vendor = response.json()
vendor_id = vendor['vendor_id']
print(f"✓ Vendor registered: {vendor_id[:8]}...")

# Create load
print("\n2. Creating load: Mumbai → West Bengal...")
load_data = {
    "vendor_id": vendor_id,
    "weight_kg": 5000,
    "pickup_address": "Mumbai, Maharashtra",
    "destination_address": "Kolkata, West Bengal",
    "price_offered": 75000,
    "currency": "INR"
}

response = requests.post(f"{BASE_URL}/vendors/loads/by-address", json=load_data)
result = response.json()

print(f"✓ Load created!")
print(f"  Load ID: {result['load_id']}")
print(f"  Pickup: {result['pickup']['address'][:50]}...")
print(f"  Delivery: {result['destination']['address'][:50]}...")
print(f"  Weight: 5000kg")
print(f"  Price: ₹75,000")

print("\n✅ Fresh load ready for assignment!")
print("\nNow try:")
print("  1. Go to Driver Dashboard")
print("  2. Enter: Pune → West Bengal")
print("  3. Click 'Plan Route'")
print("  4. Load should auto-assign!")

print("\n=== END ===\n")
