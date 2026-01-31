import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { QRCodeSVG } from 'qrcode.react';
import { Package, CheckCircle, Clock, Truck, Bell, QrCode, AlertTriangle } from 'lucide-react';
import { getLoadVerificationStatus, generatePickupQR, getVendorLoads } from '../services/api';

function VendorDashboard() {
  const { vendorId } = useParams();
  const [loads, setLoads] = useState([]);
  const [selectedLoad, setSelectedLoad] = useState(null);
  const [verificationStatus, setVerificationStatus] = useState(null);
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchVendorLoads();
    // Poll for updates every 10 seconds
    const interval = setInterval(fetchVendorLoads, 10000);
    return () => clearInterval(interval);
  }, [vendorId]);

  const fetchVendorLoads = async () => {
    try {
      const loadsData = await getVendorLoads(vendorId);
      setLoads(loadsData);
    } catch (error) {
      console.error('Error fetching loads:', error);
      // Demo data for testing
      setLoads([
        {
          load_id: 'load-001',
          weight_kg: 5000,
          pickup_location: { address: 'Mumbai Warehouse', lat: 19.0760, lng: 72.8777 },
          destination: { address: 'Pune Distribution Center', lat: 18.5204, lng: 73.8567 },
          status: 'assigned',
          assigned_driver_id: 'driver-123',
          price_offered: 15000
        }
      ]);
    }
  };

  const handleGeneratePickupQR = async (load) => {
    setLoading(true);
    try {
      const qrData = await generatePickupQR(
        load.load_id,
        load.assigned_driver_id,
        vendorId,
        load.pickup_location.lat,
        load.pickup_location.lng
      );
      
      alert(`Pickup QR generated! QR ID: ${qrData.qr_id}`);
      await fetchVerificationStatus(load.load_id);
    } catch (error) {
      console.error('Error generating QR:', error);
      alert('Error generating QR code');
    } finally {
      setLoading(false);
    }
  };

  const fetchVerificationStatus = async (loadId) => {
    try {
      const status = await getLoadVerificationStatus(loadId);
      setVerificationStatus(status);
      setSelectedLoad(loadId);
    } catch (error) {
      console.error('Error fetching status:', error);
    }
  };

  const getStatusBadge = (status) => {
    const badges = {
      assigned: { color: 'bg-yellow-100 text-yellow-800', icon: Clock, text: 'Assigned' },
      awaiting_pickup: { color: 'bg-blue-100 text-blue-800', icon: QrCode, text: 'Awaiting Pickup' },
      in_transit: { color: 'bg-purple-100 text-purple-800', icon: Truck, text: 'In Transit' },
      delivered: { color: 'bg-green-100 text-green-800', icon: CheckCircle, text: 'Delivered' }
    };
    
    const badge = badges[status] || badges.assigned;
    const Icon = badge.icon;
    
    return (
      <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${badge.color}`}>
        <Icon className="w-4 h-4 mr-1" />
        {badge.text}
      </span>
    );
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Vendor Dashboard</h1>
              <p className="text-sm text-gray-600">Vendor ID: {vendorId}</p>
            </div>
            <div className="flex items-center space-x-4">
              <button className="relative p-2 text-gray-600 hover:bg-gray-100 rounded-lg">
                <Bell className="w-6 h-6" />
                <span className="absolute top-0 right-0 w-2 h-2 bg-red-500 rounded-full"></span>
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid lg:grid-cols-3 gap-6">
          {/* Loads List */}
          <div className="lg:col-span-2 space-y-4">
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h2 className="text-xl font-bold mb-4">Your Loads</h2>
              
              {loads.length === 0 ? (
                <div className="text-center py-12 text-gray-500">
                  <Package className="w-12 h-12 mx-auto mb-4 opacity-50" />
                  <p>No loads found</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {loads.map((load) => (
                    <div
                      key={load.load_id}
                      className="border rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer"
                      onClick={() => fetchVerificationStatus(load.load_id)}
                    >
                      <div className="flex items-start justify-between mb-3">
                        <div>
                          <h3 className="font-semibold text-lg">Load #{load.load_id}</h3>
                          <p className="text-sm text-gray-600">{load.weight_kg} kg</p>
                        </div>
                        {getStatusBadge(load.status)}
                      </div>
                      
                      <div className="grid grid-cols-2 gap-4 text-sm mb-3">
                        <div>
                          <p className="text-gray-600">Pickup:</p>
                          <p className="font-medium">{load.pickup_location.address}</p>
                        </div>
                        <div>
                          <p className="text-gray-600">Delivery:</p>
                          <p className="font-medium">{load.destination.address}</p>
                        </div>
                      </div>
                      
                      <div className="flex items-center justify-between pt-3 border-t">
                        <span className="text-lg font-bold text-green-600">
                          ₹{load.price_offered.toLocaleString()}
                        </span>
                        
                        {load.status === 'assigned' && (
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              handleGeneratePickupQR(load);
                            }}
                            disabled={loading}
                            className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:bg-gray-400 flex items-center space-x-2"
                          >
                            <QrCode className="w-4 h-4" />
                            <span>Generate Pickup QR</span>
                          </button>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Verification Status Panel */}
          <div className="space-y-4">
            {verificationStatus && selectedLoad && (
              <div className="bg-white rounded-lg shadow-sm p-6">
                <h2 className="text-xl font-bold mb-4">Verification Status</h2>
                
                <div className="space-y-4">
                  {/* Pickup Status */}
                  <div className="border-l-4 border-blue-500 pl-4">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="font-semibold">Pickup Verification</h3>
                      {verificationStatus.pickup_verified ? (
                        <CheckCircle className="w-5 h-5 text-green-500" />
                      ) : verificationStatus.pickup_qr_generated ? (
                        <Clock className="w-5 h-5 text-yellow-500" />
                      ) : (
                        <AlertTriangle className="w-5 h-5 text-gray-400" />
                      )}
                    </div>
                    <p className="text-sm text-gray-600">
                      {verificationStatus.pickup_verified
                        ? '✓ Driver identity verified at pickup'
                        : verificationStatus.pickup_qr_generated
                        ? 'QR code generated, awaiting driver scan'
                        : 'QR code not generated yet'}
                    </p>
                    
                    {verificationStatus.pickup_qr_generated && !verificationStatus.pickup_verified && (
                      <div className="mt-3 p-3 bg-blue-50 rounded">
                        <p className="text-xs text-blue-800 mb-2">Pickup QR Code:</p>
                        <div className="bg-white p-2 rounded inline-block">
                          <QRCodeSVG 
                            value={JSON.stringify({
                              qr_id: verificationStatus.qr_codes.find(qr => qr.qr_type === 'pickup')?.qr_id,
                              type: 'pickup',
                              load_id: selectedLoad
                            })}
                            size={120}
                          />
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Delivery Status */}
                  <div className="border-l-4 border-green-500 pl-4">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="font-semibold">Delivery Verification</h3>
                      {verificationStatus.delivery_verified ? (
                        <CheckCircle className="w-5 h-5 text-green-500" />
                      ) : verificationStatus.delivery_qr_generated ? (
                        <Clock className="w-5 h-5 text-yellow-500" />
                      ) : (
                        <AlertTriangle className="w-5 h-5 text-gray-400" />
                      )}
                    </div>
                    <p className="text-sm text-gray-600">
                      {verificationStatus.delivery_verified
                        ? '✓ Load delivered and verified'
                        : verificationStatus.delivery_qr_generated
                        ? 'QR code generated, awaiting receiver scan'
                        : 'Awaiting pickup verification'}
                    </p>
                    
                    {verificationStatus.delivery_qr_generated && !verificationStatus.delivery_verified && (
                      <div className="mt-3 p-3 bg-green-50 rounded">
                        <p className="text-xs text-green-800 mb-2">Delivery QR Code:</p>
                        <div className="bg-white p-2 rounded inline-block">
                          <QRCodeSVG 
                            value={JSON.stringify({
                              qr_id: verificationStatus.qr_codes.find(qr => qr.qr_type === 'delivery')?.qr_id,
                              type: 'delivery',
                              load_id: selectedLoad
                            })}
                            size={120}
                          />
                        </div>
                      </div>
                    )}
                  </div>

                  {/* AI Confidence Score */}
                  {verificationStatus.verifications && verificationStatus.verifications.length > 0 && (
                    <div className="mt-4 p-4 bg-gray-50 rounded-lg">
                      <h4 className="font-semibold text-sm mb-2">AI Verification Details</h4>
                      {verificationStatus.verifications.map((v, idx) => (
                        <div key={idx} className="text-xs space-y-1">
                          <p>
                            <span className="font-medium">{v.verification_type}:</span>{' '}
                            {v.success ? '✓ Verified' : '✗ Failed'}
                          </p>
                          {v.confidence_score && (
                            <p>Confidence: {v.confidence_score.toFixed(1)}%</p>
                          )}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Quick Stats */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h2 className="text-xl font-bold mb-4">Quick Stats</h2>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Total Loads</span>
                  <span className="font-bold text-lg">{loads.length}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">In Transit</span>
                  <span className="font-bold text-lg text-purple-600">
                    {loads.filter(l => l.status === 'in_transit').length}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Delivered</span>
                  <span className="font-bold text-lg text-green-600">
                    {loads.filter(l => l.status === 'delivered').length}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default VendorDashboard;
