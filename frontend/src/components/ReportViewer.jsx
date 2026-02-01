import React, { useState, useEffect } from 'react';
import { AlertCircle, Loader } from 'lucide-react';
import { financialAPI } from '../services/api';
import toast from 'react-hot-toast';
import MetricsDisplay from './MetricsDisplay';
import ExpenseChart from './ExpenseChart';
import TripSummaryTable from './TripSummaryTable';
import ExpenseDetailsTable from './ExpenseDetailsTable';
import AIInsightsPanel from './AIInsightsPanel';
import DateSelector from './DateSelector';

/**
 * ReportViewer Component
 * Main report display container for Owner Dashboard
 * Requirements: 5.1
 */
export default function ReportViewer({ driverId }) {
  const [report, setReport] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedDate, setSelectedDate] = useState(
    new Date().toISOString().split('T')[0]
  );

  const fetchReport = async (date) => {
    try {
      setIsLoading(true);
      setError(null);

      const response = await financialAPI.getDailyReport(date, driverId);
      setReport(response.data);
    } catch (err) {
      console.error('Error fetching report:', err);
      if (err.response?.status === 404) {
        setError('No report found for this date');
      } else {
        setError('Failed to load report');
        toast.error('Failed to load report');
      }
      setReport(null);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchReport(selectedDate);
  }, [selectedDate, driverId]);

  const handleDateChange = (date) => {
    setSelectedDate(date);
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-center">
          <Loader size={32} className="animate-spin text-blue-600 mx-auto mb-4" />
          <p className="text-gray-600">Loading report...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center gap-3 text-red-600 mb-4">
          <AlertCircle size={24} />
          <span className="text-lg font-semibold">{error}</span>
        </div>
        <DateSelector selectedDate={selectedDate} onDateChange={handleDateChange} />
      </div>
    );
  }

  if (!report) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <p className="text-gray-500 text-center py-8">
          No report data available
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Date Selector */}
      <DateSelector selectedDate={selectedDate} onDateChange={handleDateChange} />

      {/* Metrics Display */}
      <MetricsDisplay metrics={report.financial_summary} />

      {/* Charts and Tables */}
      <div className="grid grid-cols-2 gap-6">
        <ExpenseChart breakdown={report.financial_summary.expense_breakdown} />
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Performance Metrics
          </h3>
          <div className="space-y-4">
            <div className="flex justify-between items-center py-2 border-b border-gray-200">
              <span className="text-gray-600">Trips Completed</span>
              <span className="font-bold text-gray-900">
                {report.financial_summary.trips_completed}
              </span>
            </div>
            <div className="flex justify-between items-center py-2 border-b border-gray-200">
              <span className="text-gray-600">Avg Earnings/Trip</span>
              <span className="font-bold text-gray-900">
                ₹{report.financial_summary.average_earnings_per_trip.toFixed(2)}
              </span>
            </div>
            <div className="flex justify-between items-center py-2">
              <span className="text-gray-600">Expense Ratio</span>
              <span className="font-bold text-gray-900">
                {(report.financial_summary.expense_ratio * 100).toFixed(1)}%
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Trip Summary */}
      <TripSummaryTable trips={report.trips} />

      {/* Expense Details */}
      <ExpenseDetailsTable expenses={report.trips.length > 0 ? [] : []} />

      {/* AI Insights */}
      <AIInsightsPanel insights={report.ai_insights} />
    </div>
  );
}
