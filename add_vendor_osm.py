"""
Add Vendor with OpenStreetMap Geocoding
Uses real GPS coordinates from OpenStreetMap
"""

from db_chromadb import db
from services.geocoding import geocoding_service
from models.domain import Coordinate


def add_vendor_with_address():
    """Add vendor by entering address - OSM will find GPS coordinates"""
    print("\n" + "="*70)
    print("📦 ADD VENDOR WITH OPENSTREETMAP GEOCODING")
    print("="*70)
    
    # Vendor details
    print("\n1️⃣  VENDOR INFORMATION")
    vendor_name = input("Vendor Name: ")
    vendor_email = input("Vendor Email: ")
    vendor_phone = input("Vendor Phone: ")
    vendor_address = input("Vendor Address (e.g., 'Azadpur Mandi, Delhi'): ")
    
    # Geocode vendor location
    print(f"\n🔍 Finding GPS coordinates for: {vendor_address}")
    vendor_location = geocoding_service.geocode(vendor_address)
    
    if not vendor_location:
        print("❌ Could not find location. Please try a different address.")
        return
    
    print(f"✅ Found location:")
    print(f"   Address: {vendor_location.address}")
    print(f"   GPS: {vendor_location.lat}, {vendor_location.lng}")
    
    confirm = input("\nIs this correct? (y/n): ")
    if confirm.lower() != 'y':
        print("❌ Cancelled")
        return
    
    # Create vendor
    vendor = db.create_vendor(
        name=vendor_name,
        email=vendor_email,
        phone=vendor_phone,
        location_lat=vendor_location.lat,
        location_lng=vendor_location.lng
    )
    
    print(f"\n✅ Vendor created with ID: {vendor['vendor_id']}")
    
    # Add load
    print("\n2️⃣  LOAD INFORMATION")
    add_load = input("Add a load for this vendor? (y/n): ")
    
    if add_load.lower() == 'y':
        weight_kg = float(input("Load weight (kg): "))
        
        # Pickup is vendor location
        pickup_address = vendor_location.address
        
        # Destination
        dest_address = input("Destination address (e.g., 'Jaipur, Rajasthan'): ")
        
        print(f"\n🔍 Finding GPS coordinates for: {dest_address}")
        destination = geocoding_service.geocode(dest_address)
        
        if not destination:
            print("❌ Could not find destination. Load not created.")
            return
        
        print(f"✅ Found destination:")
        print(f"   Address: {destination.address}")
        print(f"   GPS: {destination.lat}, {destination.lng}")
        
        price_offered = float(input("Price offered (₹): "))
        
        # Create load
        load = db.create_load(
            vendor_id=vendor['vendor_id'],
            weight_kg=weight_kg,
            pickup_lat=vendor_location.lat,
            pickup_lng=vendor_location.lng,
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
    print("✅ VENDOR DATA ADDED WITH REAL GPS COORDINATES!")
    print("="*70)


def search_and_add_vendor():
    """Search for a place and add vendor there"""
    print("\n" + "="*70)
    print("🔍 SEARCH PLACE AND ADD VENDOR")
    print("="*70)
    
    # Search for place
    query = input("\nSearch for a place (e.g., 'market yard mumbai'): ")
    
    print(f"\n🔍 Searching OpenStreetMap for: {query}")
    results = geocoding_service.search_places(query, limit=5)
    
    if not results:
        print("❌ No results found. Try a different search.")
        return
    
    print(f"\n📍 Found {len(results)} places:")
    for i, place in enumerate(results, 1):
        print(f"\n{i}. {place.address}")
        print(f"   GPS: {place.lat}, {place.lng}")
    
    choice = int(input("\nSelect place (number): "))
    
    if choice < 1 or choice > len(results):
        print("❌ Invalid choice")
        return
    
    selected_place = results[choice - 1]
    
    # Vendor details
    print("\n1️⃣  VENDOR INFORMATION")
    vendor_name = input("Vendor Name: ")
    vendor_email = input("Vendor Email: ")
    vendor_phone = input("Vendor Phone: ")
    
    # Create vendor
    vendor = db.create_vendor(
        name=vendor_name,
        email=vendor_email,
        phone=vendor_phone,
        location_lat=selected_place.lat,
        location_lng=selected_place.lng
    )
    
    print(f"\n✅ Vendor created at: {selected_place.address}")
    print(f"   Vendor ID: {vendor['vendor_id']}")
    
    # Add load
    print("\n2️⃣  LOAD INFORMATION")
    add_load = input("Add a load for this vendor? (y/n): ")
    
    if add_load.lower() == 'y':
        weight_kg = float(input("Load weight (kg): "))
        dest_address = input("Destination address: ")
        
        print(f"\n🔍 Finding destination...")
        destination = geocoding_service.geocode(dest_address)
        
        if not destination:
            print("❌ Could not find destination.")
            return
        
        print(f"✅ Destination: {destination.address}")
        
        price_offered = float(input("Price offered (₹): "))
        
        # Create load
        load = db.create_load(
            vendor_id=vendor['vendor_id'],
            weight_kg=weight_kg,
            pickup_lat=selected_place.lat,
            pickup_lng=selected_place.lng,
            pickup_address=selected_place.address,
            destination_lat=destination.lat,
            destination_lng=destination.lng,
            destination_address=destination.address,
            price_offered=price_offered,
            currency="INR"
        )
        
        print(f"\n✅ Load created with ID: {load['load_id']}")
    
    print("\n" + "="*70)
    print("✅ DONE!")
    print("="*70)


def test_geocoding():
    """Test OpenStreetMap geocoding"""
    print("\n" + "="*70)
    print("🧪 TESTING OPENSTREETMAP GEOCODING")
    print("="*70)
    
    # Test 1: Geocode address
    print("\n1. Testing address → GPS coordinates")
    address = "Azadpur Mandi, Delhi"
    print(f"   Address: {address}")
    
    result = geocoding_service.geocode(address)
    if result:
        print(f"   ✅ GPS: {result.lat}, {result.lng}")
        print(f"   Full: {result.address}")
    else:
        print("   ❌ Failed")
    
    # Test 2: Reverse geocode
    print("\n2. Testing GPS coordinates → address")
    lat, lng = 28.6139, 77.2090
    print(f"   GPS: {lat}, {lng}")
    
    address = geocoding_service.reverse_geocode(lat, lng)
    print(f"   ✅ Address: {address}")
    
    # Test 3: Search places
    print("\n3. Testing place search")
    query = "market yard mumbai"
    print(f"   Query: {query}")
    
    results = geocoding_service.search_places(query, limit=3)
    print(f"   ✅ Found {len(results)} results:")
    for i, place in enumerate(results, 1):
        print(f"      {i}. {place.address[:80]}...")
    
    print("\n" + "="*70)
    print("✅ GEOCODING TESTS COMPLETE!")
    print("="*70)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            test_geocoding()
        elif sys.argv[1] == "search":
            search_and_add_vendor()
        else:
            print("Usage:")
            print("  python add_vendor_osm.py          # Add vendor by address")
            print("  python add_vendor_osm.py search   # Search and add vendor")
            print("  python add_vendor_osm.py test     # Test geocoding")
    else:
        add_vendor_with_address()
