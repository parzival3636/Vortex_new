"""
Test script for Deadheading Optimization System API
Run this after starting the server with: python main.py
"""

import requests
import json

BASE_URL = "http://localhost:8000"


def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"TEST: {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2))
    print(f"{'='*60}\n")


def test_health_check():
    """Test health check endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print_response("Health Check", response)
    return response.status_code == 200


def test_root():
    """Test root endpoint"""
    response = requests.get(f"{BASE_URL}/")
    print_response("Root Endpoint", response)
    return response.status_code == 200


def test_profitability_calculation():
    """Test profitability calculation"""
    payload = {
        "driver_current": {
            "lat": 28.6139,
            "lng": 77.2090,
            "address": "Delhi, India"
        },
        "driver_destination": {
            "lat": 28.7041,
            "lng": 77.1025,
            "address": "Rohini, Delhi"
        },
        "vendor_pickup": {
            "lat": 28.6517,
            "lng": 77.2219,
            "address": "Connaught Place, Delhi"
        },
        "vendor_destination": {
            "lat": 28.6900,
            "lng": 77.1500,
            "address": "Pitampura, Delhi"
        },
        "vendor_offering": 5000
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/calculate/profitability",
        json=payload
    )
    print_response("Profitability Calculation", response)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Extra Distance: {data['extra_distance_km']} km")
        print(f"✅ Fuel Cost: ₹{data['fuel_cost']}")
        print(f"✅ Time Cost: ₹{data['time_cost']}")
        print(f"✅ Net Profit: ₹{data['net_profit']}")
        print(f"✅ Profitability Score: {data['profitability_score']}")
        return True
    return False


def test_long_distance():
    """Test with longer distance (Mumbai to Pune)"""
    payload = {
        "driver_current": {
            "lat": 19.0760,
            "lng": 72.8777,
            "address": "Mumbai, India"
        },
        "driver_destination": {
            "lat": 18.5204,
            "lng": 73.8567,
            "address": "Pune, India"
        },
        "vendor_pickup": {
            "lat": 19.2183,
            "lng": 72.9781,
            "address": "Thane, India"
        },
        "vendor_destination": {
            "lat": 18.6298,
            "lng": 73.7997,
            "address": "Lonavala, India"
        },
        "vendor_offering": 8000
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/calculate/profitability",
        json=payload
    )
    print_response("Long Distance Calculation (Mumbai-Pune)", response)
    return response.status_code == 200


def test_unprofitable_load():
    """Test with a load that should be unprofitable (huge detour)"""
    payload = {
        "driver_current": {
            "lat": 28.6139,
            "lng": 77.2090,
            "address": "Delhi, India"
        },
        "driver_destination": {
            "lat": 28.7041,
            "lng": 77.1025,
            "address": "Rohini, Delhi"
        },
        "vendor_pickup": {
            "lat": 28.4595,
            "lng": 77.0266,
            "address": "Gurgaon, India"
        },
        "vendor_destination": {
            "lat": 28.9845,
            "lng": 77.7064,
            "address": "Meerut, India"
        },
        "vendor_offering": 1000
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/calculate/profitability",
        json=payload
    )
    print_response("Unprofitable Load Test (Large Detour)", response)
    
    if response.status_code == 200:
        data = response.json()
        if data['net_profit'] < 0:
            print(f"✅ Correctly identified as unprofitable: ₹{data['net_profit']}")
        else:
            print(f"⚠️  Expected negative profit but got: ₹{data['net_profit']}")
        return True
    return False


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("DEADHEADING OPTIMIZATION SYSTEM - API TESTS")
    print("="*60)
    
    tests = [
        ("Health Check", test_health_check),
        ("Root Endpoint", test_root),
        ("Profitability Calculation", test_profitability_calculation),
        ("Long Distance Test", test_long_distance),
        ("Unprofitable Load Test", test_unprofitable_load),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ ERROR in {name}: {str(e)}\n")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {name}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\nTotal: {passed}/{total} tests passed")
    print("="*60 + "\n")


if __name__ == "__main__":
    try:
        run_all_tests()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to server!")
        print("Make sure the server is running: python main.py")
        print("Server should be at: http://localhost:8000\n")
