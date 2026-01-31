import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Truck, MapPin, Package, DollarSign, Navigation, 
  ArrowLeft, CheckCircle, XCircle, TrendingUp, Clock 
} from 'lucide-react';
import toast from 'react-hot-toast';
import MapView from '../components/MapView';
import { tripsAPI, loadsAPI, calculateAPI, vendorsAPI, demoAPI, schedulerAPI } from '../services/api';
import { getRoute, getMultipleRoutes } from '../services/routing';

const DriverDashboard = () => {
  const navigate = useNavigate();
  const [step, setStep] = useState('select-route'); // select-route, show-loads, navigate
  const [origin, setOrigin] = useState('');
  const [destination, setDestination] = useState('');
  const [originCoords, setOriginCoords] = useState(null);
  const [destCoords, setDestCoords] = useState(null);
  const [currentTrip, setCurrentTrip] = useState(null);
  const [availableLoads, setAvailableLoads] = useState([]);
  const [selectedLoad, setSelectedLoad] = useState(null);
  const [isDeadheading, setIsDeadheading] = useState(false);
  const [searchingOrigin, setSearchingOrigin] = useState(false);
  const [searchingDest, setSearchingDest] = useState(false);
  const [originSuggestions, setOriginSuggestions] = useState([]);
  const [destSuggestions, setDestSuggestions] = useState([]);
  const [demoData, setDemoData] = useState(null);
  const [roadRoutes, setRoadRoutes] = useState([]); // Store actual road routes

  // Initialize demo data on mount
  useEffect(() => {
    initializeDemoData();
  }, []);

  const initializeDemoData = async () => {
    try {
      const response = await demoAPI.getDemoData();
      setDemoData(response.data);
    } catch (error) {
      console.error('Failed to initialize demo data:', error);
      toast.error('Failed to initialize demo data');
    }
  };

  // Search for places
  const searchPlace = async (query, isOrigin) => {
    if (query.length < 3) return;
    
    try {
      const response = await vendorsAPI.searchPlaces(query, 5);
      const suggestions = response.data.results;
      
      if (isOrigin) {
        setOriginSuggestions(suggestions);
      } else {
        setDestSuggestions(suggestions);
      }
    } catch (error) {
      console.error('Search error:', error);
    }
  };

  // Select origin
  const selectOrigin = (suggestion) => {
    setOrigin(suggestion.address);
    setOriginCoords({ lat: suggestion.lat, lng: suggestion.lng });
    setOriginSuggestions([]);
  };

  // Select destination
  const selectDestination = (suggestion) => {
    setDestination(suggestion.address);
    setDestCoords({ lat: suggestion.lat, lng: suggestion.lng });
    setDestSuggestions([]);
  };

  // Create trip
  const createTrip = async () => {
    if (!originCoords || !destCoords) {
      toast.error('Please select both origin and destination');
      return;
    }

    if (!demoData) {
      toast.error('Demo data not initialized');
      return;
    }

    try {
      const tripData = {
        driver_id: demoData.driver_id,
        truck_id: demoData.truck_id,
        origin: {
          lat: originCoords.lat,
          lng: originCoords.lng,
          address: origin
        },
        destination: {
          lat: destCoords.lat,
          lng: destCoords.lng,
          address: destination
        },
        outbound_load: 'Demo Load'
      };

      const response = await tripsAPI.createTrip(tripData);
      setCurrentTrip(response.data);
      toast.success('Trip created successfully!');
      setStep('show-loads');
      
      // Mark as deadheading and fetch loads
      markAsDeadheading(response.data.trip_id);
    } catch (error) {
      toast.error('Failed to create trip');
      console.error(error);
    }
  };

  // Mark trip as deadheading
  const markAsDeadheading = async (tripId) => {
    try {
      await tripsAPI.markDeadheading(tripId);
      setIsDeadheading(true);
      
      // Trigger auto-scheduler to find optimal load
      toast.info('🤖 AI is finding the best load for you...');
      triggerAutoScheduler(tripId);
      
      // Fetch available loads (for manual selection if needed)
      fetchAvailableLoads();
    } catch (error) {
      console.error('Failed to mark deadheading:', error);
    }
  };

  // Trigger auto-scheduler and check for assignment
  const triggerAutoScheduler = async (tripId) => {
    try {
      // Force scheduler to run immediately
      await schedulerAPI.forceRun();
      
      // Wait a moment for scheduler to complete
      setTimeout(async () => {
        // Check if load was auto-assigned
        const response = await tripsAPI.getAssignedLoad(tripId);
        
        if (response.data.has_assigned_load) {
          const assignedLoad = response.data.load;
          
          // Calculate profitability for the assigned load
          try {
            const profitResponse = await calculateAPI.calculateProfitability({
              driver_current: originCoords,
              driver_destination: destCoords,
              vendor_pickup: {
                lat: assignedLoad.pickup_location.lat,
                lng: assignedLoad.pickup_location.lng,
                address: assignedLoad.pickup_location.address
              },
              vendor_destination: {
                lat: assignedLoad.destination.lat,
                lng: assignedLoad.destination.lng,
                address: assignedLoad.destination.address
              },
              vendor_offering: assignedLoad.price_offered
            });
            
            assignedLoad.profitability = profitResponse.data;
          } catch (error) {
            console.error('Failed to calculate profitability:', error);
          }
          
          // Auto-accept the assigned load
          setSelectedLoad(assignedLoad);
          setStep('navigate');
          toast.success(`🎉 AI found the best load! Profit: ₹${assignedLoad.profitability?.net_profit || assignedLoad.price_offered}`);
        } else {
          // No auto-assignment, show manual selection
          toast.info('No optimal load found automatically. Please select manually.');
        }
      }, 3000); // Wait 3 seconds for scheduler
      
    } catch (error) {
      console.error('Failed to trigger auto-scheduler:', error);
      toast.error('Auto-scheduler failed. Please select load manually.');
    }
  };

  // Fetch available loads
  const fetchAvailableLoads = async () => {
    try {
      const response = await loadsAPI.getAvailableLoads();
      const loads = response.data;
      
      // Calculate profitability for each load
      const loadsWithProfit = await Promise.all(
        loads.map(async (load) => {
          try {
            const profitResponse = await calculateAPI.calculateProfitability({
              driver_current: originCoords,
              driver_destination: destCoords,
              vendor_pickup: {
                lat: load.pickup_location.lat,
                lng: load.pickup_location.lng,
                address: load.pickup_location.address
              },
              vendor_destination: {
                lat: load.destination.lat,
                lng: load.destination.lng,
                address: load.destination.address
              },
              vendor_offering: load.price_offered
            });
            
            return {
              ...load,
              profitability: profitResponse.data
            };
          } catch (error) {
            return load;
          }
        })
      );

      // Sort by profitability score
      loadsWithProfit.sort((a, b) => 
        (b.profitability?.profitability_score || 0) - (a.profitability?.profitability_score || 0)
      );

      setAvailableLoads(loadsWithProfit);
    } catch (error) {
      console.error('Failed to fetch loads:', error);
      toast.error('Failed to fetch available loads');
    }
  };

  // Accept load
  const acceptLoad = async (load) => {
    if (!currentTrip) return;

    try {
      await loadsAPI.acceptLoad(load.load_id, currentTrip.trip_id);
      setSelectedLoad(load);
      setStep('navigate');
      toast.success('Load accepted! Starting navigation...');
    } catch (error) {
      toast.error('Failed to accept load');
      console.error(error);
    }
  };

  // Confirm pickup
  const confirmPickup = async () => {
    if (!currentTrip) {
      toast.error('No active trip');
      return;
    }

    try {
      await tripsAPI.confirmPickup(currentTrip.trip_id);
      toast.success('Pickup confirmed! Heading to delivery location...');
      
      // Update load status to picked_up
      if (selectedLoad) {
        // You could add an API call here to update load status
        console.log('Load picked up:', selectedLoad.load_id);
      }
    } catch (error) {
      toast.error('Failed to confirm pickup');
      console.error(error);
    }
  };

  // Get map markers
  const getMapMarkers = () => {
    const markers = [];

    if (step === 'select-route' || step === 'show-loads') {
      if (originCoords) {
        markers.push({
          lat: originCoords.lat,
          lng: originCoords.lng,
          type: 'truck',
          title: 'Origin',
          address: origin
        });
      }
      if (destCoords) {
        markers.push({
          lat: destCoords.lat,
          lng: destCoords.lng,
          type: 'destination',
          title: 'Destination',
          address: destination
        });
      }
    }

    if (step === 'show-loads') {
      availableLoads.forEach((load, index) => {
        markers.push({
          lat: load.pickup_location.lat,
          lng: load.pickup_location.lng,
          type: 'vendor',
          title: `Load ${index + 1}`,
          description: `${load.weight_kg}kg - ₹${load.price_offered}`,
          address: load.pickup_location.address,
          info: load.profitability ? {
            'Profit': `₹${load.profitability.net_profit}`,
            'Extra Distance': `${load.profitability.extra_distance_km}km`,
            'Score': load.profitability.profitability_score.toFixed(2)
          } : {}
        });
      });
    }

    if (step === 'navigate' && selectedLoad) {
      markers.push(
        {
          lat: originCoords.lat,
          lng: originCoords.lng,
          type: 'truck',
          title: 'Current Location',
          address: origin
        },
        {
          lat: selectedLoad.pickup_location.lat,
          lng: selectedLoad.pickup_location.lng,
          type: 'pickup',
          title: 'Pickup Location',
          address: selectedLoad.pickup_location.address
        },
        {
          lat: selectedLoad.destination.lat,
          lng: selectedLoad.destination.lng,
          type: 'delivery',
          title: 'Delivery Location',
          address: selectedLoad.destination.address
        },
        {
          lat: destCoords.lat,
          lng: destCoords.lng,
          type: 'destination',
          title: 'Final Destination',
          address: destination
        }
      );
    }

    return markers;
  };

  // Get map routes with real road routing
  const getMapRoutes = () => {
    // Return the fetched road routes
    return roadRoutes;
  };

  // Fetch road routes when navigation starts
  useEffect(() => {
    const fetchRoadRoutes = async () => {
      if (step === 'navigate' && selectedLoad && originCoords && destCoords) {
        try {
          // Fetch all three route segments
          const routes = await getMultipleRoutes([
            {
              start: originCoords,
              end: { lat: selectedLoad.pickup_location.lat, lng: selectedLoad.pickup_location.lng }
            },
            {
              start: { lat: selectedLoad.pickup_location.lat, lng: selectedLoad.pickup_location.lng },
              end: { lat: selectedLoad.destination.lat, lng: selectedLoad.destination.lng }
            },
            {
              start: { lat: selectedLoad.destination.lat, lng: selectedLoad.destination.lng },
              end: destCoords
            }
          ]);

          setRoadRoutes([
            {
              positions: routes[0].coordinates,
              color: '#10B981', // Green - to pickup
              weight: 5,
              opacity: 0.8
            },
            {
              positions: routes[1].coordinates,
              color: '#F59E0B', // Orange - pickup to delivery
              weight: 5,
              opacity: 0.8
            },
            {
              positions: routes[2].coordinates,
              color: '#3B82F6', // Blue - delivery to home
              weight: 4,
              opacity: 0.6,
              dashed: true
            }
          ]);
        } catch (error) {
          console.error('Failed to fetch road routes:', error);
          // Fallback to straight lines
          setRoadRoutes([
            {
              positions: [
                [originCoords.lat, originCoords.lng],
                [selectedLoad.pickup_location.lat, selectedLoad.pickup_location.lng]
              ],
              color: '#10B981',
              weight: 4
            },
            {
              positions: [
                [selectedLoad.pickup_location.lat, selectedLoad.pickup_location.lng],
                [selectedLoad.destination.lat, selectedLoad.destination.lng]
              ],
              color: '#F59E0B',
              weight: 4
            },
            {
              positions: [
                [selectedLoad.destination.lat, selectedLoad.destination.lng],
                [destCoords.lat, destCoords.lng]
              ],
              color: '#3B82F6',
              weight: 4,
              dashed: true
            }
          ]);
        }
      } else if (step === 'select-route' && originCoords && destCoords) {
        // Fetch route for initial planning
        try {
          const route = await getRoute(originCoords, destCoords);
          setRoadRoutes([
            {
              positions: route.coordinates,
              color: '#3B82F6',
              weight: 4,
              opacity: 0.7
            }
          ]);
        } catch (error) {
          console.error('Failed to fetch route:', error);
          setRoadRoutes([
            {
              positions: [
                [originCoords.lat, originCoords.lng],
                [destCoords.lat, destCoords.lng]
              ],
              color: '#3B82F6',
              weight: 4
            }
          ]);
        }
      } else {
        setRoadRoutes([]);
      }
    };

    fetchRoadRoutes();
  }, [step, selectedLoad, originCoords, destCoords]);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <button
                onClick={() => navigate('/')}
                className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <ArrowLeft className="w-6 h-6" />
              </button>
              <Truck className="w-8 h-8 text-blue-500" />
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Driver Dashboard</h1>
                <p className="text-sm text-gray-500">Find profitable return loads</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-right">
                <p className="text-sm text-gray-500">Today's Earnings</p>
                <p className="text-2xl font-bold text-green-600">₹12,450</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-6 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Panel - Controls */}
          <div className="lg:col-span-1 space-y-6">
            {/* Step 1: Select Route */}
            {step === 'select-route' && (
              <div className="bg-white rounded-xl shadow-sm p-6">
                <h2 className="text-xl font-bold mb-4 flex items-center">
                  <MapPin className="w-5 h-5 mr-2 text-blue-500" />
                  Select Your Route
                </h2>
                
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Origin (Current Location)
                    </label>
                    <input
                      type="text"
                      value={origin}
                      onChange={(e) => {
                        setOrigin(e.target.value);
                        searchPlace(e.target.value, true);
                      }}
                      placeholder="Enter origin address..."
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                    {originSuggestions.length > 0 && (
                      <div className="mt-2 bg-white border border-gray-200 rounded-lg shadow-lg max-h-48 overflow-y-auto">
                        {originSuggestions.map((suggestion, index) => (
                          <div
                            key={index}
                            onClick={() => selectOrigin(suggestion)}
                            className="px-4 py-2 hover:bg-gray-50 cursor-pointer border-b last:border-b-0"
                          >
                            <p className="text-sm font-medium">{suggestion.address}</p>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Destination (Home/Base)
                    </label>
                    <input
                      type="text"
                      value={destination}
                      onChange={(e) => {
                        setDestination(e.target.value);
                        searchPlace(e.target.value, false);
                      }}
                      placeholder="Enter destination address..."
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                    {destSuggestions.length > 0 && (
                      <div className="mt-2 bg-white border border-gray-200 rounded-lg shadow-lg max-h-48 overflow-y-auto">
                        {destSuggestions.map((suggestion, index) => (
                          <div
                            key={index}
                            onClick={() => selectDestination(suggestion)}
                            className="px-4 py-2 hover:bg-gray-50 cursor-pointer border-b last:border-b-0"
                          >
                            <p className="text-sm font-medium">{suggestion.address}</p>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>

                  <button
                    onClick={createTrip}
                    disabled={!originCoords || !destCoords}
                    className="w-full bg-blue-500 hover:bg-blue-600 disabled:bg-gray-300 text-white font-semibold py-3 rounded-lg transition-colors flex items-center justify-center"
                  >
                    <Navigation className="w-5 h-5 mr-2" />
                    Find Return Loads
                  </button>
                </div>
              </div>
            )}

            {/* Step 2: Show Available Loads */}
            {step === 'show-loads' && (
              <div className="bg-white rounded-xl shadow-sm p-6">
                <h2 className="text-xl font-bold mb-4 flex items-center">
                  <Package className="w-5 h-5 mr-2 text-green-500" />
                  Available Loads ({availableLoads.length})
                </h2>
                
                <div className="space-y-3 max-h-[600px] overflow-y-auto">
                  {availableLoads.map((load, index) => (
                    <div
                      key={load.load_id}
                      className="border border-gray-200 rounded-lg p-4 hover:border-blue-500 transition-colors cursor-pointer"
                      onClick={() => acceptLoad(load)}
                    >
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex items-center">
                          <div className="bg-blue-100 text-blue-600 font-bold w-8 h-8 rounded-full flex items-center justify-center mr-3">
                            {index + 1}
                          </div>
                          <div>
                            <p className="font-semibold text-gray-900">{load.weight_kg}kg</p>
                            <p className="text-xs text-gray-500">Load Weight</p>
                          </div>
                        </div>
                        {load.profitability && (
                          <div className="text-right">
                            <p className="text-lg font-bold text-green-600">
                              ₹{load.profitability.net_profit}
                            </p>
                            <p className="text-xs text-gray-500">Net Profit</p>
                          </div>
                        )}
                      </div>

                      <div className="space-y-1 text-sm">
                        <div className="flex items-start">
                          <MapPin className="w-4 h-4 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                          <p className="text-gray-600 line-clamp-1">{load.pickup_location.address}</p>
                        </div>
                        <div className="flex items-start">
                          <MapPin className="w-4 h-4 text-red-500 mr-2 mt-0.5 flex-shrink-0" />
                          <p className="text-gray-600 line-clamp-1">{load.destination.address}</p>
                        </div>
                      </div>

                      {load.profitability && (
                        <div className="mt-3 pt-3 border-t border-gray-100 grid grid-cols-3 gap-2 text-xs">
                          <div>
                            <p className="text-gray-500">Extra Distance</p>
                            <p className="font-semibold">{load.profitability.extra_distance_km}km</p>
                          </div>
                          <div>
                            <p className="text-gray-500">Fuel Cost</p>
                            <p className="font-semibold">₹{load.profitability.fuel_cost}</p>
                          </div>
                          <div>
                            <p className="text-gray-500">Score</p>
                            <p className="font-semibold">{load.profitability.profitability_score.toFixed(1)}</p>
                          </div>
                        </div>
                      )}

                      <button className="w-full mt-3 bg-green-500 hover:bg-green-600 text-white font-semibold py-2 rounded-lg transition-colors text-sm">
                        Accept Load
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Step 3: Navigation */}
            {step === 'navigate' && selectedLoad && (
              <div className="bg-white rounded-xl shadow-sm p-6">
                <h2 className="text-xl font-bold mb-4 flex items-center">
                  <Navigation className="w-5 h-5 mr-2 text-blue-500" />
                  Navigation Active
                </h2>
                
                <div className="space-y-4">
                  <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                    <p className="text-sm font-medium text-green-800 mb-1">Load Accepted!</p>
                    <p className="text-2xl font-bold text-green-600">
                      ₹{selectedLoad.profitability?.net_profit || selectedLoad.price_offered}
                    </p>
                    <p className="text-xs text-green-600">Expected Profit</p>
                  </div>

                  <div className="space-y-3">
                    <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
                      <div className="flex items-center">
                        <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-white font-bold mr-3">
                          1
                        </div>
                        <div>
                          <p className="font-semibold text-sm">Go to Pickup</p>
                          <p className="text-xs text-gray-600 line-clamp-1">
                            {selectedLoad.pickup_location.address}
                          </p>
                        </div>
                      </div>
                      <CheckCircle className="w-5 h-5 text-blue-500" />
                    </div>

                    <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                      <div className="flex items-center">
                        <div className="w-8 h-8 bg-gray-400 rounded-full flex items-center justify-center text-white font-bold mr-3">
                          2
                        </div>
                        <div>
                          <p className="font-semibold text-sm">Deliver Load</p>
                          <p className="text-xs text-gray-600 line-clamp-1">
                            {selectedLoad.destination.address}
                          </p>
                        </div>
                      </div>
                    </div>

                    <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                      <div className="flex items-center">
                        <div className="w-8 h-8 bg-gray-400 rounded-full flex items-center justify-center text-white font-bold mr-3">
                          3
                        </div>
                        <div>
                          <p className="font-semibold text-sm">Return Home</p>
                          <p className="text-xs text-gray-600 line-clamp-1">{destination}</p>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="pt-4 border-t">
                    <button 
                      onClick={confirmPickup}
                      className="w-full bg-green-500 hover:bg-green-600 text-white font-semibold py-3 rounded-lg transition-colors"
                    >
                      Confirm Pickup
                    </button>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Right Panel - Map */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-xl shadow-sm p-4">
              <MapView
                markers={getMapMarkers()}
                routes={getMapRoutes()}
                height="calc(100vh - 200px)"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DriverDashboard;
