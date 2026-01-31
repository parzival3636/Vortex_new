# QR Verification System - Complete Guide

## 🎯 Overview

A **separate, standalone system** for QR-based load verification with AI agents. This system runs independently from the main driver/owner platform and provides:

- **Vendor Dashboard**: Monitor loads, generate QR codes, track verification status
- **Receiver Dashboard**: Scan QR codes, verify deliveries, receive notifications
- **Driver QR Display**: Show QR codes at pickup and delivery points
- **AI Agents**: Automated verification, anomaly detection, and notifications

---

## 🏗️ Architecture

### Separate Systems

1. **Main System** (Port 8000)
   - Driver dashboard
   - Owner dashboard
   - Load matching
   - Trip management

2. **Verification System** (Port 8001) ← **NEW**
   - Vendor dashboard
   - Receiver dashboard
   - QR generation & verification
   - AI agents for automation

### Directory Structure

```
verification_backend/          # Separate backend
├── agents/
│   ├── verification_agent.py  # AI agent for identity verification
│   └── notification_agent.py  # AI agent for automated notifications
├── api/
│   ├── qr_verification.py     # QR endpoints
│   └── receivers.py           # Receiver management
├── models/
│   └── verification_models.py # Pydantic models
├── db_verification.py         # ChromaDB for verification data
├── main_verification.py       # FastAPI app (Port 8001)
└── requirements.txt

verification_webapp/           # Separate frontend
├── src/
│   ├── pages/
│   │   ├── LandingPage.jsx
│   │   ├── VendorDashboard.jsx
│   │   ├── ReceiverDashboard.jsx
│   │   └── DriverScanner.jsx
│   ├── services/
│   │   └── api.js
│   └── App.jsx
├── package.json
└── vite.config.js            # Port 5174
```

---

## 🤖 AI Agents

### 1. Verification Agent

**Purpose**: Validate driver identity and detect fraud

**Capabilities**:
- ✅ Verify driver ID matches assignment
- ✅ Check location proximity (100m radius)
- ✅ Validate QR code authenticity and expiry
- ✅ Detect anomalies (reused QR, wrong location, timing issues)
- ✅ Calculate confidence scores (0-100%)
- ✅ Ensure pickup verified before delivery

**Algorithm**:
```python
def verify_pickup_scan():
    1. Check QR not expired (24 hours)
    2. Check QR not already used
    3. Verify driver ID matches assignment
    4. Calculate distance from pickup location
    5. Check distance < 100 meters
    6. Detect time-based anomalies
    7. Calculate confidence score
    8. Return verification result
```

### 2. Notification Agent

**Purpose**: Automated real-time notifications

**Capabilities**:
- 📧 Multi-channel notifications (email, SMS, push, in-app)
- 🔔 Priority-based delivery (low, normal, high, critical)
- ⚡ Real-time updates on verification events
- 🚨 Critical alerts for anomalies
- 📊 Notification history tracking

**Notification Flow**:
```
QR Generated → Notify vendor + driver/receiver
Pickup Verified → Notify vendor + driver
Delivery Verified → Notify vendor + driver + receiver (CRITICAL)
Anomaly Detected → Critical alert to vendor (SMS + in-app)
```

---

## 🔄 Complete Workflow

### Step 1: Load Assignment
```
Main System (Port 8000):
- Vendor posts load
- Driver accepts load
- System assigns driver to load
```

### Step 2: Pickup QR Generation
```
Verification System (Port 8001):
1. Vendor clicks "Generate Pickup QR"
2. System creates unique QR code
3. AI Notification Agent sends alerts:
   - Vendor: "QR code ready"
   - Driver: "Scan QR at pickup"
4. QR displayed on vendor dashboard
```

### Step 3: Pickup Verification
```
Driver arrives at pickup location:
1. Driver opens QR scanner
2. Vendor scans driver's QR code
3. AI Verification Agent validates:
   ✓ Driver ID matches
   ✓ Location within 100m
   ✓ QR not expired/used
   ✓ Confidence score: 95%
4. If successful:
   - Mark QR as used
   - Update load status to "picked_up"
   - AI Notification Agent alerts vendor
5. If failed:
   - Send critical alert to vendor
   - Log anomaly details
```

### Step 4: Delivery QR Generation
```
After pickup verification:
1. System auto-generates delivery QR
2. AI Notification Agent sends alerts:
   - Receiver: "Driver en route, QR ready"
   - Vendor: "Load in transit"
3. QR displayed on receiver dashboard
```

### Step 5: Delivery Verification
```
Driver arrives at delivery location:
1. Driver shows delivery QR
2. Receiver scans QR code
3. AI Verification Agent validates:
   ✓ Receiver ID matches
   ✓ Driver ID matches original assignment
   ✓ Location within 100m
   ✓ Pickup was verified first
   ✓ Confidence score: 98%
4. If successful:
   - Mark load as "delivered"
   - AI Notification Agent sends:
     * Vendor: Email + in-app (CRITICAL)
     * Driver: "Payment processing"
     * Receiver: "Receipt confirmed"
5. If failed:
   - Critical alert to vendor
   - Log anomaly for investigation
```

---

## 🚀 Installation & Setup

### Backend Setup

```bash
# Navigate to verification backend
cd verification_backend

# Install dependencies
pip install -r requirements.txt

# Run the server (Port 8001)
python main_verification.py
```

Server will start at: `http://localhost:8001`

### Frontend Setup

```bash
# Navigate to verification webapp
cd verification_webapp

# Install dependencies
npm install

# Run development server (Port 5174)
npm run dev
```

Webapp will start at: `http://localhost:5174`

---

## 📡 API Endpoints

### QR Verification API

#### Generate Pickup QR
```http
POST /api/v1/qr/generate/pickup/{load_id}
Query Params:
  - driver_id: UUID
  - vendor_id: UUID
  - pickup_lat: float
  - pickup_lng: float

Response:
{
  "qr_id": "uuid",
  "qr_type": "pickup",
  "load_id": "uuid",
  "expires_at": "2026-02-01T12:00:00",
  "message": "Pickup QR code generated"
}
```

#### Generate Delivery QR
```http
POST /api/v1/qr/generate/delivery/{load_id}
Query Params:
  - driver_id: UUID
  - vendor_id: UUID
  - receiver_id: UUID
  - delivery_lat: float
  - delivery_lng: float
```

#### Verify Pickup
```http
POST /api/v1/qr/verify/pickup
Body:
{
  "qr_id": "uuid",
  "scanned_by_id": "uuid",
  "scanned_by_type": "driver",
  "scan_location_lat": 19.0760,
  "scan_location_lng": 72.8777,
  "timestamp": "2026-01-31T10:00:00"
}

Response:
{
  "success": true,
  "message": "Driver identity verified successfully",
  "qr_id": "uuid",
  "load_id": "uuid",
  "verification_type": "pickup",
  "verified_at": "2026-01-31T10:00:00",
  "next_step": "Proceed to delivery location"
}
```

#### Verify Delivery
```http
POST /api/v1/qr/verify/delivery
Body: (same as pickup)
```

#### Get Load Status
```http
GET /api/v1/qr/load/{load_id}/status

Response:
{
  "load_id": "uuid",
  "status": "in_transit",
  "pickup_qr_generated": true,
  "pickup_verified": true,
  "delivery_qr_generated": true,
  "delivery_verified": false,
  "qr_codes": [...],
  "verifications": [...]
}
```

### Receiver API

#### Create Receiver
```http
POST /api/v1/receivers/
Body:
{
  "name": "Pune Distribution Center",
  "email": "pune@example.com",
  "phone": "+91 9876543210",
  "location_lat": 18.5204,
  "location_lng": 73.8567,
  "location_address": "Pune, Maharashtra",
  "company_name": "ABC Logistics"
}
```

#### Get Receiver Notifications
```http
GET /api/v1/receivers/{receiver_id}/notifications?unread_only=true
```

---

## 🎨 User Interfaces

### 1. Landing Page (`/`)
- Role selection (Vendor / Receiver / Driver)
- ID input
- Feature showcase

### 2. Vendor Dashboard (`/vendor/{vendorId}`)
- **Load List**: All vendor loads with status
- **QR Generation**: One-click pickup QR creation
- **Verification Status**: Real-time tracking
  - Pickup verification status
  - Delivery verification status
  - QR code display
  - AI confidence scores
- **Quick Stats**: Total loads, in transit, delivered
- **Notifications**: Real-time alerts

### 3. Receiver Dashboard (`/receiver/{receiverId}`)
- **QR Scanner**: Camera-based QR scanning
- **Incoming Loads**: List of expected deliveries
- **Verification Results**: Success/failure feedback
- **Notifications**: Delivery alerts
- **Instructions**: Step-by-step guide

### 4. Driver Scanner (`/driver/scan/{loadId}`)
- **QR Display**: Large, scannable QR code
- **Status Timeline**: Pickup → Delivery progress
- **Context Info**: Current step instructions
- **Load Details**: Status summary

---

## 🔒 Security Features

### AI-Powered Verification

1. **Identity Verification**
   - Driver ID must match assignment
   - Receiver ID must match expected recipient

2. **Location Verification**
   - GPS coordinates checked
   - Must be within 100m radius
   - Distance calculated using Haversine formula

3. **Temporal Verification**
   - QR codes expire after 24 hours
   - Cannot be reused
   - Sequence enforcement (pickup before delivery)

4. **Anomaly Detection**
   - Suspicious timing patterns
   - Location mismatches
   - Reused QR codes
   - Driver mismatches
   - Sequence violations

5. **Confidence Scoring**
   - 100% = Perfect match
   - Deductions for distance (max 20 points)
   - Deductions for anomalies (10 points each)
   - Minimum threshold for acceptance

---

## 🧪 Testing

### Test Scenario 1: Complete Flow

```bash
# 1. Start both backends
python main.py                           # Port 8000
python verification_backend/main_verification.py  # Port 8001

# 2. Start both frontends
cd frontend && npm run dev               # Port 5173
cd verification_webapp && npm run dev    # Port 5174

# 3. Test flow:
- Create load in main system
- Assign driver
- Open vendor dashboard (Port 5174)
- Generate pickup QR
- Simulate driver scan (use mock location)
- Verify pickup
- Check delivery QR generated
- Open receiver dashboard
- Scan delivery QR
- Verify delivery complete
```

### Test Scenario 2: Anomaly Detection

```bash
# Test wrong driver scanning
- Generate QR for driver A
- Try scanning with driver B ID
- Should fail with "Driver ID mismatch"

# Test location mismatch
- Generate QR at location A
- Scan from location B (>100m away)
- Should fail with "Location too far"

# Test expired QR
- Generate QR
- Wait 24+ hours (or modify expiry)
- Try scanning
- Should fail with "QR expired"
```

---

## 🔗 Integration with Main System

The verification system integrates with the main system through:

1. **Shared Load IDs**: Both systems reference same load_id
2. **API Calls**: Verification system can query main system for load details
3. **Status Updates**: Verification events update main system status
4. **Webhooks** (optional): Real-time event notifications

### Integration Points

```python
# In main system (api/loads.py)
@router.post("/loads/{load_id}/assign")
def assign_load_to_driver(load_id, driver_id):
    # ... assign logic ...
    
    # Trigger QR generation in verification system
    requests.post(
        "http://localhost:8001/api/v1/qr/generate/pickup/{load_id}",
        params={
            "driver_id": driver_id,
            "vendor_id": load.vendor_id,
            "pickup_lat": load.pickup_lat,
            "pickup_lng": load.pickup_lng
        }
    )
```

---

## 📊 AI Agent Metrics

### Verification Agent Metrics
- Total verifications performed
- Success rate
- Average confidence score
- Anomalies detected by type
- False positive rate

### Notification Agent Metrics
- Notifications sent by channel
- Delivery success rate
- Average delivery time
- Critical alerts sent
- Notification history

---

## 🎯 Key Benefits

1. **Complete Separation**: Vendor/receiver logic isolated from driver/owner system
2. **AI Automation**: Zero manual verification needed
3. **Real-time Tracking**: Instant status updates for all parties
4. **Fraud Prevention**: Multi-layer verification with anomaly detection
5. **Scalability**: Independent scaling of verification system
6. **Transparency**: Complete audit trail of all verifications

---

## 🚀 Next Steps

1. **Deploy both systems** to separate servers
2. **Configure webhooks** for real-time integration
3. **Add SMS/Email** services for notifications
4. **Implement payment** triggers on delivery verification
5. **Add analytics** dashboard for verification metrics
6. **Mobile apps** for better QR scanning experience

---

## 📞 Support

For issues or questions:
- Backend API docs: `http://localhost:8001/docs`
- Frontend: `http://localhost:5174`
- Main system: `http://localhost:8000`

---

**Built with AI Agents for Maximum Automation** 🤖✨
