import React from 'react';
import { ChevronLeft, ChevronRight, Calendar } from 'lucide-react';

/**
 * DateSelector Component
 * Date picker for selecting report date
 * Requirements: 5.6, 5.7
 */
export default function DateSelector({ selectedDate, onDateChange }) {
  const handlePreviousDay = () => {
    const date = new Date(selectedDate);
    date.setDate(date.getDate() - 1);
    onDateChange(date.toISOString().split('T')[0]);
  };

  const handleNextDay = () => {
    const date = new Date(selectedDate);
    date.setDate(date.getDate() + 1);
    onDateChange(date.toISOString().split('T')[0]);
  };

  const handleToday = () => {
    onDateChange(new Date().toISOString().split('T')[0]);
  };

  const handleDateInput = (e) => {
    onDateChange(e.target.value);
  };

  const isToday = selectedDate === new Date().toISOString().split('T')[0];

  return (
    <div className="bg-white rounded-lg shadow p-4 flex items-center justify-between">
      <div className="flex items-center gap-4">
        <button
          onClick={handlePreviousDay}
          className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          title="Previous day"
        >
          <ChevronLeft size={20} className="text-gray-600" />
        </button>

        <div className="flex items-center gap-2">
          <Calendar size={20} className="text-blue-600" />
          <input
            type="date"
            value={selectedDate}
            onChange={handleDateInput}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <button
          onClick={handleNextDay}
          className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          title="Next day"
        >
          <ChevronRight size={20} className="text-gray-600" />
        </button>

        <button
          onClick={handleToday}
          className={`px-4 py-2 rounded-lg transition-colors font-medium ${
            isToday
              ? 'bg-blue-600 text-white'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
        >
          Today
        </button>
      </div>

      <div className="text-sm text-gray-600">
        {new Date(selectedDate).toLocaleDateString('en-US', {
          weekday: 'long',
          year: 'numeric',
          month: 'long',
          day: 'numeric',
        })}
      </div>
    </div>
  );
}
