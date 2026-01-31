# Final Load Ranking Algorithm

## Simple Rule
**Score = Distance to Pickup (60%) + Payment (40%)**

## How It Works

### 1. Distance Score (60% weight)
- Measures: Distance from **driver start** to **load pickup**
- Formula: `max(0, 100 - distance/5)`
- 0km = 100 points, 500km = 0 points
- Closer pickup = Higher score

### 2. Payment Score (40% weight)
- Measures: Payment offered by vendor
- Formula: `min(100, payment/200)`
- ₹20,000 = 100 points
- Higher payment = Higher score

### 3. Total Score
- `Total = (Distance Score × 0.6) + (Payment Score × 0.4)`
- Higher total = Better load

## Examples

### Example 1: Mumbai vs Surat (from Pune)

**Mumbai Load:**
- Distance: 120km → Distance Score: 76.0
- Payment: ₹10,000 → Payment Score: 50.0
- **Total: 65.6** ⭐ TOP PICK

**Surat Load:**
- Distance: 314km → Distance Score: 37.3
- Payment: ₹15,000 → Payment Score: 75.0
- **Total: 52.4**

**Winner: Mumbai** (closer distance wins despite lower payment)

### Example 2: When Higher Payment Wins

**Mumbai Load:**
- Distance: 120km → Distance Score: 76.0
- Payment: ₹8,000 → Payment Score: 40.0
- **Total: 61.6**

**Surat Load:**
- Distance: 200km → Distance Score: 60.0
- Payment: ₹18,000 → Payment Score: 90.0
- **Total: 72.0** ⭐ TOP PICK

**Winner: Surat** (much higher payment compensates for distance)

## Key Points

1. **Compares driver START to load PICKUP** (not destination!)
2. **Balances distance and payment** (60/40 split)
3. **Closer loads preferred** but higher payment can win
4. **Fair algorithm** that considers both factors

## Implementation

Location: `frontend/src/pages/DriverDashboard.jsx`

```javascript
const calculateScore = (load, distToPickup) => {
  // Distance score (60%)
  const distanceScore = Math.max(0, 100 - (distToPickup / 5));
  
  // Payment score (40%)
  const paymentScore = Math.min(100, (load.price_offered / 200));
  
  return (distanceScore * 0.6) + (paymentScore * 0.4);
};
```

## Testing

```bash
node test_balanced_ranking.js  # Test with 3 loads
node test_surat_wins.js        # Test payment vs distance
```

## Status

✅ **WORKING** - Balances distance to pickup (60%) with payment amount (40%)
