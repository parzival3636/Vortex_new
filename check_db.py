"""Check database contents"""
from db_chromadb import db

print("\n=== CHECKING DATABASE ===\n")

# Check loads
loads = db.get_available_loads()
print(f"Available loads in DB: {len(loads)}")
for i, load in enumerate(loads[:5], 1):
    print(f"\n{i}. Load ID: {load['load_id']}")
    print(f"   Pickup: {load['pickup_address']}")
    print(f"   Destination: {load['destination_address']}")
    print(f"   Weight: {load['weight_kg']}kg")
    print(f"   Price: ₹{load['price_offered']}")
    print(f"   Status: {load['status']}")

print("\n=== END ===\n")
