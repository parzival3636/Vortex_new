# Windows Installation Guide - QR Verification System

## Issue: Rust Compilation Error

If you're getting errors about Rust/Cargo when installing dependencies, use this simplified approach.

---

## Option 1: Use Simplified Requirements (Recommended for Windows)

### Step 1: Install Simplified Dependencies

```bash
cd verification_backend
pip install -r requirements-simple.txt
```

This installs:
- FastAPI (web framework)
- Uvicorn (server)
- Pydantic (data validation)
- Python-multipart (file uploads)

**Note**: This uses in-memory storage instead of ChromaDB (no Rust compilation needed).

### Step 2: Start Backend

```bash
python main_verification.py
```

Backend will run on: http://localhost:8001

---

## Option 2: Install Full Requirements (with ChromaDB)

If you want to use ChromaDB (persistent storage), you need to install Rust first.

### Step 1: Install Rust

Download and install from: https://rustup.rs/

Or use this command in PowerShell:
```powershell
Invoke-WebRequest -Uri https://win.rustup.rs/x86_64 -OutFile rustup-init.exe
.\rustup-init.exe
```

Restart your terminal after installation.

### Step 2: Verify Rust Installation

```bash
rustc --version
cargo --version
```

### Step 3: Install Full Requirements

```bash
cd verification_backend
pip install -r requirements.txt
```

---

## Frontend Installation (Same for Both Options)

### Step 1: Install Node Dependencies

```bash
cd verification_webapp
npm install
```

### Step 2: Start Frontend

```bash
npm run dev
```

Frontend will run on: http://localhost:5174

---

## Quick Test

### Test Backend

```bash
# Open browser
http://localhost:8001/docs
```

You should see the API documentation.

### Test Frontend

```bash
# Open browser
http://localhost:5174
```

You should see the landing page.

---

## Differences Between Options

| Feature | Simplified (Option 1) | Full (Option 2) |
|---------|----------------------|-----------------|
| Installation | Easy, no Rust needed | Requires Rust |
| Storage | In-memory (resets on restart) | Persistent (ChromaDB) |
| Performance | Fast | Fast |
| Production Ready | No (data lost on restart) | Yes |
| Development | Perfect | Perfect |

**Recommendation**: Use Option 1 for development and testing. Use Option 2 for production.

---

## Troubleshooting

### Issue: "pip install" fails

**Solution**: Make sure you're using Python 3.8 or higher
```bash
python --version
```

### Issue: "npm install" fails

**Solution**: Make sure you have Node.js 16 or higher
```bash
node --version
npm --version
```

### Issue: Port already in use

**Solution**: Kill the process using the port
```bash
# For port 8001 (backend)
netstat -ano | findstr :8001
taskkill /PID <PID> /F

# For port 5174 (frontend)
netstat -ano | findstr :5174
taskkill /PID <PID> /F
```

---

## Running the System

### Start Backend (Terminal 1)
```bash
cd verification_backend
python main_verification.py
```

### Start Frontend (Terminal 2)
```bash
cd verification_webapp
npm run dev
```

### Run Tests (Terminal 3)
```bash
python test_qr_verification_flow.py
```

---

## What Works with Simplified Version

✅ All API endpoints
✅ QR generation
✅ QR verification
✅ AI Verification Agent
✅ AI Notification Agent
✅ All dashboards
✅ Complete workflow

❌ Data persistence (data lost on restart)

**For development and testing, the simplified version is perfect!**

---

## Upgrading to Full Version Later

When you're ready for production:

1. Install Rust (see Option 2)
2. Install full requirements:
   ```bash
   pip install chromadb==0.4.22
   ```
3. Update imports in code (already done - automatic fallback)
4. Restart backend

That's it! The system will automatically use ChromaDB if available.

---

## Next Steps

1. ✅ Install dependencies (Option 1 or 2)
2. ✅ Start backend and frontend
3. ✅ Open http://localhost:5174
4. ✅ Test the system
5. ✅ Read `START_VERIFICATION_SYSTEM.md` for usage guide

---

**You're ready to go!** 🚀
