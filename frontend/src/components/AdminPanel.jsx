import React, { useState } from 'react';
import { Database, Trash2, CheckCircle, AlertCircle } from 'lucide-react';
import axios from 'axios';
import toast from 'react-hot-toast';

const AdminPanel = () => {
  const [seeding, setSeeding] = useState(false);
  const [clearing, setClearing] = useState(false);

  const seedDemoData = async () => {
    setSeeding(true);
    try {
      // Call backend to seed data
      const response = await axios.post('http://localhost:8000/api/admin/seed-demo-data');
      toast.success('Demo data created successfully!');
      console.log('Seeded data:', response.data);
      
      // Show summary
      const summary = response.data;
      toast.success(
        `Created:\n` +
        `• 1 Owner\n` +
        `• 5 Trucks\n` +
        `• 5 Drivers\n` +
        `• 4 Vendors\n` +
        `• 7 Loads`,
        { duration: 5000 }
      );
      
      // Reload page after 2 seconds
      setTimeout(() => window.location.reload(), 2000);
    } catch (error) {
      console.error('Failed to seed data:', error);
      toast.error('Failed to seed demo data');
    } finally {
      setSeeding(false);
    }
  };

  const clearAllData = async () => {
    if (!window.confirm('⚠️ This will delete ALL data! Are you sure?')) {
      return;
    }
    
    setClearing(true);
    try {
      await axios.post('http://localhost:8000/api/admin/clear-all-data');
      toast.success('All data cleared!');
      setTimeout(() => window.location.reload(), 1000);
    } catch (error) {
      console.error('Failed to clear data:', error);
      toast.error('Failed to clear data');
    } finally {
      setClearing(false);
    }
  };

  return (
    <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-xl shadow-sm p-6 border-2 border-purple-200">
      <div className="flex items-center mb-4">
        <Database className="w-6 h-6 text-purple-600 mr-2" />
        <h3 className="text-xl font-bold text-gray-900">Admin Panel</h3>
      </div>
      
      <div className="bg-white rounded-lg p-4 mb-4">
        <div className="flex items-start mb-3">
          <AlertCircle className="w-5 h-5 text-blue-500 mr-2 mt-0.5 flex-shrink-0" />
          <div>
            <p className="text-sm font-semibold text-gray-800 mb-1">No Data Yet?</p>
            <p className="text-sm text-gray-600">
              Click "Seed Demo Data" to create sample owners, trucks, drivers, vendors, and loads for testing.
            </p>
          </div>
        </div>
        
        <div className="bg-blue-50 rounded p-3 text-xs text-blue-800">
          <p className="font-semibold mb-1">Demo data includes:</p>
          <ul className="list-disc list-inside space-y-0.5">
            <li>1 Owner (Demo Transport Co.)</li>
            <li>5 Trucks with different license plates</li>
            <li>5 Drivers assigned to trucks</li>
            <li>4 Vendors in different cities</li>
            <li>7 Loads ready for allocation</li>
          </ul>
        </div>
      </div>

      <div className="space-y-3">
        <button
          onClick={seedDemoData}
          disabled={seeding}
          className="w-full bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 disabled:from-gray-300 disabled:to-gray-400 text-white font-semibold py-3 rounded-lg transition-all flex items-center justify-center shadow-md"
        >
          {seeding ? (
            <>
              <div className="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full mr-2"></div>
              Creating Demo Data...
            </>
          ) : (
            <>
              <CheckCircle className="w-5 h-5 mr-2" />
              Seed Demo Data
            </>
          )}
        </button>

        <button
          onClick={clearAllData}
          disabled={clearing}
          className="w-full bg-red-500 hover:bg-red-600 disabled:bg-gray-300 text-white font-semibold py-2 rounded-lg transition-colors flex items-center justify-center text-sm"
        >
          {clearing ? (
            <>
              <div className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full mr-2"></div>
              Clearing...
            </>
          ) : (
            <>
              <Trash2 className="w-4 h-4 mr-2" />
              Clear All Data
            </>
          )}
        </button>
      </div>

      <div className="mt-4 pt-4 border-t border-purple-200">
        <p className="text-xs text-gray-500 text-center">
          💡 Tip: Seed data once, then use Manual Allocation to assign vehicles to loads
        </p>
      </div>
    </div>
  );
};

export default AdminPanel;
