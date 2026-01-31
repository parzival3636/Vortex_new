# 📦 Vendor Guide - Adding Loads to the System

This guide explains how vendors can add their loads to the system using **real GPS coordinates from OpenStreetMap**.

---

## 🌍 GPS Coordinates - How It Works

### Current System Uses:

1. **OpenStreetMap (OSM)** - Free, open-source mapping service
2. **Nominatim API** - Geocoding service (address → GPS coordinates)
3. **OSRM** - Optional routing for accurate road distances

### No External GPS Device Needed!

Vendors just enter addresses like:
- "Azadpur Mandi, Delhi"
- "Vashi APMC, Mumbai"
- "Jaipur, Rajasthan"

The system automatically converts these to GPS coordinates using OpenStreetMap.

---

## 🚀 Method 1: Using Python Scripts (Easiest)

### Option A: Interactive Mode

```bash
python add_vendor_osm.py
```

Follow the prompts:
1. Enter vendor name, email, phone
2. Enter address (e.g., "Azadpur Mandi, Delhi")
3. System finds GPS coordinates automatically
4. Confirm the location
5. Add load details (weight, destination, price)

**Example:**
```
Vendor Name: Azadpur Fruits Co.
Vendor Email: fruits@azadpur.com
Vendor Phone: +91-9876543210
Vendor Address: Azadpur Mandi, Delhi

🔍 Finding GPS coordinates for: Azadpur Mandi, Delhi
✅ Found location:
   Address: Azadpur Mandi, Delhi, India
   GPS: 28.7041, 77.1025

Load weight (kg): 5000
Destination address: Jaipur, Rajasthan
Price offered (₹): 12000

✅ Load created!
```

### Option B: Search Mode

```bash
python add_vendor_osm.py search
```

Search for a place first, then add vendor:
1. Search for "market yard mumbai"
2. Select from results
3. Add vendor details
4. Add load

### Option C: Test Geocoding

```bash
python add_vendor_osm.py test
```

Tests OpenStreetMap integration to verify it's working.

---

## 🌐 Method 2: Using API Endpoints (For Frontend Integration)

### Step 1: Register Vendor

**POST** `/api/v1/vendors/register`

```json
{
  "name": "Azadpur Fruits Co.",
  "email": "fruits@azadpur.com",
  "phone": "+91-9876543210",
  "address": "Azadpur Mandi, Delhi"
}
```

**Response:**
```json
{
  "vendor_id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "Azadpur Fruits Co.",
  "email": "fruits@azadpur.com",
  "phone": "+91-9876543210",
  "location_lat": 28.7041,
  "location_lng": 77.1025,
  "address": "Azadpur Mandi, Delhi, India"
}
```

### Step 2: Create Load (Using Addresses)

**POST** `/api/v1/vendors/loads/by-address`

```json
{
  "vendor_id": "123e4567-e89b-12d3-a456-426614174000",
  "weight_kg": 5000,
  "pickup_address": "Azadpur Mandi, Delhi",
  "destination_address": "Jaipur, Rajasthan",
  "price_offered": 12000,
  "currency": "INR"
}
```

**Response:**
```json
{
  "message": "Load created successfully",
  "load_id": "456e7890-e89b-12d3-a456-426614174001",
  "pickup": {
    "address": "Azadpur Mandi, Delhi, India",
    "gps": "28.7041, 77.1025"
  },
  "destination": {
    "address": "Jaipur, Rajasthan, India",
    "gps": "26.9124, 75.7873"
  }
}
```

### Helper Endpoints

#### Search Places (For Autocomplete)

**GET** `/api/v1/vendors/geocode/search?query=market%20yard%20mumbai&limit=5`

```json
{
  "query": "market yard mumbai",
  "count": 5,
  "results": [
    {
      "address": "Vashi APMC Market, Navi Mumbai, Maharashtra, India",
      "lat": 19.0760,
      "lng": 72.8777
    },
    ...
  ]
}
```

#### Convert Address to GPS

**GET** `/api/v1/vendors/geocode/address?address=Azadpur%20Mandi,%20Delhi`

```json
{
  "input_address": "Azadpur Mandi, Delhi",
  "found_address": "Azadpur Mandi, Delhi, India",
  "lat": 28.7041,
  "lng": 77.1025
}
```

#### Convert GPS to Address

**GET** `/api/v1/vendors/geocode/reverse?lat=28.6139&lng=77.2090`

```json
{
  "lat": 28.6139,
  "lng": 77.2090,
  "address": "Connaught Place, New Delhi, Delhi, India"
}
```

---

## 🧪 Testing the System

### 1. Test Geocoding

```bash
python add_vendor_osm.py test
```

This will test:
- Address → GPS conversion
- GPS → Address conversion
- Place search

### 2. Add Test Vendor

```bash
python add_vendor_osm.py
```

Enter test data:
- Name: Test Vendor
- Email: test@example.com
- Phone: +91-9999999999
- Address: Azadpur Mandi, Delhi

### 3. Verify in Database

```bash
python -c "from db_chromadb import db; loads = db.get_available_loads(); print(f'Found {len(loads)} loads')"
```

### 4. Test API

Start the server:
```bash
python main.py
```

Visit: http://localhost:8000/docs

Try the `/api/v1/vendors/geocode/search` endpoint.

---

## 📱 Frontend Integration Example

### React/JavaScript Example

```javascript
// Search for places (autocomplete)
async function searchPlaces(query) {
  const response = await fetch(
    `http://localhost:8000/api/v1/vendors/geocode/search?query=${encodeURIComponent(query)}`
  );
  const data = await response.json();
  return data.results;
}

// Register vendor
async function registerVendor(vendorData) {
  const response = await fetch(
    'http://localhost:8000/api/v1/vendors/register',
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(vendorData)
    }
  );
  return await response.json();
}

// Create load
async function createLoad(loadData) {
  const response = await fetch(
    'http://localhost:8000/api/v1/vendors/loads/by-address',
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(loadData)
    }
  );
  return await response.json();
}

// Usage
const vendor = await registerVendor({
  name: "Azadpur Fruits Co.",
  email: "fruits@azadpur.com",
  phone: "+91-9876543210",
  address: "Azadpur Mandi, Delhi"
});

const load = await createLoad({
  vendor_id: vendor.vendor_id,
  weight_kg: 5000,
  pickup_address: "Azadpur Mandi, Delhi",
  destination_address: "Jaipur, Rajasthan",
  price_offered: 12000,
  currency: "INR"
});
```

---

## 🔧 How GPS Coordinates Are Fetched

### 1. **OpenStreetMap Nominatim API**

When you enter an address like "Azadpur Mandi, Delhi":

1. System sends request to: `https://nominatim.openstreetmap.org/search`
2. OSM searches its database of worldwide locations
3. Returns GPS coordinates: `28.7041, 77.1025`
4. Also returns formatted address: "Azadpur Mandi, Delhi, India"

### 2. **Rate Limiting**

- Nominatim allows 1 request per second (free tier)
- System automatically handles rate limiting
- For production, consider:
  - Self-hosting Nominatim
  - Using paid geocoding service (Google Maps, Mapbox)
  - Caching results

### 3. **Accuracy**

- OSM data is community-maintained
- Generally very accurate for major cities and landmarks
- For best results, use specific addresses:
  - ✅ "Azadpur Mandi, Delhi"
  - ✅ "Vashi APMC Market, Navi Mumbai"
  - ❌ "somewhere in Delhi" (too vague)

---

## 🚗 GPS Tracking for Drivers

### Current Implementation (Simulated)

The `services/gps_simulator.py` simulates GPS tracking:
- Generates intermediate points along a route
- Used for demo purposes

### For Real GPS Tracking

To integrate real GPS from driver's phone:

#### Option 1: Mobile App Integration

```javascript
// In mobile app (React Native / Flutter)
navigator.geolocation.watchPosition(
  (position) => {
    const { latitude, longitude } = position.coords;
    
    // Send to backend
    fetch('http://your-api.com/api/v1/trips/update-location', {
      method: 'POST',
      body: JSON.stringify({
        trip_id: currentTripId,
        lat: latitude,
        lng: longitude,
        timestamp: new Date().toISOString()
      })
    });
  },
  (error) => console.error(error),
  { enableHighAccuracy: true, distanceFilter: 100 } // Update every 100m
);
```

#### Option 2: Web Browser Geolocation

```javascript
// In web app
if (navigator.geolocation) {
  navigator.geolocation.getCurrentPosition((position) => {
    const lat = position.coords.latitude;
    const lng = position.coords.longitude;
    
    // Send to backend
    updateDriverLocation(lat, lng);
  });
}
```

#### Option 3: GPS Device Integration

For dedicated GPS devices:
- Use device's API to get coordinates
- Send via HTTP/MQTT to backend
- Store in ChromaDB

---

## 📊 Data Flow

```
Vendor enters address
        ↓
OpenStreetMap Nominatim API
        ↓
GPS Coordinates (lat, lng)
        ↓
Stored in ChromaDB
        ↓
Driver marks deadheading
        ↓
AI Agents fetch available loads
        ↓
Calculate distances using GPS
        ↓
Rank by profitability
        ↓
Show to driver
```

---

## 🎯 Quick Start Commands

```bash
# 1. Test geocoding
python add_vendor_osm.py test

# 2. Add vendor interactively
python add_vendor_osm.py

# 3. Search and add vendor
python add_vendor_osm.py search

# 4. Start API server
python main.py

# 5. View API docs
# Open: http://localhost:8000/docs

# 6. Run demo
python demo_automation.py
```

---

## ❓ FAQ

### Q: Do I need a GPS device?
**A:** No! Just enter addresses. OpenStreetMap converts them to GPS coordinates.

### Q: Is OpenStreetMap free?
**A:** Yes! It's completely free and open-source.

### Q: What if my address isn't found?
**A:** Try:
- More specific address: "Azadpur Mandi, Delhi" instead of "Azadpur"
- Include city and state
- Use landmarks: "Near Red Fort, Delhi"

### Q: Can I use Google Maps instead?
**A:** Yes! Replace `geocoding_service` with Google Maps Geocoding API. You'll need an API key.

### Q: How accurate are the coordinates?
**A:** Very accurate for major cities and landmarks. OSM has detailed data for India.

### Q: Can I manually enter GPS coordinates?
**A:** Yes! Use the original `/api/v1/loads/` endpoint with lat/lng directly.

---

## 🚀 Next Steps

1. **Test the system**: `python add_vendor_osm.py test`
2. **Add a vendor**: `python add_vendor_osm.py`
3. **Start the API**: `python main.py`
4. **Build frontend**: Use the API endpoints
5. **Deploy**: Add to production server

---

**Need help?** Check the API documentation at http://localhost:8000/docs
