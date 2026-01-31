# GitHub Branch Setup - Vendor/Receiver System Only

## Quick Guide: Push Only Vendor System to GitHub

### Step 1: Create New Branch

```bash
# Make sure you're in the project root
cd E:\Vortexfinal

# Create and switch to new branch
git checkout -b vendor-receiver-system
```

### Step 2: Keep Only Vendor/Receiver Files

Create a new `.gitignore` for this branch:

```bash
# Create .gitignore
cat > .gitignore << EOF
# Keep only vendor/receiver system
# Ignore main system files
/api/
/agents/
/services/
/models/
/frontend/
/alembic/
/chroma_data/
/tests/
main.py
config.py
db_chromadb.py
redis_client.py
seed_chromadb.py
*.py
!verification_backend/
!verification_webapp/

# Python
__pycache__/
*.pyc
*.pyo
venv/
env/

# Node
node_modules/
.env.local

# Database
verification_data/
*.sqlite3

# IDE
.vscode/
.idea/
EOF
```

### Step 3: Add Only Vendor Files

```bash
# Add vendor/receiver system
git add verification_backend/
git add verification_webapp/
git add SHARED_DATABASE_SETUP.md
git add README_QR_VERIFICATION.md
git add START_VERIFICATION_SYSTEM.md
git add .gitignore

# Commit
git commit -m "Vendor/Receiver QR Verification System - Standalone"
```

### Step 4: Push to GitHub

```bash
# Push the branch
git push origin vendor-receiver-system
```

### Step 5: Share with Friend

Send your friend:
1. **GitHub repo URL** with branch name
2. **Your laptop's IP address** (if using local server)
3. **Setup instructions** (see below)

---

## For Your Friend: Clone and Setup

### Clone the Vendor Branch

```bash
# Clone only the vendor branch
git clone -b vendor-receiver-system https://github.com/YOUR_USERNAME/YOUR_REPO.git vendor-system

cd vendor-system/verification_webapp
```

### Install Dependencies

```bash
npm install
```

### Configure Backend Connection

Create `.env` file:

```bash
# If connecting to your laptop (same WiFi):
VITE_API_URL=http://192.168.1.XXX:8001/api/v1
VITE_MAIN_API_URL=http://192.168.1.XXX:8000/api/v1

# Replace XXX with your laptop's IP address
```

### Start the App

```bash
npm run dev
```

Open: http://localhost:5174

---

## On Your Laptop: Run as Server

### Find Your IP Address

```bash
# Windows
ipconfig
# Look for "IPv4 Address" under your WiFi adapter
# Example: 192.168.1.100
```

### Start Both Backends

```bash
# Terminal 1: Main backend
python main.py
# Should show: Running on http://0.0.0.0:8000

# Terminal 2: Verification backend
cd verification_backend
python run.py
# Should show: Running on http://0.0.0.0:8001
```

### Allow Firewall Access

```powershell
# Run as Administrator
netsh advfirewall firewall add rule name="Logistics Main" dir=in action=allow protocol=TCP localport=8000
netsh advfirewall firewall add rule name="Logistics Verification" dir=in action=allow protocol=TCP localport=8001
```

---

## Testing the Connection

### From Friend's Laptop

```bash
# Test if backends are accessible
curl http://YOUR_IP:8000/health
curl http://YOUR_IP:8001/health

# Should return: {"status": "healthy"}
```

### Test Data Flow

1. **On your laptop (Driver app):**
   - Create a test load
   - Assign to a driver

2. **On friend's laptop (Vendor app):**
   - Open vendor dashboard
   - Should see the load
   - Generate QR code
   - QR stored in your database

3. **Verify:**
   - Both see the same data
   - Changes sync in real-time

---

## Alternative: Cloud Deployment

If you can't keep your laptop running 24/7, deploy to cloud:

### Option 1: Heroku (Free Tier)

```bash
# Install Heroku CLI
# Then:

# Deploy main backend
heroku create your-logistics-main
git push heroku main

# Deploy verification backend
heroku create your-logistics-verification
git subtree push --prefix verification_backend heroku vendor-receiver-system
```

### Option 2: Railway.app (Easy)

1. Go to railway.app
2. Connect GitHub repo
3. Deploy both backends
4. Get URLs
5. Update `.env` files

### Option 3: Render.com (Free)

1. Go to render.com
2. New Web Service
3. Connect GitHub
4. Deploy
5. Get URL

---

## Summary

✅ **Separate branch** with only vendor/receiver code
✅ **Friend clones** the vendor branch
✅ **Your laptop** runs the backend (database)
✅ **Friend's laptop** runs only the frontend
✅ **Both connect** to your backend via network
✅ **Shared database** - all data synchronized

**Your friend doesn't need the main system code, just the vendor frontend!**
