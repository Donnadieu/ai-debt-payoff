import React from 'react';
import { Debt } from '../../schemas/debt';
import { Card } from '../ui/Card';
import { Button } from '../ui/Button';
import { Badge } from '../ui/Badge';
import { formatCurrency, formatPercentage, calculateMonthsToPayoff } from '../../utils/validation';

interface DebtCardProps {
  debt: Debt;
  onEdit?: (debt: Debt) => void;
  onDelete?: (debt: Debt) => void;
  onSelect?: (debt: Debt, selected: boolean) => void;
  isSelected?: boolean;
  showActions?: boolean;
}

export const DebtCard: React.FC<DebtCardProps> = ({
  debt,
  onEdit,
  onDelete,
  onSelect,
  isSelected = false,
  showActions = true
}) => {
  const monthsToPayoff = calculateMonthsToPayoff(debt.balance, debt.apr, debt.minimumPayment);
  
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'blue';
      case 'paid_off': return 'green';
      case 'closed': return 'gray';
      default: return 'gray';
    }
  };

  const getTypeLabel = (type: string) => {
    switch (type) {
      case 'credit_card': return 'Credit Card';
      case 'loan': return 'Personal Loan';
      case 'mortgage': return 'Mortgage';
      case 'other': return 'Other';
      default: return 'Other';
    }
  };

  return (
    <Card className={`p-4 transition-all duration-200 ${isSelected ? 'ring-2 ring-blue-500 bg-blue-50' : 'hover:shadow-md'}`}>
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-start space-x-3">
          {onSelect && (
            <input
              type="checkbox"
              checked={isSelected}
              onChange={(e) => onSelect(debt, e.target.checked)}
              className="mt-1 h-4 w-4 text-blue-600 rounded border-gray-300 focus:ring-blue-500"
            />
          )}
          <div>
            <h3 className="font-semibold text-lg text-gray-900">{debt.name}</h3>
            <div className="flex items-center space-x-2 mt-1">
              <Badge color={getStatusColor(debt.status)}>
                {debt.status.replace('_', ' ').toUpperCase()}
              </Badge>
              <span className="text-sm text-gray-500">{getTypeLabel(debt.type)}</span>
            </div>
          </div>
        </div>
        
        {showActions && (
          <div className="flex space-x-2">
            {onEdit && (
              <Button
                size="sm"
                variant="outline"
                onClick={() => onEdit(debt)}
              >
                Edit
              </Button>
            )}
            {onDelete && (
              <Button
                size="sm"
                variant="outline"
                color="red"
                onClick={() => onDelete(debt)}
              >
                Delete
              </Button>
            )}
          </div>
        )}
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-3">
        <div>
          <p className="text-sm text-gray-500">Balance</p>
          <p className="font-semibold text-lg">{formatCurrency(debt.balance)}</p>
        </div>
        
        <div>
          <p className="text-sm text-gray-500">APR</p>
          <p className="font-semibold text-lg">{formatPercentage(debt.apr)}</p>
        </div>
        
        <div>
          <p className="text-sm text-gray-500">Min Payment</p>
          <p className="font-semibold text-lg">{formatCurrency(debt.minimumPayment)}</p>
        </div>
        
        <div>
          <p className="text-sm text-gray-500">Payoff Time</p>
          <p className="font-semibold text-lg">
            {monthsToPayoff === Infinity ? '∞' : `${monthsToPayoff}mo`}
          </p>
        </div>
      </div>

      {debt.description && (
        <div className="mt-3 pt-3 border-t border-gray-200">
          <p className="text-sm text-gray-600">{debt.description}</p>
        </div>
      )}

      {debt.status === 'active' && monthsToPayoff === Infinity && (
        <div className="mt-3 p-2 bg-red-50 border border-red-200 rounded-md">
          <p className="text-sm text-red-700">
            ⚠️ Minimum payment doesn't cover interest - balance will grow
          </p>
        </div>
      )}
    </Card>
  );
};
