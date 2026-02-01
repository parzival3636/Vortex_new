"""
Seed Demo Data for Manual Allocation Feature
Creates owner, trucks, drivers, vendors, and loads for testing
"""

from db_chromadb import db
import uuid

def seed_demo_data():
    """Create demo data for testing manual allocation"""
    
    print("=" * 60)
    print("SEEDING DEMO DATA")
    print("=" * 60)
    
    # 1. Create Owner
    print("\n1. Creating Owner...")
    owner = db.create_owner("Demo Transport Co.", "owner@demo.com")
    owner_id = owner['owner_id']
    print(f"   ✓ Owner created: {owner['name']} (ID: {owner_id})")
    
    # 2. Create Trucks
    print("\n2. Creating Trucks...")
    trucks = []
    truck_plates = [
        "DL-01-AB-1234",
        "MH-02-CD-5678",
        "KA-03-EF-9012",
        "RJ-04-GH-3456",
        "UP-05-IJ-7890"
    ]
    
    for plate in truck_plates:
        truck = db.create_truck(owner_id, plate, fuel_consumption_rate=0.35)
        trucks.append(truck)
        print(f"   ✓ Truck created: {plate}")
    
    # 3. Create Drivers
    print("\n3. Creating Drivers...")
    drivers = []
    driver_names = [
        ("Rajesh Kumar", "+91-9876543210"),
        ("Amit Singh", "+91-9876543211"),
        ("Suresh Reddy", "+91-9876543212"),
        ("Vijay Sharma", "+91-9876543213"),
        ("Ravi Patel", "+91-9876543214")
    ]
    
    for i, (name, phone) in enumerate(driver_names):
        driver = db.create_driver(name, phone, trucks[i]['truck_id'], hourly_rate=25.0)
        drivers.append(driver)
        print(f"   ✓ Driver created: {name} → {truck_plates[i]}")
    
    # 4. Add Vehicle Locations (GPS)
    print("\n4. Adding Vehicle Locations...")
    locations = [
        (28.6139, 77.2090, "Delhi"),      # Delhi
        (19.0760, 72.8777, "Mumbai"),     # Mumbai
        (12.9716, 77.5946, "Bangalore"),  # Bangalore
        (26.9124, 75.7873, "Jaipur"),     # Jaipur
        (22.5726, 88.3639, "Kolkata")     # Kolkata
    ]
    
    for i, (lat, lng, city) in enumerate(locations):
        db.add_location_update(trucks[i]['truck_id'], lat, lng, 10.0)
        print(f"   ✓ Location added: {truck_plates[i]} at {city}")
    
    # 5. Create Vendors
    print("\n5. Creating Vendors...")
    vendors = []
    vendor_data = [
        ("Azadpur Fruits Co.", "fruits@azadpur.com", "+91-9876540001", 28.7041, 77.1025),  # Delhi
        ("Mumbai Textiles Ltd.", "textiles@mumbai.com", "+91-9876540002", 19.0176, 72.8562),  # Mumbai
        ("Bangalore Electronics", "electronics@blr.com", "+91-9876540003", 12.9716, 77.5946),  # Bangalore
        ("Jaipur Handicrafts", "handicrafts@jaipur.com", "+91-9876540004", 26.9124, 75.7873),  # Jaipur
    ]
    
    for name, email, phone, lat, lng in vendor_data:
        vendor = db.create_vendor(name, email, phone, lat, lng)
        vendors.append(vendor)
        print(f"   ✓ Vendor created: {name}")
    
    # 6. Create Loads
    print("\n6. Creating Loads...")
    loads_data = [
        # (vendor_idx, weight, pickup_lat, pickup_lng, pickup_addr, dest_lat, dest_lng, dest_addr, price)
        (0, 5000, 28.7041, 77.1025, "Azadpur Mandi, Delhi", 26.9124, 75.7873, "Jaipur, Rajasthan", 15000),
        (1, 3000, 19.0176, 72.8562, "Mumbai Port, Mumbai", 18.5204, 73.8567, "Pune, Maharashtra", 12000),
        (2, 4000, 12.9716, 77.5946, "Electronic City, Bangalore", 13.0827, 80.2707, "Chennai, Tamil Nadu", 18000),
        (3, 2500, 26.9124, 75.7873, "Jaipur Market, Jaipur", 28.6139, 77.2090, "Delhi", 10000),
        (0, 6000, 28.6139, 77.2090, "Connaught Place, Delhi", 19.0760, 72.8777, "Mumbai, Maharashtra", 25000),
        (1, 3500, 19.0760, 72.8777, "Andheri, Mumbai", 23.0225, 72.5714, "Ahmedabad, Gujarat", 14000),
        (2, 4500, 12.9716, 77.5946, "Whitefield, Bangalore", 17.3850, 78.4867, "Hyderabad, Telangana", 16000),
    ]
    
    for vendor_idx, weight, p_lat, p_lng, p_addr, d_lat, d_lng, d_addr, price in loads_data:
        load = db.create_load(
            vendor_id=vendors[vendor_idx]['vendor_id'],
            weight_kg=weight,
            pickup_lat=p_lat,
            pickup_lng=p_lng,
            pickup_address=p_addr,
            destination_lat=d_lat,
            destination_lng=d_lng,
            destination_address=d_addr,
            price_offered=price,
            currency="INR"
        )
        print(f"   ✓ Load created: {p_addr.split(',')[0]} → {d_addr.split(',')[0]} (₹{price:,})")
    
    print("\n" + "=" * 60)
    print("DEMO DATA SEEDED SUCCESSFULLY!")
    print("=" * 60)
    print(f"\n📊 Summary:")
    print(f"   • 1 Owner")
    print(f"   • 5 Trucks")
    print(f"   • 5 Drivers")
    print(f"   • 4 Vendors")
    print(f"   • 7 Loads")
    print(f"\n🎯 Owner ID: {owner_id}")
    print(f"   Use this ID in the Owner Dashboard")
    print(f"\n🚛 Driver IDs:")
    for i, driver in enumerate(drivers):
        print(f"   • {driver['name']}: {driver['driver_id']}")
    
    print(f"\n✅ You can now:")
    print(f"   1. Open Owner Dashboard → Manual Allocation tab")
    print(f"   2. See 5 available vehicles")
    print(f"   3. See 7 unallocated loads")
    print(f"   4. Start allocating!")
    
    return {
        "owner_id": owner_id,
        "trucks": trucks,
        "drivers": drivers,
        "vendors": vendors
    }


def clear_all_data():
    """Clear all data from database"""
    print("\n⚠️  WARNING: This will delete ALL data!")
    confirm = input("Type 'yes' to confirm: ")
    if confirm.lower() == 'yes':
        db.clear_all_data()
        print("✓ All data cleared!")
    else:
        print("✗ Cancelled")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--clear':
        clear_all_data()
    else:
        seed_demo_data()
