# 🚀 Deadheading Optimization Frontend

React.js frontend with 3 dashboards and real-time map visualization using OpenStreetMap.

## ✨ Features

### 1. **Driver Dashboard** 🚛
- **Route Planning**: Enter origin and destination with address autocomplete
- **Load Matching**: AI finds profitable return loads automatically
- **Real-time Map**: Visualize route with vendors along the way
- **Navigation**: Step-by-step navigation from source → vendor → destination
- **Profitability Calculator**: See profit, fuel cost, extra distance for each load
- **Load Selection**: Choose best load based on AI ranking

### 2. **Owner Dashboard** 🏢
- **Fleet Tracking**: See all trucks on map in real-time
- **Live Location**: Track where each vehicle is currently
- **Performance Analytics**: Earnings, distance, fuel efficiency charts
- **Driver Management**: Monitor driver status and performance
- **Revenue Reports**: Weekly earnings visualization
- **Fleet Status**: In-transit, loading, idle status for each truck

### 3. **Vendor Dashboard** 📦
- **Post Loads**: Add new loads with address autocomplete
- **Find Drivers**: System automatically matches with nearby drivers
- **Track Shipments**: See load status on map
- **Load Management**: View all posted loads
- **GPS Integration**: Addresses converted to GPS automatically

## 🗺️ Map Features

- **OpenStreetMap Integration**: Free, no API key needed
- **Custom Markers**: Different icons for trucks, vendors, destinations
- **Route Visualization**: Animated routes with color coding
- **Interactive Popups**: Click markers for detailed information
- **Auto-fit Bounds**: Map automatically zooms to show all markers
- **Real-time Updates**: Markers update as data changes

## 🛠️ Tech Stack

- **React 18** - UI framework
- **React Router** - Navigation
- **React Leaflet** - Map visualization
- **Leaflet** - OpenStreetMap integration
- **Axios** - API calls
- **Recharts** - Analytics charts
- **Tailwind CSS** - Styling
- **Lucide React** - Icons
- **React Hot Toast** - Notifications
- **Vite** - Build tool

## 📦 Installation

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run on: http://localhost:3000

## 🔧 Configuration

The frontend is configured to proxy API requests to the backend:

```javascript
// vite.config.js
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

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   └── MapView.jsx          # Reusable map component
│   ├── pages/
│   │   ├── LandingPage.jsx      # Home page with dashboard selection
│   │   ├── DriverDashboard.jsx  # Driver features
│   │   ├── OwnerDashboard.jsx   # Fleet tracking
│   │   └── VendorDashboard.jsx  # Load posting
│   ├── services/
│   │   └── api.js               # API service layer
│   ├── App.jsx                  # Main app with routing
│   ├── main.jsx                 # Entry point
│   └── index.css                # Global styles
├── package.json
├── vite.config.js
├── tailwind.config.js
└── index.html
```

## 🎨 UI Components

### MapView Component

Reusable map component with props:

```jsx
<MapView
  center={[lat, lng]}           // Map center
  zoom={5}                      // Zoom level
  markers={[...]}               // Array of markers
  routes={[...]}                // Array of routes
  showRoute={true}              // Show/hide routes
  height="600px"                // Map height
/>
```

### Marker Types

- `truck` - Blue truck icon
- `vendor` / `pickup` - Green package icon
- `destination` / `delivery` - Red target icon
- `market` - Orange store icon

### Route Configuration

```javascript
{
  positions: [[lat1, lng1], [lat2, lng2]],
  color: '#3B82F6',
  weight: 4,
  opacity: 0.7,
  dashed: false
}
```

## 🚀 Usage

### 1. Start Backend

```bash
# In root directory
python main.py
```

Backend runs on: http://localhost:8000

### 2. Start Frontend

```bash
# In frontend directory
npm run dev
```

Frontend runs on: http://localhost:3000

### 3. Access Dashboards

- **Landing Page**: http://localhost:3000/
- **Driver Dashboard**: http://localhost:3000/driver
- **Owner Dashboard**: http://localhost:3000/owner
- **Vendor Dashboard**: http://localhost:3000/vendor

## 📱 Features Walkthrough

### Driver Dashboard Flow

1. **Select Route**
   - Enter origin address (autocomplete)
   - Enter destination address (autocomplete)
   - Click "Find Return Loads"

2. **View Available Loads**
   - See all loads on map
   - View profitability for each load
   - Loads ranked by AI (best profit first)
   - Click load to see details

3. **Accept Load**
   - Click "Accept Load" button
   - Navigation starts automatically

4. **Navigate**
   - Step 1: Go to pickup location (green marker)
   - Step 2: Deliver load (orange marker)
   - Step 3: Return home (blue marker)
   - Map shows complete route with color coding

### Vendor Dashboard Flow

1. **Post Load**
   - Click "Post New Load" button
   - Enter pickup address (autocomplete)
   - Enter destination address (autocomplete)
   - Enter weight (kg)
   - Enter price (₹)
   - Click "Post Load"

2. **View Loads**
   - See all posted loads on map
   - View load status
   - Track shipments

### Owner Dashboard Flow

1. **View Fleet**
   - See all trucks on map
   - View truck status (in-transit, loading, idle)
   - Click truck for details

2. **Track Vehicle**
   - Click on truck in list
   - Map zooms to truck location
   - See route to destination
   - View earnings and distance

3. **Analytics**
   - View weekly earnings chart
   - See total fleet statistics
   - Monitor fuel efficiency

## 🎨 Customization

### Colors

Edit `tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      primary: '#3B82F6',    // Blue
      secondary: '#10B981',  // Green
      danger: '#EF4444',     // Red
      warning: '#F59E0B',    // Orange
    }
  }
}
```

### Map Tiles

Change map style in `MapView.jsx`:

```jsx
<TileLayer
  url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
  // Or use other tile providers:
  // url="https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png"
  // url="https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.png"
/>
```

## 🐛 Troubleshooting

### Map not showing

1. Check if Leaflet CSS is loaded in `index.html`
2. Verify map container has height set
3. Check browser console for errors

### API calls failing

1. Ensure backend is running on port 8000
2. Check proxy configuration in `vite.config.js`
3. Verify CORS is enabled in backend

### Markers not appearing

1. Check marker data format
2. Verify lat/lng values are numbers
3. Check marker type is valid

## 📊 Performance

- **Lazy Loading**: Routes are lazy loaded
- **Memoization**: Components use React.memo where needed
- **Optimized Rendering**: Map only re-renders when data changes
- **Code Splitting**: Vite automatically splits code

## 🔒 Security

- **API Proxy**: All API calls go through Vite proxy
- **Input Validation**: Forms validate user input
- **XSS Protection**: React escapes all user input
- **CORS**: Backend handles CORS properly

## 📦 Build for Production

```bash
npm run build
```

Output in `dist/` directory.

Deploy to:
- Vercel
- Netlify
- GitHub Pages
- Any static hosting

## 🎯 Next Steps

1. **Add Authentication**: User login/signup
2. **Real-time Updates**: WebSocket for live tracking
3. **Push Notifications**: Notify drivers of new loads
4. **Mobile App**: React Native version
5. **Offline Mode**: PWA with service workers

## 📝 License

MIT License - See LICENSE file

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📧 Support

For issues or questions, open an issue on GitHub.

---

**Built with ❤️ using React, OpenStreetMap, and AI**
