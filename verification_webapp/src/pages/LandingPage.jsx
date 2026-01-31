import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Package, Truck, QrCode, Shield, CheckCircle } from 'lucide-react';

function LandingPage() {
  const navigate = useNavigate();
  const [userType, setUserType] = useState('');
  const [userId, setUserId] = useState('');

  const handleLogin = () => {
    if (!userId) {
      alert('Please enter your ID');
      return;
    }

    if (userType === 'vendor') {
      navigate(`/vendor/${userId}`);
    } else if (userType === 'receiver') {
      navigate(`/receiver/${userId}`);
    } else if (userType === 'driver') {
      // For demo, redirect to scan page with a sample load ID
      navigate(`/driver/scan/sample-load-id`);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center space-x-3">
            <Shield className="w-8 h-8 text-indigo-600" />
            <h1 className="text-3xl font-bold text-gray-900">Load Verification System</h1>
          </div>
          <p className="mt-2 text-gray-600">AI-Powered QR Verification for Secure Load Tracking</p>
        </div>
      </header>

      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 py-12">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Secure. Automated. Verified.
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Revolutionary QR-based verification system with AI agents that automatically verify driver identity 
            at pickup and delivery points, ensuring complete transparency and security.
          </p>
        </div>

        {/* Features */}
        <div className="grid md:grid-cols-3 gap-8 mb-12">
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-center w-12 h-12 bg-blue-100 rounded-lg mb-4">
              <QrCode className="w-6 h-6 text-blue-600" />
            </div>
            <h3 className="text-xl font-semibold mb-2">QR Verification</h3>
            <p className="text-gray-600">
              Unique QR codes generated for pickup and delivery. Drivers scan to verify identity at each checkpoint.
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-center w-12 h-12 bg-green-100 rounded-lg mb-4">
              <CheckCircle className="w-6 h-6 text-green-600" />
            </div>
            <h3 className="text-xl font-semibold mb-2">AI Verification Agent</h3>
            <p className="text-gray-600">
              AI agent validates driver identity, location proximity, and detects anomalies in real-time.
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-center w-12 h-12 bg-purple-100 rounded-lg mb-4">
              <Package className="w-6 h-6 text-purple-600" />
            </div>
            <h3 className="text-xl font-semibold mb-2">Automated Notifications</h3>
            <p className="text-gray-600">
              Vendors and receivers get instant notifications at every step - assignment, pickup, and delivery.
            </p>
          </div>
        </div>

        {/* Login Section */}
        <div className="max-w-md mx-auto bg-white rounded-lg shadow-lg p-8">
          <h3 className="text-2xl font-bold text-center mb-6">Access Dashboard</h3>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                I am a:
              </label>
              <div className="grid grid-cols-3 gap-2">
                <button
                  onClick={() => setUserType('vendor')}
                  className={`py-3 px-4 rounded-lg border-2 transition-all ${
                    userType === 'vendor'
                      ? 'border-indigo-600 bg-indigo-50 text-indigo-700'
                      : 'border-gray-300 hover:border-gray-400'
                  }`}
                >
                  <Package className="w-6 h-6 mx-auto mb-1" />
                  <span className="text-sm font-medium">Vendor</span>
                </button>
                
                <button
                  onClick={() => setUserType('receiver')}
                  className={`py-3 px-4 rounded-lg border-2 transition-all ${
                    userType === 'receiver'
                      ? 'border-indigo-600 bg-indigo-50 text-indigo-700'
                      : 'border-gray-300 hover:border-gray-400'
                  }`}
                >
                  <CheckCircle className="w-6 h-6 mx-auto mb-1" />
                  <span className="text-sm font-medium">Receiver</span>
                </button>
                
                <button
                  onClick={() => setUserType('driver')}
                  className={`py-3 px-4 rounded-lg border-2 transition-all ${
                    userType === 'driver'
                      ? 'border-indigo-600 bg-indigo-50 text-indigo-700'
                      : 'border-gray-300 hover:border-gray-400'
                  }`}
                >
                  <Truck className="w-6 h-6 mx-auto mb-1" />
                  <span className="text-sm font-medium">Driver</span>
                </button>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Your ID:
              </label>
              <input
                type="text"
                value={userId}
                onChange={(e) => setUserId(e.target.value)}
                placeholder="Enter your ID"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              />
            </div>

            <button
              onClick={handleLogin}
              disabled={!userType || !userId}
              className="w-full bg-indigo-600 text-white py-3 rounded-lg font-semibold hover:bg-indigo-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
            >
              Access Dashboard
            </button>
          </div>

          <div className="mt-6 text-center text-sm text-gray-500">
            <p>Demo IDs for testing:</p>
            <p className="font-mono">Vendor: vendor-123</p>
            <p className="font-mono">Receiver: receiver-456</p>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 py-6 text-center text-gray-600">
          <p>© 2026 Load Verification System. Powered by AI Agents.</p>
        </div>
      </footer>
    </div>
  );
}

export default LandingPage;
