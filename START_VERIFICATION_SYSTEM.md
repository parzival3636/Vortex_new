# 🚀 Quick Start - QR Verification System

## Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

## Step 1: Install Backend Dependencies

```bash
cd verification_backend
pip install -r requirements.txt
```

## Step 2: Install Frontend Dependencies

```bash
cd verification_webapp
npm install
```

## Step 3: Start Backend Server

```bash
# From verification_backend directory
python main_verification.py
```

Backend will run on: **http://localhost:8001**

API Documentation: **http://localhost:8001/docs**

## Step 4: Start Frontend Server

```bash
# From verification_webapp directory
npm run dev
```

Frontend will run on: **http://localhost:5174**

## Step 5: Test the System

### Option A: Run Automated Tests

```bash
# From project root
python test_qr_verification_flow.py
```

This will test:
- ✅ Receiver creation
- ✅ Pickup QR generation
- ✅ Pickup verification (success)
- ✅ Wrong driver detection (failure)
- ✅ Delivery QR generation
- ✅ Delivery verification (success)
- ✅ Load status tracking
- ✅ Notification system

### Option B: Manual Testing via UI

1. **Open the webapp**: http://localhost:5174

2. **Login as Vendor**:
   - Select "Vendor"
   - Enter ID: `vendor-123`
   - Click "Access Dashboard"

3. **Generate Pickup QR**:
   - View your loads
   - Click "Generate Pickup QR"
   - QR code will be displayed

4. **Login as Receiver** (new tab):
   - Go to http://localhost:5174
   - Select "Receiver"
   - Enter ID: `receiver-456`
   - Click "Access Dashboard"

5. **Scan Delivery QR**:
   - Click "Start Scanning"
   - Scan the QR code (or use test QR)
   - See verification result

## System URLs

| Service | URL | Port |
|---------|-----|------|
| Verification Backend | http://localhost:8001 | 8001 |
| Verification Frontend | http://localhost:5174 | 5174 |
| API Docs | http://localhost:8001/docs | 8001 |
| Main System Backend | http://localhost:8000 | 8000 |
| Main System Frontend | http://localhost:5173 | 5173 |

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   VERIFICATION SYSTEM                    │
│                     (Separate Stack)                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Frontend (Port 5174)          Backend (Port 8001)      │
│  ├── Vendor Dashboard          ├── QR Generation        │
│  ├── Receiver Dashboard        ├── QR Verification      │
│  └── Driver Scanner            ├── AI Agents            │
│                                 │   ├── Verification    │
│                                 │   └── Notification    │
│                                 └── ChromaDB            │
│                                                          │
└─────────────────────────────────────────────────────────┘
                         ↕
┌─────────────────────────────────────────────────────────┐
│                     MAIN SYSTEM                          │
│                  (Existing Stack)                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Frontend (Port 5173)          Backend (Port 8000)      │
│  ├── Driver Dashboard          ├── Load Matching        │
│  └── Owner Dashboard           ├── Trip Management      │
│                                 └── AI Agents            │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Key Features

### 🤖 AI Agents

1. **Verification Agent**
   - Validates driver identity
   - Checks location proximity (100m radius)
   - Detects anomalies and fraud
   - Calculates confidence scores

2. **Notification Agent**
   - Sends real-time alerts
   - Multi-channel delivery (email, SMS, push, in-app)
   - Priority-based notifications
   - Critical alerts for anomalies

### 🔒 Security

- QR codes expire after 24 hours
- One-time use only
- Location verification (GPS)
- Driver ID verification
- Sequence enforcement (pickup before delivery)
- Anomaly detection

### 📱 Dashboards

1. **Vendor Dashboard**
   - View all loads
   - Generate pickup QR codes
   - Track verification status
   - Receive notifications
   - View AI confidence scores

2. **Receiver Dashboard**
   - Scan delivery QR codes
   - View incoming loads
   - Receive delivery notifications
   - Confirm receipt

3. **Driver Scanner**
   - Display QR codes for scanning
   - Show current step
   - Track verification progress

## Troubleshooting

### Backend won't start
```bash
# Check if port 8001 is available
netstat -ano | findstr :8001

# Kill process if needed
taskkill /PID <PID> /F

# Try again
python verification_backend/main_verification.py
```

### Frontend won't start
```bash
# Clear node_modules and reinstall
cd verification_webapp
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### QR Scanner not working
- Ensure HTTPS or localhost (camera requires secure context)
- Grant camera permissions in browser
- Try different browser (Chrome recommended)

### API errors
- Check backend is running on port 8001
- Check API docs: http://localhost:8001/docs
- Verify request format matches API schema

## Next Steps

1. ✅ Test complete flow with automated tests
2. ✅ Explore vendor dashboard
3. ✅ Test QR scanning with receiver dashboard
4. ✅ Check AI agent notifications
5. ✅ Review verification status and confidence scores

## Support

- API Documentation: http://localhost:8001/docs
- Full Guide: See `QR_VERIFICATION_SYSTEM.md`
- Test Script: `test_qr_verification_flow.py`

---

**Ready to revolutionize load verification with AI! 🚀**
