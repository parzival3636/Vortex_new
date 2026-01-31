import React, { useEffect, useRef, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline, useMap, Circle } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix for default marker icons
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Enhanced custom icons with emoji (no image path errors)
const createCustomIcon = (emoji, size = 30, pulseColor = null) => {
  const pulseAnimation = pulseColor ? `
    @keyframes pulse {
      0% {
        box-shadow: 0 0 0 0 ${pulseColor}80;
      }
      70% {
        box-shadow: 0 0 0 15px ${pulseColor}00;
      }
      100% {
        box-shadow: 0 0 0 0 ${pulseColor}00;
      }
    }
  ` : '';

  return L.divIcon({
    className: 'custom-marker',
    html: `
      <style>
        ${pulseAnimation}
        .marker-container {
          position: relative;
          width: ${size}px;
          height: ${size}px;
        }
        .marker-emoji {
          font-size: ${size}px;
          line-height: 1;
          filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
          ${pulseColor ? `animation: pulse 2s infinite;` : ''}
        }
      </style>
      <div class="marker-container">
        <div class="marker-emoji">${emoji}</div>
      </div>
    `,
    iconSize: [size, size],
    iconAnchor: [size / 2, size / 2],
    popupAnchor: [0, -size / 2]
  });
};

// Realistic truck icon with pulsing effect for live tracking
const truckIcon = createCustomIcon('🚛', 30, '#3B82F6');
const vendorIcon = createCustomIcon('📦', 28);
const destinationIcon = createCustomIcon('🎯', 28);
const marketIcon = createCustomIcon('🏪', 28);
const pickupIcon = createCustomIcon('📍', 28, '#10B981');
const deliveryIcon = createCustomIcon('🏁', 28, '#EF4444');

// Component to auto-center with smooth animation
const AutoCenter = ({ center, zoom }) => {
  const map = useMap();
  
  useEffect(() => {
    if (center && center.length === 2) {
      map.flyTo(center, zoom || map.getZoom(), {
        duration: 1.5,
        easeLinearity: 0.25
      });
    }
  }, [center, zoom, map]);
  
  return null;
};

// Component to fit bounds with animation
const FitBounds = ({ bounds }) => {
  const map = useMap();
  
  useEffect(() => {
    if (bounds && bounds.length > 0) {
      map.flyToBounds(bounds, { 
        padding: [50, 50],
        duration: 1.5,
        easeLinearity: 0.25
      });
    }
  }, [bounds, map]);
  
  return null;
};

// Live tracking indicator component
const LiveIndicator = ({ timestamp, speed }) => {
  const [pulse, setPulse] = useState(true);

  useEffect(() => {
    const interval = setInterval(() => {
      setPulse(p => !p);
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{
      position: 'absolute',
      top: '10px',
      right: '10px',
      zIndex: 1000,
      backgroundColor: 'white',
      padding: '8px 12px',
      borderRadius: '8px',
      boxShadow: '0 2px 8px rgba(0,0,0,0.15)',
      display: 'flex',
      alignItems: 'center',
      gap: '8px'
    }}>
      <div style={{
        width: '8px',
        height: '8px',
        borderRadius: '50%',
        backgroundColor: '#EF4444',
        opacity: pulse ? 1 : 0.3,
        transition: 'opacity 0.5s'
      }} />
      <span style={{ fontSize: '12px', fontWeight: '600', color: '#EF4444' }}>
        LIVE
      </span>
      {timestamp && (
        <span style={{ fontSize: '11px', color: '#6B7280', marginLeft: '4px' }}>
          {new Date(timestamp).toLocaleTimeString()}
        </span>
      )}
      {speed && (
        <div style={{
          marginLeft: '8px',
          padding: '2px 8px',
          backgroundColor: '#3B82F6',
          color: 'white',
          borderRadius: '4px',
          fontSize: '11px',
          fontWeight: '600'
        }}>
          {speed} km/h
        </div>
      )}
    </div>
  );
};

// Progress bar component
const ProgressBar = ({ progress, label }) => {
  return (
    <div style={{
      position: 'absolute',
      bottom: '20px',
      left: '50%',
      transform: 'translateX(-50%)',
      zIndex: 1000,
      backgroundColor: 'white',
      padding: '12px 20px',
      borderRadius: '12px',
      boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
      minWidth: '300px'
    }}>
      <div style={{ marginBottom: '8px', fontSize: '13px', fontWeight: '600', color: '#374151' }}>
        {label || 'Trip Progress'}
      </div>
      <div style={{
        width: '100%',
        height: '8px',
        backgroundColor: '#E5E7EB',
        borderRadius: '4px',
        overflow: 'hidden',
        position: 'relative'
      }}>
        <div style={{
          width: `${progress}%`,
          height: '100%',
          background: 'linear-gradient(90deg, #3B82F6 0%, #10B981 100%)',
          borderRadius: '4px',
          transition: 'width 0.5s ease',
          position: 'relative',
          overflow: 'hidden'
        }}>
          <div style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: 'linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent)',
            animation: 'shimmer 2s infinite'
          }} />
        </div>
      </div>
      <div style={{ marginTop: '6px', fontSize: '12px', color: '#6B7280', textAlign: 'center' }}>
        {progress}% Complete
      </div>
      <style>{`
        @keyframes shimmer {
          0% { transform: translateX(-100%); }
          100% { transform: translateX(100%); }
        }
      `}</style>
    </div>
  );
};

const MapView = ({ 
  center = [20.5937, 78.9629], // India center
  zoom = 5,
  markers = [],
  routes = [],
  showRoute = true,
  height = '600px',
  onMapClick = null,
  liveTracking = false,
  trackingData = null, // { timestamp, speed, progress, label }
  autoCenter = false,
  completedRouteColor = '#10B981',
  remainingRouteColor = '#9CA3AF'
}) => {
  const [bounds, setBounds] = useState([]);
  const [mapCenter, setMapCenter] = useState(center);

  useEffect(() => {
    // Calculate bounds from markers
    if (markers.length > 0) {
      const latLngs = markers.map(m => [m.lat, m.lng]);
      setBounds(latLngs);
    }
  }, [markers]);

  useEffect(() => {
    // Update center for live tracking
    if (autoCenter && markers.length > 0) {
      const truckMarker = markers.find(m => m.type === 'truck');
      if (truckMarker) {
        setMapCenter([truckMarker.lat, truckMarker.lng]);
      }
    }
  }, [markers, autoCenter]);

  const getMarkerIcon = (type) => {
    switch (type) {
      case 'truck':
        return truckIcon;
      case 'vendor':
        return vendorIcon;
      case 'pickup':
        return pickupIcon;
      case 'destination':
        return destinationIcon;
      case 'delivery':
        return deliveryIcon;
      case 'market':
        return marketIcon;
      default:
        return createCustomIcon('📍', 28);
    }
  };

  const renderEnhancedPopup = (marker) => {
    return (
      <div style={{ minWidth: '200px' }}>
        <div style={{
          fontSize: '16px',
          fontWeight: '700',
          color: '#111827',
          marginBottom: '8px',
          paddingBottom: '8px',
          borderBottom: '2px solid #E5E7EB'
        }}>
          {marker.title}
        </div>
        
        {marker.description && (
          <div style={{
            fontSize: '13px',
            color: '#6B7280',
            marginBottom: '8px'
          }}>
            {marker.description}
          </div>
        )}
        
        {marker.address && (
          <div style={{
            fontSize: '12px',
            color: '#9CA3AF',
            marginBottom: '8px',
            fontStyle: 'italic'
          }}>
            📍 {marker.address}
          </div>
        )}
        
        {marker.info && Object.keys(marker.info).length > 0 && (
          <div style={{
            marginTop: '12px',
            padding: '8px',
            backgroundColor: '#F9FAFB',
            borderRadius: '6px'
          }}>
            {Object.entries(marker.info).map(([key, value]) => (
              <div key={key} style={{
                display: 'flex',
                justifyContent: 'space-between',
                fontSize: '12px',
                marginBottom: '4px'
              }}>
                <span style={{ fontWeight: '600', color: '#374151' }}>{key}:</span>
                <span style={{ color: '#6B7280' }}>{value}</span>
              </div>
            ))}
          </div>
        )}
        
        {marker.eta && (
          <div style={{
            marginTop: '8px',
            padding: '6px',
            backgroundColor: '#DBEAFE',
            borderRadius: '4px',
            fontSize: '11px',
            fontWeight: '600',
            color: '#1E40AF',
            textAlign: 'center'
          }}>
            ETA: {marker.eta}
          </div>
        )}
      </div>
    );
  };

  return (
    <div style={{ height, width: '100%', borderRadius: '12px', overflow: 'hidden', position: 'relative' }}>
      {/* Live tracking indicator */}
      {liveTracking && trackingData && (
        <LiveIndicator 
          timestamp={trackingData.timestamp} 
          speed={trackingData.speed}
        />
      )}

      {/* Progress bar */}
      {trackingData && trackingData.progress !== undefined && (
        <ProgressBar 
          progress={trackingData.progress} 
          label={trackingData.label}
        />
      )}

      <MapContainer
        center={center}
        zoom={zoom}
        style={{ height: '100%', width: '100%' }}
        scrollWheelZoom={true}
      >
        {/* Enhanced tile layer with better styling */}
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {/* Markers with enhanced popups */}
        {markers.map((marker, index) => (
          <React.Fragment key={index}>
            <Marker
              position={[marker.lat, marker.lng]}
              icon={getMarkerIcon(marker.type)}
            >
              <Popup maxWidth={300}>
                {renderEnhancedPopup(marker)}
              </Popup>
            </Marker>
            
            {/* Add radius circle for truck to show coverage area */}
            {marker.type === 'truck' && marker.radius && (
              <Circle
                center={[marker.lat, marker.lng]}
                radius={marker.radius}
                pathOptions={{
                  color: '#3B82F6',
                  fillColor: '#3B82F6',
                  fillOpacity: 0.1,
                  weight: 1,
                  dashArray: '5, 5'
                }}
              />
            )}
          </React.Fragment>
        ))}

        {/* Enhanced routes with completed/remaining styling */}
        {showRoute && routes.map((route, index) => {
          const isCompleted = route.completed || false;
          const isRemaining = route.remaining || false;
          
          return (
            <Polyline
              key={index}
              positions={route.positions}
              pathOptions={{
                color: isCompleted 
                  ? completedRouteColor 
                  : isRemaining 
                    ? remainingRouteColor 
                    : route.color || '#3B82F6',
                weight: route.weight || 5,
                opacity: route.opacity || (isRemaining ? 0.5 : 0.8),
                dashArray: isCompleted 
                  ? '10, 10' 
                  : isRemaining 
                    ? '5, 10' 
                    : route.dashed 
                      ? '10, 10' 
                      : null,
                lineCap: 'round',
                lineJoin: 'round'
              }}
            />
          );
        })}

        {/* Auto-center for live tracking */}
        {autoCenter && <AutoCenter center={mapCenter} zoom={zoom} />}

        {/* Fit bounds with animation */}
        {!autoCenter && bounds.length > 0 && <FitBounds bounds={bounds} />}
      </MapContainer>
    </div>
  );
};

export default MapView;
