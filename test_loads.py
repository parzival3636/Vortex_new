"""Test loads in database"""
from db_chromadb import db

print("\n=== TESTING LOADS ===\n")

# Try to get all loads (not just available)
try:
    result = db.loads.get()
    print(f"Total loads in collection: {len(result['ids']) if result['ids'] else 0}")
    
    if result['ids']:
        for i, (load_id, metadata) in enumerate(zip(result['ids'], result['metadatas']), 1):
            print(f"\n{i}. Load ID: {load_id}")
            print(f"   Status: {metadata.get('status', 'N/A')}")
            print(f"   Pickup: {metadata.get('pickup_address', 'N/A')}")
            print(f"   Destination: {metadata.get('destination_address', 'N/A')}")
            print(f"   Price: ₹{metadata.get('price_offered', 0)}")
except Exception as e:
    print(f"Error: {e}")

print("\n=== Available Loads ===\n")
available = db.get_available_loads()
print(f"Available loads: {len(available)}")

print("\n=== END ===\n")
