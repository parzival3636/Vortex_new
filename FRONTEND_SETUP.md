# 🎨 Frontend Setup Guide

Complete guide to set up and run the React.js frontend.

## 📋 Prerequisites

- Node.js 16+ installed
- Backend running on port 8000
- npm or yarn package manager

## ⚡ Quick Start

```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install dependencies
npm install

# 3. Start development server
npm run dev
```

Frontend will be available at: **http://localhost:3000**

## 📦 What Gets Installed

The frontend uses these key packages:

### Core
- `react` - UI framework
- `react-dom` - React DOM rendering
- `react-router-dom` - Client-side routing

### Map & Visualization
- `react-leaflet` - React wrapper for Leaflet
- `leaflet` - OpenStreetMap integration
- `leaflet-routing-machine` - Route calculation

### UI & Styling
- `tailwindcss` - Utility-first CSS
- `lucide-react` - Beautiful icons
- `recharts` - Charts and graphs

### API & State
- `axios` - HTTP client
- `react-hot-toast` - Toast notifications

### Build Tools
- `vite` - Fast build tool
- `@vitejs/plugin-react` - React plugin for Vite

## 🚀 Step-by-Step Setup

### Step 1: Install Node.js

**Windows:**
```bash
# Download from: https://nodejs.org/
# Or use Chocolatey:
choco install nodejs
```

**Verify installation:**
```bash
node --version  # Should show v16.0.0 or higher
npm --version   # Should show 8.0.0 or higher
```

### Step 2: Install Dependencies

```bash
cd frontend
npm install
```

This will:
- Download all packages from `package.json`
- Create `node_modules/` directory
- Generate `package-lock.json`

**If you see errors:**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Step 3: Start Backend

**In a separate terminal:**
```bash
# Navigate to root directory
cd ..

# Start backend
python main.py
```

Backend should be running on: http://localhost:8000

### Step 4: Start Frontend

```bash
# In frontend directory
npm run dev
```

You should see:
```
  VITE v5.0.8  ready in 500 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
  ➜  press h to show help
```

### Step 5: Open Browser

Navigate to: **http://localhost:3000**

You should see the landing page with 3 dashboard options.

## 🎯 Testing Each Dashboard

### Test Driver Dashboard

1. Go to http://localhost:3000/driver
2. Enter origin: "Delhi"
3. Select from autocomplete
4. Enter destination: "Jaipur"
5. Select from autocomplete
6. Click "Find Return Loads"
7. See available loads on map
8. Click a load to accept
9. See navigation route

### Test Vendor Dashboard

1. Go to http://localhost:3000/vendor
2. Click "Post New Load"
3. Enter pickup: "Azadpur Mandi, Delhi"
4. Enter destination: "Jaipur"
5. Enter weight: 5000
6. Enter price: 12000
7. Click "Post Load"
8. See load on map

### Test Owner Dashboard

1. Go to http://localhost:3000/owner
2. See all trucks on map
3. Click a truck in the list
4. Map zooms to truck location
5. See truck details and route
6. View analytics charts

## 🔧 Configuration

### Change API URL

Edit `frontend/src/services/api.js`:

```javascript
const API_BASE_URL = 'http://localhost:8000/api/v1';
// Change to your backend URL
```

### Change Frontend Port

Edit `frontend/vite.config.js`:

```javascript
server: {
  port: 3000,  // Change to any port
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true
    }
  }
}
```

### Customize Colors

Edit `frontend/tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      primary: '#3B82F6',    // Your primary color
      secondary: '#10B981',  // Your secondary color
    }
  }
}
```

## 📁 Project Structure

```
frontend/
├── node_modules/          # Dependencies (auto-generated)
├── public/                # Static assets
├── src/
│   ├── components/
│   │   └── MapView.jsx    # Reusable map component
│   ├── pages/
│   │   ├── LandingPage.jsx
│   │   ├── DriverDashboard.jsx
│   │   ├── OwnerDashboard.jsx
│   │   └── VendorDashboard.jsx
│   ├── services/
│   │   └── api.js         # API calls
│   ├── App.jsx            # Main app
│   ├── main.jsx           # Entry point
│   └── index.css          # Global styles
├── index.html             # HTML template
├── package.json           # Dependencies
├── vite.config.js         # Vite configuration
├── tailwind.config.js     # Tailwind configuration
└── postcss.config.js      # PostCSS configuration
```

## 🐛 Common Issues

### Issue: "Cannot find module 'react'"

**Solution:**
```bash
npm install
```

### Issue: "Port 3000 is already in use"

**Solution:**
```bash
# Kill process on port 3000
# Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Or change port in vite.config.js
```

### Issue: "Map not showing"

**Solution:**
1. Check if Leaflet CSS is loaded
2. Open browser console for errors
3. Verify backend is running
4. Check network tab for API calls

### Issue: "API calls failing"

**Solution:**
1. Ensure backend is running on port 8000
2. Check `vite.config.js` proxy configuration
3. Verify CORS is enabled in backend
4. Check browser console for errors

### Issue: "Autocomplete not working"

**Solution:**
1. Ensure backend is running
2. Check OpenStreetMap API is accessible
3. Type at least 3 characters
4. Wait 1 second for results

## 📊 Development Tips

### Hot Reload

Vite automatically reloads when you save files. No need to restart!

### Browser DevTools

- **F12** - Open DevTools
- **Console** - See errors and logs
- **Network** - See API calls
- **React DevTools** - Install extension for React debugging

### Code Formatting

```bash
# Install Prettier
npm install --save-dev prettier

# Format code
npx prettier --write "src/**/*.{js,jsx}"
```

### Linting

```bash
# Install ESLint
npm install --save-dev eslint

# Run linter
npx eslint src/
```

## 🚀 Build for Production

```bash
# Create production build
npm run build

# Output in dist/ directory
```

### Deploy to Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel
```

### Deploy to Netlify

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
netlify deploy --prod
```

## 📈 Performance Optimization

### Code Splitting

Vite automatically splits code. No configuration needed!

### Lazy Loading

```javascript
// Lazy load components
const DriverDashboard = lazy(() => import('./pages/DriverDashboard'));
```

### Image Optimization

```javascript
// Use WebP format
<img src="image.webp" alt="..." />
```

## 🔒 Security Best Practices

1. **Never commit `.env` files**
2. **Use environment variables for API URLs**
3. **Validate all user input**
4. **Sanitize data before rendering**
5. **Keep dependencies updated**

## 📚 Learn More

- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [React Leaflet](https://react-leaflet.js.org/)
- [OpenStreetMap](https://www.openstreetmap.org/)

## 🎓 Next Steps

1. **Explore the code** - Read through components
2. **Customize UI** - Change colors and styles
3. **Add features** - Implement new functionality
4. **Test thoroughly** - Try all features
5. **Deploy** - Put it online!

## 💡 Pro Tips

- Use React DevTools for debugging
- Keep components small and focused
- Use TypeScript for better type safety
- Write tests with Vitest
- Use Git for version control

## 📞 Need Help?

- Check browser console for errors
- Read error messages carefully
- Search on Stack Overflow
- Check GitHub issues
- Ask in React community

---

**Happy Coding! 🚀**
