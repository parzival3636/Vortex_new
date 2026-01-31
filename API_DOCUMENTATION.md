# Complete API Documentation

## 📋 All Available APIs

### **1. Health & Info APIs**

#### GET `/`
- **Description**: Root endpoint with API information
- **Response**: API name, version, status, LLM info
- **Test**: `curl http://localhost:8000/`

#### GET `/health`
- **Description**: Health check endpoint
- **Response**: `{"status": "healthy"}`
- **Test**: `curl http://localhost:8000/health`

---

### **2. Trip Management APIs**

#### POST `/api/v1/trips`
- **Description**: Create a new trip
- **Request Body**:
```json
{
  "driver_id": "uuid",
  "truck_id": "uuid",
  "origin": {
    "lat": 28.6139,
    "lng": 77.2090,
    "address": "Delhi, India"
  },
  "destination": {
    "lat": 28.7041,
    "lng": 77.1025,
    "address": "Rohini, Delhi"
  },
  "outbound_load": "Electronics - 5 tons"
}
```
- **Response**: Created trip details with trip_id
- **Use Case**: Driver starts a new delivery trip

#### GET `/api/v1/trips/{trip_id}`
- **Description**: Get trip details by ID
- **Response**: Complete trip information
- **Use Case**: Check trip status

#### PATCH `/api/v1/trips/{trip_id}/deadhead`
- **Description**: Mark trip as deadheading (returning empty)
- **Response**: Updated trip with is_deadheading=true
- **Use Case**: Driver completes delivery and is returning empty
- **🔥 This triggers AI load matching!**

#### PATCH `/api/v1/trips/{trip_id}/pickup`
- **Description**: Confirm load pickup
- **Response**: Pickup confirmation
- **Use Case**: Driver arrives at vendor and picks up load

#### PATCH `/api/v1/trips/{trip_id}/delivery`
- **Description**: Confirm delivery completion
- **Response**: Delivery confirmation, trip marked complete
- **Use Case**: Driver completes load delivery

---

### **3. Load Management APIs**

#### POST `/api/v1/loads`
- **Description**: Create a new load posting (Vendor)
- **Request Body**:
```json
{
  "vendor_id": "uuid",
  "weight_kg": 5000,
  "pickup_location": {
    "lat": 28.6517,
    "lng": 77.2219,
    "address": "Connaught Place, Delhi"
  },
  "destination": {
    "lat": 28.6900,
    "lng": 77.1500,
    "address": "Pitampura, Delhi"
  },
  "price_offered": 5000,
  "currency": "INR"
}
```
- **Response**: Created load with load_id
- **Use Case**: Vendor posts a load that needs transport

#### GET `/api/v1/loads/{load_id}`
- **Description**: Get load details by ID
- **Response**: Complete load information
- **Use Case**: Check load status

#### GET `/api/v1/loads/available`
- **Description**: Get all available loads
- **Response**: List of loads with status="available"
- **Use Case**: See all unassigned loads

#### PATCH `/api/v1/loads/{load_id}/accept`
- **Description**: Accept a load opportunity
- **Query Params**: `trip_id` (UUID)
- **Response**: Load acceptance confirmation
- **Use Case**: Driver accepts a recommended load

#### PATCH `/api/v1/loads/{load_id}/reject`
- **Description**: Reject a load opportunity
- **Response**: Rejection logged
- **Use Case**: Driver declines a load

---

### **4. Calculation & AI APIs** 🤖

#### POST `/api/v1/calculate/profitability`
- **Description**: Calculate profitability for any load opportunity
- **Request Body**:
```json
{
  "driver_current": {
    "lat": 28.6139,
    "lng": 77.2090,
    "address": "Delhi"
  },
  "driver_destination": {
    "lat": 28.7041,
    "lng": 77.1025,
    "address": "Rohini"
  },
  "vendor_pickup": {
    "lat": 28.6517,
    "lng": 77.2219,
    "address": "CP"
  },
  "vendor_destination": {
    "lat": 28.6900,
    "lng": 77.1500,
    "address": "Pitampura"
  },
  "vendor_offering": 5000
}
```
- **Response**:
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
- **Use Case**: Calculate if a load is profitable
- **✅ Works without database!**

#### GET `/api/v1/calculate/opportunities/{trip_id}`
- **Description**: Get AI-ranked load opportunities for a deadheading trip
- **Response**:
```json
{
  "trip_id": "uuid",
  "opportunities": [
    {
      "load_id": "uuid",
      "vendor_name": "ABC Logistics",
      "weight_kg": 5000,
      "pickup_location": {...},
      "destination": {...},
      "price_offered": 5000,
      "calculation": {
        "extra_distance_km": 15.2,
        "fuel_cost": 7.98,
        "time_cost": 6.33,
        "net_profit": 4985.69,
        "profitability_score": 1967.45
      },
      "rank": 1
    }
  ],
  "count": 5
}
```
- **Use Case**: Get top 5 most profitable loads for return journey
- **🤖 Uses AI agents (Load Matcher, Route Optimizer, Financial Analyzer)**

---

## 🔌 What to Integrate

### **1. Frontend Portals (Required)**

#### **Driver Portal** (Mobile/Web App)
- **Login/Auth**: Driver authentication
- **Trip Creation**: Form to create new trip
- **Deadheading Toggle**: Button to mark "returning empty"
- **Load Opportunities**: List of ranked loads with profitability
- **Accept/Reject**: Buttons to accept or reject loads
- **Navigation**: Map showing route to vendor pickup
- **Expense Logging**: Form to log fuel and expenses
- **Photo Upload**: Camera integration for receipts

#### **Vendor Portal** (Web App)
- **Login/Auth**: Vendor authentication
- **Load Posting**: Form to post new loads
- **My Loads**: Dashboard showing all posted loads
- **Driver Assignment**: See which driver accepted load
- **Pickup Confirmation**: Button to confirm driver arrival
- **Rating System**: Rate driver after delivery

#### **Owner Portal** (Web Dashboard)
- **Fleet Overview**: Map showing all trucks
- **Statistics**: Revenue, fuel savings, deadheading reduction
- **Financial Reports**: Daily/weekly/monthly reports
- **Truck Details**: Individual truck performance
- **Expense Verification**: Review driver expenses with photos

### **2. Database (Required for Full System)**

**PostgreSQL Setup**:
```bash
# Install PostgreSQL
# Windows: Download from postgresql.org
# Linux: sudo apt install postgresql
# Mac: brew install postgresql

# Create database
createdb deadheading_db

# Run migrations
alembic upgrade head
```

**Seed Data Script** (Create this):
```python
# seed_data.py
# Create sample owners, drivers, vendors, trucks
```

### **3. Real-time Features (Optional)**

#### **WebSocket for Notifications**
- New load opportunities
- Load claimed by another driver
- Pickup confirmations
- Delivery updates

#### **Redis for Caching**
- Cache load opportunities
- Store WebSocket connections
- Queue offline notifications

### **4. External Integrations (Optional)**

#### **Google Maps API**
- Better distance calculations
- Real-time traffic data
- Turn-by-turn navigation
- Route optimization

#### **Payment Gateway**
- Stripe/Razorpay for payments
- Automatic payment to drivers
- Commission handling

#### **SMS/Email Notifications**
- Twilio for SMS
- SendGrid for emails
- Notify drivers of new loads

#### **Photo Storage**
- AWS S3 / Cloudinary
- Store receipt photos
- Fuel pump photos

---

## 🧪 How to Test Ollama

### **Step 1: Check if Ollama is Running**

```bash
# Check Ollama service
curl http://localhost:11434/api/tags

# Should return list of installed models
```

**Expected Response**:
```json
{
  "models": [
    {
      "name": "llama3.1:8b",
      "modified_at": "2024-01-15T10:30:00Z",
      "size": 4661224448
    }
  ]
}
```

### **Step 2: Test Ollama Directly**

```bash
# Test with a simple prompt
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.1:8b",
  "prompt": "Why is the sky blue?",
  "stream": false
}'
```

### **Step 3: Test Ollama in Your App**

Create a test script:

```python
# test_ollama.py
from langchain_community.llms import Ollama

llm = Ollama(
    base_url="http://localhost:11434",
    model="llama3.1:8b"
)

response = llm.invoke("What is 2+2?")
print(response)
```

Run it:
```bash
python test_ollama.py
```

### **Step 4: Test AI Agents**

The AI agents are used in the `/api/v1/calculate/opportunities/{trip_id}` endpoint.

**Test Flow**:
1. Create a trip
2. Mark it as deadheading
3. Create some vendor loads
4. Call the opportunities endpoint
5. AI agents will:
   - **Load Matcher**: Find compatible loads
   - **Route Optimizer**: Calculate distances
   - **Financial Analyzer**: Compute profitability
   - **Coordinator**: Rank and return top 5

### **Step 5: Monitor Ollama Performance**

```bash
# Check Ollama logs
ollama logs

# Monitor resource usage
# Ollama uses GPU if available, otherwise CPU
# 8B model needs ~8GB RAM
```

---

## 🚀 Complete Testing Workflow

### **Phase 1: Basic Testing (No Database)**
```bash
# 1. Start server
python main.py

# 2. Test health
curl http://localhost:8000/health

# 3. Test profitability calculation
python test_api.py
```

### **Phase 2: Database Testing**
```bash
# 1. Set up PostgreSQL
createdb deadheading_db

# 2. Run migrations
alembic upgrade head

# 3. Create seed data
python seed_data.py  # You need to create this

# 4. Test trip creation
# Use Swagger UI at http://localhost:8000/docs
```

### **Phase 3: AI Agent Testing**
```bash
# 1. Ensure Ollama is running
ollama serve

# 2. Test model
ollama run llama3.1:8b "Hello"

# 3. Create trip and mark deadheading
# 4. Create vendor loads
# 5. Call opportunities endpoint
# 6. Verify AI agents return ranked loads
```

### **Phase 4: Integration Testing**
```bash
# 1. Build frontend portals
# 2. Connect to API
# 3. Test end-to-end workflow
# 4. Test real-time notifications
```

---

## 📊 API Testing Checklist

- [ ] Health check works
- [ ] Profitability calculation works
- [ ] Trip creation works
- [ ] Load posting works
- [ ] Deadheading activation works
- [ ] AI load matching works
- [ ] Load acceptance works
- [ ] Pickup confirmation works
- [ ] Delivery completion works
- [ ] Ollama responds correctly
- [ ] AI agents return ranked results

---

## 🐛 Troubleshooting

### Ollama Not Responding
```bash
# Restart Ollama
ollama serve

# Check if model exists
ollama list

# Pull model if missing
ollama pull llama3.1:8b
```

### Database Connection Error
```bash
# Check PostgreSQL is running
pg_isready

# Update DATABASE_URL in .env
```

### AI Agents Not Working
```bash
# Check OPENAI_API_KEY is set (even if dummy)
echo $OPENAI_API_KEY

# Verify Ollama base URL
curl http://localhost:11434/api/tags
```

---

## 📝 Next Steps

1. **Set up PostgreSQL** and run migrations
2. **Create seed data** script for testing
3. **Build frontend portals** (React/Vue/Flutter)
4. **Integrate Google Maps** for better routing
5. **Add WebSocket** for real-time updates
6. **Deploy** to production (Docker + Cloud)
