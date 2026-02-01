import React, { useState } from 'react';
import { DollarSign } from 'lucide-react';
import ExpenseForm from './ExpenseForm';

/**
 * RecordSpendageButton Component
 * Displays a button to trigger expense recording modal
 * Requirements: 1.1, 1.2
 */
export default function RecordSpendageButton({ driverId, onExpenseCreated }) {
  const [showForm, setShowForm] = useState(false);

  const handleClose = () => {
    setShowForm(false);
  };

  const handleSuccess = () => {
    setShowForm(false);
    if (onExpenseCreated) {
      onExpenseCreated();
    }
  };

  return (
    <>
      <button
        onClick={() => setShowForm(true)}
        className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-semibold"
      >
        <DollarSign size={20} />
        Record Spendage
      </button>

      {showForm && (
        <ExpenseForm
          driverId={driverId}
          onClose={handleClose}
          onSuccess={handleSuccess}
        />
      )}
    </>
  );
}
