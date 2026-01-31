# System Integration Guide

## Overview

This guide explains how the **Main System** (driver/owner) and **Verification System** (vendor/receiver) work together as separate but integrated platforms.

---

## 🏗️ Two-System Architecture

### System 1: Main Platform (Existing)
**Purpose**: Driver and owner operations, load matching, trip management

**Port**: 8000 (backend), 5173 (frontend)

**Components**:
- Driver Dashboard
- Owner Dashboard  
- Load Matching AI Agents
- Route Optimization
- Trip Management
- ChromaDB for loads/drivers/trucks

**Users**: Drivers, Fleet Owners

---

### System 2: Verification Platform (New)
**Purpose**: QR-based verification, vendor and receiver operations

**Port**: 8001 (backend), 5174 (frontend)

**Components**:
- Vendor Dashboard
- Receiver Dashboard
- Driver QR Scanner
- Verification AI Agent
- Notification AI Agent
- ChromaDB for QR codes/verifications

**Users**: Vendors, Receivers, Drivers (for QR display)

---

## 🔄 Integration Points

### 1. Load Assignment Flow

```
┌─────────────────────────────────────────────────────────────┐
│                      MAIN SYSTEM                             │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ 1. Vendor posts load
                            ↓
                    ┌───────────────┐
                    │  Load Created │
                    │  (Port 8000)  │
                    └───────────────┘
                            │
                            │ 2. Driver accepts/assigned
                            ↓
                    ┌───────────────┐
                    │Load Assigned  │
                    │to Driver      │
                    └───────────────┘
                            │
                            │ 3. Trigger QR generation
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  VERIFICATION SYSTEM                         │
└─────────────────────────────────────────────────────────────┘
                            │
                            ↓
                    ┌───────────────┐
                    │Generate Pickup│
                    │QR Code        │
                    │(Port 8001)    │
                    └───────────────┘
```

### 2. Verification Flow

```
Vendor Dashboard (5174) → Generate QR → Backend (8001)
                                              ↓
                                    Store in ChromaDB
                                              ↓
                                    Notify Driver (AI Agent)
                                              ↓
Driver Scanner (5174) ← Display QR ← Fetch QR Data
                                              ↓
Vendor Scans QR → Verification Agent → Validate
                                              ↓
                                    Update Main System (8000)
                                              ↓
                                    Notify All Parties (AI Agent)
```

---

## 🔗 API Integration

### Main System → Verification System

#### Trigger QR Generation After Assignment

```python
# In main system: api/loads.py
import requests

@router.post("/loads/{load_id}/assign")
def assign_load_to_driver(load_id: UUID, driver_id: UUID):
    # ... existing assignment logic ...
    
    # Get load details
    load = db.get_load(str(load_id))
    
    # Trigger pickup QR generation in verification system
    try:
        response = requests.post(
            f"http://localhost:8001/api/v1/qr/generate/pickup/{load_id}",
            params={
                "driver_id": str(driver_id),
                "vendor_id": load['vendor_id'],
                "pickup_lat": load['pickup_lat'],
                "pickup_lng": load['pickup_lng']
            },
            timeout=5
        )
        
        if response.status_code == 200:
            print(f"✓ Pickup QR generated for load {load_id}")
        else:
            print(f"✗ QR generation failed: {response.text}")
            
    except Exception as e:
        print(f"✗ Error calling verification system: {e}")
        # Continue even if QR generation fails
    
    return {"message": "Load assigned", "load_id": load_id}
```

### Verification System → Main System

#### Update Load Status After Verification

```python
# In verification system: api/qr_verification.py
import requests

@router.post("/verify/pickup")
def verify_pickup(request: QRVerificationRequest):
    # ... verification logic ...
    
    if verification_result["success"]:
        # Update main system
        try:
            response = requests.patch(
                f"http://localhost:8000/api/v1/loads/{qr_data['load_id']}/status",
                json={"status": "picked_up"},
                timeout=5
            )
            
            if response.status_code == 200:
                print(f"✓ Main system updated: load picked up")
                
        except Exception as e:
            print(f"✗ Error updating main system: {e}")
            # Continue even if update fails
    
    return verification_response
```

---

## 📊 Data Synchronization

### Shared Data Elements

Both systems reference the same:
- **Load IDs**: UUID format
- **Driver IDs**: UUID format
- **Vendor IDs**: UUID format
- **Location Data**: Lat/Lng coordinates

### Data Flow

```
Main System (ChromaDB)          Verification System (ChromaDB)
├── loads                       ├── qr_codes
├── drivers                     ├── verifications
├── trucks                      ├── receivers
├── trips                       └── notifications
└── vendors
        ↓                               ↓
    Shared via API calls
        ↓                               ↓
    Load ID, Driver ID, Vendor ID
```

---

## 🚀 Complete User Journey

### Scenario: Mumbai to Pune Load Delivery

#### Phase 1: Load Creation (Main System)
```
1. Vendor logs into main system (Port 5173)
2. Posts load: Mumbai → Pune, 5000kg, ₹15,000
3. System stores in ChromaDB
4. Load status: "available"
```

#### Phase 2: Load Assignment (Main System)
```
5. Driver sees load opportunity
6. Driver accepts load
7. System assigns driver to load
8. Load status: "assigned"
9. API call to verification system →
```

#### Phase 3: QR Generation (Verification System)
```
10. Verification system receives assignment
11. Generates pickup QR code
12. Stores QR in ChromaDB
13. AI Notification Agent sends alerts:
    - Vendor: "QR ready for pickup"
    - Driver: "Scan QR at pickup location"
```

#### Phase 4: Pickup (Verification System)
```
14. Driver arrives at Mumbai warehouse
15. Opens driver scanner (Port 5174)
16. Shows QR code to vendor
17. Vendor scans QR on vendor dashboard
18. AI Verification Agent validates:
    ✓ Driver ID matches
    ✓ Location within 100m
    ✓ QR not expired/used
19. Verification success!
20. System generates delivery QR
21. AI Notification Agent alerts:
    - Vendor: "Pickup verified"
    - Driver: "Proceed to delivery"
    - Receiver: "Load in transit"
22. API call to main system →
23. Main system updates: status = "picked_up"
```

#### Phase 5: Transit (Main System)
```
24. Driver dashboard shows route
25. GPS tracking active
26. ETA calculated
27. Real-time location updates
```

#### Phase 6: Delivery (Verification System)
```
28. Driver arrives at Pune distribution center
29. Shows delivery QR code
30. Receiver scans QR on receiver dashboard
31. AI Verification Agent validates:
    ✓ Receiver ID matches
    ✓ Driver ID matches original
    ✓ Location within 100m
    ✓ Pickup was verified first
32. Verification success!
33. AI Notification Agent sends:
    - Vendor: Email + in-app (CRITICAL)
    - Driver: "Payment processing"
    - Receiver: "Receipt confirmed"
34. API call to main system →
35. Main system updates: status = "delivered"
36. Payment triggered
```

---

## 🔧 Configuration

### Environment Variables

#### Main System (.env)
```env
# Main system
PORT=8000
FRONTEND_PORT=5173

# Integration
VERIFICATION_API_URL=http://localhost:8001/api/v1
ENABLE_QR_INTEGRATION=true
```

#### Verification System (verification_backend/.env)
```env
# Verification system
PORT=8001
FRONTEND_PORT=5174

# Integration
MAIN_API_URL=http://localhost:8000/api/v1
ENABLE_MAIN_SYSTEM_SYNC=true
```

### CORS Configuration

#### Main System (main.py)
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Main frontend
        "http://localhost:5174",  # Verification frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### Verification System (main_verification.py)
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Main frontend
        "http://localhost:5174",  # Verification frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🧪 Testing Integration

### Test Script

```python
# test_integration.py
import requests

def test_complete_integration():
    """Test complete flow across both systems"""
    
    # 1. Create load in main system
    load_response = requests.post(
        "http://localhost:8000/api/v1/loads/",
        json={
            "vendor_id": "vendor-123",
            "weight_kg": 5000,
            "pickup_location": {"lat": 19.0760, "lng": 72.8777},
            "destination": {"lat": 18.5204, "lng": 73.8567},
            "price_offered": 15000
        }
    )
    load_id = load_response.json()["load_id"]
    
    # 2. Assign driver in main system
    assign_response = requests.post(
        f"http://localhost:8000/api/v1/loads/{load_id}/assign",
        json={"driver_id": "driver-456"}
    )
    
    # 3. Verify QR generated in verification system
    qr_status = requests.get(
        f"http://localhost:8001/api/v1/qr/load/{load_id}/status"
    )
    assert qr_status.json()["pickup_qr_generated"] == True
    
    # 4. Simulate pickup verification
    # ... (see test_qr_verification_flow.py)
    
    # 5. Verify main system updated
    load_status = requests.get(
        f"http://localhost:8000/api/v1/loads/{load_id}"
    )
    assert load_status.json()["status"] == "picked_up"
    
    print("✓ Integration test passed!")
```

---

## 📈 Monitoring

### Health Checks

```bash
# Main system
curl http://localhost:8000/health

# Verification system
curl http://localhost:8001/health
```

### Metrics to Track

1. **Integration Success Rate**
   - QR generation success after assignment
   - Status sync success after verification

2. **API Response Times**
   - Main → Verification calls
   - Verification → Main calls

3. **Error Rates**
   - Failed QR generations
   - Failed status updates
   - Timeout errors

---

## 🔒 Security Considerations

### API Authentication (Production)

```python
# Add API keys for inter-system communication
VERIFICATION_API_KEY = "your-secret-key"

# In main system
headers = {
    "Authorization": f"Bearer {VERIFICATION_API_KEY}"
}

# In verification system
@router.post("/qr/generate/pickup/{load_id}")
def generate_pickup_qr(
    load_id: UUID,
    api_key: str = Header(None, alias="Authorization")
):
    if api_key != f"Bearer {VERIFICATION_API_KEY}":
        raise HTTPException(401, "Unauthorized")
    # ... rest of logic
```

### Network Security

- Use HTTPS in production
- Implement rate limiting
- Add request signing
- Use VPN for inter-service communication

---

## 🚀 Deployment

### Docker Compose (Recommended)

```yaml
version: '3.8'

services:
  main-backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - VERIFICATION_API_URL=http://verification-backend:8001

  main-frontend:
    build: ./frontend
    ports:
      - "5173:5173"

  verification-backend:
    build: ./verification_backend
    ports:
      - "8001:8001"
    environment:
      - MAIN_API_URL=http://main-backend:8000

  verification-frontend:
    build: ./verification_webapp
    ports:
      - "5174:5174"
```

### Kubernetes

```yaml
# Deploy both systems in same cluster
# Use internal DNS for service discovery
# main-backend.default.svc.cluster.local
# verification-backend.default.svc.cluster.local
```

---

## 📞 Troubleshooting

### Issue: QR not generated after assignment

**Check**:
1. Verification system running?
2. Network connectivity between systems?
3. Check main system logs for API call errors
4. Verify CORS settings

**Solution**:
```bash
# Test connectivity
curl http://localhost:8001/health

# Check logs
tail -f verification_backend/logs/app.log
```

### Issue: Status not updating in main system

**Check**:
1. Main system API accessible?
2. Load ID exists in main system?
3. Check verification system logs

**Solution**:
```bash
# Test main system
curl http://localhost:8000/api/v1/loads/{load_id}

# Manual status update
curl -X PATCH http://localhost:8000/api/v1/loads/{load_id}/status \
  -H "Content-Type: application/json" \
  -d '{"status": "picked_up"}'
```

---

## 🎯 Best Practices

1. **Graceful Degradation**: Systems should work independently if integration fails
2. **Async Communication**: Use message queues for non-critical updates
3. **Retry Logic**: Implement exponential backoff for failed API calls
4. **Monitoring**: Track integration health metrics
5. **Documentation**: Keep API contracts documented and versioned

---

## 📚 Additional Resources

- Main System API: http://localhost:8000/docs
- Verification System API: http://localhost:8001/docs
- Complete Guide: `QR_VERIFICATION_SYSTEM.md`
- Quick Start: `START_VERIFICATION_SYSTEM.md`

---

**Two systems, one seamless experience! 🚀**
