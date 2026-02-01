import React from 'react';
import { MapPin } from 'lucide-react';

/**
 * TripSummaryTable Component
 * Displays table with all trips for the day showing earnings per trip
 * Requirements: 5.4
 */
export default function TripSummaryTable({ trips }) {
  if (!trips || trips.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Trip Summary
        </h3>
        <p className="text-gray-500 text-center py-8">
          No trips completed today
        </p>
      </div>
    );
  }

  const totalEarnings = trips.reduce((sum, trip) => sum + trip.earnings, 0);

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        Trip Summary ({trips.length} trips)
      </h3>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-gray-200">
              <th className="text-left py-3 px-4 font-semibold text-gray-900">
                Origin
              </th>
              <th className="text-left py-3 px-4 font-semibold text-gray-900">
                Destination
              </th>
              <th className="text-left py-3 px-4 font-semibold text-gray-900">
                Load Details
              </th>
              <th className="text-right py-3 px-4 font-semibold text-gray-900">
                Earnings
              </th>
            </tr>
          </thead>
          <tbody>
            {trips.map((trip, index) => (
              <tr
                key={trip.trip_id || index}
                className="border-b border-gray-100 hover:bg-gray-50 transition-colors"
              >
                <td className="py-3 px-4">
                  <div className="flex items-start gap-2">
                    <MapPin size={16} className="text-blue-600 mt-1 flex-shrink-0" />
                    <span className="text-gray-900 font-medium">
                      {trip.origin}
                    </span>
                  </div>
                </td>
                <td className="py-3 px-4">
                  <div className="flex items-start gap-2">
                    <MapPin size={16} className="text-green-600 mt-1 flex-shrink-0" />
                    <span className="text-gray-900 font-medium">
                      {trip.destination}
                    </span>
                  </div>
                </td>
                <td className="py-3 px-4">
                  <span className="text-gray-600">{trip.load_details}</span>
                </td>
                <td className="py-3 px-4 text-right">
                  <span className="font-bold text-green-600">
                    ₹{trip.earnings.toFixed(2)}
                  </span>
                </td>
              </tr>
            ))}
            <tr className="bg-gray-50 font-semibold">
              <td colSpan="3" className="py-3 px-4 text-right">
                Total Earnings:
              </td>
              <td className="py-3 px-4 text-right text-green-600">
                ₹{totalEarnings.toFixed(2)}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}
