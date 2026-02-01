import React, { useState, useEffect } from 'react';
import { Package, MapPin, Navigation, CheckCircle, Clock } from 'lucide-react';
import axios from 'axios';
import toast from 'react-hot-toast';

const AllocatedLoads = ({ driverId, onSelectLoad }) => {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedLoadId, setSelectedLoadId] = useState(null);

  useEffect(() => {
    fetchAllocatedLoads();
    const interval = setInterval(fetchAllocatedLoads, 30000); // Refresh every 30 seconds
    return () => clearInterval(interval);
  }, [driverId]);

  const fetchAllocatedLoads = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/api/driver/allocated-loads?driver_id=${driverId}`);
      setSummary(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch allocated loads:', error);
      setLoading(false);
    }
  };

  const handlePickup = async (loadId) => {
    try {
      await axios.post(`http://localhost:8000/api/driver/allocated-loads/${loadId}/pickup`);
      toast.success('Load marked as picked up!');
      fetchAllocatedLoads();
    } catch (error) {
      toast.error('Failed to mark load as picked up');
    }
  };

  const handleComplete = async (loadId) => {
    try {
      await axios.post(`http://localhost:8000/api/driver/allocated-loads/${loadId}/complete`);
      toast.success('Load completed!');
      fetchAllocatedLoads();
    } catch (error) {
      toast.error('Failed to mark load as completed');
    }
  };

  const handleNavigate = (load) => {
    setSelectedLoadId(load.loadId);
    if (onSelectLoad) {
      onSelectLoad(load);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin h-12 w-12 border-4 border-blue-500 border-t-transparent rounded-full"></div>
      </div>
    );
  }

  if (!summary || summary.totalLoads === 0) {
    return (
      <div className="bg-white rounded-xl shadow-sm p-8 text-center">
        <Package className="w-16 h-16 mx-auto mb-4 text-gray-300" />
        <h3 className="text-xl font-bold text-gray-700 mb-2">No Allocated Loads</h3>
        <p className="text-gray-500">You don't have any loads assigned at the moment.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white rounded-xl shadow-sm p-4">
          <div className="flex items-center justify-between">
            <Package className="w-8 h-8 text-blue-500" />
            <span className="text-3xl font-bold text-gray-900">{summary.totalLoads}</span>
          </div>
          <p className="text-gray-600 mt-2">Total Loads</p>
        </div>

        <div className="bg-white rounded-xl shadow-sm p-4">
          <div className="flex items-center justify-between">
            <MapPin className="w-8 h-8 text-purple-500" />
            <span className="text-3xl font-bold text-gray-900">{summary.totalDistance}km</span>
          </div>
          <p className="text-gray-600 mt-2">Total Distance</p>
        </div>

        <div className="bg-white rounded-xl shadow-sm p-4">
          <div className="flex items-center justify-between">
            <Clock className="w-8 h-8 text-orange-500" />
            <span className="text-3xl font-bold text-gray-900">{Math.round(summary.totalTime)}min</span>
          </div>
          <p className="text-gray-600 mt-2">Total Time</p>
        </div>
      </div>

      {/* Loads List */}
      <div className="bg-white rounded-xl shadow-sm p-6">
        <h3 className="text-xl font-bold mb-4">Your Allocated Loads</h3>
        
        <div className="space-y-4">
          {summary.loads.map((load, index) => (
            <div
              key={load.id}
              className={`border rounded-lg p-4 transition-all ${
                selectedLoadId === load.loadId 
                  ? 'border-blue-500 bg-blue-50' 
                  : 'border-gray-200 hover:border-blue-300'
              }`}
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center">
                  <div className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center text-white font-bold mr-3">
                    {index + 1}
                  </div>
                  <div>
                    <p className="font-semibold text-gray-900">Load #{load.loadId.slice(0, 8)}</p>
                    <span className={`text-xs px-2 py-1 rounded ${
                      load.status === 'allocated' ? 'bg-yellow-100 text-yellow-800' :
                      load.status === 'picked_up' ? 'bg-blue-100 text-blue-800' :
                      'bg-gray-100 text-gray-800'
                    }`}>
                      {load.status}
                    </span>
                  </div>
                </div>
              </div>

              <div className="space-y-2 mb-3">
                <div className="flex items-start">
                  <MapPin className="w-4 h-4 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                  <div className="flex-1">
                    <p className="text-xs text-gray-500">Pickup</p>
                    <p className="text-sm font-medium text-gray-800">{load.pickupLocation.address}</p>
                  </div>
                </div>
                <div className="flex items-start">
                  <MapPin className="w-4 h-4 text-red-500 mr-2 mt-0.5 flex-shrink-0" />
                  <div className="flex-1">
                    <p className="text-xs text-gray-500">Destination</p>
                    <p className="text-sm font-medium text-gray-800">{load.destination.address}</p>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3 mb-3 text-xs">
                <div className="bg-gray-50 p-2 rounded">
                  <p className="text-gray-500">Distance to Pickup</p>
                  <p className="font-bold text-gray-800">{load.estimatedDistanceToPickup}km</p>
                </div>
                <div className="bg-gray-50 p-2 rounded">
                  <p className="text-gray-500">Time to Pickup</p>
                  <p className="font-bold text-gray-800">{Math.round(load.estimatedTimeToPickup)}min</p>
                </div>
                <div className="bg-gray-50 p-2 rounded">
                  <p className="text-gray-500">Total Distance</p>
                  <p className="font-bold text-gray-800">{load.totalEstimatedDistance}km</p>
                </div>
                <div className="bg-gray-50 p-2 rounded">
                  <p className="text-gray-500">Total Time</p>
                  <p className="font-bold text-gray-800">{Math.round(load.totalEstimatedTime)}min</p>
                </div>
              </div>

              {load.specialInstructions && (
                <div className="bg-yellow-50 border border-yellow-200 rounded p-2 mb-3 text-xs">
                  <p className="font-semibold text-yellow-800">Special Instructions:</p>
                  <p className="text-yellow-700">{load.specialInstructions}</p>
                </div>
              )}

              <div className="flex space-x-2">
                <button
                  onClick={() => handleNavigate(load)}
                  className="flex-1 bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 rounded-lg transition-colors flex items-center justify-center"
                >
                  <Navigation className="w-4 h-4 mr-2" />
                  Navigate
                </button>
                
                {load.status === 'allocated' && (
                  <button
                    onClick={() => handlePickup(load.loadId)}
                    className="flex-1 bg-green-500 hover:bg-green-600 text-white font-semibold py-2 rounded-lg transition-colors flex items-center justify-center"
                  >
                    <CheckCircle className="w-4 h-4 mr-2" />
                    Mark Picked Up
                  </button>
                )}
                
                {load.status === 'picked_up' && (
                  <button
                    onClick={() => handleComplete(load.loadId)}
                    className="flex-1 bg-purple-500 hover:bg-purple-600 text-white font-semibold py-2 rounded-lg transition-colors flex items-center justify-center"
                  >
                    <CheckCircle className="w-4 h-4 mr-2" />
                    Complete
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AllocatedLoads;
