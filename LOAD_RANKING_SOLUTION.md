# Load Ranking Solution - Pickup Proximity Priority

## Problem
Backend ranked Noida load higher than Mumbai load for Pune→Delhi driver because it used "profit per hour" (shorter detour = higher score). But Noida pickup is 1,170km from Pune while Mumbai is only 120km away!

## Solution
New frontend sorting algorithm prioritizes **pickup proximity to driver start** (50% weight).

### Scoring Formula
1. **Pickup Proximity (50%)**: `max(0, 100 - distance_to_pickup/10)` - Closer is better
2. **Absolute Profit (30%)**: `min(100, net_profit/150)` - Higher profit is better  
3. **Payment Amount (15%)**: `min(100, payment/150)` - Higher payment is better
4. **Fuel Efficiency (5%)**: `max(0, 100 - fuel_cost/30)` - Lower fuel is better

## Results
**Pune→Delhi Driver:**
- Mumbai→Delhi: Score 84.65 (120km to pickup) ✅ TOP PICK
- Noida→Delhi: Score 16.94 (1,170km to pickup)

## Testing
```bash
python test_load_ranking.py    # Shows backend issue
node test_frontend_sorting.js  # Shows frontend fix
```

## Implementation
Location: `frontend/src/pages/DriverDashboard.jsx` (lines 290-360)
- Calculates distance from driver start to each load pickup using Haversine formula
- Applies weighted scoring with 50% on pickup proximity
- Sorts loads by score (higher = better)
- Console logs show distance to pickup for debugging

## Status
✅ FIXED - Frontend correctly prioritizes loads with pickup near driver start
