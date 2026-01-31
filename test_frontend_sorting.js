// Test frontend sorting algorithm for load ranking
// This simulates the sorting logic in DriverDashboard.jsx

// Driver location: Pune
const originCoords = { lat: 18.5204, lng: 73.8567 };

// Load 1: Mumbai → Delhi (should be TOP PICK)
const load1 = {
  load_id: 'load1',
  pickup_location: { lat: 19.0760, lng: 72.8777, address: 'Mumbai, Maharashtra' },
  destination: { lat: 28.6139, lng: 77.2090, address: 'Delhi, Delhi' },
  price_offered: 12000,
  weight_kg: 5000,
  profitability: {
    extra_distance_km: 123.83,
    fuel_cost: 65.01,
    net_profit: 11883.49,
    profitability_score: 5768.6845
  }
};

// Load 2: Noida → Delhi (should be lower ranked)
const load2 = {
  load_id: 'load2',
  pickup_location: { lat: 28.5355, lng: 77.3910, address: 'Noida, Uttar Pradesh' },
  destination: { lat: 28.6139, lng: 77.2090, address: 'Delhi, Delhi' },
  price_offered: 4000,
  weight_kg: 2000,
  profitability: {
    extra_distance_km: 22.16,
    fuel_cost: 11.63,
    net_profit: 3979.12,
    profitability_score: 10754.3784
  }
};

// Calculate distance from driver start to load pickup (Haversine formula)
function calculatePickupDistance(load) {
  const lat1 = originCoords.lat;
  const lon1 = originCoords.lng;
  const lat2 = load.pickup_location.lat;
  const lon2 = load.pickup_location.lng;
  
  const R = 6371; // Earth's radius in km
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
           Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
           Math.sin(dLon/2) * Math.sin(dLon/2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  return R * c;
}

// Calculate weighted score
function calculateScore(load, profit, distanceToPickup) {
  // Pickup proximity score (50% weight) - closer pickup is MUCH better
  const pickupScore = Math.max(0, 100 - (distanceToPickup / 10)); // -10 points per 100km
  
  // Absolute profit score (30% weight) - higher profit is better
  const profitScore = Math.min(100, (profit.net_profit / 150)); // Scale: ₹15,000 = 100 points
  
  // Payment amount score (15% weight) - higher payment is better
  const paymentScore = Math.min(100, (load.price_offered / 150)); // Scale: ₹15,000 = 100 points
  
  // Fuel efficiency score (5% weight) - lower fuel cost is bonus
  const fuelScore = Math.max(0, 100 - (profit.fuel_cost / 30)); // -3.33 points per ₹100
  
  // Weighted total - PICKUP PROXIMITY IS KING
  return (
    (pickupScore * 0.50) +
    (profitScore * 0.30) +
    (paymentScore * 0.15) +
    (fuelScore * 0.05)
  );
}

// Calculate distances and scores
const distToPickup1 = calculatePickupDistance(load1);
const distToPickup2 = calculatePickupDistance(load2);

const score1 = calculateScore(load1, load1.profitability, distToPickup1);
const score2 = calculateScore(load2, load2.profitability, distToPickup2);

console.log('='.repeat(60));
console.log('FRONTEND SORTING ALGORITHM TEST');
console.log('='.repeat(60));
console.log(`\nDriver Location: Pune (${originCoords.lat}, ${originCoords.lng})`);
console.log();

console.log('LOAD 1: Mumbai → Delhi');
console.log('-'.repeat(40));
console.log(`Pickup: ${load1.pickup_location.address}`);
console.log(`Distance to Pickup: ${distToPickup1.toFixed(2)} km`);
console.log(`Payment: ₹${load1.price_offered.toLocaleString()}`);
console.log(`Net Profit: ₹${load1.profitability.net_profit.toLocaleString()}`);
console.log(`Backend Score: ${load1.profitability.profitability_score.toFixed(2)}`);
console.log();
console.log('Score Breakdown:');
console.log(`  Pickup Proximity (50%): ${(Math.max(0, 100 - (distToPickup1 / 10)) * 0.50).toFixed(2)}`);
console.log(`  Absolute Profit (30%):  ${(Math.min(100, (load1.profitability.net_profit / 150)) * 0.30).toFixed(2)}`);
console.log(`  Payment Amount (15%):   ${(Math.min(100, (load1.price_offered / 150)) * 0.15).toFixed(2)}`);
console.log(`  Fuel Efficiency (5%):   ${(Math.max(0, 100 - (load1.profitability.fuel_cost / 30)) * 0.05).toFixed(2)}`);
console.log(`  TOTAL FRONTEND SCORE:   ${score1.toFixed(2)}`);
console.log();

console.log('LOAD 2: Noida → Delhi');
console.log('-'.repeat(40));
console.log(`Pickup: ${load2.pickup_location.address}`);
console.log(`Distance to Pickup: ${distToPickup2.toFixed(2)} km`);
console.log(`Payment: ₹${load2.price_offered.toLocaleString()}`);
console.log(`Net Profit: ₹${load2.profitability.net_profit.toLocaleString()}`);
console.log(`Backend Score: ${load2.profitability.profitability_score.toFixed(2)}`);
console.log();
console.log('Score Breakdown:');
console.log(`  Pickup Proximity (50%): ${(Math.max(0, 100 - (distToPickup2 / 10)) * 0.50).toFixed(2)}`);
console.log(`  Absolute Profit (30%):  ${(Math.min(100, (load2.profitability.net_profit / 150)) * 0.30).toFixed(2)}`);
console.log(`  Payment Amount (15%):   ${(Math.min(100, (load2.price_offered / 150)) * 0.15).toFixed(2)}`);
console.log(`  Fuel Efficiency (5%):   ${(Math.max(0, 100 - (load2.profitability.fuel_cost / 30)) * 0.05).toFixed(2)}`);
console.log(`  TOTAL FRONTEND SCORE:   ${score2.toFixed(2)}`);
console.log();

console.log('='.repeat(60));
console.log('COMPARISON');
console.log('='.repeat(60));
console.log(`\nLoad 1 (Mumbai) Frontend Score: ${score1.toFixed(2)}`);
console.log(`Load 2 (Noida) Frontend Score:  ${score2.toFixed(2)}`);
console.log();

if (score1 > score2) {
  console.log('✅ CORRECT: Mumbai load ranks HIGHER (as expected)');
  console.log(`   Mumbai pickup is ${distToPickup1.toFixed(0)}km from Pune`);
  console.log(`   Noida pickup is ${distToPickup2.toFixed(0)}km from Pune`);
  console.log(`   Frontend algorithm correctly prioritizes closer pickup!`);
} else {
  console.log('❌ ERROR: Noida load ranks HIGHER (unexpected!)');
  console.log(`   Mumbai pickup is ${distToPickup1.toFixed(0)}km from Pune`);
  console.log(`   Noida pickup is ${distToPickup2.toFixed(0)}km from Pune`);
  console.log(`   Frontend algorithm needs adjustment!`);
}

console.log();
console.log('='.repeat(60));
