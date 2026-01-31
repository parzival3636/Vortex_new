import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Truck, MapPin, Package, Navigation, 
  ArrowLeft, CheckCircle, X
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
  const [loadingOrigin, setLoadingOrigin] = useState(false);
  const [loadingDest, setLoadingDest] = useState(false);
  const [originSuggestions, setOriginSuggestions] = useState([]);
  const [destSuggestions, setDestSuggestions] = useState([]);
  const [demoData, setDemoData] = useState(null);
  const [roadRoutes, setRoadRoutes] = useState([]); // Store actual road routes
  const [showAutoAssignModal, setShowAutoAssignModal] = useState(false); // Show AI assignment modal
  const [autoAssignedLoad, setAutoAssignedLoad] = useState(null); // Store auto-assigned load details
  const [isAutoAssigning, setIsAutoAssigning] = useState(false); // Show loading state
  
  // Refs for debouncing
  const originTimeoutRef = useRef(null);
  const destTimeoutRef = useRef(null);

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

  // Search for places with debouncing
  const searchPlace = async (query, isOrigin) => {
    if (query.length < 3) {
      if (isOrigin) {
        setOriginSuggestions([]);
      } else {
        setDestSuggestions([]);
      }
      return;
    }
    
    // Set loading state
    if (isOrigin) {
      setLoadingOrigin(true);
    } else {
      setLoadingDest(true);
    }
    
    try {
      const response = await vendorsAPI.searchPlaces(query, 8);
      const suggestions = response.data.results || [];
      
      if (isOrigin) {
        setOriginSuggestions(suggestions);
        setLoadingOrigin(false);
      } else {
        setDestSuggestions(suggestions);
        setLoadingDest(false);
      }
    } catch (error) {
      console.error('Search error:', error);
      if (isOrigin) {
        setLoadingOrigin(false);
      } else {
        setLoadingDest(false);
      }
    }
  };

  // Handle input change with debouncing
  const handleOriginChange = (value) => {
    setOrigin(value);
    
    // Clear previous timeout
    if (originTimeoutRef.current) {
      clearTimeout(originTimeoutRef.current);
    }
    
    // Set new timeout for debounced search
    originTimeoutRef.current = setTimeout(() => {
      searchPlace(value, true);
    }, 300); // 300ms debounce
  };

  const handleDestChange = (value) => {
    setDestination(value);
    
    // Clear previous timeout
    if (destTimeoutRef.current) {
      clearTimeout(destTimeoutRef.current);
    }
    
    // Set new timeout for debounced search
    destTimeoutRef.current = setTimeout(() => {
      searchPlace(value, false);
    }, 300); // 300ms debounce
  };

  // Cleanup timeouts on unmount
  useEffect(() => {
    return () => {
      if (originTimeoutRef.current) {
        clearTimeout(originTimeoutRef.current);
      }
      if (destTimeoutRef.current) {
        clearTimeout(destTimeoutRef.current);
      }
    };
  }, []);

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
      
      // Trigger auto-scheduler to find optimal load
      toast('🤖 AI is finding the best load for you...', {
        icon: '🤖',
        duration: 4000
      });
      triggerAutoScheduler(tripId);
      
      // Fetch available loads (for manual selection if needed)
      fetchAvailableLoads();
    } catch (error) {
      console.error('Failed to mark deadheading:', error);
      toast.error('Failed to mark trip as deadheading');
    }
  };

  // Trigger auto-scheduler and check for assignment
  const triggerAutoScheduler = async (tripId) => {
    try {
      setIsAutoAssigning(true);
      
      // Force scheduler to run immediately
      console.log('🤖 Triggering AI scheduler...');
      await schedulerAPI.forceRun();
      
      // Wait a moment for scheduler to complete
      setTimeout(async () => {
        console.log('✅ Checking for auto-assignment...');
        
        // Check if load was auto-assigned
        const response = await tripsAPI.getAssignedLoad(tripId);
        
        console.log('Assignment response:', response.data);
        
        if (response.data.has_assigned_load) {
          const assignedLoad = response.data.load;
          
          console.log('🎉 Load auto-assigned!', assignedLoad);
          
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
            console.log('💰 Profitability calculated:', assignedLoad.profitability);
          } catch (error) {
            console.error('Failed to calculate profitability:', error);
          }
          
          // Show auto-assignment modal with detailed journey info
          setAutoAssignedLoad(assignedLoad);
          setShowAutoAssignModal(true);
          setIsAutoAssigning(false);
          
          // Auto-accept the assigned load
          setSelectedLoad(assignedLoad);
          setStep('navigate');
          
          // Show detailed success message
          toast.success(
            `🤖 AI Auto-Assigned Load!\n` +
            `Journey: ${origin.split(',')[0]} → ${assignedLoad.pickup_location.address.split(',')[0]} → ${assignedLoad.destination.address.split(',')[0]}\n` +
            `Profit: ₹${assignedLoad.profitability?.net_profit || assignedLoad.price_offered}`,
            {
              duration: 6000,
              style: {
                minWidth: '300px'
              }
            }
          );
        } else {
          console.log('ℹ️ No auto-assignment found');
          setIsAutoAssigning(false);
          // No auto-assignment, show manual selection
          toast.info('No optimal load found automatically. Please select manually.');
        }
      }, 3000); // Wait 3 seconds for scheduler
      
    } catch (error) {
      console.error('Failed to trigger auto-scheduler:', error);
      setIsAutoAssigning(false);
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

      // BALANCED SORTING: Distance to Pickup + Payment Price
      // Compare: Driver START → Load PICKUP distance + Load PAYMENT
      loadsWithProfit.sort((a, b) => {
        const aProfit = a.profitability;
        const bProfit = b.profitability;
        
        // If no profitability data, put at end
        if (!aProfit && !bProfit) return 0;
        if (!aProfit) return 1;
        if (!bProfit) return -1;
        
        // Calculate distance from DRIVER START to LOAD PICKUP
        const calculatePickupDistance = (load) => {
          const lat1 = originCoords.lat;  // DRIVER START POINT
          const lon1 = originCoords.lng;
          const lat2 = load.pickup_location.lat;  // LOAD PICKUP POINT
          const lon2 = load.pickup_location.lng;
          
          // Haversine formula
          const R = 6371;
          const dLat = (lat2 - lat1) * Math.PI / 180;
          const dLon = (lon2 - lon1) * Math.PI / 180;
          const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
                   Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
                   Math.sin(dLon/2) * Math.sin(dLon/2);
          const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
          return R * c;
        };
        
        const distA = calculatePickupDistance(a);
        const distB = calculatePickupDistance(b);
        
        // BALANCED SCORE: 60% Distance + 40% Payment
        const calculateScore = (load, distToPickup) => {
          // Distance score (60%) - closer is better
          // 0km = 100 points, 500km = 0 points
          const distanceScore = Math.max(0, 100 - (distToPickup / 5));
          
          // Payment score (40%) - higher payment is better
          // ₹20,000 = 100 points
          const paymentScore = Math.min(100, (load.price_offered / 200));
          
          return (distanceScore * 0.6) + (paymentScore * 0.4);
        };
        
        const scoreA = calculateScore(a, distA);
        const scoreB = calculateScore(b, distB);
        
        // Sort by score (higher is better)
        return scoreB - scoreA;
      });

      console.log('🚛 DRIVER START:', origin.split(',')[0]);
      console.log('🏁 DRIVER DESTINATION:', destination.split(',')[0]);
      console.log('');
      console.log('📦 LOADS RANKED BY: Distance to Pickup (60%) + Payment (40%)');
      console.log('='.repeat(70));
      
      loadsWithProfit.forEach((l, index) => {
        // Calculate distance to pickup
        const lat1 = originCoords.lat;
        const lon1 = originCoords.lng;
        const lat2 = l.pickup_location.lat;
        const lon2 = l.pickup_location.lng;
        const R = 6371;
        const dLat = (lat2 - lat1) * Math.PI / 180;
        const dLon = (lon2 - lon1) * Math.PI / 180;
        const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
                 Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
                 Math.sin(dLon/2) * Math.sin(dLon/2);
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
        const distToPickup = Math.round(R * c);
        
        // Calculate scores
        const distScore = Math.max(0, 100 - (distToPickup / 5));
        const paymentScore = Math.min(100, (l.price_offered / 200));
        const totalScore = (distScore * 0.6) + (paymentScore * 0.4);
        
        console.log(`${index === 0 ? '⭐ ' : ''}#${index + 1} ${index === 0 ? 'TOP PICK' : ''}`);
        console.log(`   📍 Pickup: ${l.pickup_location.address.split(',').slice(0, 2).join(',')}`);
        console.log(`   🎯 Delivery: ${l.destination.address.split(',').slice(0, 2).join(',')}`);
        console.log(`   📏 Distance from ${origin.split(',')[0]} to Pickup: ${distToPickup}km`);
        console.log(`   💰 Payment: ₹${l.price_offered.toLocaleString()}`);
        console.log(`   📊 Distance Score (60%): ${distScore.toFixed(1)}`);
        console.log(`   📊 Payment Score (40%): ${paymentScore.toFixed(1)}`);
        console.log(`   ⭐ TOTAL SCORE: ${totalScore.toFixed(1)}`);
        console.log('');
      });

      setAvailableLoads(loadsWithProfit);
    } catch (error) {
      console.error('Failed to fetch loads:', error);
      toast.error('Failed to fetch available loads');
    }
  };

  // Accept load
  const acceptLoad = async (load) => {
    console.log('🔵 acceptLoad called with:', { load, currentTrip });
    
    if (!currentTrip) {
      console.error('❌ No current trip!');
      toast.error('No active trip. Please create a trip first.');
      return;
    }

    if (!load || !load.load_id) {
      console.error('❌ Invalid load:', load);
      toast.error('Invalid load data');
      return;
    }

    try {
      console.log('📤 Accepting load:', load.load_id, 'for trip:', currentTrip.trip_id);
      await loadsAPI.acceptLoad(load.load_id, currentTrip.trip_id);
      console.log('✅ Load accepted successfully');
      setSelectedLoad(load);
      setStep('navigate');
      toast.success('Load accepted! Starting navigation...');
    } catch (error) {
      console.error('❌ Failed to accept load:', error);
      toast.error(`Failed to accept load: ${error.message || 'Unknown error'}`);
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

  // Get map markers with proper 3-point route (driver start → pickup → delivery)
  const getMapMarkers = () => {
    const markers = [];

    if (step === 'select-route' || step === 'show-loads') {
      if (originCoords) {
        markers.push({
          lat: originCoords.lat,
          lng: originCoords.lng,
          type: 'truck',
          title: 'Your Current Location',
          address: origin,
          description: 'Starting Point',
          info: {
            'Status': 'Ready to Start'
          }
        });
      }
      if (destCoords) {
        markers.push({
          lat: destCoords.lat,
          lng: destCoords.lng,
          type: 'destination',
          title: 'Your Destination',
          address: destination,
          description: 'Final Destination'
        });
      }
    }

    if (step === 'show-loads') {
      availableLoads.forEach((load, index) => {
        markers.push({
          lat: load.pickup_location.lat,
          lng: load.pickup_location.lng,
          type: 'vendor',
          title: `Load ${index + 1} - Pickup`,
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

    // 3-POINT ROUTE: Driver Start → Load Pickup → Load Delivery
    if (step === 'navigate' && selectedLoad) {
      markers.push(
        {
          lat: originCoords.lat,
          lng: originCoords.lng,
          type: 'truck',
          title: '1. Your Starting Point',
          address: origin,
          description: 'Driver Current Location',
          info: {
            'Status': 'Starting Journey',
            'Next Stop': 'Load Pickup'
          },
          radius: 5000
        },
        {
          lat: selectedLoad.pickup_location.lat,
          lng: selectedLoad.pickup_location.lng,
          type: 'pickup',
          title: '2. Load Pickup Location',
          address: selectedLoad.pickup_location.address,
          description: `Pickup ${selectedLoad.weight_kg}kg`,
          info: {
            'Weight': `${selectedLoad.weight_kg}kg`,
            'Payment': `₹${selectedLoad.price_offered}`,
            'Status': 'Pending Pickup'
          },
          eta: '1h 30m'
        },
        {
          lat: selectedLoad.destination.lat,
          lng: selectedLoad.destination.lng,
          type: 'delivery',
          title: '3. Load Delivery Location',
          address: selectedLoad.destination.address,
          description: 'Final Delivery Point',
          info: {
            'Delivery': selectedLoad.destination.address.split(',')[0],
            'Status': 'Awaiting Delivery'
          },
          eta: '3h 45m'
        }
      );
    }

    return markers;
  };

  // Get map routes with real road routing and completion status
  const getMapRoutes = () => {
    if (step === 'navigate' && selectedLoad && roadRoutes.length >= 3) {
      // Mark routes as completed or remaining based on navigation state
      return [
        {
          ...roadRoutes[0],
          completed: false, // To pickup (in progress)
          color: '#10B981',
          weight: 6
        },
        {
          ...roadRoutes[1],
          remaining: true, // Pickup to delivery (not started)
          weight: 5
        },
        {
          ...roadRoutes[2],
          remaining: true, // Delivery to home (not started)
          weight: 4
        }
      ];
    }
    return roadRoutes;
  };

  // Fetch road routes when navigation starts - 3 SEGMENTS
  useEffect(() => {
    const fetchRoadRoutes = async () => {
      if (step === 'navigate' && selectedLoad && originCoords && destCoords) {
        try {
          // Fetch THREE route segments:
          // 1. Driver Start → Load Pickup
          // 2. Load Pickup → Load Delivery
          // 3. (Optional: Load Delivery → Driver Final Destination if different)
          
          const routes = await getMultipleRoutes([
            {
              start: originCoords,
              end: { lat: selectedLoad.pickup_location.lat, lng: selectedLoad.pickup_location.lng }
            },
            {
              start: { lat: selectedLoad.pickup_location.lat, lng: selectedLoad.pickup_location.lng },
              end: { lat: selectedLoad.destination.lat, lng: selectedLoad.destination.lng }
            }
          ]);

          setRoadRoutes([
            {
              positions: routes[0].coordinates,
              color: '#3B82F6', // Blue - to pickup
              weight: 6,
              opacity: 0.8,
              remaining: true // Not started yet
            },
            {
              positions: routes[1].coordinates,
              color: '#10B981', // Green - pickup to delivery (main journey)
              weight: 6,
              opacity: 0.8,
              remaining: true // Not started yet
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
              color: '#3B82F6',
              weight: 5,
              remaining: true
            },
            {
              positions: [
                [selectedLoad.pickup_location.lat, selectedLoad.pickup_location.lng],
                [selectedLoad.destination.lat, selectedLoad.destination.lng]
              ],
              color: '#10B981',
              weight: 5,
              remaining: true
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

      {/* AI Auto-Assigning Banner */}
      {isAutoAssigning && (
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-4 px-6 shadow-lg">
          <div className="container mx-auto flex items-center justify-center space-x-3 animate-pulse">
            <span className="text-3xl">🤖</span>
            <span className="font-bold text-xl">AI is finding the best load for you...</span>
            <span className="text-3xl">✨</span>
          </div>
        </div>
      )}

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
                  <div className="relative">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Origin (Current Location) <span className="text-red-500">*</span>
                    </label>
                    <div className="relative">
                      <input
                        type="text"
                        value={origin}
                        onChange={(e) => handleOriginChange(e.target.value)}
                        placeholder="Type street, landmark, or area..."
                        className="w-full px-4 py-2 pr-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                      {loadingOrigin && (
                        <div className="absolute right-3 top-1/2 -translate-y-1/2">
                          <div className="animate-spin h-5 w-5 border-2 border-blue-500 border-t-transparent rounded-full"></div>
                        </div>
                      )}
                      {!loadingOrigin && origin && (
                        <button
                          onClick={() => {
                            setOrigin('');
                            setOriginSuggestions([]);
                            setOriginCoords(null);
                          }}
                          className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                        >
                          <X className="w-5 h-5" />
                        </button>
                      )}
                    </div>
                    {originSuggestions.length > 0 && (
                      <div className="absolute z-10 w-full mt-1 bg-white border border-gray-200 rounded-lg shadow-lg max-h-60 overflow-y-auto">
                        {originSuggestions.map((suggestion, index) => (
                          <div
                            key={index}
                            onClick={() => selectOrigin(suggestion)}
                            className="px-4 py-3 hover:bg-blue-50 cursor-pointer border-b last:border-b-0 transition-colors"
                          >
                            <div className="flex items-start">
                              <MapPin className="w-4 h-4 text-blue-500 mr-2 mt-1 flex-shrink-0" />
                              <div className="flex-1 min-w-0">
                                <p className="text-sm font-medium text-gray-900 truncate">{suggestion.address}</p>
                                {suggestion.type && (
                                  <p className="text-xs text-gray-500 mt-0.5">{suggestion.type}</p>
                                )}
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>

                  <div className="relative">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Destination (Home/Base) <span className="text-red-500">*</span>
                    </label>
                    <div className="relative">
                      <input
                        type="text"
                        value={destination}
                        onChange={(e) => handleDestChange(e.target.value)}
                        placeholder="Type street, landmark, or area..."
                        className="w-full px-4 py-2 pr-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                      {loadingDest && (
                        <div className="absolute right-3 top-1/2 -translate-y-1/2">
                          <div className="animate-spin h-5 w-5 border-2 border-blue-500 border-t-transparent rounded-full"></div>
                        </div>
                      )}
                      {!loadingDest && destination && (
                        <button
                          onClick={() => {
                            setDestination('');
                            setDestSuggestions([]);
                            setDestCoords(null);
                          }}
                          className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                        >
                          <X className="w-5 h-5" />
                        </button>
                      )}
                    </div>
                    {destSuggestions.length > 0 && (
                      <div className="absolute z-10 w-full mt-1 bg-white border border-gray-200 rounded-lg shadow-lg max-h-60 overflow-y-auto">
                        {destSuggestions.map((suggestion, index) => (
                          <div
                            key={index}
                            onClick={() => selectDestination(suggestion)}
                            className="px-4 py-3 hover:bg-blue-50 cursor-pointer border-b last:border-b-0 transition-colors"
                          >
                            <div className="flex items-start">
                              <MapPin className="w-4 h-4 text-red-500 mr-2 mt-1 flex-shrink-0" />
                              <div className="flex-1 min-w-0">
                                <p className="text-sm font-medium text-gray-900 truncate">{suggestion.address}</p>
                                {suggestion.type && (
                                  <p className="text-xs text-gray-500 mt-0.5">{suggestion.type}</p>
                                )}
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>

                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 text-sm text-blue-800">
                    <p className="font-medium mb-1">💡 Tips for accurate location:</p>
                    <ul className="list-disc list-inside space-y-1 text-xs">
                      <li>Type at least 3 characters to see suggestions</li>
                      <li>Include street name or landmark for precision</li>
                      <li>Select from dropdown for accurate GPS</li>
                    </ul>
                  </div>

                  <button
                    onClick={createTrip}
                    disabled={!originCoords || !destCoords}
                    className="w-full bg-blue-500 hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed text-white font-semibold py-3 rounded-lg transition-colors flex items-center justify-center"
                  >
                    <Navigation className="w-5 h-5 mr-2" />
                    Find Return Loads
                  </button>
                </div>
              </div>
            )}

            {/* Step 2: Show Available Loads with Top Pick */}
            {step === 'show-loads' && (
              <>
                {/* TOP PICK SECTION - Best Filtered Choice */}
                {availableLoads.length > 0 && availableLoads[0].profitability && (
                  <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-xl shadow-lg p-6 mb-6 border-2 border-green-500">
                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center">
                        <div className="bg-gradient-to-r from-green-500 to-emerald-500 text-white px-4 py-2 rounded-full font-bold text-sm flex items-center shadow-lg">
                          <span className="mr-2">⭐</span>
                          TOP PICK
                          <span className="ml-2">🎯</span>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className="text-sm text-gray-600">Best Match Score</p>
                        <p className="text-3xl font-bold text-green-600">
                          {availableLoads[0].profitability.profitability_score.toFixed(1)}
                        </p>
                      </div>
                    </div>

                    <div className="bg-white rounded-lg p-5 shadow-md">
                      {/* Load Details */}
                      <div className="grid grid-cols-2 gap-4 mb-4">
                        <div className="bg-blue-50 p-3 rounded-lg">
                          <p className="text-xs text-gray-600 mb-1">Load Weight</p>
                          <p className="text-2xl font-bold text-blue-600">{availableLoads[0].weight_kg}kg</p>
                        </div>
                        <div className="bg-green-50 p-3 rounded-lg">
                          <p className="text-xs text-gray-600 mb-1">Net Profit</p>
                          <p className="text-2xl font-bold text-green-600">₹{availableLoads[0].profitability.net_profit.toLocaleString()}</p>
                        </div>
                      </div>

                      {/* Route */}
                      <div className="space-y-2 mb-4">
                        <div className="flex items-start">
                          <MapPin className="w-4 h-4 text-green-500 mr-2 mt-1 flex-shrink-0" />
                          <div className="flex-1">
                            <p className="text-xs text-gray-500">Pickup Location</p>
                            <p className="font-semibold text-gray-800 text-sm">{availableLoads[0].pickup_location.address}</p>
                          </div>
                        </div>
                        <div className="flex items-start">
                          <MapPin className="w-4 h-4 text-red-500 mr-2 mt-1 flex-shrink-0" />
                          <div className="flex-1">
                            <p className="text-xs text-gray-500">Delivery Location</p>
                            <p className="font-semibold text-gray-800 text-sm">{availableLoads[0].destination.address}</p>
                          </div>
                        </div>
                      </div>

                      {/* AI Reasoning */}
                      <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-4 mb-4">
                        <p className="font-bold text-gray-800 mb-3 flex items-center">
                          <span className="mr-2">🤖</span>
                          Why This is the Best Choice:
                        </p>
                        <div className="space-y-2 text-sm">
                          {/* Distance to Pickup */}
                          <div className="flex items-start">
                            <span className="text-green-500 mr-2 text-lg">✓</span>
                            <div>
                              <span className="font-bold text-green-600">Distance to Pickup:</span>
                              <span className="text-gray-700 ml-1">
                                {(() => {
                                  const lat1 = originCoords.lat;
                                  const lon1 = originCoords.lng;
                                  const lat2 = availableLoads[0].pickup_location.lat;
                                  const lon2 = availableLoads[0].pickup_location.lng;
                                  const R = 6371;
                                  const dLat = (lat2 - lat1) * Math.PI / 180;
                                  const dLon = (lon2 - lon1) * Math.PI / 180;
                                  const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
                                           Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
                                           Math.sin(dLon/2) * Math.sin(dLon/2);
                                  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
                                  return Math.round(R * c);
                                })()}km from {origin.split(',')[0]} to {availableLoads[0].pickup_location.address.split(',')[0]}
                              </span>
                            </div>
                          </div>

                          {/* Payment */}
                          <div className="flex items-start">
                            <span className="text-green-500 mr-2 text-lg">✓</span>
                            <div>
                              <span className="font-bold text-green-600">Payment Offered:</span>
                              <span className="text-gray-700 ml-1">
                                ₹{availableLoads[0].price_offered.toLocaleString()}
                              </span>
                            </div>
                          </div>

                          {/* Net Profit */}
                          <div className="flex items-start">
                            <span className="text-green-500 mr-2">✓</span>
                            <div>
                              <span className="font-semibold">Net Profit:</span>
                              <span className="text-gray-700 ml-1">
                                ₹{availableLoads[0].profitability.net_profit.toLocaleString()} after costs
                              </span>
                            </div>
                          </div>

                          {/* Route */}
                          <div className="flex items-start">
                            <span className="text-blue-500 mr-2">→</span>
                            <div>
                              <span className="font-semibold">Route:</span>
                              <span className="text-gray-700 ml-1">
                                {origin.split(',')[0]} → {availableLoads[0].pickup_location.address.split(',')[0]} → {availableLoads[0].destination.address.split(',')[0]}
                              </span>
                            </div>
                          </div>

                          {/* Algorithm */}
                          <div className="flex items-start bg-blue-100 p-2 rounded mt-2">
                            <span className="text-blue-600 mr-2">ℹ️</span>
                            <div>
                              <span className="font-semibold text-blue-800">Ranking:</span>
                              <span className="text-blue-700 ml-1 text-xs">
                                60% distance to pickup + 40% payment amount
                              </span>
                            </div>
                          </div>
                        </div>
                      </div>

                      {/* Metrics Comparison */}
                      <div className="grid grid-cols-4 gap-2 mb-4 text-center text-xs">
                        <div className="bg-gray-50 p-2 rounded">
                          <p className="text-gray-500">Extra Distance</p>
                          <p className="font-bold text-gray-800">{availableLoads[0].profitability.extra_distance_km}km</p>
                        </div>
                        <div className="bg-gray-50 p-2 rounded">
                          <p className="text-gray-500">Payment</p>
                          <p className="font-bold text-blue-600">₹{availableLoads[0].price_offered.toLocaleString()}</p>
                        </div>
                        <div className="bg-gray-50 p-2 rounded">
                          <p className="text-gray-500">Fuel Cost</p>
                          <p className="font-bold text-orange-600">₹{availableLoads[0].profitability.fuel_cost}</p>
                        </div>
                        <div className="bg-gray-50 p-2 rounded">
                          <p className="text-gray-500">Net Profit</p>
                          <p className="font-bold text-green-600">₹{availableLoads[0].profitability.net_profit.toLocaleString()}</p>
                        </div>
                      </div>

                      {/* Accept Button */}
                      <button
                        onClick={() => acceptLoad(availableLoads[0])}
                        className="w-full bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 text-white font-bold py-3 rounded-lg transition-all transform hover:scale-105 shadow-lg flex items-center justify-center"
                      >
                        <span className="mr-2">⭐</span>
                        Accept Top Pick
                        <span className="ml-2">→</span>
                      </button>
                    </div>
                  </div>
                )}

                {/* ALL AVAILABLE LOADS SECTION */}
                <div className="bg-white rounded-xl shadow-sm p-6">
                  <h2 className="text-xl font-bold mb-4 flex items-center">
                    <Package className="w-5 h-5 mr-2 text-green-500" />
                    All Available Loads ({availableLoads.length})
                  </h2>
                  
                  <div className="space-y-3 max-h-[600px] overflow-y-auto">
                    {availableLoads.map((load, index) => (
                      <div
                        key={load.load_id}
                        className={`border rounded-lg p-4 hover:border-blue-500 transition-colors ${
                          index === 0 ? 'border-green-300 bg-green-50/30' : 'border-gray-200'
                        }`}
                      >
                        <div className="flex items-start justify-between mb-2">
                          <div className="flex items-center">
                            <div className={`font-bold w-8 h-8 rounded-full flex items-center justify-center mr-3 ${
                              index === 0 ? 'bg-green-100 text-green-600' : 'bg-blue-100 text-blue-600'
                            }`}>
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

                        <button 
                          onClick={(e) => {
                            e.stopPropagation();
                            acceptLoad(load);
                          }}
                          className={`w-full mt-3 font-semibold py-2 rounded-lg transition-colors text-sm ${
                            index === 0 
                              ? 'bg-green-500 hover:bg-green-600 text-white' 
                              : 'bg-blue-500 hover:bg-blue-600 text-white'
                          }`}
                        >
                          Accept Load
                        </button>
                      </div>
                    ))}
                  </div>
                </div>
              </>
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
                liveTracking={step === 'navigate'}
                trackingData={step === 'navigate' && selectedLoad ? {
                  timestamp: new Date().toISOString(),
                  speed: 65,
                  progress: 35,
                  label: `${origin.split(',')[0]} → ${selectedLoad.destination.address.split(',')[0]}`
                } : null}
                autoCenter={step === 'navigate'}
                zoom={step === 'navigate' ? 10 : 8}
              />
            </div>
          </div>
        </div>
      </div>

      {/* AI Auto-Assignment Modal */}
      {showAutoAssignModal && autoAssignedLoad && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4 animate-fadeIn">
          <div className="bg-gradient-to-br from-blue-50 to-purple-50 rounded-2xl max-w-2xl w-full p-8 shadow-2xl animate-slideUp border-4 border-blue-500">
            {/* AI Badge */}
            <div className="flex items-center justify-center mb-6">
              <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-3 rounded-full font-bold text-xl flex items-center shadow-lg">
                <span className="mr-2">🤖</span>
                AI AUTO-ASSIGNED
                <span className="ml-2">✨</span>
              </div>
            </div>

            {/* Title */}
            <h2 className="text-3xl font-bold text-center mb-2 text-gray-800">
              Perfect Match Found!
            </h2>
            <p className="text-center text-gray-600 mb-6">
              Our AI analyzed all available loads and found the most profitable option for you
            </p>

            {/* Load Details Card with 3-Point Journey */}
            <div className="bg-white rounded-xl p-6 shadow-lg mb-6">
              <div className="grid grid-cols-2 gap-4 mb-4">
                <div className="bg-blue-50 p-4 rounded-lg">
                  <p className="text-sm text-gray-600 mb-1">Weight</p>
                  <p className="text-2xl font-bold text-blue-600">{autoAssignedLoad.weight_kg}kg</p>
                </div>
                <div className="bg-green-50 p-4 rounded-lg">
                  <p className="text-sm text-gray-600 mb-1">Payment</p>
                  <p className="text-2xl font-bold text-green-600">₹{autoAssignedLoad.price_offered.toLocaleString()}</p>
                </div>
              </div>

              {/* 3-Point Journey Visualization */}
              <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-4 mb-4">
                <p className="text-sm font-bold text-gray-700 mb-3 text-center">📍 Your Journey (3 Points)</p>
                <div className="space-y-3">
                  {/* Point 1: Driver Start */}
                  <div className="flex items-center">
                    <div className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center text-white font-bold mr-3 flex-shrink-0">
                      1
                    </div>
                    <div className="flex-1">
                      <p className="text-xs text-gray-500">Your Starting Point</p>
                      <p className="font-semibold text-gray-800 text-sm">{origin.split(',').slice(0, 2).join(',')}</p>
                    </div>
                    <span className="text-blue-500 font-bold">🚛</span>
                  </div>
                  
                  {/* Arrow */}
                  <div className="flex items-center justify-center">
                    <div className="text-2xl text-blue-500">↓</div>
                  </div>
                  
                  {/* Point 2: Load Pickup */}
                  <div className="flex items-center">
                    <div className="w-10 h-10 bg-green-500 rounded-full flex items-center justify-center text-white font-bold mr-3 flex-shrink-0">
                      2
                    </div>
                    <div className="flex-1">
                      <p className="text-xs text-gray-500">Load Pickup Location</p>
                      <p className="font-semibold text-gray-800 text-sm">{autoAssignedLoad.pickup_location.address.split(',').slice(0, 2).join(',')}</p>
                    </div>
                    <span className="text-green-500 font-bold">📦</span>
                  </div>
                  
                  {/* Arrow */}
                  <div className="flex items-center justify-center">
                    <div className="text-2xl text-green-500">↓</div>
                  </div>
                  
                  {/* Point 3: Load Delivery */}
                  <div className="flex items-center">
                    <div className="w-10 h-10 bg-red-500 rounded-full flex items-center justify-center text-white font-bold mr-3 flex-shrink-0">
                      3
                    </div>
                    <div className="flex-1">
                      <p className="text-xs text-gray-500">Load Delivery Location</p>
                      <p className="font-semibold text-gray-800 text-sm">{autoAssignedLoad.destination.address.split(',').slice(0, 2).join(',')}</p>
                    </div>
                    <span className="text-red-500 font-bold">🏁</span>
                  </div>
                </div>
              </div>

              {/* Profitability */}
              {autoAssignedLoad.profitability && (
                <div className="mt-4 pt-4 border-t border-gray-200">
                  <div className="grid grid-cols-3 gap-3 text-center">
                    <div>
                      <p className="text-xs text-gray-500">Extra Distance</p>
                      <p className="font-bold text-gray-800">{autoAssignedLoad.profitability.extra_distance_km}km</p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-500">Fuel Cost</p>
                      <p className="font-bold text-orange-600">₹{autoAssignedLoad.profitability.fuel_cost}</p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-500">Net Profit</p>
                      <p className="font-bold text-green-600 text-xl">₹{autoAssignedLoad.profitability.net_profit.toLocaleString()}</p>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* AI Analysis Badge */}
            <div className="bg-gradient-to-r from-purple-100 to-blue-100 rounded-lg p-4 mb-6">
              <p className="text-sm text-center text-gray-700">
                <span className="font-bold">AI Analysis:</span> This load offers the best profitability score 
                based on distance, fuel cost, and payment. Navigation will start automatically.
              </p>
            </div>

            {/* Action Button */}
            <button
              onClick={() => setShowAutoAssignModal(false)}
              className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-bold py-4 rounded-xl transition-all transform hover:scale-105 shadow-lg"
            >
              Start Navigation →
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default DriverDashboard;
