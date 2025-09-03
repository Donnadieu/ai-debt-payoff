import React from 'react';
import { Debt } from '../../schemas/debt';
import { Modal } from '../ui/Modal';
import { Button } from '../ui/Button';
import { formatCurrency } from '../../utils/validation';

interface DeleteDebtModalProps {
  debt: Debt | null;
  isOpen: boolean;
  onClose: () => void;
  onConfirm: (debt: Debt) => void;
  isLoading?: boolean;
}

export const DeleteDebtModal: React.FC<DeleteDebtModalProps> = ({
  debt,
  isOpen,
  onClose,
  onConfirm,
  isLoading = false
}) => {
  if (!debt) return null;

  const handleConfirm = () => {
    onConfirm(debt);
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Delete Debt"
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
            Are you sure you want to delete this debt?
          </h3>
          <p className="text-sm text-gray-500 mb-4">
            This action cannot be undone. All payment history and data for this debt will be permanently removed.
          </p>
        </div>

        <div className="bg-gray-50 p-4 rounded-lg">
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="font-medium text-gray-700">Name:</span>
              <span className="text-gray-900">{debt.name}</span>
            </div>
            <div className="flex justify-between">
              <span className="font-medium text-gray-700">Balance:</span>
              <span className="text-gray-900">{formatCurrency(debt.balance)}</span>
            </div>
            <div className="flex justify-between">
              <span className="font-medium text-gray-700">APR:</span>
              <span className="text-gray-900">{debt.apr}%</span>
            </div>
            <div className="flex justify-between">
              <span className="font-medium text-gray-700">Status:</span>
              <span className="text-gray-900 capitalize">
                {debt.status.replace('_', ' ')}
              </span>
            </div>
          </div>
        </div>

        <div className="flex space-x-3 pt-4">
          <Button
            variant="outline"
            onClick={onClose}
            disabled={isLoading}
            className="flex-1"
          >
            Cancel
          </Button>
          <Button
            color="red"
            onClick={handleConfirm}
            loading={isLoading}
            disabled={isLoading}
            className="flex-1"
          >
            Delete Debt
          </Button>
        </div>
      </div>
    </Modal>
  );
};
