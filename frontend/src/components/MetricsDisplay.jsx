import React from 'react';
import { TrendingUp, TrendingDown, DollarSign } from 'lucide-react';

/**
 * MetricsDisplay Component
 * Shows key financial metrics: Total Earnings, Total Expenses, Net Profit
 * Requirements: 5.2
 */
export default function MetricsDisplay({ metrics }) {
  if (!metrics) {
    return null;
  }

  const netProfit = metrics.total_earnings - metrics.total_expenses;
  const isPositive = netProfit >= 0;

  return (
    <div className="grid grid-cols-3 gap-6 mb-8">
      {/* Total Earnings */}
      <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-lg shadow p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">Total Earnings</h3>
          <TrendingUp size={24} className="text-green-600" />
        </div>
        <p className="text-3xl font-bold text-green-600">
          ₹{metrics.total_earnings.toFixed(2)}
        </p>
        <p className="text-sm text-gray-600 mt-2">
          {metrics.trips_completed} trips completed
        </p>
      </div>

      {/* Total Expenses */}
      <div className="bg-gradient-to-br from-red-50 to-red-100 rounded-lg shadow p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">Total Expenses</h3>
          <TrendingDown size={24} className="text-red-600" />
        </div>
        <p className="text-3xl font-bold text-red-600">
          ₹{metrics.total_expenses.toFixed(2)}
        </p>
        <p className="text-sm text-gray-600 mt-2">
          {(metrics.expense_ratio * 100).toFixed(1)}% of earnings
        </p>
      </div>

      {/* Net Profit */}
      <div
        className={`bg-gradient-to-br ${
          isPositive
            ? 'from-blue-50 to-blue-100'
            : 'from-orange-50 to-orange-100'
        } rounded-lg shadow p-6`}
      >
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">Net Profit</h3>
          <DollarSign
            size={24}
            className={isPositive ? 'text-blue-600' : 'text-orange-600'}
          />
        </div>
        <p
          className={`text-3xl font-bold ${
            isPositive ? 'text-blue-600' : 'text-orange-600'
          }`}
        >
          ₹{netProfit.toFixed(2)}
        </p>
        <p className="text-sm text-gray-600 mt-2">
          {isPositive ? 'Profit' : 'Loss'} for the day
        </p>
      </div>
    </div>
  );
}
