"""
Unit tests for Math Engine
Run with: python test_math_engine.py
"""

from services.math_engine import math_engine
from models.domain import Coordinate


def test_distance_calculation():
    """Test distance calculation between two points"""
    print("\n" + "="*60)
    print("TEST: Distance Calculation")
    print("="*60)
    
    # Delhi to Mumbai
    delhi = Coordinate(lat=28.6139, lng=77.2090)
    mumbai = Coordinate(lat=19.0760, lng=72.8777)
    
    distance = math_engine.calculate_distance(delhi, mumbai)
    print(f"Delhi to Mumbai: {distance} km")
    print(f"Expected: ~1150-1200 km (with road adjustment)")
    
    # Should be around 1150-1200 km with road adjustment
    assert 1100 < distance < 1300, f"Distance seems incorrect: {distance}"
    print("✅ PASSED\n")


def test_extra_distance():
    """Test extra distance calculation for detour"""
    print("="*60)
    print("TEST: Extra Distance Calculation")
    print("="*60)
    
    driver_current = Coordinate(lat=28.6139, lng=77.2090)  # Delhi
    driver_dest = Coordinate(lat=28.7041, lng=77.1025)     # Rohini
    vendor_pickup = Coordinate(lat=28.6517, lng=77.2219)   # CP
    vendor_dest = Coordinate(lat=28.6900, lng=77.1500)     # Pitampura
    
    extra_distance = math_engine.calculate_extra_distance(
        driver_current, driver_dest, vendor_pickup, vendor_dest
    )
    
    print(f"Extra distance for detour: {extra_distance} km")
    print(f"This is the additional distance to take the load")
    
    assert extra_distance >= 0, "Extra distance should be positive"
    print("✅ PASSED\n")


def test_fuel_cost():
    """Test fuel cost calculation"""
    print("="*60)
    print("TEST: Fuel Cost Calculation")
    print("="*60)
    
    distance = 100  # km
    fuel_cost = math_engine.calculate_fuel_cost(distance)
    
    print(f"Distance: {distance} km")
    print(f"Fuel consumption rate: {math_engine.fuel_consumption_rate} L/km")
    print(f"Fuel price: ₹{math_engine.fuel_price}/L")
    print(f"Total fuel cost: ₹{fuel_cost}")
    
    expected = distance * 0.35 * 1.50  # 100 * 0.35 * 1.50 = 52.5
    assert abs(fuel_cost - expected) < 0.01, f"Expected {expected}, got {fuel_cost}"
    print("✅ PASSED\n")


def test_time_cost():
    """Test time cost calculation"""
    print("="*60)
    print("TEST: Time Cost Calculation")
    print("="*60)
    
    time_hours = 2.5
    time_cost = math_engine.calculate_time_cost(time_hours)
    
    print(f"Time: {time_hours} hours")
    print(f"Driver hourly rate: ₹{math_engine.driver_hourly_rate}/hour")
    print(f"Total time cost: ₹{time_cost}")
    
    expected = time_hours * 25.0  # 2.5 * 25 = 62.5
    assert abs(time_cost - expected) < 0.01, f"Expected {expected}, got {time_cost}"
    print("✅ PASSED\n")


def test_net_profit():
    """Test net profit calculation"""
    print("="*60)
    print("TEST: Net Profit Calculation")
    print("="*60)
    
    vendor_offering = 5000
    fuel_cost = 500
    time_cost = 300
    
    net_profit = math_engine.calculate_net_profit(vendor_offering, fuel_cost, time_cost)
    
    print(f"Vendor offering: ₹{vendor_offering}")
    print(f"Fuel cost: ₹{fuel_cost}")
    print(f"Time cost: ₹{time_cost}")
    print(f"Net profit: ₹{net_profit}")
    
    expected = 5000 - 500 - 300  # 4200
    assert abs(net_profit - expected) < 0.01, f"Expected {expected}, got {net_profit}"
    print("✅ PASSED\n")


def test_profitability_score():
    """Test profitability score calculation"""
    print("="*60)
    print("TEST: Profitability Score Calculation")
    print("="*60)
    
    net_profit = 4200
    total_time = 3.5
    
    score = math_engine.calculate_profitability_score(net_profit, total_time)
    
    print(f"Net profit: ₹{net_profit}")
    print(f"Total time: {total_time} hours")
    print(f"Profitability score: {score} (profit per hour)")
    
    expected = 4200 / 3.5  # 1200
    assert abs(score - expected) < 0.01, f"Expected {expected}, got {score}"
    print("✅ PASSED\n")


def test_full_profitability():
    """Test complete profitability analysis"""
    print("="*60)
    print("TEST: Full Profitability Analysis")
    print("="*60)
    
    driver_current = Coordinate(lat=28.6139, lng=77.2090)
    driver_dest = Coordinate(lat=28.7041, lng=77.1025)
    vendor_pickup = Coordinate(lat=28.6517, lng=77.2219)
    vendor_dest = Coordinate(lat=28.6900, lng=77.1500)
    vendor_offering = 5000
    
    result = math_engine.calculate_full_profitability(
        driver_current, driver_dest, vendor_pickup, vendor_dest, vendor_offering
    )
    
    print(f"Extra distance: {result['extra_distance_km']} km")
    print(f"Estimated time: {result['estimated_time_hours']} hours")
    print(f"Fuel cost: ₹{result['fuel_cost']}")
    print(f"Time cost: ₹{result['time_cost']}")
    print(f"Net profit: ₹{result['net_profit']}")
    print(f"Profitability score: {result['profitability_score']}")
    
    assert result['net_profit'] > 0, "Should be profitable"
    assert result['profitability_score'] > 0, "Score should be positive"
    print("✅ PASSED\n")


def run_all_tests():
    """Run all math engine tests"""
    print("\n" + "="*60)
    print("MATH ENGINE UNIT TESTS")
    print("="*60)
    
    tests = [
        test_distance_calculation,
        test_extra_distance,
        test_fuel_cost,
        test_time_cost,
        test_net_profit,
        test_profitability_score,
        test_full_profitability,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ FAILED: {str(e)}\n")
            failed += 1
        except Exception as e:
            print(f"❌ ERROR: {str(e)}\n")
            failed += 1
    
    print("="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total: {passed + failed}")
    print("="*60 + "\n")


if __name__ == "__main__":
    run_all_tests()
