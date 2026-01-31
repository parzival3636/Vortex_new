# Testing Guide - Deadheading Optimization System

## Quick Start Testing

### 1. Check if Server is Running

Open your browser and go to:
- **http://localhost:8000** - Should show API info
- **http://localhost:8000/docs** - Interactive API documentation (Swagger UI)
- **http://localhost:8000/health** - Health check endpoint

### 2. Test Using Swagger UI (Easiest Method)

1. Go to **http://localhost:8000/docs**
2. You'll see all available endpoints
3. Click on any endpoint to expand it
4. Click "Try it out"
5. Fill in the request body
6. Click "Execute"
7. See the response below

## Testing Workflow

### Step 1: Create Test Data (Owners, Drivers, Vendors, Trucks)

Since we don't have database seeding yet, you'll need to manually insert test data or skip to testing the Math Engine.

### Step 2: Test Math Engine (No Database Required)

**Endpoint**: `POST /api/v1/calculate/profitability`

**Test Request**:
```json
{
  "driver_current": {
    "lat": 28.6139,
    "lng": 77.2090,
    "address": "Delhi, India"
  },
  "driver_destination": {
    "lat": 28.7041,
    "lng": 77.1025,
    "address": "Rohini, Delhi"
  },
  "vendor_pickup": {
    "lat": 28.6517,
    "lng": 77.2219,
    "address": "Connaught Place, Delhi"
  },
  "vendor_destination": {
    "lat": 28.6900,
    "lng": 77.1500,
    "address": "Pitampura, Delhi"
  },
  "vendor_offering": 5000
}
```

**Expected Response**:
```json
{
  "extra_distance_km": 15.2,
  "fuel_cost": 7.98,
  "time_cost": 6.33,
  "net_profit": 4985.69,
  "profitability_score": 1967.45,
  "estimated_time_hours": 0.25
}
```

### Step 3: Test Using cURL (Command Line)

#### Health Check
```bash
curl http://localhost:8000/health
```

#### Calculate Profitability
```bash
curl -X POST "http://localhost:8000/api/v1/calculate/profitability" \
  -H "Content-Type: application/json" \
  -d '{
    "driver_current": {"lat": 28.6139, "lng": 77.2090},
    "driver_destination": {"lat": 28.7041, "lng": 77.1025},
    "vendor_pickup": {"lat": 28.6517, "lng": 77.2219},
    "vendor_destination": {"lat": 28.6900, "lng": 77.1500},
    "vendor_offering": 5000
  }'
```

### Step 4: Test Using Python Script

Run the test script:
```bash
python test_api.py
```

## Testing Scenarios

### Scenario 1: Short Detour (Profitable)
- Driver going from Point A to Point B
- Vendor load is slightly off route
- Should show positive profit

### Scenario 2: Long Detour (Not Profitable)
- Driver going from Point A to Point B
- Vendor load is far off route
- Should show negative profit or not appear in recommendations

### Scenario 3: Multiple Load Opportunities
- Create multiple vendor loads
- Mark trip as deadheading
- Get ranked load opportunities
- Should return top 5 most profitable

## Testing with Postman

1. Download Postman: https://www.postman.com/downloads/
2. Import the OpenAPI spec from http://localhost:8000/openapi.json
3. All endpoints will be automatically configured
4. Start testing!

## Common Test Coordinates

### Indian Cities
- **Delhi**: 28.6139, 77.2090
- **Mumbai**: 19.0760, 72.8777
- **Bangalore**: 12.9716, 77.5946
- **Chennai**: 13.0827, 80.2707
- **Kolkata**: 22.5726, 88.3639

### US Cities
- **New York**: 40.7128, -74.0060
- **Los Angeles**: 34.0522, -118.2437
- **Chicago**: 41.8781, -87.6298
- **Houston**: 29.7604, -95.3698
- **Phoenix**: 33.4484, -112.0740

## Troubleshooting

### Server won't start
- Check if port 8000 is already in use
- Verify .env file exists and has correct values
- Check if Ollama is running: `curl http://localhost:11434/api/tags`

### Database errors
- The system can run without database for Math Engine testing
- For full testing, set up PostgreSQL and update DATABASE_URL in .env

### AI Agent errors
- Ensure Ollama is running: `ollama serve`
- Verify model is downloaded: `ollama list`
- Check OLLAMA_BASE_URL in .env is correct

## Next Steps

1. Set up PostgreSQL database
2. Run migrations: `alembic upgrade head`
3. Create seed data (owners, drivers, vendors, trucks)
4. Test full workflow: Create trip → Mark deadheading → Get recommendations → Accept load
