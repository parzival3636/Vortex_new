import React from 'react';
import { PieChart, Pie, Cell, Legend, Tooltip, ResponsiveContainer } from 'recharts';

/**
 * ExpenseChart Component
 * Renders pie chart for expense breakdown by category
 * Requirements: 5.3
 */
export default function ExpenseChart({ breakdown }) {
  if (!breakdown) {
    return null;
  }

  const COLORS = {
    fuel: '#f97316',
    maintenance: '#ef4444',
    toll: '#a855f7',
    food: '#22c55e',
    other: '#6b7280',
  };

  // Convert breakdown to chart data
  const data = Object.entries(breakdown)
    .filter(([_, value]) => value > 0)
    .map(([category, value]) => ({
      name: category.charAt(0).toUpperCase() + category.slice(1),
      value: parseFloat(value.toFixed(2)),
      category,
    }));

  if (data.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Expense Breakdown
        </h3>
        <p className="text-gray-500 text-center py-8">
          No expenses recorded
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        Expense Breakdown
      </h3>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, value }) => `${name}: ₹${value}`}
            outerRadius={100}
            fill="#8884d8"
            dataKey="value"
          >
            {data.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={COLORS[entry.category]}
              />
            ))}
          </Pie>
          <Tooltip
            formatter={(value) => `₹${value.toFixed(2)}`}
            contentStyle={{
              backgroundColor: '#fff',
              border: '1px solid #ccc',
              borderRadius: '4px',
            }}
          />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
