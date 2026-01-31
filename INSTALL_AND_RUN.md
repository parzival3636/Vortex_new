# 🚀 Install and Run - Complete Guide

## ⚡ Super Quick Start (5 Minutes)

### Step 1: Install Backend Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Seed Database

```bash
python seed_chromadb.py
```

### Step 3: Start Backend

```bash
python main.py
```

Keep this terminal open. Backend runs on **http://localhost:8000**

### Step 4: Install Frontend (New Terminal)

```bash
cd frontend
npm install
```

### Step 5: Start Frontend

```bash
npm run dev
```

Frontend runs on **http://localhost:3000**

### Step 6: Open Browser

Go to: **http://localhost:3000**

**Done! 🎉**

---

## 📋 Detailed Installation

### Prerequisites

- Python 3.11+
- Node.js 16+
- Ollama (for AI features)

### Backend Setup

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env

# 3. Seed database with sample data
python seed_chromadb.py

# 4. Test backend
python test_system.py

# 5. Start backend server
python main.py
```

**Verify backend:**
- Open: http://localhost:8000
- Should see: `{"message":"Deadheading Optimization System API"...}`

### Frontend Setup

```bash
# 1. Navigate to frontend
cd frontend

# 2. Install dependencies
npm install

# 3. Start development server
npm run dev
```

**Verify frontend:**
- Open: http://localhost:3000
- Should see landing page with 3 dashboards

---

## 🎯 Test Each Feature

### Test 1: Driver Dashboard

```bash
# 1. Open http://localhost:3000/driver

# 2. Enter origin: "Delhi"
# 3. Select from dropdown

# 4. Enter destination: "Jaipur"
# 5. Select from dropdown

# 6. Click "Find Return Loads"

# Expected: See loads on map with profitability
```

### Test 2: Vendor Dashboard

```bash
# 1. Open http://localhost:3000/vendor

# 2. Click "Post New Load"

# 3. Enter:
#    - Pickup: "Azadpur Mandi, Delhi"
#    - Destination: "Jaipur"
#    - Weight: 5000
#    - Price: 12000

# 4. Click "Post Load"

# Expected: Load appears on map
```

### Test 3: Owner Dashboard

```bash
# 1. Open http://localhost:3000/owner

# 2. See all trucks on map

# 3. Click a truck in the list

# Expected: Map zooms to truck, shows route
```

---

## 🐛 Common Issues & Solutions

### Issue: "pip: command not found"

**Solution:**
```bash
# Install Python from python.org
# Or use:
python -m pip install -r requirements.txt
```

### Issue: "npm: command not found"

**Solution:**
```bash
# Install Node.js from nodejs.org
# Verify:
node --version
npm --version
```

### Issue: "Port 8000 already in use"

**Solution:**
```bash
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:8000 | xargs kill -9
```

### Issue: "Port 3000 already in use"

**Solution:**
```bash
# Change port in frontend/vite.config.js:
server: { port: 3001 }
```

### Issue: "Module not found"

**Backend:**
```bash
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Issue: "Map not showing"

**Solution:**
1. Check browser console for errors
2. Verify backend is running
3. Check network tab for API calls
4. Ensure Leaflet CSS is loaded

### Issue: "Autocomplete not working"

**Solution:**
1. Type at least 3 characters
2. Wait 1 second for results
3. Check backend is running
4. Verify OpenStreetMap API is accessible

---

## 📦 What Gets Installed

### Backend (Python)

```
fastapi          - Web framework
uvicorn          - ASGI server
chromadb         - Embedded database
crewai           - AI agents
requests         - HTTP client
pydantic         - Data validation
```

### Frontend (Node.js)

```
react            - UI framework
react-router-dom - Routing
react-leaflet    - Maps
leaflet          - OpenStreetMap
axios            - HTTP client
tailwindcss      - Styling
recharts         - Charts
lucide-react     - Icons
```

---

## 🔧 Configuration

### Backend (.env)

```env
# ChromaDB
CHROMA_PERSIST_DIRECTORY=./chroma_data

# Ollama (Local LLM)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b

# OpenAI (dummy for CrewAI)
OPENAI_API_KEY=dummy-key-not-used

# App Settings
APP_ENV=development
DEBUG=True
```

### Frontend (vite.config.js)

```javascript
server: {
  port: 3000,
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true
    }
  }
}
```

---

## 📊 Verify Installation

### Backend Health Check

```bash
curl http://localhost:8000/health
# Expected: {"status":"healthy"}
```

### Frontend Health Check

```bash
curl http://localhost:3000
# Expected: HTML page
```

### API Test

```bash
curl http://localhost:8000/api/v1/loads/available
# Expected: JSON array of loads
```

---

## 🚀 Production Deployment

### Backend (Railway/Render)

```bash
# 1. Create account on Railway/Render

# 2. Connect GitHub repo

# 3. Set environment variables:
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
CHROMA_PERSIST_DIRECTORY=./chroma_data

# 4. Deploy
```

### Frontend (Vercel/Netlify)

```bash
# 1. Build frontend
cd frontend
npm run build

# 2. Deploy to Vercel
npm install -g vercel
vercel deploy --prod

# 3. Set environment variable:
VITE_API_URL=https://your-backend.com/api/v1
```

---

## 📁 Directory Structure

```
project/
├── backend/
│   ├── api/              # API endpoints
│   ├── agents/           # AI agents
│   ├── services/         # Business logic
│   ├── models/           # Data models
│   ├── main.py           # Entry point
│   └── requirements.txt  # Dependencies
│
├── frontend/
│   ├── src/
│   │   ├── components/   # Reusable components
│   │   ├── pages/        # Dashboard pages
│   │   ├── services/     # API calls
│   │   └── App.jsx       # Main app
│   ├── package.json      # Dependencies
│   └── vite.config.js    # Configuration
│
└── chroma_data/          # Database (auto-created)
```

---

## 🎓 Learning Path

### Day 1: Setup
- Install dependencies
- Run backend and frontend
- Test all dashboards

### Day 2: Explore Code
- Read backend API code
- Understand frontend components
- Study map integration

### Day 3: Customize
- Change colors and styles
- Add new features
- Modify UI components

### Day 4: Deploy
- Build for production
- Deploy to cloud
- Test live system

---

## 📚 Documentation

- **Complete Guide**: `COMPLETE_SYSTEM_GUIDE.md`
- **Frontend Setup**: `FRONTEND_SETUP.md`
- **API Docs**: `API_DOCUMENTATION.md`
- **How It Works**: `HOW_IT_WORKS.md`
- **Vendor Guide**: `VENDOR_GUIDE.md`

---

## ✅ Installation Checklist

### Backend
- [ ] Python 3.11+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Database seeded (`python seed_chromadb.py`)
- [ ] Backend running (`python main.py`)
- [ ] Health check passes (`curl http://localhost:8000/health`)

### Frontend
- [ ] Node.js 16+ installed
- [ ] Dependencies installed (`npm install`)
- [ ] Frontend running (`npm run dev`)
- [ ] Landing page loads (`http://localhost:3000`)
- [ ] All dashboards accessible

### Features
- [ ] Driver dashboard works
- [ ] Vendor dashboard works
- [ ] Owner dashboard works
- [ ] Maps display correctly
- [ ] Autocomplete works
- [ ] API calls succeed

---

## 🎯 Quick Commands

```bash
# Backend
python main.py                    # Start backend
python seed_chromadb.py          # Seed database
python test_system.py            # Run tests
python demo_automation.py        # Run demo

# Frontend
cd frontend
npm install                      # Install dependencies
npm run dev                      # Start dev server
npm run build                    # Build for production

# Both
# Terminal 1: python main.py
# Terminal 2: cd frontend && npm run dev
```

---

## 💡 Pro Tips

1. **Use two terminals** - One for backend, one for frontend
2. **Check browser console** - For frontend errors
3. **Check terminal output** - For backend errors
4. **Use API docs** - http://localhost:8000/docs
5. **Read error messages** - They usually tell you what's wrong

---

## 📞 Need Help?

1. **Check documentation** - Read the guides
2. **Search errors** - Google the error message
3. **Check issues** - Look at GitHub issues
4. **Ask community** - Post on Stack Overflow
5. **Contact support** - Create GitHub issue

---

**Installation complete! Start building! 🚀**
