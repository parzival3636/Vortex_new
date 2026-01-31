import React, { useEffect, useRef, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix for default marker icons
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Custom icons
const createCustomIcon = (color, icon) => {
  return L.divIcon({
    className: 'custom-marker',
    html: `
      <div style="
        background-color: ${color};
        width: 40px;
        height: 40px;
        border-radius: 50% 50% 50% 0;
        transform: rotate(-45deg);
        border: 3px solid white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        display: flex;
        align-items: center;
        justify-content: center;
      ">
        <span style="
          transform: rotate(45deg);
          font-size: 20px;
          color: white;
        ">${icon}</span>
      </div>
    `,
    iconSize: [40, 40],
    iconAnchor: [20, 40],
    popupAnchor: [0, -40]
  });
};

const truckIcon = createCustomIcon('#3B82F6', '🚛');
const vendorIcon = createCustomIcon('#10B981', '📦');
const destinationIcon = createCustomIcon('#EF4444', '🎯');
const marketIcon = createCustomIcon('#F59E0B', '🏪');

// Component to fit bounds
const FitBounds = ({ bounds }) => {
  const map = useMap();
  
  useEffect(() => {
    if (bounds && bounds.length > 0) {
      map.fitBounds(bounds, { padding: [50, 50] });
    }
  }, [bounds, map]);
  
  return null;
};

const MapView = ({ 
  center = [20.5937, 78.9629], // India center
  zoom = 5,
  markers = [],
  routes = [],
  showRoute = true,
  height = '600px',
  onMapClick = null
}) => {
  const [bounds, setBounds] = useState([]);

  useEffect(() => {
    // Calculate bounds from markers
    if (markers.length > 0) {
      const latLngs = markers.map(m => [m.lat, m.lng]);
      setBounds(latLngs);
    }
  }, [markers]);

  const getMarkerIcon = (type) => {
    switch (type) {
      case 'truck':
        return truckIcon;
      case 'vendor':
      case 'pickup':
        return vendorIcon;
      case 'destination':
      case 'delivery':
        return destinationIcon;
      case 'market':
        return marketIcon;
      default:
        return null;
    }
  };

  return (
    <div style={{ height, width: '100%', borderRadius: '12px', overflow: 'hidden' }}>
      <MapContainer
        center={center}
        zoom={zoom}
        style={{ height: '100%', width: '100%' }}
        scrollWheelZoom={true}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {/* Markers */}
        {markers.map((marker, index) => (
          <Marker
            key={index}
            position={[marker.lat, marker.lng]}
            icon={getMarkerIcon(marker.type)}
          >
            <Popup>
              <div className="p-2">
                <h3 className="font-bold text-lg mb-1">{marker.title}</h3>
                {marker.description && (
                  <p className="text-sm text-gray-600 mb-2">{marker.description}</p>
                )}
                {marker.address && (
                  <p className="text-xs text-gray-500">{marker.address}</p>
                )}
                {marker.info && (
                  <div className="mt-2 text-sm">
                    {Object.entries(marker.info).map(([key, value]) => (
                      <div key={key} className="flex justify-between">
                        <span className="font-medium">{key}:</span>
                        <span>{value}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </Popup>
          </Marker>
        ))}

        {/* Routes */}
        {showRoute && routes.map((route, index) => (
          <Polyline
            key={index}
            positions={route.positions}
            color={route.color || '#3B82F6'}
            weight={route.weight || 4}
            opacity={route.opacity || 0.7}
            dashArray={route.dashed ? '10, 10' : null}
          />
        ))}

        {/* Fit bounds */}
        {bounds.length > 0 && <FitBounds bounds={bounds} />}
      </MapContainer>
    </div>
  );
};

export default MapView;
