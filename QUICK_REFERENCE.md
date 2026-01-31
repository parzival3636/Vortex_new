# Quick Reference Card

## 🚀 Start Commands

```bash
# Backend
cd verification_backend
python main_verification.py

# Frontend
cd verification_webapp
npm run dev

# Tests
python test_qr_verification_flow.py
```

## 🌐 URLs

| Service | URL | Port |
|---------|-----|------|
| Verification Backend | http://localhost:8001 | 8001 |
| Verification Frontend | http://localhost:5174 | 5174 |
| API Documentation | http://localhost:8001/docs | 8001 |
| Health Check | http://localhost:8001/health | 8001 |

## 📱 User Access

| Role | URL Pattern | Example |
|------|-------------|---------|
| Vendor | `/vendor/{vendorId}` | `/vendor/vendor-123` |
| Receiver | `/receiver/{receiverId}` | `/receiver/receiver-456` |
| Driver | `/driver/scan/{loadId}` | `/driver/scan/load-789` |

## 🔑 API Endpoints

### QR Generation
```bash
# Pickup QR
POST /api/v1/qr/generate/pickup/{load_id}
  ?driver_id={uuid}
  &vendor_id={uuid}
  &pickup_lat={float}
  &pickup_lng={float}

# Delivery QR
POST /api/v1/qr/generate/delivery/{load_id}
  ?driver_id={uuid}
  &vendor_id={uuid}
  &receiver_id={uuid}
  &delivery_lat={float}
  &delivery_lng={float}
```

### QR Verification
```bash
# Verify Pickup
POST /api/v1/qr/verify/pickup
Body: {
  "qr_id": "uuid",
  "scanned_by_id": "uuid",
  "scanned_by_type": "driver",
  "scan_location_lat": 19.0760,
  "scan_location_lng": 72.8777,
  "timestamp": "2026-01-31T10:00:00"
}

# Verify Delivery
POST /api/v1/qr/verify/delivery
Body: (same as pickup)
```

### Status Check
```bash
# Get Load Status
GET /api/v1/qr/load/{load_id}/status
```

## 🤖 AI Agents

### Verification Agent
- **Purpose**: Validate identity and location
- **Checks**: Driver ID, Location (100m), QR validity, Sequence
- **Output**: Success/failure + confidence score (0-100%)

### Notification Agent
- **Purpose**: Automated alerts
- **Channels**: Email, SMS, Push, In-app
- **Priorities**: Low, Normal, High, Critical
- **Events**: QR generated, Pickup verified, Delivery verified, Anomaly detected

## 🔒 Security Rules

| Rule | Value | Description |
|------|-------|-------------|
| QR Expiry | 24 hours | QR codes expire after 24h |
| Location Radius | 100 meters | Must scan within 100m |
| QR Usage | One-time | Can only be used once |
| Sequence | Pickup first | Delivery requires pickup verification |
| Confidence Threshold | 70% | Minimum score for acceptance |

## 📊 Status Flow

```
assigned → awaiting_pickup → in_transit → delivered
```

## 🎯 Confidence Scoring

```
Base Score: 100%
- Distance penalty: (distance/100m) × 20 points (max 20)
- Anomaly penalty: 10 points each
Final Score: max(0, min(100, score))
```

## 🧪 Test Data

```python
# Test IDs
VENDOR_ID = "vendor-123"
DRIVER_ID = "driver-456"
RECEIVER_ID = "receiver-789"
LOAD_ID = "load-001"

# Test Locations
MUMBAI = (19.0760, 72.8777)
PUNE = (18.5204, 73.8567)
```

## 📝 Common Tasks

### Generate Pickup QR
```bash
curl -X POST "http://localhost:8001/api/v1/qr/generate/pickup/load-001?driver_id=driver-456&vendor_id=vendor-123&pickup_lat=19.0760&pickup_lng=72.8777"
```

### Verify Pickup
```bash
curl -X POST "http://localhost:8001/api/v1/qr/verify/pickup" \
  -H "Content-Type: application/json" \
  -d '{
    "qr_id": "qr-uuid",
    "scanned_by_id": "driver-456",
    "scanned_by_type": "driver",
    "scan_location_lat": 19.0760,
    "scan_location_lng": 72.8777,
    "timestamp": "2026-01-31T10:00:00"
  }'
```

### Check Status
```bash
curl "http://localhost:8001/api/v1/qr/load/load-001/status"
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Backend won't start | Check port 8001 available |
| Frontend won't start | Run `npm install` first |
| QR scanner not working | Use Chrome, grant camera permission |
| API errors | Check backend running, verify request format |
| Location mismatch | Ensure within 100m radius |
| QR expired | Generate new QR (24h expiry) |

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `QR_VERIFICATION_SYSTEM.md` | Complete system guide |
| `START_VERIFICATION_SYSTEM.md` | Quick start guide |
| `SYSTEM_INTEGRATION_GUIDE.md` | Integration with main system |
| `VERIFICATION_SYSTEM_SUMMARY.md` | Executive summary |
| `SYSTEM_ARCHITECTURE_DIAGRAM.md` | Visual diagrams |
| `test_qr_verification_flow.py` | Automated test suite |

## 🔧 Configuration

### Backend (.env)
```env
PORT=8001
MAIN_API_URL=http://localhost:8000/api/v1
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8001/api/v1
```

## 📞 Support

- API Docs: http://localhost:8001/docs
- Health: http://localhost:8001/health
- Frontend: http://localhost:5174

---

**Keep this card handy for quick reference!** 📋
