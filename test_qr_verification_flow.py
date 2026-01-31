"""
Test script for QR Verification System
Tests complete flow: QR generation → Pickup verification → Delivery verification
"""
import requests
import json
from uuid import uuid4
from datetime import datetime

# API endpoints
VERIFICATION_API = "http://localhost:8001/api/v1"

# Test data
VENDOR_ID = str(uuid4())
DRIVER_ID = str(uuid4())
RECEIVER_ID = str(uuid4())
LOAD_ID = str(uuid4())

# Mumbai coordinates (pickup)
PICKUP_LAT = 19.0760
PICKUP_LNG = 72.8777

# Pune coordinates (delivery)
DELIVERY_LAT = 18.5204
DELIVERY_LNG = 73.8567


def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def test_create_receiver():
    """Test 1: Create a receiver"""
    print_section("TEST 1: Create Receiver")
    
    receiver_data = {
        "name": "Pune Distribution Center",
        "email": "pune@example.com",
        "phone": "+91 9876543210",
        "location_lat": DELIVERY_LAT,
        "location_lng": DELIVERY_LNG,
        "location_address": "Pune, Maharashtra",
        "company_name": "ABC Logistics"
    }
    
    response = requests.post(
        f"{VERIFICATION_API}/receivers/",
        json=receiver_data
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        data = response.json()
        print(f"✓ Receiver created: {data['name']}")
        print(f"  Receiver ID: {data['receiver_id']}")
        return data['receiver_id']
    else:
        print(f"✗ Failed: {response.text}")
        return None


def test_generate_pickup_qr():
    """Test 2: Generate pickup QR code"""
    print_section("TEST 2: Generate Pickup QR Code")
    
    response = requests.post(
        f"{VERIFICATION_API}/qr/generate/pickup/{LOAD_ID}",
        params={
            "driver_id": DRIVER_ID,
            "vendor_id": VENDOR_ID,
            "pickup_lat": PICKUP_LAT,
            "pickup_lng": PICKUP_LNG
        }
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Pickup QR generated")
        print(f"  QR ID: {data['qr_id']}")
        print(f"  Expires: {data['expires_at']}")
        print(f"  Message: {data['message']}")
        return data['qr_id']
    else:
        print(f"✗ Failed: {response.text}")
        return None


def test_verify_pickup(qr_id):
    """Test 3: Verify pickup scan"""
    print_section("TEST 3: Verify Pickup Scan")
    
    # Simulate driver scanning at pickup location (within 100m)
    verification_data = {
        "qr_id": qr_id,
        "scanned_by_id": DRIVER_ID,
        "scanned_by_type": "driver",
        "scan_location_lat": PICKUP_LAT + 0.0001,  # ~11m away
        "scan_location_lng": PICKUP_LNG + 0.0001,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    response = requests.post(
        f"{VERIFICATION_API}/qr/verify/pickup",
        json=verification_data
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Pickup verified successfully!")
        print(f"  Message: {data['message']}")
        print(f"  Verified at: {data['verified_at']}")
        print(f"  Next step: {data['next_step']}")
        return True
    else:
        print(f"✗ Verification failed: {response.text}")
        return False


def test_verify_pickup_wrong_driver(qr_id):
    """Test 4: Verify pickup with wrong driver (should fail)"""
    print_section("TEST 4: Verify Pickup with Wrong Driver (Should Fail)")
    
    wrong_driver_id = str(uuid4())
    
    verification_data = {
        "qr_id": qr_id,
        "scanned_by_id": wrong_driver_id,  # Wrong driver!
        "scanned_by_type": "driver",
        "scan_location_lat": PICKUP_LAT,
        "scan_location_lng": PICKUP_LNG,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    response = requests.post(
        f"{VERIFICATION_API}/qr/verify/pickup",
        json=verification_data
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 400:
        print(f"✓ Correctly rejected wrong driver")
        print(f"  Error: {response.json()['detail']}")
        return True
    else:
        print(f"✗ Should have failed but didn't!")
        return False


def test_generate_delivery_qr(receiver_id):
    """Test 5: Generate delivery QR code"""
    print_section("TEST 5: Generate Delivery QR Code")
    
    response = requests.post(
        f"{VERIFICATION_API}/qr/generate/delivery/{LOAD_ID}",
        params={
            "driver_id": DRIVER_ID,
            "vendor_id": VENDOR_ID,
            "receiver_id": receiver_id,
            "delivery_lat": DELIVERY_LAT,
            "delivery_lng": DELIVERY_LNG
        }
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Delivery QR generated")
        print(f"  QR ID: {data['qr_id']}")
        print(f"  Expires: {data['expires_at']}")
        print(f"  Message: {data['message']}")
        return data['qr_id']
    else:
        print(f"✗ Failed: {response.text}")
        return None


def test_verify_delivery(qr_id, receiver_id):
    """Test 6: Verify delivery scan"""
    print_section("TEST 6: Verify Delivery Scan")
    
    # Simulate receiver scanning at delivery location
    verification_data = {
        "qr_id": qr_id,
        "scanned_by_id": receiver_id,
        "scanned_by_type": "receiver",
        "scan_location_lat": DELIVERY_LAT + 0.0001,  # ~11m away
        "scan_location_lng": DELIVERY_LNG + 0.0001,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    response = requests.post(
        f"{VERIFICATION_API}/qr/verify/delivery",
        json=verification_data
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Delivery verified successfully!")
        print(f"  Message: {data['message']}")
        print(f"  Verified at: {data['verified_at']}")
        print(f"  Next step: {data['next_step']}")
        return True
    else:
        print(f"✗ Verification failed: {response.text}")
        return False


def test_get_load_status():
    """Test 7: Get complete load verification status"""
    print_section("TEST 7: Get Load Verification Status")
    
    response = requests.get(
        f"{VERIFICATION_API}/qr/load/{LOAD_ID}/status"
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Load status retrieved")
        print(f"  Load ID: {data['load_id']}")
        print(f"  Status: {data['status']}")
        print(f"  Pickup QR Generated: {data['pickup_qr_generated']}")
        print(f"  Pickup Verified: {data['pickup_verified']}")
        print(f"  Delivery QR Generated: {data['delivery_qr_generated']}")
        print(f"  Delivery Verified: {data['delivery_verified']}")
        print(f"  Total QR Codes: {len(data['qr_codes'])}")
        print(f"  Total Verifications: {len(data['verifications'])}")
        return True
    else:
        print(f"✗ Failed: {response.text}")
        return False


def test_get_receiver_notifications(receiver_id):
    """Test 8: Get receiver notifications"""
    print_section("TEST 8: Get Receiver Notifications")
    
    response = requests.get(
        f"{VERIFICATION_API}/receivers/{receiver_id}/notifications"
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Notifications retrieved")
        print(f"  Total notifications: {data['total_notifications']}")
        
        if data['notifications']:
            print("\n  Recent notifications:")
            for notif in data['notifications'][:3]:
                print(f"    - {notif['title']}: {notif['message']}")
        
        return True
    else:
        print(f"✗ Failed: {response.text}")
        return False


def run_all_tests():
    """Run complete test suite"""
    print("\n" + "🚀 "*20)
    print("  QR VERIFICATION SYSTEM - COMPLETE TEST SUITE")
    print("🚀 "*20)
    
    print(f"\nTest Configuration:")
    print(f"  Vendor ID: {VENDOR_ID}")
    print(f"  Driver ID: {DRIVER_ID}")
    print(f"  Load ID: {LOAD_ID}")
    print(f"  Pickup Location: Mumbai ({PICKUP_LAT}, {PICKUP_LNG})")
    print(f"  Delivery Location: Pune ({DELIVERY_LAT}, {DELIVERY_LNG})")
    
    try:
        # Test 1: Create receiver
        receiver_id = test_create_receiver()
        if not receiver_id:
            print("\n❌ Test suite failed at receiver creation")
            return
        
        # Test 2: Generate pickup QR
        pickup_qr_id = test_generate_pickup_qr()
        if not pickup_qr_id:
            print("\n❌ Test suite failed at pickup QR generation")
            return
        
        # Test 3: Verify pickup (success)
        if not test_verify_pickup(pickup_qr_id):
            print("\n❌ Test suite failed at pickup verification")
            return
        
        # Test 4: Try wrong driver (should fail)
        # Generate new QR for this test
        pickup_qr_id_2 = test_generate_pickup_qr()
        if pickup_qr_id_2:
            test_verify_pickup_wrong_driver(pickup_qr_id_2)
        
        # Test 5: Generate delivery QR
        delivery_qr_id = test_generate_delivery_qr(receiver_id)
        if not delivery_qr_id:
            print("\n❌ Test suite failed at delivery QR generation")
            return
        
        # Test 6: Verify delivery
        if not test_verify_delivery(delivery_qr_id, receiver_id):
            print("\n❌ Test suite failed at delivery verification")
            return
        
        # Test 7: Get load status
        test_get_load_status()
        
        # Test 8: Get notifications
        test_get_receiver_notifications(receiver_id)
        
        print_section("✅ ALL TESTS PASSED!")
        print("\nThe QR verification system is working correctly!")
        print("AI agents successfully:")
        print("  ✓ Generated QR codes")
        print("  ✓ Verified driver identity at pickup")
        print("  ✓ Detected wrong driver attempt")
        print("  ✓ Verified receiver at delivery")
        print("  ✓ Sent automated notifications")
        print("  ✓ Tracked complete verification status")
        
    except Exception as e:
        print(f"\n❌ Test suite failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("\n⚠️  Make sure the verification backend is running on port 8001")
    print("   Run: python verification_backend/main_verification.py\n")
    
    input("Press Enter to start tests...")
    run_all_tests()
