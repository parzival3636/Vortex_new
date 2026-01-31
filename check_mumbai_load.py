"""Check if Mumbai to West Bengal load exists and why it's not showing"""
from db_chromadb import db

print("\n=== CHECKING MUMBAI → WEST BENGAL LOAD ===\n")

# Get all loads
all_loads = db.loads.get()

if not all_loads['ids']:
    print("❌ No loads in database!")
else:
    print(f"Total loads in database: {len(all_loads['ids'])}\n")
    
    # Find Mumbai/West Bengal loads
    mumbai_loads = []
    
    for load_meta in all_loads['metadatas']:
        pickup = load_meta.get('pickup_address', '').lower()
        destination = load_meta.get('destination_address', '').lower()
        
        if 'mumbai' in pickup or 'mumbai' in destination or 'bengal' in destination or 'kolkata' in destination:
            mumbai_loads.append(load_meta)
    
    if mumbai_loads:
        print(f"✅ Found {len(mumbai_loads)} load(s) related to Mumbai/West Bengal:\n")
        
        for i, load in enumerate(mumbai_loads, 1):
            print(f"{i}. Load ID: {load['load_id'][:8]}...")
            print(f"   Status: {load['status']}")
            print(f"   Weight: {load['weight_kg']}kg")
            print(f"   Price: ₹{load['price_offered']}")
            print(f"   Pickup: {load['pickup_address']}")
            print(f"   Delivery: {load['destination_address']}")
            
            if load['status'] == 'assigned':
                print(f"   ⚠️  ALREADY ASSIGNED!")
                print(f"   Assigned to Trip: {load['assigned_trip_id'][:8]}...")
                print(f"   Assigned to Driver: {load['assigned_driver_id'][:8]}...")
            elif load['status'] == 'available':
                print(f"   ✅ AVAILABLE for assignment")
            
            print()
    else:
        print("❌ No loads found with Mumbai or West Bengal in addresses")
        print("\nShowing all loads:")
        for i, load_meta in enumerate(all_loads['metadatas'][:5], 1):
            print(f"\n{i}. {load_meta['pickup_address'][:50]} → {load_meta['destination_address'][:50]}")
            print(f"   Status: {load_meta['status']}")

print("=== END ===\n")
