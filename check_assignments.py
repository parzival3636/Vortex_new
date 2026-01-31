"""Check auto-scheduler assignments"""
from db_chromadb import db

print("\n=== CHECKING AUTO-SCHEDULER ASSIGNMENTS ===\n")

# Get all loads
all_loads = db.loads.get()

if not all_loads['ids']:
    print("No loads in database")
else:
    assigned_loads = []
    available_loads = []
    
    for load_meta in all_loads['metadatas']:
        if load_meta.get('status') == 'assigned':
            assigned_loads.append(load_meta)
        elif load_meta.get('status') == 'available':
            available_loads.append(load_meta)
    
    print(f"Total Loads: {len(all_loads['ids'])}")
    print(f"  - Assigned: {len(assigned_loads)}")
    print(f"  - Available: {len(available_loads)}")
    
    if assigned_loads:
        print(f"\n✅ AUTO-ASSIGNED LOADS:\n")
        for i, load in enumerate(assigned_loads[:10], 1):
            print(f"{i}. Load ID: {load['load_id'][:8]}...")
            print(f"   Status: {load['status']}")
            print(f"   Weight: {load['weight_kg']}kg")
            print(f"   Price: ₹{load['price_offered']}")
            print(f"   Pickup: {load['pickup_address'][:50]}...")
            print(f"   Delivery: {load['destination_address'][:50]}...")
            print(f"   Assigned to Trip: {load['assigned_trip_id'][:8]}...")
            print(f"   Assigned to Driver: {load['assigned_driver_id'][:8]}...")
            print()

print("=== END ===\n")
