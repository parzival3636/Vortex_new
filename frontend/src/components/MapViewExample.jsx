import React, { useState, useEffect } from 'react';
import MapView from './MapView';

/**
 * Example usage of the enhanced MapView component
 * Demonstrates all realistic features:
 * - Live tracking with pulsing indicator
 * - Speed display
 * - Progress bar with animation
 * - Completed route (green dotted)
 * - Remaining route (gray dotted)
 * - Auto-centering with smooth flyTo
 * - Enhanced popups
 */

const MapViewExample = () => {
  const [currentPosition, setCurrentPosition] = useState({ lat: 28.6139, lng: 77.2090 });
  const [progress, setProgress] = useState(35);
  const [speed, setSpeed] = useState(65);

  // Simulate truck movement
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentPosition(prev => ({
        lat: prev.lat + 0.001,
        lng: prev.lng + 0.001
      }));
      setProgress(prev => Math.min(prev + 1, 100));
      setSpeed(Math.floor(Math.random() * 20) + 55); // 55-75 km/h
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  // Define markers
  const markers = [
    {
      lat: currentPosition.lat,
      lng: currentPosition.lng,
      type: 'truck',
      title: 'Truck DL-01-AB-1234',
      description: 'Driver: Rajesh Kumar',
      info: {
        'Status': 'In Transit',
        'Load': '5000 kg Electronics',
        'ETA': '2 hours 15 mins'
      },
      eta: '14:30 PM',
      radius: 5000 // 5km radius circle
    },
    {
      lat: 28.7219,
      lng: 77.1649,
      type: 'pickup',
      title: 'Pickup Location',
      description: 'Azadpur Mandi',
      address: 'Azadpur Mandi, Delhi, India',
      info: {
        'Contact': '+91-9876543210',
        'Gate': 'Gate 3',
        'Status': 'Completed ✓'
      }
    },
    {
      lat: 26.9124,
      lng: 75.7873,
      type: 'delivery',
      title: 'Delivery Location',
      description: 'Jaipur Market Yard',
      address: 'Market Yard, Jaipur, Rajasthan',
      info: {
        'Contact': '+91-9988776655',
        'Warehouse': 'B-12',
        'Status': 'Pending'
      },
      eta: '14:30 PM'
    },
    {
      lat: 28.5355,
      lng: 77.3910,
      type: 'destination',
      title: 'Final Destination',
      description: 'Return to Base',
      address: 'Noida, Uttar Pradesh',
      info: {
        'Type': 'Home Base',
        'Distance': '125 km'
      }
    }
  ];

  // Define routes with completed and remaining sections
  const routes = [
    // Completed route (green dotted)
    {
      positions: [
        [28.7219, 77.1649], // Pickup
        [currentPosition.lat, currentPosition.lng] // Current position
      ],
      completed: true,
      weight: 6,
      opacity: 0.8
    },
    // Remaining route (gray dotted)
    {
      positions: [
        [currentPosition.lat, currentPosition.lng], // Current position
        [26.9124, 75.7873], // Delivery
        [28.5355, 77.3910]  // Final destination
      ],
      remaining: true,
      weight: 5,
      opacity: 0.5
    }
  ];

  // Tracking data for live indicator and progress bar
  const trackingData = {
    timestamp: new Date().toISOString(),
    speed: speed,
    progress: progress,
    label: 'Delhi → Jaipur'
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Enhanced Map View - Live Tracking</h1>
      
      <div className="mb-4 p-4 bg-blue-50 rounded-lg">
        <h2 className="font-semibold mb-2">Features Demonstrated:</h2>
        <ul className="text-sm space-y-1">
          <li>✅ Live tracking with pulsing red dot</li>
          <li>✅ Real-time speed indicator (65 km/h)</li>
          <li>✅ Animated progress bar with gradient</li>
          <li>✅ Green dotted line for completed route</li>
          <li>✅ Gray dotted line for remaining route</li>
          <li>✅ Auto-centering with smooth flyTo animation</li>
          <li>✅ 🚛 Emoji icons (no image path errors)</li>
          <li>✅ Enhanced popups with rich information</li>
          <li>✅ 5km radius circle around truck</li>
        </ul>
      </div>

      <MapView
        markers={markers}
        routes={routes}
        height="600px"
        liveTracking={true}
        trackingData={trackingData}
        autoCenter={true}
        zoom={8}
        completedRouteColor="#10B981"
        remainingRouteColor="#9CA3AF"
      />

      <div className="mt-4 grid grid-cols-3 gap-4">
        <div className="p-4 bg-green-50 rounded-lg">
          <div className="text-sm text-gray-600">Progress</div>
          <div className="text-2xl font-bold text-green-600">{progress}%</div>
        </div>
        <div className="p-4 bg-blue-50 rounded-lg">
          <div className="text-sm text-gray-600">Current Speed</div>
          <div className="text-2xl font-bold text-blue-600">{speed} km/h</div>
        </div>
        <div className="p-4 bg-purple-50 rounded-lg">
          <div className="text-sm text-gray-600">Distance Remaining</div>
          <div className="text-2xl font-bold text-purple-600">125 km</div>
        </div>
      </div>
    </div>
  );
};

export default MapViewExample;
