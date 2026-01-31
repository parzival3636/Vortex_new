// Test: Can Surat win if payment is much higher?

const originCoords = { lat: 18.5204, lng: 73.8567 }; // Pune

// Load 1: Mumbai (closer, lower payment)
const mumbai = {
  pickup_location: { lat: 19.0760, lng: 72.8777, address: 'Mumbai' },
  price_offered: 10000
};

// Load 2: Surat (farther, MUCH higher payment)
const surat = {
  pickup_location: { lat: 21.1702, lng: 72.8311, address: 'Surat' },
  price_offered: 18000  // Much higher!
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
  const distanceScore = Math.max(0, 100 - (distance / 5));
  const paymentScore = Math.min(100, (load.price_offered / 200));
  return (distanceScore * 0.6) + (paymentScore * 0.4);
}

const distMumbai = calculateDistance(mumbai);
const distSurat = calculateDistance(surat);

const scoreMumbai = calculateScore(mumbai, distMumbai);
const scoreSurat = calculateScore(surat, distSurat);

console.log('TEST: Can Surat win with much higher payment?');
console.log('='.repeat(60));
console.log('\nMumbai:');
console.log(`  Distance: ${Math.round(distMumbai)}km`);
console.log(`  Payment: ₹${mumbai.price_offered.toLocaleString()}`);
console.log(`  Score: ${scoreMumbai.toFixed(1)}`);
console.log('\nSurat:');
console.log(`  Distance: ${Math.round(distSurat)}km`);
console.log(`  Payment: ₹${surat.price_offered.toLocaleString()}`);
console.log(`  Score: ${scoreSurat.toFixed(1)}`);
console.log('\n' + '='.repeat(60));

if (scoreSurat > scoreMumbai) {
  console.log('✅ SURAT WINS! Higher payment compensates for distance');
} else {
  console.log('✅ MUMBAI WINS! Closer distance + decent payment');
}
console.log('='.repeat(60));
