import React, { useState } from 'react';
import { RefreshCw } from 'lucide-react';
import { financialAPI } from '../services/api';
import toast from 'react-hot-toast';

/**
 * GenerateReportButton Component
 * Button to trigger on-demand report generation
 * Requirements: 6.1, 6.2
 */
export default function GenerateReportButton({ driverId, onReportGenerated }) {
  const [isLoading, setIsLoading] = useState(false);

  const handleGenerateReport = async () => {
    try {
      setIsLoading(true);

      const response = await financialAPI.generateReport({
        driver_id: driverId,
        date: new Date().toISOString().split('T')[0],
      });

      toast.success('Report generated successfully!');
      
      if (onReportGenerated) {
        onReportGenerated(response.data);
      }
    } catch (error) {
      console.error('Error generating report:', error);
      toast.error(error.response?.data?.detail || 'Failed to generate report');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <button
      onClick={handleGenerateReport}
      disabled={isLoading}
      className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
    >
      <RefreshCw size={20} className={isLoading ? 'animate-spin' : ''} />
      {isLoading ? 'Generating...' : 'Generate Report Now'}
    </button>
  );
}
