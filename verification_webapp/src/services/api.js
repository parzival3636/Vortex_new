import axios from 'axios';

const API_BASE_URL = 'http://localhost:8001/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// QR Code APIs
export const generatePickupQR = async (loadId, driverId, vendorId, pickupLat, pickupLng) => {
  const response = await api.post(`/qr/generate/pickup/${loadId}`, null, {
    params: { driver_id: driverId, vendor_id: vendorId, pickup_lat: pickupLat, pickup_lng: pickupLng }
  });
  return response.data;
};

export const generateDeliveryQR = async (loadId, driverId, vendorId, receiverId, deliveryLat, deliveryLng) => {
  const response = await api.post(`/qr/generate/delivery/${loadId}`, null, {
    params: { 
      driver_id: driverId, 
      vendor_id: vendorId, 
      receiver_id: receiverId,
      delivery_lat: deliveryLat, 
      delivery_lng: deliveryLng 
    }
  });
  return response.data;
};

export const verifyPickupQR = async (qrId, scannedById, scannedByType, scanLat, scanLng) => {
  const response = await api.post('/qr/verify/pickup', {
    qr_id: qrId,
    scanned_by_id: scannedById,
    scanned_by_type: scannedByType,
    scan_location_lat: scanLat,
    scan_location_lng: scanLng,
    timestamp: new Date().toISOString()
  });
  return response.data;
};

export const verifyDeliveryQR = async (qrId, scannedById, scannedByType, scanLat, scanLng) => {
  const response = await api.post('/qr/verify/delivery', {
    qr_id: qrId,
    scanned_by_id: scannedById,
    scanned_by_type: scannedByType,
    scan_location_lat: scanLat,
    scan_location_lng: scanLng,
    timestamp: new Date().toISOString()
  });
  return response.data;
};

export const getLoadVerificationStatus = async (loadId) => {
  const response = await api.get(`/qr/load/${loadId}/status`);
  return response.data;
};

// Receiver APIs
export const createReceiver = async (receiverData) => {
  const response = await api.post('/receivers/', receiverData);
  return response.data;
};

export const getAllReceivers = async () => {
  const response = await api.get('/receivers/');
  return response.data;
};

export const getReceiver = async (receiverId) => {
  const response = await api.get(`/receivers/${receiverId}`);
  return response.data;
};

export const getReceiverNotifications = async (receiverId, unreadOnly = false) => {
  const response = await api.get(`/receivers/${receiverId}/notifications`, {
    params: { unread_only: unreadOnly }
  });
  return response.data;
};

export const markNotificationRead = async (receiverId, notificationId) => {
  const response = await api.patch(`/receivers/${receiverId}/notifications/${notificationId}/read`);
  return response.data;
};

// Integration with main system (would call main backend at port 8000)
export const getVendorLoads = async (vendorId) => {
  try {
    const response = await axios.get(`http://localhost:8000/api/v1/vendors/${vendorId}/loads`);
    return response.data;
  } catch (error) {
    console.error('Error fetching vendor loads:', error);
    return [];
  }
};

export default api;
