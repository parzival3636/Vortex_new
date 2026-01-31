import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Package, ArrowLeft, Plus, MapPin, DollarSign, Weight } from 'lucide-react';
import toast from 'react-hot-toast';
import MapView from '../components/MapView';
import { vendorsAPI, loadsAPI } from '../services/api';

const VendorDashboard = () => {
  const navigate = useNavigate();
  const [showAddLoad, setShowAddLoad] = useState(false);
  const [myLoads, setMyLoads] = useState([]);
  const [vendorId, setVendorId] = useState(null);
  
  // Form state
  const [pickupAddress, setPickupAddress] = useState('');
  const [destinationAddress, setDestinationAddress] = useState('');
  const [weight, setWeight] = useState('');
  const [price, setPrice] = useState('');
  const [pickupSuggestions, setPickupSuggestions] = useState([]);
  const [destSuggestions, setDestSuggestions] = useState([]);

  // Register vendor on mount (demo)
  useEffect(() => {
    registerVendor();
  }, []);

  const registerVendor = async () => {
    try {
      const response = await vendorsAPI.register({
        name: 'Demo Vendor',
        email: 'vendor@demo.com',
        phone: '+91-9999999999',
        address: 'Azadpur Mandi, Delhi'
      });
      setVendorId(response.data.vendor_id);
      fetchMyLoads(response.data.vendor_id);
    } catch (error) {
      console.error('Vendor registration failed:', error);
    }
  };

  const fetchMyLoads = async (vId) => {
    try {
      const response = await loadsAPI.getAvailableLoads();
      setMyLoads(response.data);
    } catch (error) {
      console.error('Failed to fetch loads:', error);
    }
  };

  const searchPlace = async (query, isPickup) => {
    if (query.length < 3) return;
    
    try {
      const response = await vendorsAPI.searchPlaces(query, 5);
      if (isPickup) {
        setPickupSuggestions(response.data.results);
      } else {
        setDestSuggestions(response.data.results);
      }
    } catch (error) {
      console.error('Search error:', error);
    }
  };

  const createLoad = async () => {
    if (!vendorId || !pickupAddress || !destinationAddress || !weight || !price) {
      toast.error('Please fill all fields');
      return;
    }

    try {
      await vendorsAPI.createLoadByAddress({
        vendor_id: vendorId,
        weight_kg: parseFloat(weight),
        pickup_address: pickupAddress,
        destination_address: destinationAddress,
        price_offered: parseFloat(price),
        currency: 'INR'
      });
      
      toast.success('Load posted successfully!');
      setShowAddLoad(false);
      setPickupAddress('');
      setDestinationAddress('');
      setWeight('');
      setPrice('');
      fetchMyLoads(vendorId);
    } catch (error) {
      toast.error('Failed to post load');
      console.error(error);
    }
  };

  const getMapMarkers = () => {
    return myLoads.map((load, index) => ({
      lat: load.pickup_location.lat,
      lng: load.pickup_location.lng,
      type: 'market',
      title: `Load ${index + 1}`,
      description: `${load.weight_kg}kg - ₹${load.price_offered}`,
      address: load.pickup_location.address,
      info: {
        'Weight': `${load.weight_kg}kg`,
        'Price': `₹${load.price_offered}`,
        'Status': load.status
      }
    }));
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <button onClick={() => navigate('/')} className="p-2 hover:bg-gray-100 rounded-lg">
                <ArrowLeft className="w-6 h-6" />
              </button>
              <Package className="w-8 h-8 text-purple-500" />
              <div>
                <h1 className="text-2xl font-bold">Vendor Dashboard</h1>
                <p className="text-sm text-gray-500">Post loads and find drivers</p>
              </div>
            </div>
            <button
              onClick={() => setShowAddLoad(true)}
              className="bg-purple-500 hover:bg-purple-600 text-white px-4 py-2 rounded-lg flex items-center"
            >
              <Plus className="w-5 h-5 mr-2" />
              Post New Load
            </button>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-6 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-1 space-y-6">
            {/* Stats */}
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-white rounded-xl shadow-sm p-4">
                <p className="text-sm text-gray-500">Active Loads</p>
                <p className="text-2xl font-bold text-purple-600">{myLoads.length}</p>
              </div>
              <div className="bg-white rounded-xl shadow-sm p-4">
                <p className="text-sm text-gray-500">Total Value</p>
                <p className="text-2xl font-bold text-green-600">
                  ₹{myLoads.reduce((sum, load) => sum + load.price_offered, 0).toLocaleString()}
                </p>
              </div>
            </div>

            {/* My Loads */}
            <div className="bg-white rounded-xl shadow-sm p-6">
              <h2 className="text-xl font-bold mb-4">My Posted Loads</h2>
              <div className="space-y-3 max-h-[500px] overflow-y-auto">
                {myLoads.map((load, index) => (
                  <div key={load.load_id} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex justify-between items-start mb-2">
                      <div>
                        <p className="font-semibold">{load.weight_kg}kg</p>
                        <p className="text-sm text-gray-500">{load.status}</p>
                      </div>
                      <p className="text-lg font-bold text-green-600">₹{load.price_offered}</p>
                    </div>
                    <div className="space-y-1 text-sm">
                      <div className="flex items-start">
                        <MapPin className="w-4 h-4 text-green-500 mr-2 mt-0.5" />
                        <p className="text-gray-600 line-clamp-1">{load.pickup_location.address}</p>
                      </div>
                      <div className="flex items-start">
                        <MapPin className="w-4 h-4 text-red-500 mr-2 mt-0.5" />
                        <p className="text-gray-600 line-clamp-1">{load.destination.address}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="lg:col-span-2">
            <div className="bg-white rounded-xl shadow-sm p-4">
              <MapView markers={getMapMarkers()} height="calc(100vh - 200px)" />
            </div>
          </div>
        </div>
      </div>

      {/* Add Load Modal */}
      {showAddLoad && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl max-w-md w-full p-6">
            <h2 className="text-2xl font-bold mb-4">Post New Load</h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">Pickup Address</label>
                <input
                  type="text"
                  value={pickupAddress}
                  onChange={(e) => {
                    setPickupAddress(e.target.value);
                    searchPlace(e.target.value, true);
                  }}
                  placeholder="Enter pickup location..."
                  className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500"
                />
                {pickupSuggestions.length > 0 && (
                  <div className="mt-2 bg-white border rounded-lg shadow-lg max-h-32 overflow-y-auto">
                    {pickupSuggestions.map((s, i) => (
                      <div
                        key={i}
                        onClick={() => {
                          setPickupAddress(s.address);
                          setPickupSuggestions([]);
                        }}
                        className="px-4 py-2 hover:bg-gray-50 cursor-pointer text-sm"
                      >
                        {s.address}
                      </div>
                    ))}
                  </div>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Destination Address</label>
                <input
                  type="text"
                  value={destinationAddress}
                  onChange={(e) => {
                    setDestinationAddress(e.target.value);
                    searchPlace(e.target.value, false);
                  }}
                  placeholder="Enter destination..."
                  className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500"
                />
                {destSuggestions.length > 0 && (
                  <div className="mt-2 bg-white border rounded-lg shadow-lg max-h-32 overflow-y-auto">
                    {destSuggestions.map((s, i) => (
                      <div
                        key={i}
                        onClick={() => {
                          setDestinationAddress(s.address);
                          setDestSuggestions([]);
                        }}
                        className="px-4 py-2 hover:bg-gray-50 cursor-pointer text-sm"
                      >
                        {s.address}
                      </div>
                    ))}
                  </div>
                )}
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Weight (kg)</label>
                  <input
                    type="number"
                    value={weight}
                    onChange={(e) => setWeight(e.target.value)}
                    placeholder="5000"
                    className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Price (₹)</label>
                  <input
                    type="number"
                    value={price}
                    onChange={(e) => setPrice(e.target.value)}
                    placeholder="12000"
                    className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500"
                  />
                </div>
              </div>

              <div className="flex space-x-3 pt-4">
                <button
                  onClick={() => setShowAddLoad(false)}
                  className="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold py-2 rounded-lg"
                >
                  Cancel
                </button>
                <button
                  onClick={createLoad}
                  className="flex-1 bg-purple-500 hover:bg-purple-600 text-white font-semibold py-2 rounded-lg"
                >
                  Post Load
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default VendorDashboard;
