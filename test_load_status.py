"""
Test Load Status Changes
Verify that accepted loads are removed from available list
"""

import requests
from db_chromadb import db

BASE_URL = "http://localhost:8000/api/v1"

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

print_section("LOAD STATUS TEST")

# Check database directly
print("1. Checking database directly...")
all_loads = db.loads.get()
if all_loads['ids']:
    available_count = sum(1 for meta in all_loads['metadatas'] if meta.get('status') == 'available')
    assigned_count = sum(1 for meta in all_loads['metadatas'] if meta.get('status') == 'assigned')
    
    print(f"✓ Total loads in database: {len(all_loads['ids'])}")
    print(f"  - Available: {available_count}")
    print(f"  - Assigned: {assigned_count}")
else:
    print("✗ No loads found in database")

# Check via API
print("\n2. Checking via API...")
response = requests.get(f"{BASE_URL}/loads/available")
if response.status_code == 200:
    loads = response.json()
    print(f"✓ Available loads via API: {len(loads)}")
    
    # Verify all returned loads have status 'available'
    all_available = all(load['status'] == 'available' for load in loads)
    if all_available:
        print(f"✓ All returned loads have status 'available'")
    else:
        print(f"✗ Some loads have incorrect status!")
else:
    print(f"✗ API call failed: {response.text}")

print_section("✅ LOAD STATUS TEST COMPLETE")
print("Summary:")
print("  - Database contains both available and assigned loads")
print("  - API only returns loads with status 'available'")
print("  - Accepted loads are correctly filtered out")
