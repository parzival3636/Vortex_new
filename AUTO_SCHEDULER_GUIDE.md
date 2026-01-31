# AI-Powered Auto-Scheduler 🤖

## Overview

The Auto-Scheduler is an intelligent system that automatically matches optimal loads to drivers every 2 minutes using:
- **Math Engine** for precise profitability calculations
- **AI Agents** (CrewAI + Ollama) for intelligent decision making
- **Automated Assignment** without manual intervention

## How It Works

### Every 2 Minutes:

```
1. Find Active Trips
   ↓
2. Get Available Loads
   ↓
3. For Each Driver:
   ├─ Use AI Load Matcher Agent
   ├─ Use AI Route Optimizer Agent
   ├─ Use AI Financial Analyzer Agent
   ├─ Use Math Engine for calculations
   └─ Find most profitable load
   ↓
4. Auto-Assign Best Load
   ↓
5. Update Database
```

## Features

### ✅ Intelligent Matching
- Uses AI agents to understand route compatibility
- Considers geographic proximity
- Analyzes route deviation
- Filters by maximum acceptable detour

### ✅ Profitability Analysis
- Math Engine calculates exact costs:
  - Fuel cost (distance × consumption × price)
  - Time cost (hours × driver rate)
  - Extra distance
- Calculates net profit
- Computes profitability score (profit per hour)

### ✅ Optimal Selection
- Ranks all compatible loads
- Selects highest profitability score
- Only assigns if profitable (net profit > 0)
- Considers driver's route and preferences

### ✅ Automatic Assignment
- No manual intervention needed
- Instant assignment to driver
- Updates load status to "assigned"
- Links load to trip and driver

## API Endpoints

### Start Scheduler
```bash
POST /api/v1/scheduler/start
```

**Response:**
```json
{
  "message": "Auto-scheduler started",
  "interval_seconds": 120,
  "status": "running"
}
```

### Stop Scheduler
```bash
POST /api/v1/scheduler/stop
```

**Response:**
```json
{
  "message": "Auto-scheduler stopped",
  "status": "stopped"
}
```

### Get Status
```bash
GET /api/v1/scheduler/status
```

**Response:**
```json
{
  "running": true,
  "interval_seconds": 120,
  "total_runs": 45,
  "total_matches": 38,
  "total_assignments": 35,
  "last_run_time": "2026-01-31T14:30:00",
  "last_run_matches": 2
}
```

### Force Run (Testing)
```bash
POST /api/v1/scheduler/force-run
```

Runs scheduler immediately without waiting for interval.

### Get Statistics
```bash
GET /api/v1/scheduler/stats
```

**Response:**
```json
{
  "running": true,
  "interval_seconds": 120,
  "total_runs": 45,
  "total_matches": 38,
  "total_assignments": 35,
  "last_run_time": "2026-01-31T14:30:00",
  "last_run_matches": 2
}
```

## Usage

### Start Auto-Scheduler

```python
import requests

# Start scheduler
response = requests.post('http://localhost:8000/api/v1/scheduler/start')
print(response.json())
# Output: {"message": "Auto-scheduler started", "status": "running"}
```

### Check Status

```python
# Get status
response = requests.get('http://localhost:8000/api/v1/scheduler/status')
status = response.json()

print(f"Running: {status['running']}")
print(f"Total Assignments: {status['total_assignments']}")
```

### Force Immediate Run

```python
# Force run (for testing)
response = requests.post('http://localhost:8000/api/v1/scheduler/force-run')
result = response.json()

print(f"Matches: {result['stats']['last_run_matches']}")
```

### Stop Scheduler

```python
# Stop scheduler
response = requests.post('http://localhost:8000/api/v1/scheduler/stop')
print(response.json())
# Output: {"message": "Auto-scheduler stopped", "status": "stopped"}
```

## Testing

### Run Test Script

```bash
python test_auto_scheduler.py
```

**Test Flow:**
1. Creates demo data (driver, truck)
2. Creates a trip (deadheading driver)
3. Checks available loads
4. Forces scheduler run
5. Verifies auto-assignment
6. Starts continuous scheduler

**Expected Output:**
```
============================================================
  AI-POWERED AUTO-SCHEDULER TEST
============================================================

1. Setting up test data...
✓ Demo data created
  Driver ID: abc123...
  Truck ID: def456...

2. Creating trip (deadheading driver)...
✓ Trip created: ghi789...
  Route: Delhi → Jaipur

3. Checking available loads...
✓ Found 5 available loads

============================================================
  FORCING SCHEDULER RUN (IMMEDIATE)
============================================================

Running AI-powered auto-scheduler...
✓ Scheduler run completed!

Stats:
  Total Runs: 1
  Total Matches: 1
  Total Assignments: 1
  Last Run Matches: 1

============================================================
  VERIFYING AUTO-ASSIGNMENT
============================================================

✅ LOAD AUTO-ASSIGNED!

Load Details:
  Load ID: jkl012...
  Status: assigned
  Weight: 5000kg
  Price: ₹15000
  Assigned to Trip: ghi789...
  Assigned to Driver: abc123...
```

## Architecture

### Components

1. **Auto-Scheduler Service** (`services/auto_scheduler.py`)
   - Background thread running every 2 minutes
   - Orchestrates the entire matching process
   - Manages statistics and state

2. **Math Engine** (`services/math_engine.py`)
   - Calculates distances (Haversine formula)
   - Computes fuel costs
   - Calculates time costs
   - Determines net profit
   - Computes profitability score

3. **AI Agents** (`agents/`)
   - **Load Matcher**: Finds compatible loads
   - **Route Optimizer**: Calculates route metrics
   - **Financial Analyzer**: Analyzes profitability
   - **Coordinator**: Orchestrates all agents

4. **API Layer** (`api/scheduler.py`)
   - REST endpoints for control
   - Status monitoring
   - Statistics reporting

### Data Flow

```
Active Trip
    ↓
Load Matcher Agent
    ↓ (compatible loads)
Route Optimizer Agent
    ↓ (route metrics)
Math Engine
    ↓ (profitability data)
Financial Analyzer Agent
    ↓ (ranked loads)
Auto-Scheduler
    ↓ (best load)
Database Update
    ↓
Driver Notified
```

## Profitability Calculation

### Formula

```python
# 1. Calculate extra distance
extra_distance = (current → pickup) + (pickup → delivery) + 
                 (delivery → home) - (current → home)

# 2. Calculate costs
fuel_cost = extra_distance × fuel_consumption_rate × fuel_price
time_cost = (extra_distance / avg_speed) × driver_hourly_rate

# 3. Calculate profit
net_profit = vendor_offering - fuel_cost - time_cost

# 4. Calculate score
profitability_score = net_profit / time_hours
```

### Example

```
Driver Route: Delhi → Jaipur (direct: 280km)
Load: Pickup in Delhi, Deliver in Jaipur

Extra Distance:
  Delhi → Pickup: 5km
  Pickup → Delivery: 280km
  Delivery → Jaipur: 0km
  Total: 285km
  Direct: 280km
  Extra: 5km

Costs:
  Fuel: 5km × 0.35 L/km × ₹100/L = ₹175
  Time: 0.1 hours × ₹25/hr = ₹2.50
  Total Cost: ₹177.50

Profit:
  Vendor Offering: ₹15,000
  Net Profit: ₹15,000 - ₹177.50 = ₹14,822.50
  
Score:
  Profitability Score: ₹14,822.50 / 0.1 hrs = ₹148,225/hr
  
Decision: ✅ HIGHLY PROFITABLE - AUTO-ASSIGN
```

## Configuration

### Interval

Change scheduling interval in `services/auto_scheduler.py`:

```python
auto_scheduler = AutoScheduler(interval_seconds=120)  # 2 minutes
```

### Math Engine Settings

Configure in `config.py`:

```python
default_fuel_consumption_rate = 0.35  # liters per km
default_fuel_price = 100.0  # INR per liter
default_driver_hourly_rate = 25.0  # INR per hour
average_truck_speed = 50.0  # km/h
max_route_deviation_km = 100.0  # maximum detour
```

## Manual vs Automatic

### Manual Mode (Existing)
- Driver sees available loads
- Driver reviews profitability
- Driver manually accepts load
- Full control and transparency

### Automatic Mode (New)
- System finds optimal load
- System calculates profitability
- System auto-assigns if profitable
- No driver intervention needed

### Both Modes Available
- Manual mode still works
- Automatic mode runs in parallel
- Driver can still manually accept loads
- System prevents double-assignment

## Benefits

### For Drivers
- ✅ No need to search for loads
- ✅ Always get most profitable option
- ✅ Instant assignment
- ✅ Maximize earnings
- ✅ Reduce deadheading

### For Vendors
- ✅ Faster load pickup
- ✅ Automatic driver matching
- ✅ Reduced wait times
- ✅ Better service

### For Fleet Owners
- ✅ Maximize fleet utilization
- ✅ Reduce empty miles
- ✅ Increase revenue
- ✅ Lower costs
- ✅ Better efficiency

## Monitoring

### Real-time Stats

```python
# Get current stats
response = requests.get('http://localhost:8000/api/v1/scheduler/stats')
stats = response.json()

print(f"Total Runs: {stats['total_runs']}")
print(f"Success Rate: {stats['total_assignments'] / stats['total_runs'] * 100}%")
print(f"Average Matches: {stats['total_matches'] / stats['total_runs']}")
```

### Logs

Scheduler logs to console:

```
============================================================
🤖 AUTO-SCHEDULER CYCLE - 2026-01-31 14:30:00
============================================================

📍 Found 3 active trips
📦 Found 12 available loads

🚛 Processing Trip: abc123...
   Driver: def456...
   Route: Delhi → Jaipur
   🤖 Using AI Agents for load matching...
   🧮 Calculating profitability with Math Engine...
   ✅ Optimal load found: ghi789...
      Profit: ₹14,822.50
      Score: 148,225.00
      ✅ Auto-assigned to driver

============================================================
📊 CYCLE SUMMARY
============================================================
Matches Found: 3
Assignments Made: 3
Total Runs: 45
Total Assignments: 42
============================================================
```

## Troubleshooting

### Scheduler Not Running
```python
# Check status
response = requests.get('http://localhost:8000/api/v1/scheduler/status')
if not response.json()['running']:
    # Start it
    requests.post('http://localhost:8000/api/v1/scheduler/start')
```

### No Assignments Made
- Check if there are active trips
- Check if there are available loads
- Verify loads are profitable
- Check max_route_deviation_km setting

### Low Match Rate
- Increase max_route_deviation_km
- Lower fuel_price or driver_hourly_rate
- Check if loads are geographically compatible

## Future Enhancements

### Possible Additions
1. **Priority Levels**: Assign priority to certain loads
2. **Driver Preferences**: Consider driver preferences
3. **Time Windows**: Match loads with delivery deadlines
4. **Multi-Load**: Assign multiple loads to one trip
5. **Predictive**: Predict future load availability

### Advanced Features
```python
# Priority-based assignment
auto_scheduler.set_priority_rules({
    "high_value_loads": True,
    "preferred_vendors": ["vendor1", "vendor2"],
    "max_detour_km": 50
})

# Driver preferences
auto_scheduler.set_driver_preferences(driver_id, {
    "preferred_routes": ["Delhi-Jaipur"],
    "avoid_night_driving": True,
    "min_profit": 10000
})
```

## Summary

✅ **AI-Powered**: Uses CrewAI agents with Ollama LLM  
✅ **Math Engine**: Precise profitability calculations  
✅ **Automatic**: Runs every 2 minutes  
✅ **Intelligent**: Finds optimal matches  
✅ **Profitable**: Only assigns if net profit > 0  
✅ **Efficient**: Reduces deadheading  
✅ **Scalable**: Handles multiple drivers and loads  
✅ **Monitored**: Real-time stats and logs  

Perfect for AI Agentic Hackathon! 🏆
