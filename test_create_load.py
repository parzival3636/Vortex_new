"""Test creating a single load"""
from db_chromadb import db

print("\n=== TESTING LOAD CREATION ===\n")

# First create a vendor
print("Creating vendor...")
vendor = db.create_vendor(
    name="Test Vendor",
    email="test@vendor.com",
    phone="+91-9999999999",
    location_lat=28.6139,
    location_lng=77.2090
)
print(f"✅ Vendor created: {vendor['vendor_id']}")

# Now create a load
print("\nCreating load...")
try:
    load = db.create_load(
        vendor_id=vendor["vendor_id"],
        weight_kg=5000.0,
        pickup_lat=28.6139,
        pickup_lng=77.2090,
        pickup_address="Delhi, India",
        destination_lat=26.9124,
        destination_lng=75.7873,
        destination_address="Jaipur, India",
        price_offered=12000.0,
        currency="INR"
    )
    print(f"✅ Load created: {load['load_id']}")
    print(f"   Status: {load['status']}")
    print(f"   Pickup: {load['pickup_address']}")
    print(f"   Destination: {load['destination_address']}")
except Exception as e:
    print(f"❌ Error creating load: {e}")
    import traceback
    traceback.print_exc()

# Check if load is in database
print("\nChecking database...")
loads = db.get_available_loads()
print(f"Available loads: {len(loads)}")

print("\n=== END ===\n")
