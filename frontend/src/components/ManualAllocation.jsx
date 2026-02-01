import React, { useState, useEffect } from 'react';
import { Truck, Package, MapPin, CheckCircle, X, AlertCircle } from 'lucide-react';
import axios from 'axios';
import toast from 'react-hot-toast';

const ManualAllocation = ({ ownerId }) => {
  const [vehicles, setVehicles] = useState([]);
  const [loads, setLoads] = useState([]);
  const [selectedVehicle, setSelectedVehicle] = useState(null);
  const [selectedLoad, setSelectedLoad] = useState(null);
  const [compatibleLoads, setCompatibleLoads] = useState([]);
  const [compatibleVehicles, setCompatibleVehicles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [allocating, setAllocating] = useState(false);
  const [showSuccessModal, setShowSuccessModal] = useState(false);
  const [lastAllocation, setLastAllocation] = useState(null);

  useEffect(() => {
    fetchData();
  }, [ownerId]);

  useEffect(() => {
    if (selectedVehicle) {
      fetchCompatibleLoads(selectedVehicle.id);
    } else {
      setCompatibleLoads([]);
    }
  }, [selectedVehicle]);

  useEffect(() => {
    if (selectedLoad) {
      fetchCompatibleVehicles(selectedLoad.id);
    } else {
      setCompatibleVehicles([]);
    }
  }, [selectedLoad]);

  const fetchData = async () => {
    try {
      const [vehiclesRes, loadsRes] = await Promise.all([
        axios.get(`http://localhost:8000/api/allocations/available-vehicles?owner_id=${ownerId}`),
        axios.get('http://localhost:8000/api/allocations/unallocated-loads')
      ]);
      setVehicles(vehiclesRes.data);
      setLoads(loadsRes.data);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch data:', error);
      toast.error('Failed to load allocation data');
      setLoading(false);
    }
  };

  const fetchCompatibleLoads = async (vehicleId) => {
    try {
      const response = await axios.get(`http://localhost:8000/api/allocations/compatible-loads?vehicleId=${vehicleId}`);
      setCompatibleLoads(response.data);
    } catch (error) {
      console.error('Failed to fetch compatible loads:', error);
    }
  };

  const fetchCompatibleVehicles = async (loadId) => {
    try {
      const response = await axios.get(`http://localhost:8000/api/allocations/compatible-vehicles?loadId=${loadId}&ownerId=${ownerId}`);
      setCompatibleVehicles(response.data);
    } catch (error) {
      console.error('Failed to fetch compatible vehicles:', error);
    }
  };

  const handleAllocate = async () => {
    if (!selectedVehicle || !selectedLoad) {
      toast.error('Please select both a vehicle and a load');
      return;
    }

    setAllocating(true);
    try {
      const response = await axios.post('http://localhost:8000/api/allocations', {
        vehicleId: selectedVehicle.id,
        loadId: selectedLoad.id,
        ownerId: ownerId
      });
      
      // Store allocation details for modal
      setLastAllocation({
        vehicle: selectedVehicle,
        load: selectedLoad,
        allocationId: response.data.id
      });
      
      // Show success modal
      setShowSuccessModal(true);
      
      // Show toast notification
      toast.success('Allocation created successfully!', {
        duration: 3000
      });
      
      // Clear selections
      setSelectedVehicle(null);
      setSelectedLoad(null);
      
      // Refresh data
      fetchData();
    } catch (error) {
      const errorMsg = error.response?.data?.detail || 'Failed to create allocation';
      toast.error(errorMsg);
    } finally {
      setAllocating(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin h-12 w-12 border-4 border-blue-500 border-t-transparent rounded-full"></div>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Available Vehicles */}
      <div className="bg-white rounded-xl shadow-sm p-6">
        <h3 className="text-xl font-bold mb-4 flex items-center">
          <Truck className="w-5 h-5 mr-2 text-blue-500" />
          Available Vehicles ({vehicles.length})
        </h3>
        
        <div className="space-y-3 max-h-[600px] overflow-y-auto">
          {vehicles.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <Truck className="w-12 h-12 mx-auto mb-2 opacity-50" />
              <p>No available vehicles</p>
            </div>
          ) : (
            vehicles.map((vehicle) => {
              const isCompatible = compatibleVehicles.some(v => v.id === vehicle.id);
              const isSelected = selectedVehicle?.id === vehicle.id;
              
              return (
                <div
                  key={vehicle.id}
                  onClick={() => setSelectedVehicle(isSelected ? null : vehicle)}
                  className={`border rounded-lg p-4 cursor-pointer transition-all ${
                    isSelected 
                      ? 'border-blue-500 bg-blue-50' 
                      : isCompatible && selectedLoad
                      ? 'border-green-300 bg-green-50'
                      : 'border-gray-200 hover:border-blue-300'
                  }`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center">
                      <Truck className="w-5 h-5 text-blue-500 mr-2" />
                      <div>
                        <p className="font-semibold">{vehicle.name}</p>
                        <p className="text-xs text-gray-500">{vehicle.status}</p>
                      </div>
                    </div>
                    {isSelected && <CheckCircle className="w-5 h-5 text-blue-500" />}
                    {isCompatible && selectedLoad && !isSelected && (
                      <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded">Compatible</span>
                    )}
                  </div>
                  
                  <div className="text-sm text-gray-600">
                    <div className="flex items-center">
                      <MapPin className="w-4 h-4 mr-1" />
                      <span className="truncate">{vehicle.currentLocation.address}</span>
                    </div>
                    <div className="mt-1">
                      <span className="text-xs">Distance to nearest load: </span>
                      <span className="font-semibold">{vehicle.distanceToNearestLoad}km</span>
                    </div>
                  </div>
                </div>
              );
            })
          )}
        </div>
      </div>

      {/* Unallocated Loads */}
      <div className="bg-white rounded-xl shadow-sm p-6">
        <h3 className="text-xl font-bold mb-4 flex items-center">
          <Package className="w-5 h-5 mr-2 text-green-500" />
          Unallocated Loads ({loads.length})
        </h3>
        
        <div className="space-y-3 max-h-[600px] overflow-y-auto">
          {loads.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <Package className="w-12 h-12 mx-auto mb-2 opacity-50" />
              <p>No unallocated loads</p>
            </div>
          ) : (
            loads.map((load) => {
              const isCompatible = compatibleLoads.some(l => l.id === load.id);
              const isSelected = selectedLoad?.id === load.id;
              
              return (
                <div
                  key={load.id}
                  onClick={() => setSelectedLoad(isSelected ? null : load)}
                  className={`border rounded-lg p-4 cursor-pointer transition-all ${
                    isSelected 
                      ? 'border-green-500 bg-green-50' 
                      : isCompatible && selectedVehicle
                      ? 'border-blue-300 bg-blue-50'
                      : 'border-gray-200 hover:border-green-300'
                  }`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center">
                      <Package className="w-5 h-5 text-green-500 mr-2" />
                      <div>
                        <p className="font-semibold">Load #{load.id.slice(0, 8)}</p>
                        <p className="text-xs text-gray-500">{load.status}</p>
                      </div>
                    </div>
                    {isSelected && <CheckCircle className="w-5 h-5 text-green-500" />}
                    {isCompatible && selectedVehicle && !isSelected && (
                      <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">Compatible</span>
                    )}
                  </div>
                  
                  <div className="space-y-1 text-sm text-gray-600">
                    <div className="flex items-start">
                      <MapPin className="w-4 h-4 text-green-500 mr-1 mt-0.5 flex-shrink-0" />
                      <span className="truncate">{load.pickupLocation.address}</span>
                    </div>
                    <div className="flex items-start">
                      <MapPin className="w-4 h-4 text-red-500 mr-1 mt-0.5 flex-shrink-0" />
                      <span className="truncate">{load.destination.address}</span>
                    </div>
                    {load.distanceFromVehicle && (
                      <div className="mt-1 text-xs">
                        <span>Distance from selected vehicle: </span>
                        <span className="font-semibold">{load.distanceFromVehicle}km</span>
                      </div>
                    )}
                  </div>
                </div>
              );
            })
          )}
        </div>
      </div>

      {/* Allocation Action */}
      {(selectedVehicle || selectedLoad) && (
        <div className="lg:col-span-2 bg-gradient-to-r from-blue-50 to-green-50 rounded-xl shadow-sm p-6 border-2 border-blue-200">
          <div className="flex items-center justify-between">
            <div className="flex-1">
              <h4 className="font-bold text-lg mb-2">Create Allocation</h4>
              <div className="space-y-2 text-sm">
                {selectedVehicle ? (
                  <div className="flex items-center">
                    <Truck className="w-4 h-4 text-blue-500 mr-2" />
                    <span className="font-semibold">Vehicle:</span>
                    <span className="ml-2">{selectedVehicle.name}</span>
                  </div>
                ) : (
                  <div className="flex items-center text-gray-500">
                    <AlertCircle className="w-4 h-4 mr-2" />
                    <span>Select a vehicle</span>
                  </div>
                )}
                
                {selectedLoad ? (
                  <div className="flex items-center">
                    <Package className="w-4 h-4 text-green-500 mr-2" />
                    <span className="font-semibold">Load:</span>
                    <span className="ml-2 truncate">{selectedLoad.pickupLocation.address.split(',')[0]}</span>
                  </div>
                ) : (
                  <div className="flex items-center text-gray-500">
                    <AlertCircle className="w-4 h-4 mr-2" />
                    <span>Select a load</span>
                  </div>
                )}
              </div>
            </div>
            
            <div className="flex items-center space-x-3">
              <button
                onClick={() => {
                  setSelectedVehicle(null);
                  setSelectedLoad(null);
                }}
                className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
              <button
                onClick={handleAllocate}
                disabled={!selectedVehicle || !selectedLoad || allocating}
                className="px-6 py-2 bg-blue-500 hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed text-white font-semibold rounded-lg transition-colors flex items-center"
              >
                {allocating ? (
                  <>
                    <div className="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full mr-2"></div>
                    Allocating...
                  </>
                ) : (
                  <>
                    <CheckCircle className="w-5 h-5 mr-2" />
                    Allocate
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Success Modal */}
      {showSuccessModal && lastAllocation && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl shadow-2xl max-w-2xl w-full p-8 animate-scale-in">
            <div className="text-center mb-6">
              <div className="mx-auto w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mb-4">
                <CheckCircle className="w-12 h-12 text-green-500" />
              </div>
              <h2 className="text-3xl font-bold text-gray-900 mb-2">Allocation Successful!</h2>
              <p className="text-gray-600">Vehicle has been assigned to the load</p>
            </div>

            <div className="bg-gradient-to-r from-blue-50 to-green-50 rounded-xl p-6 mb-6 border-2 border-green-200">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Vehicle Details */}
                <div className="space-y-3">
                  <div className="flex items-center text-blue-600 font-semibold mb-2">
                    <Truck className="w-5 h-5 mr-2" />
                    <span>Vehicle Assigned</span>
                  </div>
                  <div className="bg-white rounded-lg p-4 space-y-2">
                    <div>
                      <p className="text-xs text-gray-500">License Plate</p>
                      <p className="font-bold text-lg">{lastAllocation.vehicle.name}</p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-500">Current Location</p>
                      <p className="text-sm">{lastAllocation.vehicle.currentLocation.address}</p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-500">Status</p>
                      <p className="text-sm font-semibold text-blue-600">{lastAllocation.vehicle.status}</p>
                    </div>
                  </div>
                </div>

                {/* Load Details */}
                <div className="space-y-3">
                  <div className="flex items-center text-green-600 font-semibold mb-2">
                    <Package className="w-5 h-5 mr-2" />
                    <span>Load Details</span>
                  </div>
                  <div className="bg-white rounded-lg p-4 space-y-2">
                    <div>
                      <p className="text-xs text-gray-500">Load ID</p>
                      <p className="font-mono text-sm">#{lastAllocation.load.id.slice(0, 12)}...</p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-500 flex items-center">
                        <MapPin className="w-3 h-3 text-green-500 mr-1" />
                        Pickup Location
                      </p>
                      <p className="text-sm">{lastAllocation.load.pickupLocation.address}</p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-500 flex items-center">
                        <MapPin className="w-3 h-3 text-red-500 mr-1" />
                        Delivery Location
                      </p>
                      <p className="text-sm">{lastAllocation.load.destination.address}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-blue-50 rounded-lg p-4 mb-6 border border-blue-200">
              <p className="text-sm text-blue-800">
                <strong>📱 Next Steps:</strong> The driver will be notified about this allocation and can view it in their "Allocated Loads" section.
              </p>
            </div>

            <button
              onClick={() => setShowSuccessModal(false)}
              className="w-full py-3 bg-gradient-to-r from-blue-500 to-green-500 hover:from-blue-600 hover:to-green-600 text-white font-bold rounded-lg transition-all transform hover:scale-105"
            >
              Done
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ManualAllocation;
