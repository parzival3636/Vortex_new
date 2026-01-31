# Shared Database Setup Guide

## Problem
You want to push only the vendor/receiver system to GitHub for your friend, but both systems need to share the same database for loads, drivers, and verifications.

---

## 🎯 Solution: Centralized API Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    CENTRALIZED BACKEND                           │
│              (Your Laptop or Cloud Server)                       │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  Main Backend (Port 8000)                              │    │
│  │  - Loads API                                           │    │
│  │  - Drivers API                                         │    │
│  │  - Vendors API                                         │    │
│  │  - ChromaDB (loads, drivers, trucks, vendors)          │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  Verification Backend (Port 8001)                      │    │
│  │  - QR Generation API                                   │    │
│  │  - QR Verification API                                 │    │
│  │  - Receivers API                                       │    │
│  │  - ChromaDB (qr_codes, verifications, receivers)       │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                            ↑                    ↑
                            │                    │
                    API Calls (HTTP)      API Calls (HTTP)
                            │                    │
        ┌───────────────────┴────────┬───────────┴──────────────┐
        │                            │                           │
┌───────────────────┐    ┌───────────────────┐    ┌────────────────────┐
│  Your Laptop      │    │  Friend's Laptop  │    │  Mobile Apps       │
│  (Driver App)     │    │  (Vendor App)     │    │  (Future)          │
├───────────────────┤    ├───────────────────┤    ├────────────────────┤
│ Frontend (5173)   │    │ Frontend (5174)   │    │ React Native       │
│ - Driver Dashboard│    │ - Vendor Dashboard│    │ - Driver App       │
│ - Owner Dashboard │    │ - Receiver Dash   │    │ - Vendor App       │
└───────────────────┘    └───────────────────┘    └────────────────────┘
```

---

## 📦 Step 1: Create Separate Git Branch for Vendor System

### On Your Laptop:

```bash
# Navigate to your project
cd E:\Vortexfinal

# Create a new branch for vendor system
git checkout -b vendor-receiver-system

# Remove everything except vendor/receiver folders
# (Don't worry, main branch still has everything)

# Keep only these folders:
# - verification_backend/
# - verification_webapp/
# - Documentation for vendor system

# Create a .gitignore for the branch
cat > .gitignore << EOF
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
*.egg-info/
dist/
build/

# Node
node_modules/
npm-debug.log
yarn-error.log
.env.local

# Database (don't share local data)
verification_data/
*.sqlite3
chroma_data/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db
EOF

# Commit the vendor system
git add verification_backend/ verification_webapp/ *.md
git commit -m "Vendor/Receiver QR Verification System"

# Push to GitHub
git push origin vendor-receiver-system
```

---

## 🔧 Step 2: Configure for Shared Database

### Create Shared Configuration

Create `verification_backend/config_shared.py`:

```python
"""
Shared configuration for connecting to centralized backend
"""
import os

# Centralized backend URL (your laptop's IP or cloud server)
MAIN_BACKEND_URL = os.getenv("MAIN_BACKEND_URL", "http://192.168.1.100:8000")
VERIFICATION_BACKEND_URL = os.getenv("VERIFICATION_BACKEND_URL", "http://192.168.1.100:8001")

# For cloud deployment
# MAIN_BACKEND_URL = "https://your-app.herokuapp.com"
# VERIFICATION_BACKEND_URL = "https://your-verification.herokuapp.com"
```

### Update Frontend API Configuration

Update `verification_webapp/src/services/api.js`:

```javascript
// Get backend URL from environment or use default
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001/api/v1';
const MAIN_API_URL = import.meta.env.VITE_MAIN_API_URL || 'http://localhost:8000/api/v1';

// For your friend's laptop, they'll set:
// VITE_API_URL=http://YOUR_LAPTOP_IP:8001/api/v1
// VITE_MAIN_API_URL=http://YOUR_LAPTOP_IP:8000/api/v1
```

---

## 🌐 Step 3: Setup Options

### Option A: Your Laptop as Server (Easiest)

**On Your Laptop (Server):**

1. **Find your IP address:**
   ```bash
   # Windows
   ipconfig
   # Look for IPv4 Address (e.g., 192.168.1.100)
   ```

2. **Start both backends:**
   ```bash
   # Terminal 1: Main backend
   python main.py
   # Runs on 0.0.0.0:8000 (accessible from network)

   # Terminal 2: Verification backend
   cd verification_backend
   python run.py
   # Runs on 0.0.0.0:8001 (accessible from network)
   ```

3. **Configure Windows Firewall:**
   ```powershell
   # Allow ports 8000 and 8001
   netsh advfirewall firewall add rule name="Main Backend" dir=in action=allow protocol=TCP localport=8000
   netsh advfirewall firewall add rule name="Verification Backend" dir=in action=allow protocol=TCP localport=8001
   ```

**On Friend's Laptop (Client):**

1. **Clone the vendor branch:**
   ```bash
   git clone -b vendor-receiver-system https://github.com/yourusername/yourrepo.git
   cd yourrepo
   ```

2. **Create `.env` file:**
   ```bash
   cd verification_webapp
   cat > .env << EOF
   VITE_API_URL=http://192.168.1.100:8001/api/v1
   VITE_MAIN_API_URL=http://192.168.1.100:8000/api/v1
   EOF
   ```

3. **Install and run:**
   ```bash
   npm install
   npm run dev
   # Opens on http://localhost:5174
   ```

**Now both laptops share the same database!**

---

### Option B: Cloud Database (Production Ready)

Use a cloud service to host the backend:

**1. Deploy to Heroku/Railway/Render:**

```bash
# On your laptop
cd E:\Vortexfinal

# Deploy main backend
heroku create your-logistics-backend
git push heroku main

# Deploy verification backend
cd verification_backend
heroku create your-verification-backend
git push heroku vendor-receiver-system
```

**2. Update environment variables:**

Your laptop:
```env
MAIN_BACKEND_URL=https://your-logistics-backend.herokuapp.com
VERIFICATION_BACKEND_URL=https://your-verification-backend.herokuapp.com
```

Friend's laptop:
```env
VITE_API_URL=https://your-verification-backend.herokuapp.com/api/v1
VITE_MAIN_API_URL=https://your-logistics-backend.herokuapp.com/api/v1
```

---

## 📝 Step 4: Create README for Friend

Create `verification_webapp/README_SETUP.md`:

```markdown
# Vendor/Receiver System Setup

## Prerequisites
- Node.js 16+
- Internet connection to main backend

## Installation

1. Clone this repository:
   \`\`\`bash
   git clone -b vendor-receiver-system <repo-url>
   cd verification_webapp
   \`\`\`

2. Install dependencies:
   \`\`\`bash
   npm install
   \`\`\`

3. Create `.env` file:
   \`\`\`bash
   VITE_API_URL=http://MAIN_SERVER_IP:8001/api/v1
   VITE_MAIN_API_URL=http://MAIN_SERVER_IP:8000/api/v1
   \`\`\`
   
   Replace `MAIN_SERVER_IP` with the IP address provided by your team.

4. Start the app:
   \`\`\`bash
   npm run dev
   \`\`\`

5. Open browser:
   \`\`\`
   http://localhost:5174
   \`\`\`

## Usage

- Login as vendor: Use vendor ID provided
- View loads from shared database
- Generate QR codes for pickup
- Track verifications in real-time

## Troubleshooting

**Cannot connect to backend:**
- Check if main server is running
- Verify IP address in `.env`
- Check firewall settings
- Ping the server: `ping MAIN_SERVER_IP`

**No loads showing:**
- Loads are created in the main system (driver app)
- Ask your team to create test loads
- Check API connection: `http://MAIN_SERVER_IP:8000/docs`
\`\`\`

---

## 🔄 Data Flow

### When Vendor Posts a Load:

```
Friend's Laptop (Vendor App)
    ↓
    POST /api/v1/loads
    ↓
Your Laptop (Main Backend)
    ↓
    Store in ChromaDB
    ↓
    ✓ Load available for drivers
```

### When Driver Accepts Load:

```
Your Laptop (Driver App)
    ↓
    POST /api/v1/loads/{id}/assign
    ↓
Your Laptop (Main Backend)
    ↓
    Update ChromaDB
    ↓
    Trigger QR generation
    ↓
Your Laptop (Verification Backend)
    ↓
    Generate QR code
    ↓
    Notify vendor (Friend's laptop)
```

### When Vendor Generates QR:

```
Friend's Laptop (Vendor Dashboard)
    ↓
    Click "Generate Pickup QR"
    ↓
Your Laptop (Verification Backend)
    ↓
    Create QR in ChromaDB
    ↓
    Return QR to vendor dashboard
    ↓
Friend's Laptop displays QR
```

---

## 🧪 Testing the Setup

### Test 1: Check Backend Connection

On friend's laptop:
```bash
# Test main backend
curl http://YOUR_LAPTOP_IP:8000/health

# Test verification backend
curl http://YOUR_LAPTOP_IP:8001/health
```

### Test 2: Create Load from Driver App

On your laptop:
1. Open driver dashboard
2. Create a test load
3. Check if it appears in vendor dashboard on friend's laptop

### Test 3: Generate QR from Vendor App

On friend's laptop:
1. Open vendor dashboard
2. Click "Generate Pickup QR"
3. QR should be stored in your laptop's database
4. Check verification status

---

## 📊 Database Synchronization

Both systems share the same database because:

1. **Main Backend (Port 8000)** has:
   - Loads database
   - Drivers database
   - Vendors database
   - Trucks database

2. **Verification Backend (Port 8001)** has:
   - QR codes database
   - Verifications database
   - Receivers database

3. **Both frontends** connect to these backends via API calls

**No data duplication!** Everything is centralized.

---

## 🔒 Security Considerations

### For Local Network:
- Use strong WiFi password
- Enable firewall rules
- Use VPN if on different networks

### For Cloud Deployment:
- Use HTTPS
- Add API authentication
- Use environment variables for secrets
- Enable CORS only for trusted origins

---

## 📱 Future: Mobile Apps

Same architecture works for mobile apps:

```javascript
// React Native app
const API_URL = 'http://YOUR_SERVER_IP:8001/api/v1';

// Or cloud
const API_URL = 'https://your-backend.herokuapp.com/api/v1';
```

---

## 🎯 Summary

✅ **Vendor system** on separate Git branch
✅ **Shared database** via centralized backend
✅ **Both laptops** connect to same API
✅ **Real-time sync** - changes visible to both
✅ **Scalable** - add more clients easily
✅ **Cloud-ready** - deploy to Heroku/AWS later

**Your friend only needs the frontend, connects to your backend!**
