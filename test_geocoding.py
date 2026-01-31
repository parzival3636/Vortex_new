"""
Test geocoding service
"""

from services.geocoding import geocoding_service

print("\n=== TESTING GEOCODING ===\n")

# Test addresses
test_addresses = [
    "New Delhi, Delhi, India",
    "New Delhi",
    "Delhi",
    "Connaught Place, Delhi",
    "Azadpur Mandi, Delhi",
    "Jaipur, Rajasthan"
]

for address in test_addresses:
    print(f"\nTesting: {address}")
    result = geocoding_service.geocode(address)
    
    if result:
        print(f"✓ Success!")
        print(f"  Lat: {result.lat}")
        print(f"  Lng: {result.lng}")
        print(f"  Address: {result.address[:80]}...")
    else:
        print(f"✗ Failed to geocode")

print("\n=== END ===\n")
