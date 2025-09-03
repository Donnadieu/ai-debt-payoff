import React, { useState } from 'react';
import { Debt } from '../../schemas/debt';
import { Button } from '../ui/Button';
import { Modal } from '../ui/Modal';
import { formatCurrency } from '../../utils/validation';

interface BulkActionsProps {
  selectedDebts: Debt[];
  onBulkDelete: (debts: Debt[]) => void;
  onBulkStatusChange: (debts: Debt[], status: string) => void;
  onClearSelection: () => void;
  isLoading?: boolean;
}

export const BulkActions: React.FC<BulkActionsProps> = ({
  selectedDebts,
  onBulkDelete,
  onBulkStatusChange,
  onClearSelection,
  isLoading = false
}) => {
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [showStatusModal, setShowStatusModal] = useState(false);
  const [newStatus, setNewStatus] = useState('');

  const selectedCount = selectedDebts.length;
  const totalBalance = selectedDebts.reduce((sum, debt) => sum + debt.balance, 0);

  const handleBulkDelete = () => {
    onBulkDelete(selectedDebts);
    setShowDeleteModal(false);
  };

  const handleStatusChange = (status: string) => {
    setNewStatus(status);
    setShowStatusModal(true);
  };

  const confirmStatusChange = () => {
    onBulkStatusChange(selectedDebts, newStatus);
    setShowStatusModal(false);
    setNewStatus('');
  };

  if (selectedCount === 0) {
    return null;
  }

  return (
    <>
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div>
              <p className="font-medium text-blue-900">
                {selectedCount} debt{selectedCount > 1 ? 's' : ''} selected
              </p>
              <p className="text-sm text-blue-700">
                Total balance: {formatCurrency(totalBalance)}
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-2">
            <Button
              variant="outline"
              size="sm"
              onClick={onClearSelection}
              disabled={isLoading}
            >
              Clear Selection
            </Button>

            <div className="flex space-x-1">
              <Button
                variant="outline"
                size="sm"
                onClick={() => handleStatusChange('active')}
                disabled={isLoading}
              >
                Mark Active
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => handleStatusChange('paid_off')}
                disabled={isLoading}
              >
                Mark Paid Off
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => handleStatusChange('closed')}
                disabled={isLoading}
              >
                Mark Closed
              </Button>
            </div>

            <Button
              color="red"
              size="sm"
              onClick={() => setShowDeleteModal(true)}
              disabled={isLoading}
            >
              Delete Selected
            </Button>
          </div>
        </div>
      </div>

      {/* Delete Confirmation Modal */}
      <Modal
        isOpen={showDeleteModal}
        onClose={() => setShowDeleteModal(false)}
        title="Delete Multiple Debts"
        size="md"
      >
        <div className="space-y-4">
          <div className="flex items-center justify-center w-12 h-12 mx-auto bg-red-100 rounded-full">
            <svg
              className="w-6 h-6 text-red-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"
              />
            </svg>
          </div>

          <div className="text-center">
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Delete {selectedCount} debt{selectedCount > 1 ? 's' : ''}?
            </h3>
            <p className="text-sm text-gray-500 mb-4">
              This action cannot be undone. All payment history and data for these debts will be permanently removed.
            </p>
          </div>

          <div className="bg-gray-50 p-4 rounded-lg max-h-60 overflow-y-auto">
            <h4 className="font-medium text-gray-700 mb-2">Debts to be deleted:</h4>
            <div className="space-y-2">
              {selectedDebts.map((debt) => (
                <div key={debt.id} className="flex justify-between text-sm">
                  <span className="text-gray-900">{debt.name}</span>
                  <span className="text-gray-600">{formatCurrency(debt.balance)}</span>
                </div>
              ))}
            </div>
            <div className="border-t border-gray-200 mt-2 pt-2">
              <div className="flex justify-between font-medium">
                <span>Total Balance:</span>
                <span>{formatCurrency(totalBalance)}</span>
              </div>
            </div>
          </div>

          <div className="flex space-x-3 pt-4">
            <Button
              variant="outline"
              onClick={() => setShowDeleteModal(false)}
              disabled={isLoading}
              className="flex-1"
            >
              Cancel
            </Button>
            <Button
              color="red"
              onClick={handleBulkDelete}
              loading={isLoading}
              disabled={isLoading}
              className="flex-1"
            >
              Delete All
            </Button>
          </div>
        </div>
      </Modal>

      {/* Status Change Confirmation Modal */}
      <Modal
        isOpen={showStatusModal}
        onClose={() => setShowStatusModal(false)}
        title="Change Status"
        size="md"
      >
        <div className="space-y-4">
          <div className="text-center">
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Change status to "{newStatus.replace('_', ' ')}"?
            </h3>
            <p className="text-sm text-gray-500 mb-4">
              This will update the status for {selectedCount} selected debt{selectedCount > 1 ? 's' : ''}.
            </p>
          </div>

          <div className="bg-gray-50 p-4 rounded-lg max-h-40 overflow-y-auto">
            <div className="space-y-1">
              {selectedDebts.map((debt) => (
                <div key={debt.id} className="text-sm text-gray-900">
                  {debt.name}
                </div>
              ))}
            </div>
          </div>

          <div className="flex space-x-3 pt-4">
            <Button
              variant="outline"
              onClick={() => setShowStatusModal(false)}
              disabled={isLoading}
              className="flex-1"
            >
              Cancel
            </Button>
            <Button
              onClick={confirmStatusChange}
              loading={isLoading}
              disabled={isLoading}
              className="flex-1"
            >
              Update Status
            </Button>
          </div>
        </div>
      </Modal>
    </>
  );
};
