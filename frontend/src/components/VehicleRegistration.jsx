import React, { useState } from 'react';
import { Truck, Plus, X, MapPin } from 'lucide-react';
import axios from 'axios';
import toast from 'react-hot-toast';

const VehicleRegistration = ({ ownerId, onVehicleAdded }) => {
  const [showForm, setShowForm] = useState(false);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    licensePlate: '',
    driverName: '',
    driverPhone: '',
    fuelConsumptionRate: '0.35',
    currentLat: '',
    currentLng: '',
    currentAddress: ''
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.licensePlate || !formData.driverName || !formData.driverPhone) {
      toast.error('Please fill all required fields');
      return;
    }

    setLoading(true);
    try {
      // Create vehicle with driver
      const response = await axios.post('http://localhost:8000/api/vehicles/register', {
        ownerId: ownerId,
        licensePlate: formData.licensePlate,
        driverName: formData.driverName,
        driverPhone: formData.driverPhone,
        fuelConsumptionRate: parseFloat(formData.fuelConsumptionRate),
        currentLocation: formData.currentLat && formData.currentLng ? {
          latitude: parseFloat(formData.currentLat),
          longitude: parseFloat(formData.currentLng),
          address: formData.currentAddress || 'Current Location'
        } : null
      });

      toast.success('Vehicle registered successfully!');
      
      // Reset form
      setFormData({
        licensePlate: '',
        driverName: '',
        driverPhone: '',
        fuelConsumptionRate: '0.35',
        currentLat: '',
        currentLng: '',
        currentAddress: ''
      });
      setShowForm(false);
      
      // Callback to refresh vehicle list
      if (onVehicleAdded) {
        onVehicleAdded();
      }
    } catch (error) {
      console.error('Failed to register vehicle:', error);
      toast.error(error.response?.data?.detail || 'Failed to register vehicle');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  if (!showForm) {
    return (
      <div className="bg-white rounded-xl shadow-sm p-6 mb-6">
        <button
          onClick={() => setShowForm(true)}
          className="w-full bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 text-white font-semibold py-3 rounded-lg transition-all flex items-center justify-center shadow-md"
        >
          <Plus className="w-5 h-5 mr-2" />
          Register New Vehicle
        </button>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-sm p-6 mb-6 border-2 border-blue-200">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center">
          <Truck className="w-6 h-6 text-blue-500 mr-2" />
          <h3 className="text-xl font-bold text-gray-900">Register New Vehicle</h3>
        </div>
        <button
          onClick={() => setShowForm(false)}
          className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <X className="w-5 h-5 text-gray-500" />
        </button>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Vehicle Information */}
        <div className="bg-blue-50 rounded-lg p-4">
          <h4 className="font-semibold text-gray-800 mb-3">Vehicle Information</h4>
          
          <div className="space-y-3">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                License Plate <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                name="licensePlate"
                value={formData.licensePlate}
                onChange={handleChange}
                placeholder="e.g., DL-01-AB-1234"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Fuel Consumption Rate (L/km)
              </label>
              <input
                type="number"
                name="fuelConsumptionRate"
                value={formData.fuelConsumptionRate}
                onChange={handleChange}
                step="0.01"
                min="0.1"
                max="1.0"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <p className="text-xs text-gray-500 mt-1">Default: 0.35 L/km</p>
            </div>
          </div>
        </div>

        {/* Driver Information */}
        <div className="bg-green-50 rounded-lg p-4">
          <h4 className="font-semibold text-gray-800 mb-3">Driver Information</h4>
          
          <div className="space-y-3">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Driver Name <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                name="driverName"
                value={formData.driverName}
                onChange={handleChange}
                placeholder="e.g., Rajesh Kumar"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Driver Phone <span className="text-red-500">*</span>
              </label>
              <input
                type="tel"
                name="driverPhone"
                value={formData.driverPhone}
                onChange={handleChange}
                placeholder="e.g., +91-9876543210"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                required
              />
            </div>
          </div>
        </div>

        {/* Current Location (Optional) */}
        <div className="bg-purple-50 rounded-lg p-4">
          <div className="flex items-center mb-3">
            <MapPin className="w-5 h-5 text-purple-500 mr-2" />
            <h4 className="font-semibold text-gray-800">Current Location (Optional)</h4>
          </div>
          
          <div className="space-y-3">
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Latitude
                </label>
                <input
                  type="number"
                  name="currentLat"
                  value={formData.currentLat}
                  onChange={handleChange}
                  step="0.0001"
                  placeholder="e.g., 28.6139"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Longitude
                </label>
                <input
                  type="number"
                  name="currentLng"
                  value={formData.currentLng}
                  onChange={handleChange}
                  step="0.0001"
                  placeholder="e.g., 77.2090"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Address
              </label>
              <input
                type="text"
                name="currentAddress"
                value={formData.currentAddress}
                onChange={handleChange}
                placeholder="e.g., Delhi, India"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              />
            </div>

            <div className="bg-purple-100 rounded p-2 text-xs text-purple-800">
              💡 Tip: If not provided, default location (Delhi) will be used
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex space-x-3 pt-2">
          <button
            type="button"
            onClick={() => setShowForm(false)}
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors font-medium text-gray-700"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={loading}
            className="flex-1 bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 disabled:from-gray-300 disabled:to-gray-400 text-white font-semibold py-2 rounded-lg transition-all flex items-center justify-center"
          >
            {loading ? (
              <>
                <div className="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full mr-2"></div>
                Registering...
              </>
            ) : (
              <>
                <Truck className="w-5 h-5 mr-2" />
                Register Vehicle
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default VehicleRegistration;
