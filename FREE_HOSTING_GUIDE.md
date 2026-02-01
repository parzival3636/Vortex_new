# 🚀 Free Hosting Guide - Complete Setup

## ✅ Your System is Ready for FREE Hosting!

**What you have:**
- ✅ Groq AI (cloud-based, no server needed)
- ✅ ChromaDB (file-based, persistent storage)
- ✅ FastAPI backend
- ✅ React frontend

**Total Monthly Cost: $0** 🎉

---

## 📋 Prerequisites

1. GitHub account
2. Render.com account (free)
3. Vercel account (free)
4. Your code pushed to GitHub

---

## 🎯 Deployment Steps

### **Part 1: Backend Deployment (Render.com)**

#### Step 1: Push to GitHub
```bash
git add .
git commit -m "Ready for deployment with Groq and ChromaDB"
git push origin main
```

#### Step 2: Deploy to Render.com

1. **Go to:** https://render.com
2. **Sign up/Login** (free account)
3. **Click:** "New +" → "Web Service"
4. **Connect GitHub:** Authorize Render to access your repo
5. **Select your repository**
6. **Configure:**
   - **Name:** `deadheading-backend` (or your choice)
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free

7. **Add Environment Variables:**
   Click "Advanced" → "Add Environment Variable"
   
   ```
   GROQ_API_KEY = your_groq_api_key_here
   GROQ_MODEL = llama-3.1-8b-instant
   CHROMA_PERSIST_DIRECTORY = /opt/render/project/src/data/chroma_data
   APP_ENV = production
   DEBUG = False
   ```

8. **Add Persistent Disk (IMPORTANT!):**
   - Scroll to "Disks"
   - Click "Add Disk"
   - **Name:** `chroma-data`
   - **Mount Path:** `/opt/render/project/src/data`
   - **Size:** 1 GB (FREE!)
   - Click "Save"

9. **Click "Create Web Service"**

10. **Wait 5-10 minutes** for deployment

11. **Your backend URL:** `https://deadheading-backend.onrender.com`

#### ✅ Verify Backend:
```bash
curl https://your-backend-url.onrender.com/health
# Should return: {"status":"healthy"}

curl https://your-backend-url.onrender.com/
# Should show: "llm":"Groq (llama-3.1-8b-instant)"
```

---

### **Part 2: Frontend Deployment (Vercel)**

#### Step 1: Update Frontend API URL

Edit `frontend/src/services/api.js`:
```javascript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://your-backend-url.onrender.com';
```

#### Step 2: Deploy to Vercel

1. **Go to:** https://vercel.com
2. **Sign up/Login** (free account)
3. **Click:** "Add New" → "Project"
4. **Import your GitHub repository**
5. **Configure:**
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`

6. **Add Environment Variable:**
   ```
   VITE_API_URL = https://your-backend-url.onrender.com
   ```

7. **Click "Deploy"**

8. **Wait 2-3 minutes**

9. **Your frontend URL:** `https://your-app.vercel.app`

#### ✅ Verify Frontend:
Open `https://your-app.vercel.app` in browser
- Should load your React app
- Should connect to backend API

---

## 🗄️ ChromaDB Persistence - How It Works

### **On Render.com:**

```
Your Backend Container
├── /opt/render/project/src/
│   ├── main.py
│   ├── agents/
│   ├── api/
│   └── data/  ← PERSISTENT DISK MOUNTED HERE
│       └── chroma_data/  ← YOUR DATABASE
│           ├── chroma.sqlite3
│           └── [all your data collections]
```

### **What Happens:**

1. **First Deploy:**
   - Render creates persistent disk
   - ChromaDB initializes empty database
   - You seed data: `python seed_demo_data.py`

2. **On Restart/Redeploy:**
   - Container restarts
   - Persistent disk remounts
   - **All data is still there!** ✅
   - No data loss

3. **Data Persistence:**
   - ✅ Survives restarts
   - ✅ Survives redeployments
   - ✅ Survives crashes
   - ✅ Backed up by Render

---

## 📊 Free Tier Limits

### **Render.com (Backend)**
| Feature | Free Tier | Your Usage | Status |
|---------|-----------|------------|--------|
| RAM | 512 MB | ~200 MB | ✅ OK |
| CPU | Shared | Light | ✅ OK |
| Disk | 1 GB | ~50 MB | ✅ OK |
| Bandwidth | 100 GB/mo | ~10 GB | ✅ OK |
| Sleep | After 15 min | Wakes in 30s | ⚠️ Acceptable |

**Note:** Free tier sleeps after 15 min inactivity. First request takes ~30s to wake up.

### **Vercel (Frontend)**
| Feature | Free Tier | Your Usage | Status |
|---------|-----------|------------|--------|
| Bandwidth | 100 GB/mo | ~5 GB | ✅ OK |
| Builds | 6000 min/mo | ~10 min | ✅ OK |
| Deployments | Unlimited | Unlimited | ✅ OK |

### **Groq (AI)**
| Feature | Free Tier | Your Usage | Status |
|---------|-----------|------------|--------|
| Requests | 30/min | ~5/min | ✅ OK |
| Tokens | 14,400/min | ~1000/min | ✅ OK |

---

## 🔧 Post-Deployment Setup

### **Seed Your Database:**

1. **SSH into Render (optional):**
   - Go to Render dashboard
   - Click your service
   - Click "Shell" tab
   - Run: `python seed_demo_data.py`

2. **Or use API to add data:**
   ```bash
   # Create owner
   curl -X POST https://your-backend.onrender.com/api/v1/owners \
     -H "Content-Type: application/json" \
     -d '{"name":"Test Owner","email":"owner@test.com"}'
   
   # Create vendor
   curl -X POST https://your-backend.onrender.com/api/v1/vendors \
     -H "Content-Type: application/json" \
     -d '{"name":"Test Vendor","email":"vendor@test.com","phone":"1234567890","location":{"lat":19.076,"lng":72.8777}}'
   ```

---

## 🎯 Testing Your Deployment

### **Test Backend:**
```bash
# Health check
curl https://your-backend.onrender.com/health

# Check Groq integration
curl https://your-backend.onrender.com/

# Test API endpoints
curl https://your-backend.onrender.com/api/v1/vendors
```

### **Test Frontend:**
1. Open `https://your-app.vercel.app`
2. Check browser console for errors
3. Test navigation
4. Test API calls

---

## 🐛 Troubleshooting

### **Backend Issues:**

**Problem:** Service won't start
```bash
# Check logs in Render dashboard
# Look for:
- Missing dependencies
- Environment variable errors
- Port binding issues
```

**Problem:** ChromaDB data not persisting
```bash
# Verify disk is mounted:
# In Render Shell:
ls -la /opt/render/project/src/data/
# Should show chroma_data folder
```

**Problem:** Groq API errors
```bash
# Check environment variables
# Verify GROQ_API_KEY is set correctly
# Test API key: https://console.groq.com
```

### **Frontend Issues:**

**Problem:** Can't connect to backend
```bash
# Check VITE_API_URL is set correctly
# Verify backend is running
# Check CORS settings in main.py
```

**Problem:** Build fails
```bash
# Check Node version (should be 18+)
# Verify package.json is correct
# Check build logs in Vercel
```

---

## 📈 Monitoring

### **Render Dashboard:**
- View logs in real-time
- Monitor CPU/RAM usage
- Check disk usage
- View request metrics

### **Vercel Dashboard:**
- View deployment logs
- Monitor bandwidth
- Check build times
- View analytics

### **Groq Console:**
- Monitor API usage
- Check rate limits
- View request logs
- https://console.groq.com

---

## 💰 Cost Breakdown

| Service | Plan | Cost | What You Get |
|---------|------|------|--------------|
| **Render.com** | Free | $0 | Backend + 1GB disk |
| **Vercel** | Free | $0 | Frontend hosting |
| **Groq** | Free | $0 | AI API (30 req/min) |
| **GitHub** | Free | $0 | Code hosting |
| **TOTAL** | | **$0/month** | Full production app! |

---

## 🚀 Upgrade Path (Optional)

### **If you outgrow free tier:**

**Render.com:**
- Starter: $7/month
  - No sleep
  - 512 MB RAM
  - Faster CPU

**Vercel:**
- Pro: $20/month
  - More bandwidth
  - Priority support

**Groq:**
- Pay-as-you-go
  - $0.10 per 1M tokens
  - Higher rate limits

---

## ✅ Deployment Checklist

### **Before Deployment:**
- [ ] Code pushed to GitHub
- [ ] `.env` file NOT committed (use .gitignore)
- [ ] `render.yaml` created
- [ ] Frontend API URL configurable
- [ ] Dependencies in requirements.txt

### **Backend Deployment:**
- [ ] Render account created
- [ ] Repository connected
- [ ] Environment variables set
- [ ] Persistent disk added (1GB)
- [ ] Service deployed successfully
- [ ] Health check passing

### **Frontend Deployment:**
- [ ] Vercel account created
- [ ] Repository connected
- [ ] API URL environment variable set
- [ ] Build successful
- [ ] Site accessible

### **Post-Deployment:**
- [ ] Backend API responding
- [ ] Frontend loading
- [ ] API calls working
- [ ] ChromaDB data persisting
- [ ] Groq AI working

---

## 🎉 Success!

Your app is now live and FREE:
- ✅ Backend: `https://your-backend.onrender.com`
- ✅ Frontend: `https://your-app.vercel.app`
- ✅ Database: ChromaDB (persistent)
- ✅ AI: Groq (cloud)
- ✅ Cost: $0/month

---

## 📞 Support

**Render Issues:**
- Docs: https://render.com/docs
- Community: https://community.render.com

**Vercel Issues:**
- Docs: https://vercel.com/docs
- Support: https://vercel.com/support

**Groq Issues:**
- Docs: https://console.groq.com/docs
- Discord: https://discord.gg/groq

---

*Last Updated: February 1, 2026*
*Status: Ready for Deployment*
*Cost: $0/month*
