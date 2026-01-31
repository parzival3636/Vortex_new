import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Vendors API
export const vendorsAPI = {
  register: (data) => api.post('/vendors/register', data),
  getVendor: (vendorId) => api.get(`/vendors/${vendorId}`),
  createLoadByAddress: (data) => api.post('/vendors/loads/by-address', data),
  searchPlaces: (query, limit = 5) => 
    api.get(`/vendors/geocode/search?query=${encodeURIComponent(query)}&limit=${limit}`),
  geocodeAddress: (address) => 
    api.get(`/vendors/geocode/address?address=${encodeURIComponent(address)}`),
  reverseGeocode: (lat, lng) => 
    api.get(`/vendors/geocode/reverse?lat=${lat}&lng=${lng}`),
};

// Trips API
export const tripsAPI = {
  createTrip: (data) => api.post('/trips/', data),
  getTrip: (tripId) => api.get(`/trips/${tripId}`),
  getAssignedLoad: (tripId) => api.get(`/trips/${tripId}/assigned-load`),
  markDeadheading: (tripId) => api.patch(`/trips/${tripId}/deadhead`),
  confirmPickup: (tripId) => api.patch(`/trips/${tripId}/pickup`),
  confirmDelivery: (tripId) => api.patch(`/trips/${tripId}/delivery`),
};

// Loads API
export const loadsAPI = {
  createLoad: (data) => api.post('/loads/', data),
  getLoad: (loadId) => api.get(`/loads/${loadId}`),
  getAvailableLoads: () => api.get('/loads/available'),
  acceptLoad: (loadId, tripId) => api.patch(`/loads/${loadId}/accept?trip_id=${tripId}`),
  rejectLoad: (loadId) => api.patch(`/loads/${loadId}/reject`),
};

// Calculate API
export const calculateAPI = {
  calculateProfitability: (data) => api.post('/calculate/profitability', data),
  getLoadOpportunities: (tripId) => api.get(`/calculate/opportunities/${tripId}`),
};

// Demo API
export const demoAPI = {
  initDemoData: () => api.post('/demo/init'),
  getDemoData: () => api.get('/demo/data'),
};

// Scheduler API
export const schedulerAPI = {
  start: () => api.post('/scheduler/start'),
  stop: () => api.post('/scheduler/stop'),
  getStatus: () => api.get('/scheduler/status'),
  forceRun: () => api.post('/scheduler/force-run'),
  getStats: () => api.get('/scheduler/stats'),
};

export default api;
