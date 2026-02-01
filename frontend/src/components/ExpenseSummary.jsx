import React, { useState, useEffect } from 'react';
import { TrendingDown, AlertCircle } from 'lucide-react';
import { financialAPI } from '../services/api';
import toast from 'react-hot-toast';

/**
 * ExpenseSummary Component
 * Displays daily expense totals and breakdown by category
 * Requirements: 2.1, 2.2, 2.3, 2.4, 2.5
 */
export default function ExpenseSummary({ driverId, refreshTrigger }) {
  const [summary, setSummary] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const CATEGORY_COLORS = {
    fuel: 'bg-orange-100 text-orange-800',
    maintenance: 'bg-red-100 text-red-800',
    toll: 'bg-purple-100 text-purple-800',
    food: 'bg-green-100 text-green-800',
    other: 'bg-gray-100 text-gray-800',
  };

  const CATEGORY_ICONS = {
    fuel: '⛽',
    maintenance: '🔧',
    toll: '🛣️',
    food: '🍽️',
    other: '📦',
  };

  const fetchExpenses = async () => {
    try {
      setError(null);

      const today = new Date().toISOString().split('T')[0];
      const response = await financialAPI.getDailyExpenses(today, driverId);

      setSummary(response.data);
      setIsLoading(false);
    } catch (err) {
      console.error('Error fetching expenses:', err);
      setError('Failed to load expenses');
      if (isLoading) {
        toast.error('Failed to load daily expenses');
      }
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchExpenses();
  }, [driverId, refreshTrigger]);

  // Set up polling for real-time updates (every 5 seconds)
  useEffect(() => {
    const interval = setInterval(() => {
      fetchExpenses();
    }, 5000);

    return () => clearInterval(interval);
  }, [driverId]);

  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-gray-200 rounded w-1/3"></div>
          <div className="h-12 bg-gray-200 rounded"></div>
          <div className="grid grid-cols-5 gap-4">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="h-20 bg-gray-200 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center gap-2 text-red-600">
          <AlertCircle size={20} />
          <span>{error}</span>
        </div>
      </div>
    );
  }

  if (!summary) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <p className="text-gray-500">No expenses recorded today</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-2">
          <TrendingDown size={24} className="text-red-600" />
          <h2 className="text-2xl font-bold text-gray-900">Daily Expenses</h2>
        </div>
        <div className="text-right">
          <p className="text-sm text-gray-600">Total Expenses</p>
          <p className="text-3xl font-bold text-red-600">
            ₹{summary.total_expenses.toFixed(2)}
          </p>
        </div>
      </div>

      {/* Expense Breakdown */}
      <div className="grid grid-cols-5 gap-4 mb-6">
        {Object.entries(summary.expense_breakdown).map(([category, amount]) => (
          <div
            key={category}
            className={`p-4 rounded-lg ${CATEGORY_COLORS[category]}`}
          >
            <div className="text-2xl mb-2">{CATEGORY_ICONS[category]}</div>
            <p className="text-sm font-medium capitalize">{category}</p>
            <p className="text-lg font-bold">₹{amount.toFixed(2)}</p>
          </div>
        ))}
      </div>

      {/* Expenses List */}
      {summary.expenses.length > 0 ? (
        <div className="border-t pt-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Expenses ({summary.expenses.length})
          </h3>
          <div className="space-y-3 max-h-64 overflow-y-auto">
            {summary.expenses.map(expense => (
              <div
                key={expense.expense_id}
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
              >
                <div className="flex-1">
                  <p className="font-medium text-gray-900">
                    {expense.description}
                  </p>
                  <p className="text-sm text-gray-600">
                    {expense.category.charAt(0).toUpperCase() +
                      expense.category.slice(1)}{' '}
                    • {new Date(expense.timestamp).toLocaleTimeString()}
                  </p>
                </div>
                <p className="font-bold text-gray-900">
                  ₹{expense.amount.toFixed(2)}
                </p>
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div className="border-t pt-6">
          <p className="text-gray-500 text-center">No expenses recorded today</p>
        </div>
      )}
    </div>
  );
}
