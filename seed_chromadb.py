"""
Seed ChromaDB with sample data
Run this to add test data: python seed_chromadb.py
"""

from db_chromadb import db


def seed_data():
    """Seed the database with sample data"""
    
    print("🌱 Seeding ChromaDB...")
    
    # Create Owners
    print("\n📦 Creating Owners...")
    owner1 = db.create_owner(
        name="Rajesh Transport Co.",
        email="rajesh@transport.com"
    )
    owner2 = db.create_owner(
        name="Singh Logistics",
        email="singh@logistics.com"
    )
    print(f"✅ Created 2 owners")
    
    # Create Trucks
    print("\n🚛 Creating Trucks...")
    truck1 = db.create_truck(
        owner_id=owner1["owner_id"],
        license_plate="DL-01-AB-1234",
        fuel_consumption_rate=0.35
    )
    truck2 = db.create_truck(
        owner_id=owner1["owner_id"],
        license_plate="DL-01-CD-5678",
        fuel_consumption_rate=0.40
    )
    truck3 = db.create_truck(
        owner_id=owner2["owner_id"],
        license_plate="MH-02-EF-9012",
        fuel_consumption_rate=0.38
    )
    print(f"✅ Created 3 trucks")
    
    # Create Drivers
    print("\n👨‍✈️ Creating Drivers...")
    driver1 = db.create_driver(
        name="Amit Kumar",
        phone="+91-9876543210",
        truck_id=truck1["truck_id"],
        hourly_rate=25.0
    )
    driver2 = db.create_driver(
        name="Vijay Singh",
        phone="+91-9876543211",
        truck_id=truck2["truck_id"],
        hourly_rate=28.0
    )
    driver3 = db.create_driver(
        name="Suresh Patil",
        phone="+91-9876543212",
        truck_id=truck3["truck_id"],
        hourly_rate=30.0
    )
    print(f"✅ Created 3 drivers")
    
    # Create Vendors
    print("\n🏪 Creating Vendors...")
    vendor1 = db.create_vendor(
        name="Delhi Market Yard",
        email="delhi@market.com",
        phone="+91-9876543220",
        location_lat=28.6517,
        location_lng=77.2219
    )
    vendor2 = db.create_vendor(
        name="Gurgaon Wholesale",
        email="gurgaon@wholesale.com",
        phone="+91-9876543221",
        location_lat=28.4595,
        location_lng=77.0266
    )
    vendor3 = db.create_vendor(
        name="Noida Distribution Center",
        email="noida@distribution.com",
        phone="+91-9876543222",
        location_lat=28.5355,
        location_lng=77.3910
    )
    print(f"✅ Created 3 vendors")
    
    # Create Sample Trips
    print("\n🚗 Creating Sample Trips...")
    trip1 = db.create_trip(
        driver_id=driver1["driver_id"],
        truck_id=truck1["truck_id"],
        origin_lat=28.6139,
        origin_lng=77.2090,
        origin_address="Delhi, India",
        destination_lat=28.7041,
        destination_lng=77.1025,
        destination_address="Rohini, Delhi",
        outbound_load="Electronics - 5 tons"
    )
    trip2 = db.create_trip(
        driver_id=driver2["driver_id"],
        truck_id=truck2["truck_id"],
        origin_lat=19.0760,
        origin_lng=72.8777,
        origin_address="Mumbai, India",
        destination_lat=18.5204,
        destination_lng=73.8567,
        destination_address="Pune, India",
        outbound_load="Textiles - 8 tons"
    )
    # Mark trip2 as deadheading
    db.mark_deadheading(trip2["trip_id"])
    print(f"✅ Created 2 trips (1 deadheading)")
    
    # Create Available Loads
    print("\n📦 Creating Available Loads...")
    load1 = db.create_load(
        vendor_id=vendor1["vendor_id"],
        weight_kg=5000,
        pickup_lat=28.6517,
        pickup_lng=77.2219,
        pickup_address="Connaught Place, Delhi",
        destination_lat=28.6900,
        destination_lng=77.1500,
        destination_address="Pitampura, Delhi",
        price_offered=5000,
        currency="INR"
    )
    load2 = db.create_load(
        vendor_id=vendor2["vendor_id"],
        weight_kg=7000,
        pickup_lat=28.4595,
        pickup_lng=77.0266,
        pickup_address="Gurgaon, India",
        destination_lat=28.7041,
        destination_lng=77.1025,
        destination_address="Rohini, Delhi",
        price_offered=8000,
        currency="INR"
    )
    load3 = db.create_load(
        vendor_id=vendor3["vendor_id"],
        weight_kg=3000,
        pickup_lat=28.5355,
        pickup_lng=77.3910,
        pickup_address="Noida, India",
        destination_lat=28.6139,
        destination_lng=77.2090,
        destination_address="Delhi, India",
        price_offered=4000,
        currency="INR"
    )
    load4 = db.create_load(
        vendor_id=vendor1["vendor_id"],
        weight_kg=6000,
        pickup_lat=18.6298,
        pickup_lng=73.7997,
        pickup_address="Lonavala, India",
        destination_lat=19.0760,
        destination_lng=72.8777,
        destination_address="Mumbai, India",
        price_offered=7000,
        currency="INR"
    )
    print(f"✅ Created 4 available loads")
    
    print("\n" + "="*60)
    print("✅ CHROMADB SEEDED SUCCESSFULLY!")
    print("="*60)
    print(f"\n📊 Summary:")
    print(f"   - 2 Owners")
    print(f"   - 3 Trucks")
    print(f"   - 3 Drivers")
    print(f"   - 3 Vendors")
    print(f"   - 2 Trips (1 deadheading)")
    print(f"   - 4 Available Loads")
    print("\n🎯 Data stored in: ./chroma_data/")
    print("\n💡 Test IDs:")
    print(f"   Driver 1: {driver1['driver_id']}")
    print(f"   Driver 2 (deadheading): {driver2['driver_id']}")
    print(f"   Trip 2 (deadheading): {trip2['trip_id']}")
    print("="*60 + "\n")


def clear_data():
    """Clear all data"""
    print("🗑️  Clearing ChromaDB...")
    db.clear_all_data()
    print("✅ ChromaDB cleared")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--clear":
        clear_data()
    else:
        seed_data()
