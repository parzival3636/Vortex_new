# 🚀 How the System Works - Complete Guide

## 📍 GPS Coordinates - How They're Fetched

### **NO GPS DEVICE NEEDED!**

The system uses **OpenStreetMap (OSM)** - a free, open-source mapping service - to convert addresses into GPS coordinates.

### How It Works:

```
Vendor enters: "Azadpur Mandi, Delhi"
        ↓
System sends to OpenStreetMap API
        ↓
OSM returns: lat=28.7041, lng=77.1025
        ↓
Stored in ChromaDB
```

### Which API?

**OpenStreetMap Nominatim API**
- URL: `https://nominatim.openstreetmap.org`
- Free and open-source
- No API key required
- Rate limit: 1 request per second

**Alternative APIs** (if you want to use them):
- Google Maps Geocoding API (requires API key, paid)
- Mapbox Geocoding API (requires API key, free tier available)
- Here Maps API (requires API key)

---

## 📦 How to Add Vendor Data

### Method 1: Using Python Script (Easiest)

```bash
# Interactive mode - asks questions
python add_vendor_osm.py
```

**What happens:**
1. You enter vendor name, email, phone
2. You enter address: "Azadpur Mandi, Delhi"
3. System calls OpenStreetMap API
4. OSM returns GPS coordinates
5. System shows you the location
6. You confirm
7. You add load details (weight, destination, price)
8. System geocodes destination too
9. Everything saved to ChromaDB

**Example session:**
```
Vendor Name: Azadpur Fruits Co.
Vendor Email: fruits@azadpur.com
Vendor Phone: +91-9876543210
Vendor Address: Azadpur Mandi, Delhi

🔍 Finding GPS coordinates for: Azadpur Mandi, Delhi
✅ Found location:
   Address: Azadpur Mandi, Delhi, India
   GPS: 28.7041, 77.1025

Is this correct? (y/n): y

✅ Vendor created with ID: 123e4567-e89b-12d3-a456-426614174000

Add a load for this vendor? (y/n): y

Load weight (kg): 5000
Destination address: Jaipur, Rajasthan

🔍 Finding GPS coordinates for: Jaipur, Rajasthan
✅ Found destination:
   Address: Jaipur, Rajasthan, India
   GPS: 26.9124, 75.7873

Price offered (₹): 12000

✅ Load created with ID: 456e7890-e89b-12d3-a456-426614174001
```

### Method 2: Using API (For Frontend/Mobile App)

**Step 1: Register Vendor**

```bash
curl -X POST http://localhost:8000/api/v1/vendors/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Azadpur Fruits Co.",
    "email": "fruits@azadpur.com",
    "phone": "+91-9876543210",
    "address": "Azadpur Mandi, Delhi"
  }'
```

**Response:**
```json
{
  "vendor_id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "Azadpur Fruits Co.",
  "location_lat": 28.7041,
  "location_lng": 77.1025,
  "address": "Azadpur Mandi, Delhi, India"
}
```

**Step 2: Create Load**

```bash
curl -X POST http://localhost:8000/api/v1/vendors/loads/by-address \
  -H "Content-Type: application/json" \
  -d '{
    "vendor_id": "123e4567-e89b-12d3-a456-426614174000",
    "weight_kg": 5000,
    "pickup_address": "Azadpur Mandi, Delhi",
    "destination_address": "Jaipur, Rajasthan",
    "price_offered": 12000,
    "currency": "INR"
  }'
```

### Method 3: Seed Script (For Testing)

```bash
python seed_chromadb.py
```

This creates sample vendors and loads with real Indian market yards.

---

## 🔄 Complete Data Flow

### 1. Vendor Adds Load

```
Vendor → API/Script → OpenStreetMap → GPS Coordinates → ChromaDB
```

**Example:**
- Vendor enters: "Azadpur Mandi, Delhi"
- OSM returns: `28.7041, 77.1025`
- Saved in ChromaDB with load details

### 2. Driver Marks Deadheading

```
Driver completes delivery → Marks "returning empty" → System activates AI agents
```

### 3. AI Agents Find Loads

```
AI Coordinator
    ↓
Load Matcher Agent → Finds loads within 50km of driver's route
    ↓
Route Optimizer Agent → Calculates distances using GPS coordinates
    ↓
Financial Analyzer Agent → Calculates profit (price - fuel - time)
    ↓
Coordinator → Ranks by profitability score
    ↓
Shows top 5 to driver
```

### 4. Driver Accepts Load

```
Driver sees: "₹16,886 profit for 2384 km detour"
    ↓
Driver accepts
    ↓
System updates load status
    ↓
Driver gets navigation to vendor
    ↓
Picks up load
    ↓
Delivers to destination
    ↓
Earns money instead of driving empty!
```

---

## 🌍 GPS Coordinate Sources

### Current System (No External GPS)

**For Vendors/Loads:**
- Source: OpenStreetMap Nominatim API
- Input: Address string
- Output: GPS coordinates
- Cost: FREE
- Accuracy: Very good for cities and landmarks

**For Driver Tracking (Simulated):**
- Source: `services/gps_simulator.py`
- Generates fake GPS points along route
- Used for demo purposes only

### For Real GPS Tracking (Future)

**Option 1: Mobile Phone GPS**
```javascript
// In driver's mobile app
navigator.geolocation.getCurrentPosition((position) => {
  const lat = position.coords.latitude;
  const lng = position.coords.longitude;
  
  // Send to backend
  fetch('http://api.com/api/v1/trips/update-location', {
    method: 'POST',
    body: JSON.stringify({ trip_id, lat, lng })
  });
});
```

**Option 2: GPS Device**
- Use device API to get coordinates
- Send via HTTP to backend
- Update trip location in real-time

**Option 3: Vehicle Telematics**
- Integrate with truck's built-in GPS
- Use OBD-II adapter
- Stream data to backend

---

## 🗄️ How Data is Stored in ChromaDB

### ChromaDB Structure

```
./chroma_data/
├── owners/          # Truck owners
├── drivers/         # Truck drivers
├── vendors/         # Market yard vendors
├── trucks/          # Truck details
├── trips/           # Trip records
└── loads/           # Available loads
```

### Example Load Record

```json
{
  "load_id": "456e7890-e89b-12d3-a456-426614174001",
  "vendor_id": "123e4567-e89b-12d3-a456-426614174000",
  "weight_kg": 5000,
  "pickup_lat": 28.7041,
  "pickup_lng": 77.1025,
  "pickup_address": "Azadpur Mandi, Delhi, India",
  "destination_lat": 26.9124,
  "destination_lng": 75.7873,
  "destination_address": "Jaipur, Rajasthan, India",
  "price_offered": 12000,
  "currency": "INR",
  "status": "available",
  "created_at": "2026-01-31T10:30:00"
}
```

### How Backend Fetches Data

```python
from db_chromadb import db

# Get all available loads
loads = db.get_available_loads()

# Each load has GPS coordinates
for load in loads:
    print(f"Pickup: {load['pickup_lat']}, {load['pickup_lng']}")
    print(f"Destination: {load['destination_lat']}, {load['destination_lng']}")
```

---

## 🧮 Distance Calculation

### Using GPS Coordinates

```python
from services.math_engine import math_engine
from models.domain import Coordinate

# Define locations
delhi = Coordinate(lat=28.6139, lng=77.2090, address="Delhi")
jaipur = Coordinate(lat=26.9124, lng=75.7873, address="Jaipur")

# Calculate distance
distance = math_engine.calculate_distance(delhi, jaipur)
# Returns: 305.88 km
```

### Formula Used

**Haversine Formula** (calculates distance between two GPS points):
```
a = sin²(Δlat/2) + cos(lat1) × cos(lat2) × sin²(Δlon/2)
c = 2 × atan2(√a, √(1−a))
distance = R × c

Where:
- R = Earth's radius (6371 km)
- Δlat = lat2 - lat1
- Δlon = lon2 - lon1
```

Then multiply by 1.3 for road adjustment (straight line × 1.3 ≈ actual road distance).

---

## 🚀 Quick Start Commands

### 1. Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Seed database with sample data
python seed_chromadb.py
```

### 2. Add Vendor (Interactive)

```bash
python add_vendor_osm.py
```

### 3. Test Geocoding

```bash
python add_vendor_osm.py test
```

### 4. Start Backend

```bash
python main.py
```

Backend runs at: http://localhost:8000

### 5. Test API

```bash
# Test geocoding
curl "http://localhost:8000/api/v1/vendors/geocode/address?address=Azadpur%20Mandi,%20Delhi"

# Search places
curl "http://localhost:8000/api/v1/vendors/geocode/search?query=market%20yard%20mumbai"
```

### 6. Run Demo

```bash
python demo_automation.py
```

Shows full AI workflow with GPS tracking simulation.

---

## 📱 Frontend Integration

### HTML Form Example

```html
<form id="vendorForm">
  <input type="text" id="vendorName" placeholder="Vendor Name" required>
  <input type="email" id="vendorEmail" placeholder="Email" required>
  <input type="tel" id="vendorPhone" placeholder="Phone" required>
  <input type="text" id="vendorAddress" placeholder="Address" required>
  
  <input type="number" id="loadWeight" placeholder="Weight (kg)" required>
  <input type="text" id="destination" placeholder="Destination" required>
  <input type="number" id="price" placeholder="Price (₹)" required>
  
  <button type="submit">Add Vendor & Load</button>
</form>

<script>
document.getElementById('vendorForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  
  // Register vendor
  const vendorResponse = await fetch('http://localhost:8000/api/v1/vendors/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      name: document.getElementById('vendorName').value,
      email: document.getElementById('vendorEmail').value,
      phone: document.getElementById('vendorPhone').value,
      address: document.getElementById('vendorAddress').value
    })
  });
  
  const vendor = await vendorResponse.json();
  
  // Create load
  const loadResponse = await fetch('http://localhost:8000/api/v1/vendors/loads/by-address', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      vendor_id: vendor.vendor_id,
      weight_kg: parseFloat(document.getElementById('loadWeight').value),
      pickup_address: document.getElementById('vendorAddress').value,
      destination_address: document.getElementById('destination').value,
      price_offered: parseFloat(document.getElementById('price').value),
      currency: 'INR'
    })
  });
  
  const load = await loadResponse.json();
  alert('Load created successfully! ID: ' + load.load_id);
});
</script>
```

---

## 🔍 Troubleshooting

### "Could not find GPS coordinates"

**Problem:** OpenStreetMap can't find the address.

**Solutions:**
1. Be more specific: "Azadpur Mandi, Delhi" not just "Azadpur"
2. Include city and state
3. Use landmarks: "Near Red Fort, Delhi"
4. Try searching first: `python add_vendor_osm.py search`

### "Rate limit exceeded"

**Problem:** Too many requests to OpenStreetMap (max 1/second).

**Solutions:**
1. System automatically handles this
2. Wait 1 second between requests
3. For production, self-host Nominatim
4. Use paid geocoding service

### "No loads found"

**Problem:** Database is empty.

**Solution:**
```bash
python seed_chromadb.py
```

---

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    VENDOR PORTAL                        │
│  (Web/Mobile App - Enter Address, Not GPS)             │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│              OPENSTREETMAP API                          │
│  (Converts Address → GPS Coordinates)                   │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│                 FASTAPI BACKEND                         │
│  - Vendor Registration                                  │
│  - Load Creation                                        │
│  - Geocoding Endpoints                                  │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│              CHROMADB (Embedded)                        │
│  Stores: Vendors, Loads, Trips, GPS Coordinates         │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│                  AI AGENTS                              │
│  - Load Matcher (finds compatible loads)                │
│  - Route Optimizer (calculates distances)               │
│  - Financial Analyzer (calculates profit)               │
│  - Coordinator (ranks opportunities)                    │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│                 DRIVER PORTAL                           │
│  (Shows ranked load opportunities with profit)          │
└─────────────────────────────────────────────────────────┘
```

---

## ✅ Summary

### GPS Coordinates:
- **Source**: OpenStreetMap Nominatim API (FREE)
- **Input**: Address string
- **Output**: Latitude, Longitude
- **No GPS device needed!**

### Adding Vendor Data:
- **Method 1**: `python add_vendor_osm.py` (interactive)
- **Method 2**: API endpoint `/api/v1/vendors/register`
- **Method 3**: `python seed_chromadb.py` (sample data)

### Backend Fetches Data:
- From ChromaDB: `db.get_available_loads()`
- Each load has GPS coordinates
- AI agents use coordinates to calculate distances
- Math engine calculates profitability

### Complete Flow:
1. Vendor enters address
2. OSM converts to GPS
3. Saved in ChromaDB
4. Driver marks deadheading
5. AI finds loads using GPS
6. Calculates profit
7. Shows to driver
8. Driver accepts
9. Earns money!

---

**Need more help?** Check:
- `VENDOR_GUIDE.md` - Detailed vendor instructions
- `API_DOCUMENTATION.md` - All API endpoints
- `SYSTEM_STATUS.md` - System overview
- http://localhost:8000/docs - Interactive API docs
