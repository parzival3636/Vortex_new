import React from 'react';
import { Lightbulb, AlertTriangle, TrendingUp } from 'lucide-react';

/**
 * AIInsightsPanel Component
 * Displays AI-generated insights, anomalies, and recommendations
 * Requirements: 8.1, 8.3, 8.4, 8.5
 */
export default function AIInsightsPanel({ insights }) {
  if (!insights) {
    return null;
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-6">
        AI Insights & Recommendations
      </h3>

      {/* Summary */}
      <div className="mb-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
        <div className="flex items-start gap-3">
          <Lightbulb size={20} className="text-blue-600 mt-1 flex-shrink-0" />
          <div>
            <p className="font-semibold text-blue-900 mb-1">Summary</p>
            <p className="text-blue-800">{insights.summary}</p>
          </div>
        </div>
      </div>

      {/* Anomalies */}
      {insights.anomalies && insights.anomalies.length > 0 && (
        <div className="mb-6">
          <div className="flex items-center gap-2 mb-3">
            <AlertTriangle size={20} className="text-orange-600" />
            <h4 className="font-semibold text-gray-900">Anomalies Detected</h4>
          </div>
          <div className="space-y-2">
            {insights.anomalies.map((anomaly, index) => (
              <div
                key={index}
                className="p-3 bg-orange-50 border border-orange-200 rounded-lg text-orange-800"
              >
                {anomaly}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Recommendations */}
      {insights.recommendations && insights.recommendations.length > 0 && (
        <div>
          <div className="flex items-center gap-2 mb-3">
            <TrendingUp size={20} className="text-green-600" />
            <h4 className="font-semibold text-gray-900">Recommendations</h4>
          </div>
          <div className="space-y-2">
            {insights.recommendations.map((rec, index) => (
              <div
                key={index}
                className="p-3 bg-green-50 border border-green-200 rounded-lg text-green-800"
              >
                {rec}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
