import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { QRCodeSVG } from 'qrcode.react';
import { Truck, MapPin, Package, CheckCircle, AlertCircle } from 'lucide-react';
import { getLoadVerificationStatus } from '../services/api';

function DriverScanner() {
  const { loadId } = useParams();
  const [verificationStatus, setVerificationStatus] = useState(null);
  const [currentQR, setCurrentQR] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 5000);
    return () => clearInterval(interval);
  }, [loadId]);

  const fetchStatus = async () => {
    try {
      const status = await getLoadVerificationStatus(loadId);
      setVerificationStatus(status);
      
      // Determine which QR to show
      if (!status.pickup_verified && status.pickup_qr_generated) {
        const pickupQR = status.qr_codes.find(qr => qr.qr_type === 'pickup');
        setCurrentQR({ ...pickupQR, type: 'pickup' });
      } else if (status.pickup_verified && !status.delivery_verified && status.delivery_qr_generated) {
        const deliveryQR = status.qr_codes.find(qr => qr.qr_type === 'delivery');
        setCurrentQR({ ...deliveryQR, type: 'delivery' });
      } else {
        setCurrentQR(null);
      }
      
      setLoading(false);
    } catch (error) {
      console.error('Error fetching status:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-blue-100">
      <div className="max-w-2xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <div className="flex items-center space-x-3 mb-4">
            <div className="w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center">
              <Truck className="w-6 h-6 text-indigo-600" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Driver QR Scanner</h1>
              <p className="text-sm text-gray-600">Load ID: {loadId}</p>
            </div>
          </div>

          {/* Status Timeline */}
          <div className="flex items-center justify-between mt-6">
            <div className="flex-1">
              <div className={`w-full h-2 rounded-full ${verificationStatus?.pickup_verified ? 'bg-green-500' : 'bg-gray-300'}`}></div>
              <p className="text-xs mt-1 text-center font-medium">Pickup</p>
            </div>
            <div className="w-8"></div>
            <div className="flex-1">
              <div className={`w-full h-2 rounded-full ${verificationStatus?.delivery_verified ? 'bg-green-500' : 'bg-gray-300'}`}></div>
              <p className="text-xs mt-1 text-center font-medium">Delivery</p>
            </div>
          </div>
        </div>

        {/* QR Code Display */}
        {currentQR ? (
          <div className="bg-white rounded-lg shadow-lg p-8">
            <div className="text-center">
              <div className={`inline-flex items-center px-4 py-2 rounded-full mb-6 ${
                currentQR.type === 'pickup' ? 'bg-blue-100 text-blue-800' : 'bg-green-100 text-green-800'
              }`}>
                <MapPin className="w-5 h-5 mr-2" />
                <span className="font-semibold">
                  {currentQR.type === 'pickup' ? 'Pickup Location' : 'Delivery Location'}
                </span>
              </div>

              <div className="bg-gray-50 p-8 rounded-lg inline-block mb-6">
                <QRCodeSVG
                  value={JSON.stringify({
                    qr_id: currentQR.qr_id,
                    type: currentQR.type,
                    load_id: loadId
                  })}
                  size={280}
                  level="H"
                  includeMargin={true}
                />
              </div>

              <div className="space-y-3">
                <h2 className="text-xl font-bold text-gray-900">
                  {currentQR.type === 'pickup' 
                    ? 'Show this QR to vendor at pickup' 
                    : 'Show this QR to receiver at delivery'}
                </h2>
                <p className="text-gray-600">
                  {currentQR.type === 'pickup'
                    ? 'The vendor will scan this code to verify your identity before loading.'
                    : 'The receiver will scan this code to confirm delivery and verify your identity.'}
                </p>

                <div className="mt-6 p-4 bg-yellow-50 rounded-lg border border-yellow-200">
                  <div className="flex items-start space-x-3">
                    <AlertCircle className="w-5 h-5 text-yellow-600 flex-shrink-0 mt-0.5" />
                    <div className="text-left">
                      <p className="text-sm font-medium text-yellow-900">Important:</p>
                      <ul className="text-sm text-yellow-800 mt-1 space-y-1">
                        <li>• Ensure you're at the correct location</li>
                        <li>• QR code expires in 24 hours</li>
                        <li>• Can only be used once</li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        ) : (
          <div className="bg-white rounded-lg shadow-lg p-8">
            {verificationStatus?.delivery_verified ? (
              <div className="text-center">
                <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <CheckCircle className="w-12 h-12 text-green-600" />
                </div>
                <h2 className="text-2xl font-bold text-gray-900 mb-2">
                  Delivery Complete!
                </h2>
                <p className="text-gray-600">
                  Load has been successfully delivered and verified.
                </p>
              </div>
            ) : verificationStatus?.pickup_verified ? (
              <div className="text-center">
                <div className="w-20 h-20 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Package className="w-12 h-12 text-blue-600" />
                </div>
                <h2 className="text-2xl font-bold text-gray-900 mb-2">
                  In Transit
                </h2>
                <p className="text-gray-600 mb-4">
                  Pickup verified. Delivery QR will be generated automatically.
                </p>
                <div className="animate-pulse text-sm text-gray-500">
                  Waiting for delivery QR code...
                </div>
              </div>
            ) : (
              <div className="text-center">
                <div className="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <AlertCircle className="w-12 h-12 text-gray-400" />
                </div>
                <h2 className="text-2xl font-bold text-gray-900 mb-2">
                  No QR Code Available
                </h2>
                <p className="text-gray-600">
                  QR code has not been generated yet or has already been used.
                </p>
              </div>
            )}
          </div>
        )}

        {/* Load Details */}
        {verificationStatus && (
          <div className="bg-white rounded-lg shadow-lg p-6 mt-6">
            <h3 className="font-bold text-lg mb-4">Load Status</h3>
            <div className="space-y-3 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-600">Status:</span>
                <span className="font-semibold capitalize">{verificationStatus.status.replace('_', ' ')}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Pickup Verified:</span>
                <span className={verificationStatus.pickup_verified ? 'text-green-600 font-semibold' : 'text-gray-400'}>
                  {verificationStatus.pickup_verified ? '✓ Yes' : '✗ No'}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Delivery Verified:</span>
                <span className={verificationStatus.delivery_verified ? 'text-green-600 font-semibold' : 'text-gray-400'}>
                  {verificationStatus.delivery_verified ? '✓ Yes' : '✗ No'}
                </span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default DriverScanner;
