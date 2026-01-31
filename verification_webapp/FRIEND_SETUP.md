# Setup Guide for Vendor/Receiver System

## 👋 Welcome!

This is the **Vendor and Receiver Dashboard** for the logistics QR verification system. You'll be able to:
- View loads posted by vendors
- Generate QR codes for driver verification
- Track pickup and delivery status
- Receive real-time notifications

---

## 📋 Prerequisites

- Node.js 16 or higher ([Download](https://nodejs.org/))
- Internet connection
- IP address of the main server (ask your team)

---

## 🚀 Quick Setup

### Step 1: Install Dependencies

```bash
npm install
```

This will install all required packages.

### Step 2: Configure Backend Connection

Create a file named `.env` in this folder:

```bash
# Copy the example file
copy .env.example .env

# Or create manually with this content:
VITE_API_URL=http://SERVER_IP:8001/api/v1
VITE_MAIN_API_URL=http://SERVER_IP:8000/api/v1
```

**Replace `SERVER_IP` with the IP address provided by your team.**

Example:
```
VITE_API_URL=http://192.168.1.100:8001/api/v1
VITE_MAIN_API_URL=http://192.168.1.100:8000/api/v1
```

### Step 3: Start the Application

```bash
npm run dev
```

The app will open at: **http://localhost:5174**

---

## 🎯 How to Use

### Login

1. Open http://localhost:5174
2. Select your role:
   - **Vendor**: If you're posting loads
   - **Receiver**: If you're receiving deliveries
3. Enter your ID (provided by your team)
4. Click "Access Dashboard"

### Vendor Dashboard

**View Loads:**
- See all your posted loads
- Check status (assigned, in transit, delivered)
- View driver assignments

**Generate QR Codes:**
1. Click on a load
2. Click "Generate Pickup QR"
3. QR code will be displayed
4. Driver scans this at pickup location

**Track Verifications:**
- See when driver picks up load
- See when receiver gets delivery
- View AI confidence scores
- Check verification history

### Receiver Dashboard

**Scan QR Codes:**
1. Click "Start Scanning"
2. Allow camera access
3. Scan driver's QR code
4. System verifies driver identity
5. Confirmation displayed

**View Incoming Loads:**
- See loads being delivered to you
- Check driver details
- View estimated arrival

---

## 🔧 Troubleshooting

### Cannot Connect to Backend

**Error:** "Network Error" or "Cannot connect"

**Solutions:**
1. Check if main server is running (ask your team)
2. Verify IP address in `.env` file
3. Make sure you're on the same WiFi network
4. Try pinging the server:
   ```bash
   ping SERVER_IP
   ```

### No Loads Showing

**Possible reasons:**
- No loads have been created yet
- Backend connection issue
- Wrong vendor ID

**Solutions:**
1. Ask team to create test loads
2. Check backend connection
3. Verify your vendor ID

### QR Scanner Not Working

**Solutions:**
1. Use Chrome browser (recommended)
2. Allow camera permissions
3. Ensure good lighting
4. Hold QR code steady

### Port Already in Use

**Error:** "Port 5174 is already in use"

**Solution:**
```bash
# Kill the process
netstat -ano | findstr :5174
taskkill /PID <PID> /F

# Or use a different port
npm run dev -- --port 5175
```

---

## 📱 Features

### Real-Time Updates
- Loads update automatically
- Notifications appear instantly
- Status changes sync immediately

### AI Verification
- Driver identity verified automatically
- Location checked (within 100m)
- Confidence scores displayed
- Anomaly detection

### Multi-Channel Notifications
- In-app notifications
- Email alerts (if configured)
- SMS alerts (if configured)
- Priority-based delivery

---

## 🔒 Security

### QR Codes
- Expire after 24 hours
- One-time use only
- Location-verified
- Cannot be reused

### Data Privacy
- All data encrypted in transit
- Secure API connections
- No data stored locally
- Complete audit trail

---

## 📞 Support

### Common Issues

**Q: Can I use this offline?**
A: No, you need internet connection to the main server.

**Q: Can I use this on mobile?**
A: Yes! Open http://localhost:5174 on your phone's browser (if on same WiFi).

**Q: How do I get a vendor ID?**
A: Ask your team administrator to create one for you.

**Q: Can multiple people use the same vendor ID?**
A: Yes, but it's not recommended for security reasons.

### Contact

- **Technical Issues**: Contact your team's tech lead
- **Account Issues**: Contact your administrator
- **Feature Requests**: Submit via your team's process

---

## 🎓 Training Videos

(Ask your team for training materials)

---

## 📊 System Status

Check if the backend is running:
- Main Backend: http://SERVER_IP:8000/health
- Verification Backend: http://SERVER_IP:8001/health

Both should return: `{"status": "healthy"}`

---

## 🔄 Updates

To get the latest version:

```bash
# Pull latest changes
git pull origin vendor-receiver-system

# Reinstall dependencies (if needed)
npm install

# Restart the app
npm run dev
```

---

## ✅ Quick Checklist

Before starting work:
- [ ] Node.js installed
- [ ] Dependencies installed (`npm install`)
- [ ] `.env` file created with correct IP
- [ ] Backend server is running (ask team)
- [ ] Can access http://localhost:5174
- [ ] Can login with your ID
- [ ] Can see test loads

---

**You're all set! Happy verifying! 🚀**
