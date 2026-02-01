import React, { useState } from 'react';
import { Download } from 'lucide-react';
import { financialAPI } from '../services/api';
import toast from 'react-hot-toast';

/**
 * DownloadButton Component
 * Button to download report as PDF
 * Requirements: 7.1, 7.4
 */
export default function DownloadButton({ reportId, reportDate }) {
  const [isLoading, setIsLoading] = useState(false);

  const handleDownloadPDF = async () => {
    try {
      setIsLoading(true);

      const response = await financialAPI.getReportPDF(reportId);

      // Create blob and download
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `report_${reportDate}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);

      toast.success('Report downloaded successfully!');
    } catch (error) {
      console.error('Error downloading PDF:', error);
      toast.error(error.response?.data?.detail || 'Failed to download PDF');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <button
      onClick={handleDownloadPDF}
      disabled={isLoading}
      className="flex items-center gap-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
    >
      <Download size={20} />
      {isLoading ? 'Downloading...' : 'Download PDF'}
    </button>
  );
}
