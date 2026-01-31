"""Simple scheduler test"""
import requests

BASE_URL = "http://localhost:8000/api/v1"

print("Testing scheduler endpoints...")

# Test 1: Get status
print("\n1. GET /scheduler/status")
try:
    response = requests.get(f"{BASE_URL}/scheduler/status")
    print(f"   Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"   Response: {response.json()}")
    else:
        print(f"   Error: {response.text}")
except Exception as e:
    print(f"   Exception: {e}")

# Test 2: Force run
print("\n2. POST /scheduler/force-run")
try:
    response = requests.post(f"{BASE_URL}/scheduler/force-run")
    print(f"   Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"   Response: {response.json()}")
    else:
        print(f"   Error: {response.text}")
except Exception as e:
    print(f"   Exception: {e}")

# Test 3: Start scheduler
print("\n3. POST /scheduler/start")
try:
    response = requests.post(f"{BASE_URL}/scheduler/start")
    print(f"   Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"   Response: {response.json()}")
    else:
        print(f"   Error: {response.text}")
except Exception as e:
    print(f"   Exception: {e}")
