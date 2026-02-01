"""
Test script for Daily Financial Report feature
Tests all endpoints to ensure they're working correctly
"""

import requests
from datetime import datetime

BASE_URL = "http://localhost:8000/api/v1"

def test_create_expense():
    """Test creating an expense"""
    print("\n1. Testing POST /financial/expenses...")
    
    expense_data = {
        "driver_id": "test-driver",
        "amount": 250.75,
        "category": "fuel",
        "description": "Fuel refill at highway pump"
    }
    
    response = requests.post(f"{BASE_URL}/financial/expenses", json=expense_data)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 201:
        data = response.json()
        print(f"   ✓ Expense created: {data['expense_id']}")
        return True
    else:
        print(f"   ✗ Failed: {response.text}")
        return False


def test_get_expenses():
    """Test getting daily expenses"""
    print("\n2. Testing GET /financial/expenses/{date}...")
    
    today = datetime.now().strftime("%Y-%m-%d")
    response = requests.get(f"{BASE_URL}/financial/expenses/{today}")
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Total expenses: ₹{data['total_expenses']}")
        print(f"   ✓ Expense count: {len(data['expenses'])}")
        return True
    else:
        print(f"   ✗ Failed: {response.text}")
        return False


def test_generate_report():
    """Test generating a report"""
    print("\n3. Testing POST /financial/reports/generate...")
    
    report_data = {
        "driver_id": "test-driver",
        "date": datetime.now().strftime("%Y-%m-%d")
    }
    
    response = requests.post(f"{BASE_URL}/financial/reports/generate", json=report_data)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 201:
        data = response.json()
        print(f"   ✓ Report generated: {data['report_id']}")
        print(f"   ✓ Total earnings: ₹{data['financial_summary']['total_earnings']}")
        print(f"   ✓ Total expenses: ₹{data['financial_summary']['total_expenses']}")
        print(f"   ✓ Net profit: ₹{data['financial_summary']['net_profit']}")
        return data['report_id']
    else:
        print(f"   ✗ Failed: {response.text}")
        return None


def test_get_report():
    """Test getting a report"""
    print("\n4. Testing GET /financial/reports/{date}...")
    
    today = datetime.now().strftime("%Y-%m-%d")
    response = requests.get(f"{BASE_URL}/financial/reports/{today}")
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Report found: {data['report_id']}")
        return True
    else:
        print(f"   ✗ Failed: {response.text}")
        return False


def test_scheduler_status():
    """Test scheduler status"""
    print("\n5. Testing GET /report-scheduler/status...")
    
    response = requests.get(f"{BASE_URL}/report-scheduler/status")
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Scheduler running: {data['is_running']}")
        if data['is_running']:
            print(f"   ✓ Next run: {data['next_run_time']}")
        return True
    else:
        print(f"   ✗ Failed: {response.text}")
        return False


def test_start_scheduler():
    """Test starting scheduler"""
    print("\n6. Testing POST /report-scheduler/start...")
    
    response = requests.post(f"{BASE_URL}/report-scheduler/start")
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ {data['message']}")
        return True
    else:
        print(f"   ✗ Failed: {response.text}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("Daily Financial Report Feature - API Tests")
    print("=" * 60)
    
    results = []
    
    # Test all endpoints
    results.append(("Create Expense", test_create_expense()))
    results.append(("Get Expenses", test_get_expenses()))
    report_id = test_generate_report()
    results.append(("Generate Report", report_id is not None))
    results.append(("Get Report", test_get_report()))
    results.append(("Scheduler Status", test_scheduler_status()))
    results.append(("Start Scheduler", test_start_scheduler()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Feature is working correctly.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the errors above.")
