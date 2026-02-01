"""
Test Manual Allocation Feature
Quick test to verify all endpoints are working
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_owner_statistics():
    """Test owner statistics endpoint"""
    print("\n1. Testing Owner Statistics...")
    try:
        response = requests.get(f"{BASE_URL}/api/owner/statistics?owner_id=demo-owner-123")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Active Vehicles: {data['totalActiveVehicles']}")
            print(f"   ✓ Pending Loads: {data['totalPendingLoads']}")
            print(f"   ✓ Allocated Loads: {data['totalAllocatedLoads']}")
            print(f"   ✓ Allocation Rate: {data['allocationRate']}%")
        else:
            print(f"   ✗ Error: {response.text}")
    except Exception as e:
        print(f"   ✗ Exception: {e}")

def test_available_vehicles():
    """Test available vehicles endpoint"""
    print("\n2. Testing Available Vehicles...")
    try:
        response = requests.get(f"{BASE_URL}/api/allocations/available-vehicles?owner_id=demo-owner-123")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Found {len(data)} available vehicles")
            if data:
                print(f"   ✓ First vehicle: {data[0]['name']}")
        else:
            print(f"   ✗ Error: {response.text}")
    except Exception as e:
        print(f"   ✗ Exception: {e}")

def test_unallocated_loads():
    """Test unallocated loads endpoint"""
    print("\n3. Testing Unallocated Loads...")
    try:
        response = requests.get(f"{BASE_URL}/api/allocations/unallocated-loads")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Found {len(data)} unallocated loads")
            if data:
                print(f"   ✓ First load pickup: {data[0]['pickupLocation']['address']}")
        else:
            print(f"   ✗ Error: {response.text}")
    except Exception as e:
        print(f"   ✗ Exception: {e}")

def test_driver_allocated_loads():
    """Test driver allocated loads endpoint"""
    print("\n4. Testing Driver Allocated Loads...")
    try:
        response = requests.get(f"{BASE_URL}/api/driver/allocated-loads?driver_id=demo-driver-123")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Total Loads: {data['totalLoads']}")
            print(f"   ✓ Total Distance: {data['totalDistance']}km")
            print(f"   ✓ Total Time: {data['totalTime']}min")
        else:
            print(f"   ✗ Error: {response.text}")
    except Exception as e:
        print(f"   ✗ Exception: {e}")

def test_notifications():
    """Test notifications endpoint"""
    print("\n5. Testing Notifications...")
    try:
        response = requests.get(f"{BASE_URL}/api/notifications?driver_id=demo-driver-123")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Found {len(data)} notifications")
        else:
            print(f"   ✗ Error: {response.text}")
    except Exception as e:
        print(f"   ✗ Exception: {e}")

def test_unread_count():
    """Test unread notification count"""
    print("\n6. Testing Unread Notification Count...")
    try:
        response = requests.get(f"{BASE_URL}/api/notifications/unread-count?driver_id=demo-driver-123")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Unread Count: {data['count']}")
        else:
            print(f"   ✗ Error: {response.text}")
    except Exception as e:
        print(f"   ✗ Exception: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("MANUAL ALLOCATION FEATURE TEST")
    print("=" * 60)
    
    print("\nMake sure the backend is running on http://localhost:8000")
    print("Press Enter to start tests...")
    input()
    
    test_owner_statistics()
    test_available_vehicles()
    test_unallocated_loads()
    test_driver_allocated_loads()
    test_notifications()
    test_unread_count()
    
    print("\n" + "=" * 60)
    print("TESTS COMPLETE")
    print("=" * 60)
    print("\nIf all tests passed, the backend is working correctly!")
    print("Now test the frontend:")
    print("1. Start frontend: cd frontend && npm run dev")
    print("2. Open Owner Dashboard and click 'Manual Allocation' tab")
    print("3. Open Driver Dashboard and click 'Allocated Loads' tab")
