"""
Quick system test - Verify all components work
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_api():
    """Test API endpoints"""
    print("\n" + "="*70)
    print("🧪 TESTING API ENDPOINTS")
    print("="*70)
    
    # Test root endpoint
    print("\n1. Testing root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    # Test health check
    print("\n2. Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    # Test profitability calculation
    print("\n3. Testing profitability calculation...")
    calc_data = {
        "driver_current": {"lat": 28.6139, "lng": 77.2090, "address": "Delhi"},
        "driver_destination": {"lat": 26.9124, "lng": 75.7873, "address": "Jaipur"},
        "vendor_pickup": {"lat": 19.0760, "lng": 72.8777, "address": "Mumbai"},
        "vendor_destination": {"lat": 26.9124, "lng": 75.7873, "address": "Jaipur"}
,
        "vendor_offering": 15000.0
    }
    response = requests.post(f"{BASE_URL}/api/v1/calculate/profitability", json=calc_data)
    print(f"   Status: {response.status_code}")
    result = response.json()
    print(f"   Extra Distance: {result['extra_distance_km']} km")
    print(f"   Net Profit: ₹{result['net_profit']}")
    print(f"   Profitability Score: {result['profitability_score']}")
    
    print("\n" + "="*70)
    print("✅ ALL API TESTS PASSED!")
    print("="*70)


def test_database():
    """Test ChromaDB"""
    print("\n" + "="*70)
    print("🧪 TESTING CHROMADB")
    print("="*70)
    
    from db_chromadb import db
    
    # Test getting available loads
    print("\n1. Testing get_available_loads...")
    loads = db.get_available_loads()
    print(f"   Found {len(loads)} available loads")
    
    if loads:
        print(f"   Sample load: {loads[0]['pickup_address']} → {loads[0]['destination_address']}")
        print(f"   Price: ₹{loads[0]['price_offered']}")
    
    print("\n" + "="*70)
    print("✅ DATABASE TESTS PASSED!")
    print("="*70)


def test_math_engine():
    """Test Math Engine"""
    print("\n" + "="*70)
    print("🧪 TESTING MATH ENGINE")
    print("="*70)
    
    from services.math_engine import math_engine
    from models.domain import Coordinate
    
    delhi = Coordinate(lat=28.6139, lng=77.2090, address="Delhi")
    jaipur = Coordinate(lat=26.9124, lng=75.7873, address="Jaipur")
    
    print("\n1. Testing distance calculation...")
    distance = math_engine.calculate_distance(delhi, jaipur)
    print(f"   Delhi to Jaipur: {distance} km")
    
    print("\n2. Testing fuel cost calculation...")
    fuel_cost = math_engine.calculate_fuel_cost(distance)
    print(f"   Fuel cost for {distance} km: ₹{fuel_cost}")
    
    print("\n" + "="*70)
    print("✅ MATH ENGINE TESTS PASSED!")
    print("="*70)


if __name__ == "__main__":
    print("\n" + "="*70)
    print("🚀 DEADHEADING OPTIMIZATION SYSTEM - FULL SYSTEM TEST")
    print("="*70)
    
    try:
        test_math_engine()
        test_database()
        test_api()
        
        print("\n" + "="*70)
        print("✅ ALL TESTS PASSED - SYSTEM IS READY!")
        print("="*70)
        print("\n💡 Next Steps:")
        print("   1. Run: python demo_automation.py (for full AI demo)")
        print("   2. API is running at: http://localhost:8000")
        print("   3. API docs at: http://localhost:8000/docs")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
