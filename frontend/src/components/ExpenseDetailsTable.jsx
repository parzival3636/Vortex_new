import React from 'react';
import { Clock, Tag } from 'lucide-react';

/**
 * ExpenseDetailsTable Component
 * Displays table with all expenses for the day with categorization
 * Requirements: 5.5
 */
export default function ExpenseDetailsTable({ expenses }) {
  if (!expenses || expenses.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Expense Details
        </h3>
        <p className="text-gray-500 text-center py-8">
          No expenses recorded today
        </p>
      </div>
    );
  }

  const CATEGORY_COLORS = {
    fuel: 'bg-orange-100 text-orange-800',
    maintenance: 'bg-red-100 text-red-800',
    toll: 'bg-purple-100 text-purple-800',
    food: 'bg-green-100 text-green-800',
    other: 'bg-gray-100 text-gray-800',
  };

  const totalExpenses = expenses.reduce((sum, exp) => sum + exp.amount, 0);

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        Expense Details ({expenses.length} expenses)
      </h3>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-gray-200">
              <th className="text-left py-3 px-4 font-semibold text-gray-900">
                Description
              </th>
              <th className="text-left py-3 px-4 font-semibold text-gray-900">
                Category
              </th>
              <th className="text-left py-3 px-4 font-semibold text-gray-900">
                Time
              </th>
              <th className="text-right py-3 px-4 font-semibold text-gray-900">
                Amount
              </th>
            </tr>
          </thead>
          <tbody>
            {expenses.map((expense, index) => (
              <tr
                key={expense.expense_id || index}
                className="border-b border-gray-100 hover:bg-gray-50 transition-colors"
              >
                <td className="py-3 px-4">
                  <span className="text-gray-900 font-medium">
                    {expense.description}
                  </span>
                </td>
                <td className="py-3 px-4">
                  <span
                    className={`inline-flex items-center gap-1 px-3 py-1 rounded-full text-sm font-medium ${
                      CATEGORY_COLORS[expense.category]
                    }`}
                  >
                    <Tag size={14} />
                    {expense.category.charAt(0).toUpperCase() +
                      expense.category.slice(1)}
                  </span>
                </td>
                <td className="py-3 px-4">
                  <div className="flex items-center gap-2 text-gray-600">
                    <Clock size={16} />
                    {new Date(expense.timestamp).toLocaleTimeString()}
                  </div>
                </td>
                <td className="py-3 px-4 text-right">
                  <span className="font-bold text-red-600">
                    ₹{expense.amount.toFixed(2)}
                  </span>
                </td>
              </tr>
            ))}
            <tr className="bg-gray-50 font-semibold">
              <td colSpan="3" className="py-3 px-4 text-right">
                Total Expenses:
              </td>
              <td className="py-3 px-4 text-right text-red-600">
                ₹{totalExpenses.toFixed(2)}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}
