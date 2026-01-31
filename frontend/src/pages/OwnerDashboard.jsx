import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Building2, ArrowLeft, Truck, TrendingUp, DollarSign, MapPin, Activity } from 'lucide-react';
import MapView from '../components/MapView';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const OwnerDashboard = () => {
  const navigate = useNavigate();
  const [selectedTruck, setSelectedTruck] = useState(null);
  
  // Demo fleet data
  const [fleet, setFleet] = useState([
    {
      id: 1,
      license: 'DL-01-AB-1234',
      driver: 'Rajesh Kumar',
      status: 'in-transit',
      currentLocation: { lat: 28.6139, lng: 77.2090, address: 'Delhi' },
      destination: { lat: 26.9124, lng: 75.7873, address: 'Jaipur' },
      load: 'Electronics - 5000kg',
      earnings: 45000,
      distance: 1250,
      fuelEfficiency: 6.5
    },
    {
      id: 2,
      license: 'MH-02-CD-5678',
      driver: 'Amit Singh',
      status: 'loading',
      currentLocation: { lat: 19.0760, lng: 72.8777, address: 'Mumbai' },
      destination: { lat: 18.5204, lng: 73.8567, address: 'Pune' },
      load: 'Textiles - 3000kg',
      earnings: 28000,
      distance: 850,
      fuelEfficiency: 7.2
    },
    {
      id: 3,
      license: 'KA-03-EF-9012',
      driver: 'Suresh Reddy',
      status: 'idle',
      currentLocation: { lat: 12.9716, lng: 77.5946, address: 'Bangalore' },
      destination: null,
      load: null,
      earnings: 52000,
      distance: 1580,
      fuelEfficiency: 6.8
    }
  ]);

  // Demo earnings data
  const earningsData = [
    { day: 'Mon', earnings: 45000 },
    { day: 'Tue', earnings: 52000 },
    { day: 'Wed', earnings: 48000 },
    { day: 'Thu', earnings: 61000 },
    { day: 'Fri', earnings: 55000 },
    { day: 'Sat', earnings: 58000 },
    { day: 'Sun', earnings: 50000 }
  ];

  const getStatusColor = (status) => {
    switch (status) {
      case 'in-transit': return 'bg-blue-100 text-blue-800';
      case 'loading': return 'bg-yellow-100 text-yellow-800';
      case 'idle': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'in-transit': return '🚛';
      case 'loading': return '📦';
      case 'idle': return '⏸️';
      default: return '❓';
    }
  };

  const getMapMarkers = () => {
    if (selectedTruck) {
      const truck = fleet.find(t => t.id === selectedTruck);
      const markers = [
        {
          lat: truck.currentLocation.lat,
          lng: truck.currentLocation.lng,
          type: 'truck',
          title: truck.license,
          description: `Driver: ${truck.driver}`,
          address: truck.currentLocation.address,
          info: {
            'Status': truck.status,
            'Load': truck.load || 'Empty',
            'Earnings': `₹${truck.earnings.toLocaleString()}`
          }
        }
      ];

      if (truck.destination) {
        markers.push({
          lat: truck.destination.lat,
          lng: truck.destination.lng,
          type: 'destination',
          title: 'Destination',
          address: truck.destination.address
        });
      }

      return markers;
    }

    return fleet.map(truck => ({
      lat: truck.currentLocation.lat,
      lng: truck.currentLocation.lng,
      type: 'truck',
      title: truck.license,
      description: `Driver: ${truck.driver}`,
      address: truck.currentLocation.address,
      info: {
        'Status': truck.status,
        'Load': truck.load || 'Empty'
      }
    }));
  };

  const getMapRoutes = () => {
    if (selectedTruck) {
      const truck = fleet.find(t => t.id === selectedTruck);
      if (truck.destination) {
        return [{
          positions: [
            [truck.currentLocation.lat, truck.currentLocation.lng],
            [truck.destination.lat, truck.destination.lng]
          ],
          color: '#3B82F6',
          weight: 4
        }];
      }
    }
    return [];
  };

  const totalEarnings = fleet.reduce((sum, truck) => sum + truck.earnings, 0);
  const totalDistance = fleet.reduce((sum, truck) => sum + truck.distance, 0);
  const avgFuelEfficiency = (fleet.reduce((sum, truck) => sum + truck.fuelEfficiency, 0) / fleet.length).toFixed(1);

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <button onClick={() => navigate('/')} className="p-2 hover:bg-gray-100 rounded-lg">
                <ArrowLeft className="w-6 h-6" />
              </button>
              <Building2 className="w-8 h-8 text-green-500" />
              <div>
                <h1 className="text-2xl font-bold">Owner Dashboard</h1>
                <p className="text-sm text-gray-500">Fleet Management & Analytics</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-right">
                <p className="text-sm text-gray-500">Total Fleet Earnings</p>
                <p className="text-2xl font-bold text-green-600">₹{totalEarnings.toLocaleString()}</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-6 py-6">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
          <div className="bg-white rounded-xl shadow-sm p-6">
            <div className="flex items-center justify-between mb-2">
              <Truck className="w-8 h-8 text-blue-500" />
              <span className="text-3xl font-bold text-gray-900">{fleet.length}</span>
            </div>
            <p className="text-gray-600">Active Trucks</p>
          </div>

          <div className="bg-white rounded-xl shadow-sm p-6">
            <div className="flex items-center justify-between mb-2">
              <DollarSign className="w-8 h-8 text-green-500" />
              <span className="text-3xl font-bold text-gray-900">₹{totalEarnings.toLocaleString()}</span>
            </div>
            <p className="text-gray-600">Total Earnings</p>
          </div>

          <div className="bg-white rounded-xl shadow-sm p-6">
            <div className="flex items-center justify-between mb-2">
              <MapPin className="w-8 h-8 text-purple-500" />
              <span className="text-3xl font-bold text-gray-900">{totalDistance}</span>
            </div>
            <p className="text-gray-600">Total Distance (km)</p>
          </div>

          <div className="bg-white rounded-xl shadow-sm p-6">
            <div className="flex items-center justify-between mb-2">
              <Activity className="w-8 h-8 text-orange-500" />
              <span className="text-3xl font-bold text-gray-900">{avgFuelEfficiency}</span>
            </div>
            <p className="text-gray-600">Avg Fuel (km/L)</p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Fleet List */}
          <div className="lg:col-span-1 space-y-6">
            <div className="bg-white rounded-xl shadow-sm p-6">
              <h2 className="text-xl font-bold mb-4">Fleet Status</h2>
              <div className="space-y-3">
                {fleet.map(truck => (
                  <div
                    key={truck.id}
                    onClick={() => setSelectedTruck(truck.id)}
                    className={`border rounded-lg p-4 cursor-pointer transition-all ${
                      selectedTruck === truck.id ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-blue-300'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center">
                        <span className="text-2xl mr-3">{getStatusIcon(truck.status)}</span>
                        <div>
                          <p className="font-semibold">{truck.license}</p>
                          <p className="text-sm text-gray-500">{truck.driver}</p>
                        </div>
                      </div>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(truck.status)}`}>
                        {truck.status}
                      </span>
                    </div>
                    
                    <div className="space-y-1 text-sm">
                      <div className="flex items-center">
                        <MapPin className="w-4 h-4 text-blue-500 mr-2" />
                        <p className="text-gray-600">{truck.currentLocation.address}</p>
                      </div>
                      {truck.load && (
                        <div className="flex items-center">
                          <Activity className="w-4 h-4 text-green-500 mr-2" />
                          <p className="text-gray-600">{truck.load}</p>
                        </div>
                      )}
                    </div>

                    <div className="mt-3 pt-3 border-t border-gray-100 grid grid-cols-2 gap-2 text-xs">
                      <div>
                        <p className="text-gray-500">Earnings</p>
                        <p className="font-semibold text-green-600">₹{truck.earnings.toLocaleString()}</p>
                      </div>
                      <div>
                        <p className="text-gray-500">Distance</p>
                        <p className="font-semibold">{truck.distance}km</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Map and Analytics */}
          <div className="lg:col-span-2 space-y-6">
            <div className="bg-white rounded-xl shadow-sm p-4">
              <h2 className="text-xl font-bold mb-4 px-2">Live Fleet Tracking</h2>
              <MapView
                markers={getMapMarkers()}
                routes={getMapRoutes()}
                height="400px"
              />
            </div>

            <div className="bg-white rounded-xl shadow-sm p-6">
              <h2 className="text-xl font-bold mb-4">Weekly Earnings</h2>
              <ResponsiveContainer width="100%" height={250}>
                <LineChart data={earningsData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="day" />
                  <YAxis />
                  <Tooltip formatter={(value) => `₹${value.toLocaleString()}`} />
                  <Line type="monotone" dataKey="earnings" stroke="#10B981" strokeWidth={3} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default OwnerDashboard;
