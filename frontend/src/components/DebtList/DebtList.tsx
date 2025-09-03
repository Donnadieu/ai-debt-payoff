import React, { useState } from 'react';
import { Debt } from '../../schemas/debt';
import { DebtCard } from '../DebtCard';
import { DebtFilters, DebtFiltersType } from '../DebtFilters';
import { Button } from '../ui/Button';
import { useDebtFilters } from '../../hooks/useDebtFilters';

interface DebtListProps {
  debts: Debt[];
  onEdit?: (debt: Debt) => void;
  onDelete?: (debt: Debt) => void;
  onBulkDelete?: (debts: Debt[]) => void;
  isLoading?: boolean;
  showFilters?: boolean;
  showBulkActions?: boolean;
}

export const DebtList: React.FC<DebtListProps> = ({
  debts,
  onEdit,
  onDelete,
  onBulkDelete,
  isLoading = false,
  showFilters = true,
  showBulkActions = true
}) => {
  const [selectedDebts, setSelectedDebts] = useState<Set<string>>(new Set());
  const { filters, filteredDebts, updateFilters, resetFilters } = useDebtFilters(debts);

  const handleSelectDebt = (debt: Debt, selected: boolean) => {
    const newSelected = new Set(selectedDebts);
    if (selected) {
      newSelected.add(debt.id!);
    } else {
      newSelected.delete(debt.id!);
    }
    setSelectedDebts(newSelected);
  };

  const handleSelectAll = () => {
    if (selectedDebts.size === filteredDebts.length) {
      setSelectedDebts(new Set());
    } else {
      setSelectedDebts(new Set(filteredDebts.map(debt => debt.id!)));
    }
  };

  const handleBulkDelete = () => {
    const debtsToDelete = filteredDebts.filter(debt => selectedDebts.has(debt.id!));
    onBulkDelete?.(debtsToDelete);
    setSelectedDebts(new Set());
  };

  const selectedCount = selectedDebts.size;
  const totalBalance = filteredDebts.reduce((sum, debt) => sum + debt.balance, 0);
  const activeDebts = filteredDebts.filter(debt => debt.status === 'active');

  if (isLoading) {
    return (
      <div className="space-y-4">
        {showFilters && (
          <div className="bg-gray-100 animate-pulse h-32 rounded-lg"></div>
        )}
        <div className="space-y-4">
          {[1, 2, 3].map(i => (
            <div key={i} className="bg-gray-100 animate-pulse h-48 rounded-lg"></div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-blue-50 p-4 rounded-lg">
          <h3 className="font-medium text-blue-900">Total Debts</h3>
          <p className="text-2xl font-bold text-blue-700">{filteredDebts.length}</p>
        </div>
        <div className="bg-red-50 p-4 rounded-lg">
          <h3 className="font-medium text-red-900">Active Debts</h3>
          <p className="text-2xl font-bold text-red-700">{activeDebts.length}</p>
        </div>
        <div className="bg-green-50 p-4 rounded-lg">
          <h3 className="font-medium text-green-900">Total Balance</h3>
          <p className="text-2xl font-bold text-green-700">
            ${totalBalance.toLocaleString()}
          </p>
        </div>
      </div>

      {/* Filters */}
      {showFilters && (
        <DebtFilters
          filters={filters}
          onFiltersChange={updateFilters}
          onReset={resetFilters}
        />
      )}

      {/* Bulk Actions */}
      {showBulkActions && filteredDebts.length > 0 && (
        <div className="flex items-center justify-between bg-gray-50 p-4 rounded-lg">
          <div className="flex items-center space-x-4">
            <label className="flex items-center space-x-2">
              <input
                type="checkbox"
                checked={selectedCount === filteredDebts.length && filteredDebts.length > 0}
                onChange={handleSelectAll}
                className="h-4 w-4 text-blue-600 rounded border-gray-300 focus:ring-blue-500"
              />
              <span className="text-sm text-gray-700">
                Select All ({selectedCount} selected)
              </span>
            </label>
          </div>

          {selectedCount > 0 && (
            <div className="flex space-x-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setSelectedDebts(new Set())}
              >
                Clear Selection
              </Button>
              {onBulkDelete && (
                <Button
                  variant="outline"
                  color="red"
                  size="sm"
                  onClick={handleBulkDelete}
                >
                  Delete Selected ({selectedCount})
                </Button>
              )}
            </div>
          )}
        </div>
      )}

      {/* Debt List */}
      <div className="space-y-4">
        {filteredDebts.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-gray-400 text-6xl mb-4">💳</div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">No debts found</h3>
            <p className="text-gray-500">
              {debts.length === 0 
                ? "Start by adding your first debt to begin tracking your payoff journey."
                : "Try adjusting your filters to see more results."
              }
            </p>
          </div>
        ) : (
          filteredDebts.map((debt) => (
            <DebtCard
              key={debt.id}
              debt={debt}
              onEdit={onEdit}
              onDelete={onDelete}
              onSelect={showBulkActions ? handleSelectDebt : undefined}
              isSelected={selectedDebts.has(debt.id!)}
            />
          ))
        )}
      </div>

      {/* Results Summary */}
      {filteredDebts.length > 0 && debts.length !== filteredDebts.length && (
        <div className="text-center text-sm text-gray-500">
          Showing {filteredDebts.length} of {debts.length} debts
        </div>
      )}
    </div>
  );
};
