import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Html5QrcodeScanner } from 'html5-qrcode';
import { Package, CheckCircle, Clock, Scan, Bell, MapPin } from 'lucide-react';
import { getReceiverNotifications, verifyDeliveryQR, getReceiver } from '../services/api';

function ReceiverDashboard() {
  const { receiverId } = useParams();
  const [receiver, setReceiver] = useState(null);
  const [notifications, setNotifications] = useState([]);
  const [scanning, setScanning] = useState(false);
  const [scanResult, setScanResult] = useState(null);
  const [incomingLoads, setIncomingLoads] = useState([]);

  useEffect(() => {
    fetchReceiverData();
    fetchNotifications();
    
    // Poll for updates every 10 seconds
    const interval = setInterval(fetchNotifications, 10000);
    return () => clearInterval(interval);
  }, [receiverId]);

  const fetchReceiverData = async () => {
    try {
      const data = await getReceiver(receiverId);
      setReceiver(data);
    } catch (error) {
      console.error('Error fetching receiver:', error);
      // Demo data
      setReceiver({
        receiver_id: receiverId,
        name: 'Pune Distribution Center',
        email: 'pune@example.com',
        phone: '+91 9876543210',
        location_address: 'Pune, Maharashtra',
        company_name: 'ABC Logistics'
      });
    }
  };

  const fetchNotifications = async () => {
    try {
      const data = await getReceiverNotifications(receiverId);
      setNotifications(data.notifications || []);
      
      // Extract incoming loads from notifications
      const loads = data.notifications
        .filter(n => n.title.includes('Delivery QR Code Ready'))
        .map(n => ({
          load_id: n.metadata || 'unknown',
          status: 'in_transit',
          notification: n
        }));
      setIncomingLoads(loads);
    } catch (error) {
      console.error('Error fetching notifications:', error);
    }
  };

  const startScanning = () => {
    setScanning(true);
    setScanResult(null);
    
    const scanner = new Html5QrcodeScanner('qr-reader', {
      fps: 10,
      qrbox: { width: 250, height: 250 }
    });

    scanner.render(onScanSuccess, onScanError);

    function onScanSuccess(decodedText) {
      scanner.clear();
      setScanning(false);
      handleQRScan(decodedText);
    }

    function onScanError(error) {
      // Ignore scan errors (happens continuously while scanning)
    }
  };

  const handleQRScan = async (qrData) => {
    try {
      const data = JSON.parse(qrData);
      
      if (data.type !== 'delivery') {
        setScanResult({
          success: false,
          message: 'This QR code is not for delivery verification'
        });
        return;
      }

      // Get current location (in production, use actual GPS)
      const mockLocation = { lat: 18.5204, lng: 73.8567 };

      const result = await verifyDeliveryQR(
        data.qr_id,
        receiverId,
        'receiver',
        mockLocation.lat,
        mockLocation.lng
      );

      setScanResult({
        success: true,
        message: result.message,
        load_id: result.load_id,
        verified_at: result.verified_at
      });

      // Refresh notifications
      await fetchNotifications();
    } catch (error) {
      console.error('Verification error:', error);
      setScanResult({
        success: false,
        message: error.response?.data?.detail || 'Verification failed'
      });
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Receiver Dashboard</h1>
              {receiver && (
                <div className="flex items-center space-x-4 mt-1">
                  <p className="text-sm text-gray-600">{receiver.name}</p>
                  <span className="text-gray-400">•</span>
                  <p className="text-sm text-gray-600 flex items-center">
                    <MapPin className="w-4 h-4 mr-1" />
                    {receiver.location_address}
                  </p>
                </div>
              )}
            </div>
            <div className="flex items-center space-x-4">
              <button className="relative p-2 text-gray-600 hover:bg-gray-100 rounded-lg">
                <Bell className="w-6 h-6" />
                {notifications.filter(n => !n.read).length > 0 && (
                  <span className="absolute top-0 right-0 w-5 h-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
                    {notifications.filter(n => !n.read).length}
                  </span>
                )}
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid lg:grid-cols-3 gap-6">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* QR Scanner Section */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h2 className="text-xl font-bold mb-4">Scan Delivery QR Code</h2>
              
              {!scanning && !scanResult && (
                <div className="text-center py-12">
                  <div className="w-24 h-24 bg-indigo-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Scan className="w-12 h-12 text-indigo-600" />
                  </div>
                  <p className="text-gray-600 mb-6">
                    Scan the QR code shown by the driver to verify delivery
                  </p>
                  <button
                    onClick={startScanning}
                    className="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 font-semibold"
                  >
                    Start Scanning
                  </button>
                </div>
              )}

              {scanning && (
                <div>
                  <div id="qr-reader" className="mb-4"></div>
                  <button
                    onClick={() => {
                      setScanning(false);
                      const scanner = document.getElementById('qr-reader');
                      if (scanner) scanner.innerHTML = '';
                    }}
                    className="w-full px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
                  >
                    Cancel Scanning
                  </button>
                </div>
              )}

              {scanResult && (
                <div className={`p-6 rounded-lg ${scanResult.success ? 'bg-green-50 border-2 border-green-500' : 'bg-red-50 border-2 border-red-500'}`}>
                  <div className="flex items-start space-x-3">
                    {scanResult.success ? (
                      <CheckCircle className="w-8 h-8 text-green-600 flex-shrink-0" />
                    ) : (
                      <div className="w-8 h-8 text-red-600 flex-shrink-0">✗</div>
                    )}
                    <div className="flex-1">
                      <h3 className={`font-bold text-lg mb-2 ${scanResult.success ? 'text-green-900' : 'text-red-900'}`}>
                        {scanResult.success ? 'Delivery Verified!' : 'Verification Failed'}
                      </h3>
                      <p className={`mb-4 ${scanResult.success ? 'text-green-800' : 'text-red-800'}`}>
                        {scanResult.message}
                      </p>
                      {scanResult.success && (
                        <div className="text-sm text-green-700 space-y-1">
                          <p><strong>Load ID:</strong> {scanResult.load_id}</p>
                          <p><strong>Verified At:</strong> {new Date(scanResult.verified_at).toLocaleString()}</p>
                        </div>
                      )}
                    </div>
                  </div>
                  <button
                    onClick={() => {
                      setScanResult(null);
                      setScanning(false);
                    }}
                    className="mt-4 w-full px-4 py-2 bg-white border-2 border-gray-300 rounded-lg hover:bg-gray-50"
                  >
                    Scan Another QR Code
                  </button>
                </div>
              )}
            </div>

            {/* Incoming Loads */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h2 className="text-xl font-bold mb-4">Incoming Loads</h2>
              
              {incomingLoads.length === 0 ? (
                <div className="text-center py-12 text-gray-500">
                  <Package className="w-12 h-12 mx-auto mb-4 opacity-50" />
                  <p>No incoming loads at the moment</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {incomingLoads.map((load, idx) => (
                    <div key={idx} className="border rounded-lg p-4">
                      <div className="flex items-center justify-between mb-2">
                        <h3 className="font-semibold">Load #{load.load_id}</h3>
                        <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-purple-100 text-purple-800">
                          <Clock className="w-4 h-4 mr-1" />
                          In Transit
                        </span>
                      </div>
                      <p className="text-sm text-gray-600">
                        {load.notification.message}
                      </p>
                      <p className="text-xs text-gray-500 mt-2">
                        Notified: {new Date(load.notification.created_at).toLocaleString()}
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Notifications */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h2 className="text-xl font-bold mb-4">Notifications</h2>
              
              {notifications.length === 0 ? (
                <p className="text-gray-500 text-sm">No notifications</p>
              ) : (
                <div className="space-y-3 max-h-96 overflow-y-auto">
                  {notifications.slice(0, 10).map((notification, idx) => (
                    <div
                      key={idx}
                      className={`p-3 rounded-lg border ${notification.read ? 'bg-gray-50' : 'bg-blue-50 border-blue-200'}`}
                    >
                      <div className="flex items-start justify-between mb-1">
                        <h4 className="font-semibold text-sm">{notification.title}</h4>
                        {notification.priority === 'high' && (
                          <span className="text-xs bg-red-100 text-red-700 px-2 py-1 rounded">
                            High
                          </span>
                        )}
                      </div>
                      <p className="text-xs text-gray-600">{notification.message}</p>
                      <p className="text-xs text-gray-400 mt-1">
                        {new Date(notification.created_at).toLocaleTimeString()}
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Instructions */}
            <div className="bg-indigo-50 rounded-lg p-6">
              <h3 className="font-bold text-indigo-900 mb-3">How It Works</h3>
              <ol className="space-y-2 text-sm text-indigo-800">
                <li className="flex items-start">
                  <span className="font-bold mr-2">1.</span>
                  <span>Wait for delivery notification</span>
                </li>
                <li className="flex items-start">
                  <span className="font-bold mr-2">2.</span>
                  <span>When driver arrives, click "Start Scanning"</span>
                </li>
                <li className="flex items-start">
                  <span className="font-bold mr-2">3.</span>
                  <span>Scan the QR code shown by driver</span>
                </li>
                <li className="flex items-start">
                  <span className="font-bold mr-2">4.</span>
                  <span>AI verifies driver identity automatically</span>
                </li>
                <li className="flex items-start">
                  <span className="font-bold mr-2">5.</span>
                  <span>Vendor gets instant confirmation</span>
                </li>
              </ol>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ReceiverDashboard;
