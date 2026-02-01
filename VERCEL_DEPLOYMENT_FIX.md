# 🔧 Vercel Deployment Fix

## Error: Permission denied on vite

**Error message:**
```
sh: line 1: /vercel/path0/node_modules/.bin/vite: Permission denied
Error: Command "npm run build" exited with 126
```

---

## ✅ Solution: Configure Vercel Correctly

The issue is that Vercel is trying to build from the root directory, but your frontend is in the `frontend/` subdirectory.

### **Option 1: Configure in Vercel Dashboard (RECOMMENDED)**

1. **Go to your Vercel project settings**
2. **Click "Settings" → "General"**
3. **Configure these settings:**

   **Root Directory:**
   ```
   frontend
   ```

   **Build Command:**
   ```
   npm run build
   ```

   **Output Directory:**
   ```
   dist
   ```

   **Install Command:**
   ```
   npm install
   ```

4. **Click "Save"**
5. **Redeploy:** Go to "Deployments" → Click "..." → "Redeploy"

---

### **Option 2: Use vercel.json (Alternative)**

Create `vercel.json` in the **root** of your project:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "frontend/package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "dist"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/frontend/$1"
    }
  ]
}
```

Then add this to `frontend/package.json`:

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "vercel-build": "vite build"
  }
}
```

---

### **Option 3: Deploy Only Frontend Folder**

1. **Create a separate GitHub repo** for just the frontend
2. **Copy `frontend/` contents to new repo**
3. **Deploy that repo to Vercel**

This is the cleanest approach for monorepo projects.

---

## 🎯 Recommended Approach

**Use Option 1** - It's the easiest and most reliable:

1. Set **Root Directory** to `frontend` in Vercel dashboard
2. Vercel will automatically detect it's a Vite project
3. Build will work correctly

---

## 📝 Step-by-Step Fix

### Step 1: Go to Vercel Dashboard
- Open your project
- Click "Settings"

### Step 2: Update Root Directory
- Scroll to "Root Directory"
- Enter: `frontend`
- Click "Save"

### Step 3: Verify Build Settings
- **Framework Preset:** Vite (should auto-detect)
- **Build Command:** `npm run build` (default)
- **Output Directory:** `dist` (default)
- **Install Command:** `npm install` (default)

### Step 4: Redeploy
- Go to "Deployments" tab
- Click latest deployment
- Click "..." menu
- Click "Redeploy"

---

## ✅ After Fix

Your build should succeed with output like:
```
✓ built in 3.45s
✓ 125 modules transformed.
dist/index.html                   0.45 kB
dist/assets/index-abc123.css      12.34 kB
dist/assets/index-xyz789.js       145.67 kB
```

---

## 🔍 Troubleshooting

### If build still fails:

**Check Node version:**
- Vercel Settings → "Node.js Version"
- Set to: `18.x` or `20.x`

**Check environment variables:**
- Add `VITE_API_URL` with your backend URL
- Example: `https://your-backend.onrender.com`

**Clear build cache:**
- Vercel Dashboard → Deployments
- Click "..." → "Redeploy" → Check "Clear cache"

---

## 📦 Alternative: Separate Frontend Repo

If you want cleaner deployments:

```bash
# Create new repo for frontend only
cd ..
mkdir vortex-frontend
cd vortex-frontend

# Copy frontend files
cp -r ../Vortexfinal/frontend/* .

# Initialize git
git init
git add .
git commit -m "Initial frontend"

# Push to GitHub
git remote add origin https://github.com/yourusername/vortex-frontend.git
git push -u origin main

# Deploy to Vercel
# Connect this new repo to Vercel
# It will auto-detect Vite and work perfectly
```

---

## 🎉 Success Indicators

After fixing, you should see:
- ✅ Build completes successfully
- ✅ No permission errors
- ✅ Deployment URL works
- ✅ Frontend loads correctly

---

*Fix takes 2 minutes in Vercel dashboard!*
