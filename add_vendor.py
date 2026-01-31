"""
Add Vendor and Load Data to ChromaDB
Simple script to add vendors and their loads
"""

from db_chromadb import db
from services.real_world_data import real_world_data

def add_vendor_interactive():
    """Interactive vendor addition"""
    print("\n" + "="*70)
    print("📦 ADD VENDOR AND LOAD TO SYSTEM")
    print("="*70)
    
    # Get vendor details
    print("\n1️⃣  VENDOR INFORMATION")
    vendor_name = input("Vendor Name: ")
    vendor_email = input("Vendor Email: ")
    vendor_phone = input("Vendor Phone: ")
    
    # Get location - show available market yards
    print("\n📍 Available Market Yards:")
    market_yards = real_world_data.get_all_market_yards()
    for i, yard in enumerate(market_yards, 1):
        print(f"   {i}. {yard.name} - {yard.address}")
    
    choice = int(input("\nSelect market yard (number) or 0 for custom location: "))
    
    if choice > 0 and choice <= len(market_yards):
        location = market_yards[choice - 1]
        vendor_lat = location.lat
        vendor_lng = location.lng
    else:
        vendor_lat = float(input("Vendor Latitude: "))
        vendor_lng = float(input("Vendor Longitude: "))
    
    # Create vendor
    vendor = db.create_vendor(
        name=vendor_name,
        email=vendor_email,
        phone=vendor_phone,
        location_lat=vendor_lat,
        location_lng=vendor_lng
    )
    
    print(f"\n✅ Vendor created with ID: {vendor['vendor_id']}")
    
    # Add load
    print("\n2️⃣  LOAD INFORMATION")
    add_load = input("Add a load for this vendor? (y/n): ")
    
    if add_load.lower() == 'y':
        weight_kg = float(input("Load weight (kg): "))
        
        # Pickup location (use vendor location)
        print(f"\nPickup Location: {location.address if choice > 0 else 'Custom'}")
        pickup_lat = vendor_lat
        pickup_lng = vendor_lng
        pickup_address = location.address if choice > 0 else input("Pickup Address: ")
        
        # Destination
        print("\n📍 Available Cities for Delivery:")
        cities = real_world_data.get_all_cities()
        for i, city in enumerate(cities, 1):
            print(f"   {i}. {city.address}")
        
        dest_choice = int(input("\nSelect destination city (number): "))
        destination = cities[dest_choice - 1]
        
        price_offered = float(input("Price offered (₹): "))
        
        # Create load
        load = db.create_load(
            vendor_id=vendor['vendor_id'],
            weight_kg=weight_kg,
            pickup_lat=pickup_lat,
            pickup_lng=pickup_lng,
            pickup_address=pickup_address,
            destination_lat=destination.lat,
            destination_lng=destination.lng,
            destination_address=destination.address,
            price_offered=price_offered,
            currency="INR"
        )
        
        print(f"\n✅ Load created with ID: {load['load_id']}")
        print(f"   From: {pickup_address}")
        print(f"   To: {destination.address}")
        print(f"   Weight: {weight_kg} kg")
        print(f"   Price: ₹{price_offered}")
    
    print("\n" + "="*70)
    print("✅ VENDOR DATA ADDED SUCCESSFULLY!")
    print("="*70)


def add_vendor_quick(name, email, phone, market_yard_name, destination_city, weight_kg, price):
    """Quick vendor addition with predefined data"""
    # Find market yard
    market_yards = real_world_data.get_all_market_yards()
    market_yard = next((m for m in market_yards if market_yard_name.lower() in m.name.lower()), None)
    
    if not market_yard:
        print(f"❌ Market yard '{market_yard_name}' not found")
        return
    
    # Create vendor
    vendor = db.create_vendor(
        name=name,
        email=email,
        phone=phone,
        location_lat=market_yard.lat,
        location_lng=market_yard.lng
    )
    
    # Find destination city
    cities = real_world_data.get_all_cities()
    city = next((c for c in cities if destination_city.lower() in c.address.lower()), None)
    
    if not city:
        print(f"❌ City '{destination_city}' not found")
        return
    
    # Create load
    load = db.create_load(
        vendor_id=vendor['vendor_id'],
        weight_kg=weight_kg,
        pickup_lat=market_yard.lat,
        pickup_lng=market_yard.lng,
        pickup_address=market_yard.address,
        destination_lat=city.lat,
        destination_lng=city.lng,
        destination_address=city.address,
        price_offered=price,
        currency="INR"
    )
    
    print(f"✅ Added vendor '{name}' with load to {destination_city}")
    print(f"   Load ID: {load['load_id']}")
    print(f"   Price: ₹{price}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        # Quick mode with example data
        print("\n🚀 Quick Mode - Adding sample vendors...\n")
        
        add_vendor_quick(
            "Azadpur Fruits Co.",
            "fruits@azadpur.com",
            "+91-9876543210",
            "Azadpur",
            "Jaipur",
            5000,
            12000
        )
        
        add_vendor_quick(
            "Vashi Vegetables Ltd.",
            "veg@vashi.com",
            "+91-9876543211",
            "Vashi",
            "Pune",
            3000,
            8000
        )
        
    else:
        # Interactive mode
        add_vendor_interactive()
