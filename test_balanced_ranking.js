// Test balanced ranking: Distance (60%) + Payment (40%)
// Example: Driver in Pune, loads in Mumbai and Surat

const originCoords = { lat: 18.5204, lng: 73.8567 }; // Pune

// Load 1: Mumbai (closer, lower payment)
const load1 = {
  pickup_location: { lat: 19.0760, lng: 72.8777, address: 'Mumbai, Maharashtra' },
  destination: { lat: 28.6139, lng: 77.2090, address: 'Delhi, Delhi' },
  price_offered: 10000,
  profitability: { net_profit: 9500 }
};

// Load 2: Surat (farther, higher payment)
const load2 = {
  pickup_location: { lat: 21.1702, lng: 72.8311, address: 'Surat, Gujarat' },
  destination: { lat: 28.6139, lng: 77.2090, address: 'Delhi, Delhi' },
  price_offered: 15000,
  profitability: { net_profit: 14200 }
};

// Load 3: Jaipur (very far, medium payment)
const load3 = {
  pickup_location: { lat: 26.9124, lng: 75.7873, address: 'Jaipur, Rajasthan' },
  destination: { lat: 28.6139, lng: 77.2090, address: 'Delhi, Delhi' },
  price_offered: 12000,
  profitability: { net_profit: 11000 }
};

function calculateDistance(load) {
  const lat1 = originCoords.lat;
  const lon1 = originCoords.lng;
  const lat2 = load.pickup_location.lat;
  const lon2 = load.pickup_location.lng;
  
  const R = 6371;
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
           Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
           Math.sin(dLon/2) * Math.sin(dLon/2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  return R * c;
}

function calculateScore(load, distance) {
  // Distance score (60%) - 0km = 100, 500km = 0
  const distanceScore = Math.max(0, 100 - (distance / 5));
  
  // Payment score (40%) - ₹20,000 = 100
  const paymentScore = Math.min(100, (load.price_offered / 200));
  
  return (distanceScore * 0.6) + (paymentScore * 0.4);
}

const loads = [
  { name: 'Mumbai', load: load1 },
  { name: 'Surat', load: load2 },
  { name: 'Jaipur', load: load3 }
];

console.log('='.repeat(70));
console.log('BALANCED RANKING TEST: Distance (60%) + Payment (40%)');
console.log('='.repeat(70));
console.log(`\nDriver Start: Pune\n`);

const results = loads.map(({ name, load }) => {
  const distance = calculateDistance(load);
  const distScore = Math.max(0, 100 - (distance / 5));
  const paymentScore = Math.min(100, (load.price_offered / 200));
  const totalScore = calculateScore(load, distance);
  
  return {
    name,
    distance: Math.round(distance),
    payment: load.price_offered,
    distScore: distScore.toFixed(1),
    paymentScore: paymentScore.toFixed(1),
    totalScore: totalScore.toFixed(1)
  };
});

// Sort by total score
results.sort((a, b) => b.totalScore - a.totalScore);

results.forEach((r, i) => {
  console.log(`${i === 0 ? '⭐ ' : ''}#${i + 1} ${r.name} ${i === 0 ? '(TOP PICK)' : ''}`);
  console.log(`   📏 Distance to Pickup: ${r.distance}km`);
  console.log(`   💰 Payment: ₹${r.payment.toLocaleString()}`);
  console.log(`   📊 Distance Score (60%): ${r.distScore}`);
  console.log(`   📊 Payment Score (40%): ${r.paymentScore}`);
  console.log(`   ⭐ TOTAL SCORE: ${r.totalScore}`);
  console.log('');
});

console.log('='.repeat(70));
console.log('EXPLANATION:');
console.log('='.repeat(70));
console.log('The algorithm balances distance and payment:');
console.log('- If Mumbai is closer AND has good payment → Mumbai wins');
console.log('- If Surat is farther BUT has much higher payment → Surat can win');
console.log('- The 60/40 split ensures both factors matter');
console.log('='.repeat(70));
