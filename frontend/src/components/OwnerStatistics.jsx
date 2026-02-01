import React, { useState, useEffect } from 'react';
import { Truck, Package, CheckCircle, TrendingUp, Activity, DollarSign } from 'lucide-react';
import axios from 'axios';

const OwnerStatistics = ({ ownerId }) => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStatistics();
    const interval = setInterval(fetchStatistics, 30000); // Update every 30 seconds
    return () => clearInterval(interval);
  }, [ownerId]);

  const fetchStatistics = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/api/owner/statistics?owner_id=${ownerId}`);
      setStats(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch statistics:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        {[1, 2, 3, 4, 5, 6].map((i) => (
          <div key={i} className="bg-white rounded-xl shadow-sm p-6 animate-pulse">
            <div className="h-8 bg-gray-200 rounded mb-2"></div>
            <div className="h-6 bg-gray-200 rounded"></div>
          </div>
        ))}
      </div>
    );
  }

  if (!stats) return null;

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
      <div className="bg-white rounded-xl shadow-sm p-6">
        <div className="flex items-center justify-between mb-2">
          <Truck className="w-8 h-8 text-blue-500" />
          <span className="text-3xl font-bold text-gray-900">{stats.totalActiveVehicles}</span>
        </div>
        <p className="text-gray-600">Active Vehicles</p>
      </div>

      <div className="bg-white rounded-xl shadow-sm p-6">
        <div className="flex items-center justify-between mb-2">
          <Package className="w-8 h-8 text-orange-500" />
          <span className="text-3xl font-bold text-gray-900">{stats.totalPendingLoads}</span>
        </div>
        <p className="text-gray-600">Pending Loads</p>
      </div>

      <div className="bg-white rounded-xl shadow-sm p-6">
        <div className="flex items-center justify-between mb-2">
          <Activity className="w-8 h-8 text-purple-500" />
          <span className="text-3xl font-bold text-gray-900">{stats.totalAllocatedLoads}</span>
        </div>
        <p className="text-gray-600">Allocated Loads</p>
      </div>

      <div className="bg-white rounded-xl shadow-sm p-6">
        <div className="flex items-center justify-between mb-2">
          <CheckCircle className="w-8 h-8 text-green-500" />
          <span className="text-3xl font-bold text-gray-900">{stats.totalCompletedLoads}</span>
        </div>
        <p className="text-gray-600">Completed Loads</p>
      </div>

      <div className="bg-white rounded-xl shadow-sm p-6">
        <div className="flex items-center justify-between mb-2">
          <TrendingUp className="w-8 h-8 text-blue-500" />
          <span className="text-3xl font-bold text-gray-900">{stats.allocationRate}%</span>
        </div>
        <p className="text-gray-600">Allocation Rate</p>
      </div>

      <div className="bg-white rounded-xl shadow-sm p-6">
        <div className="flex items-center justify-between mb-2">
          <DollarSign className="w-8 h-8 text-green-500" />
          <span className="text-3xl font-bold text-gray-900">{stats.averageVehicleUtilization}%</span>
        </div>
        <p className="text-gray-600">Vehicle Utilization</p>
      </div>
    </div>
  );
};

export default OwnerStatistics;
