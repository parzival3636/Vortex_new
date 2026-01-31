# 🚚 QR Verification System for Load Tracking

> **AI-Powered Identity Verification System for Secure Load Pickup and Delivery**

A complete, standalone verification platform that uses QR codes and AI agents to automatically verify driver identity at pickup and delivery points, ensuring complete transparency and security in logistics operations.

---

## 🌟 Key Features

### 🤖 AI-Powered Automation
- **Verification Agent**: Automatically validates driver/receiver identity, location, and QR authenticity
- **Notification Agent**: Sends real-time alerts to all parties via multiple channels
- **Anomaly Detection**: AI detects fraud attempts, location mismatches, and suspicious patterns
- **Confidence Scoring**: Quantifiable trust metric (0-100%) for each verification

### 🔒 Multi-Layer Security
- **Identity Verification**: Driver/receiver ID must match assignment
- **Location Verification**: GPS validation within 100m radius
- **Temporal Verification**: QR codes expire after 24 hours, one-time use only
- **Sequence Enforcement**: Delivery requires pickup verification first
- **Audit Trail**: Complete immutable history of all verifications

### 📱 User-Friendly Dashboards
- **Vendor Dashboard**: Monitor loads, generate QR codes, track verifications
- **Receiver Dashboard**: Scan QR codes, verify deliveries, view notifications
- **Driver Scanner**: Display QR codes for pickup and delivery

### ⚡ Real-Time Updates
- Instant notifications on QR generation, pickup, and delivery
- Live verification status tracking
- Multi-channel alerts (email, SMS, push, in-app)
- Priority-based notification delivery

---

## 🏗️ Architecture

### Separate System Design

The verification system runs **completely independently** from the main driver/owner platform:

```
Main System (Port 8000/5173)          Verification System (Port 8001/5174)
├── Driver Dashboard                  ├── Vendor Dashboard
├── Owner Dashboard                   ├── Receiver Dashboard
├── Load Matching                     ├── Driver QR Scanner
└── Trip Management                   ├── AI Verification Agent
                                      ├── AI Notification Agent
                                      └── QR Management
```

### Technology Stack

**Backend**:
- FastAPI (Python web framework)
- ChromaDB (vector database)
- Pydantic (data validation)
- Uvicorn (ASGI server)

**Frontend**:
- React 18
- Vite (build tool)
- TailwindCSS (styling)
- React Router (routing)
- QRCode.react (QR generation)
- html5-qrcode (QR scanning)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Installation

```bash
# 1. Install backend dependencies
cd verification_backend
pip install -r requirements.txt

# 2. Install frontend dependencies
cd verification_webapp
npm install
```

### Running the System

```bash
# Terminal 1: Start backend
cd verification_backend
python main_verification.py
# Runs on http://localhost:8001

# Terminal 2: Start frontend
cd verification_webapp
npm run dev
# Runs on http://localhost:5174
```

### Testing

```bash
# Run automated test suite
python test_qr_verification_flow.py
```

---

## 📖 Complete Workflow

### 1. Load Assignment (Main System)
- Vendor posts load
- Driver accepts load
- System assigns driver to load

### 2. Pickup QR Generation (Verification System)
- Vendor clicks "Generate Pickup QR"
- System creates unique QR code (expires in 24h)
- AI Notification Agent alerts vendor and driver
- QR displayed on vendor dashboard

### 3. Pickup Verification (Verification System)
- Driver arrives at pickup location
- Driver shows QR code to vendor
- Vendor scans QR code
- **AI Verification Agent validates**:
  - ✅ Driver ID matches assignment
  - ✅ Location within 100m of pickup point
  - ✅ QR not expired or already used
  - ✅ Calculates confidence score (e.g., 95%)
- If successful:
  - Mark QR as used
  - Update status to "picked_up"
  - Auto-generate delivery QR
  - AI Notification Agent alerts all parties
- If failed:
  - Send critical alert to vendor
  - Log anomaly details
  - Block pickup

### 4. In Transit (Main System)
- Driver dashboard shows route
- GPS tracking active
- Real-time location updates

### 5. Delivery QR Generation (Verification System)
- System auto-generates delivery QR after pickup
- AI Notification Agent alerts receiver and vendor
- QR displayed on receiver dashboard

### 6. Delivery Verification (Verification System)
- Driver arrives at delivery location
- Driver shows delivery QR to receiver
- Receiver scans QR code
- **AI Verification Agent validates**:
  - ✅ Receiver ID matches expected recipient
  - ✅ Driver ID matches original assignment
  - ✅ Location within 100m of delivery point
  - ✅ Pickup was verified first
  - ✅ Calculates confidence score (e.g., 98%)
- If successful:
  - Mark load as "delivered"
  - AI Notification Agent sends critical alerts:
    - Vendor: Email + in-app
    - Driver: "Payment processing"
    - Receiver: "Receipt confirmed"
  - Trigger payment in main system
- If failed:
  - Critical alert to vendor
  - Log anomaly for investigation
  - Block delivery

---

## 🎨 User Interfaces

### Vendor Dashboard
**URL**: `http://localhost:5174/vendor/{vendorId}`

**Features**:
- View all loads with real-time status badges
- One-click pickup QR generation
- Live verification status tracking
- Display QR codes with expiry timers
- View AI confidence scores
- Notification feed with priority indicators
- Quick stats dashboard

### Receiver Dashboard
**URL**: `http://localhost:5174/receiver/{receiverId}`

**Features**:
- Camera-based QR scanner
- Incoming loads list
- Real-time verification results
- Success/failure feedback with details
- Notification feed
- Step-by-step instructions

### Driver Scanner
**URL**: `http://localhost:5174/driver/scan/{loadId}`

**Features**:
- Large, scannable QR code display
- Status timeline (pickup → delivery)
- Context-aware instructions
- Auto-refresh on status change
- Load details summary

---

## 🤖 AI Agents in Detail

### Verification Agent

**Purpose**: Validate driver/receiver identity and detect fraud

**Validation Process**:
1. **QR Code Validation**
   - Check not expired (24 hours)
   - Check not already used
   - Verify QR signature

2. **Identity Verification**
   - Match driver/receiver ID with assignment
   - Cross-reference with database
   - Prevent impersonation

3. **Location Verification**
   - Get scan GPS coordinates
   - Calculate distance using Haversine formula
   - Validate distance < 100 meters

4. **Anomaly Detection**
   - Check timing patterns
   - Verify sequence (pickup before delivery)
   - Detect duplicate scans
   - Flag suspicious behavior

5. **Confidence Scoring**
   - Base score: 100%
   - Distance penalty: (distance/100m) × 20 points
   - Anomaly penalty: 10 points each
   - Final score: max(0, min(100, score))

**Output**:
```json
{
  "success": true,
  "message": "Driver identity verified successfully",
  "confidence_score": 95.0,
  "distance_meters": 11.5,
  "anomalies": [],
  "verified_at": "2026-01-31T10:00:00"
}
```

### Notification Agent

**Purpose**: Automated real-time notifications

**Capabilities**:
- Multi-channel delivery (email, SMS, push, in-app)
- Priority-based routing (low, normal, high, critical)
- Event-driven notifications
- Complete notification history

**Notification Events**:
1. **QR Generated**: Notify vendor + driver/receiver
2. **Pickup Verified**: Notify vendor + driver
3. **Delivery Verified**: Notify vendor + driver + receiver (CRITICAL)
4. **Anomaly Detected**: Critical alert to vendor (SMS + in-app)

---

## 📡 API Documentation

### QR Generation

#### Generate Pickup QR
```http
POST /api/v1/qr/generate/pickup/{load_id}
Query Parameters:
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
Query Parameters:
  - driver_id: UUID
  - vendor_id: UUID
  - receiver_id: UUID
  - delivery_lat: float
  - delivery_lng: float
```

### QR Verification

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
Body: (same structure as pickup)
```

### Status Check

#### Get Load Verification Status
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

**Full API Documentation**: http://localhost:8001/docs

---

## 🧪 Testing

### Automated Test Suite

```bash
python test_qr_verification_flow.py
```

**Tests Include**:
1. ✅ Receiver creation
2. ✅ Pickup QR generation
3. ✅ Pickup verification (success case)
4. ✅ Wrong driver detection (failure case)
5. ✅ Delivery QR generation
6. ✅ Delivery verification (success case)
7. ✅ Load status tracking
8. ✅ Notification system

### Manual Testing

1. Start both backend and frontend
2. Open vendor dashboard: `http://localhost:5174/vendor/vendor-123`
3. Generate pickup QR for a load
4. Open driver scanner: `http://localhost:5174/driver/scan/{loadId}`
5. Simulate pickup verification
6. Check delivery QR generated
7. Open receiver dashboard: `http://localhost:5174/receiver/receiver-456`
8. Scan delivery QR
9. Verify delivery complete
10. Check all notifications sent

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| `QR_VERIFICATION_SYSTEM.md` | Complete system guide with detailed workflows |
| `START_VERIFICATION_SYSTEM.md` | Quick start guide for setup and testing |
| `SYSTEM_INTEGRATION_GUIDE.md` | Integration with main system |
| `VERIFICATION_SYSTEM_SUMMARY.md` | Executive summary and key features |
| `SYSTEM_ARCHITECTURE_DIAGRAM.md` | Visual architecture diagrams |
| `QUICK_REFERENCE.md` | Quick reference card for common tasks |
| `test_qr_verification_flow.py` | Automated test suite |

---

## 🔧 Configuration

### Backend Environment Variables

Create `verification_backend/.env`:
```env
PORT=8001
MAIN_API_URL=http://localhost:8000/api/v1
ENABLE_MAIN_SYSTEM_SYNC=true
```

### Frontend Environment Variables

Create `verification_webapp/.env`:
```env
VITE_API_URL=http://localhost:8001/api/v1
```

---

## 🐛 Troubleshooting

### Backend Issues

**Port already in use**:
```bash
# Windows
netstat -ano | findstr :8001
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8001 | xargs kill -9
```

**Dependencies not installed**:
```bash
cd verification_backend
pip install -r requirements.txt
```

### Frontend Issues

**Node modules error**:
```bash
cd verification_webapp
rm -rf node_modules package-lock.json
npm install
```

**QR scanner not working**:
- Use Chrome browser (recommended)
- Grant camera permissions
- Ensure HTTPS or localhost

### API Issues

**Connection refused**:
- Check backend is running on port 8001
- Verify CORS settings
- Check firewall rules

**Verification failed**:
- Ensure within 100m of location
- Check QR not expired (24 hours)
- Verify correct driver/receiver ID

---

## 🚀 Deployment

### Docker Deployment

```dockerfile
# Backend Dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main_verification.py"]
```

```dockerfile
# Frontend Dockerfile
FROM node:16
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
CMD ["npm", "run", "preview"]
```

### Docker Compose

```yaml
version: '3.8'
services:
  verification-backend:
    build: ./verification_backend
    ports:
      - "8001:8001"
    environment:
      - PORT=8001
  
  verification-frontend:
    build: ./verification_webapp
    ports:
      - "5174:5174"
    depends_on:
      - verification-backend
```

---

## 🎯 Benefits

### For Vendors
- ✅ Complete transparency on load status
- ✅ Automated fraud prevention
- ✅ Real-time pickup/delivery notifications
- ✅ Complete audit trail
- ✅ Zero manual verification needed

### For Receivers
- ✅ Easy driver identity verification
- ✅ Secure delivery confirmation
- ✅ Instant vendor notification
- ✅ Digital receipt (no paperwork)

### For Drivers
- ✅ Quick verification process
- ✅ Automated proof of delivery
- ✅ Clear step-by-step instructions
- ✅ Faster payment processing

### For System
- ✅ 100% automated verification
- ✅ Scalable to thousands of loads
- ✅ 24/7 AI agent operation
- ✅ Seamless integration with main system

---

## 📊 Metrics & Analytics

### Verification Metrics
- Total verifications performed
- Success rate percentage
- Average confidence score
- Anomalies detected by type
- False positive rate

### Performance Metrics
- Average verification time
- QR generation time
- Notification delivery time
- API response times

### Business Metrics
- Loads verified per day
- Fraud attempts prevented
- Time saved vs manual verification
- Customer satisfaction scores

---

## 🔮 Future Enhancements

### Phase 2
- [ ] SMS/Email service integration
- [ ] Mobile apps (iOS/Android)
- [ ] Biometric verification
- [ ] Blockchain audit trail

### Phase 3
- [ ] ML fraud pattern detection
- [ ] Predictive delivery analytics
- [ ] Payment gateway integration
- [ ] Multi-language support

### Phase 4
- [ ] IoT sensor integration
- [ ] Real-time video verification
- [ ] Automated dispute resolution
- [ ] Advanced analytics dashboard

---

## 📞 Support

- **API Documentation**: http://localhost:8001/docs
- **Health Check**: http://localhost:8001/health
- **Frontend**: http://localhost:5174
- **GitHub Issues**: [Create an issue]
- **Email**: support@example.com

---

## 📄 License

MIT License - see LICENSE file for details

---

## 🙏 Acknowledgments

Built with:
- FastAPI
- React
- ChromaDB
- TailwindCSS
- And lots of ☕

---

## 🎉 Get Started Now!

```bash
# Clone the repository
git clone <repository-url>

# Install and run
cd verification_backend && pip install -r requirements.txt && python main_verification.py &
cd verification_webapp && npm install && npm run dev

# Open browser
open http://localhost:5174
```

**Start verifying loads with AI today!** 🚀

---

**Made with ❤️ for the logistics industry**
