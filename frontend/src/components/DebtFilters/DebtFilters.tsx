import React from 'react';
import { Select } from '../ui/Select';
import { Input } from '../ui/Input';
import { Button } from '../ui/Button';

export interface DebtFilters {
  status: string;
  type: string;
  sortBy: string;
  sortOrder: 'asc' | 'desc';
  minBalance: string;
  maxBalance: string;
  search: string;
}

interface DebtFiltersProps {
  filters: DebtFilters;
  onFiltersChange: (filters: DebtFilters) => void;
  onReset: () => void;
}

export const DebtFilters: React.FC<DebtFiltersProps> = ({
  filters,
  onFiltersChange,
  onReset
}) => {
  const updateFilter = (key: keyof DebtFilters, value: string) => {
    onFiltersChange({ ...filters, [key]: value });
  };

  const statusOptions = [
    { value: '', label: 'All Statuses' },
    { value: 'active', label: 'Active' },
    { value: 'paid_off', label: 'Paid Off' },
    { value: 'closed', label: 'Closed' }
  ];

  const typeOptions = [
    { value: '', label: 'All Types' },
    { value: 'credit_card', label: 'Credit Card' },
    { value: 'loan', label: 'Personal Loan' },
    { value: 'mortgage', label: 'Mortgage' },
    { value: 'other', label: 'Other' }
  ];

  const sortOptions = [
    { value: 'name', label: 'Name' },
    { value: 'balance', label: 'Balance' },
    { value: 'apr', label: 'APR' },
    { value: 'minimumPayment', label: 'Min Payment' },
    { value: 'created', label: 'Date Added' }
  ];

  const sortOrderOptions = [
    { value: 'asc', label: 'Ascending' },
    { value: 'desc', label: 'Descending' }
  ];

  return (
    <div className="bg-white p-4 rounded-lg border border-gray-200 space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="font-medium text-gray-900">Filters & Sorting</h3>
        <Button
          variant="outline"
          size="sm"
          onClick={onReset}
        >
          Reset
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Input
          label="Search"
          placeholder="Search debts..."
          value={filters.search}
          onChange={(e) => updateFilter('search', e.target.value)}
        />

        <Select
          label="Status"
          options={statusOptions}
          value={filters.status}
          onChange={(e) => updateFilter('status', e.target.value)}
        />

        <Select
          label="Type"
          options={typeOptions}
          value={filters.type}
          onChange={(e) => updateFilter('type', e.target.value)}
        />

        <div className="flex space-x-2">
          <Select
            label="Sort By"
            options={sortOptions}
            value={filters.sortBy}
            onChange={(e) => updateFilter('sortBy', e.target.value)}
          />
          <Select
            label="Order"
            options={sortOrderOptions}
            value={filters.sortOrder}
            onChange={(e) => updateFilter('sortOrder', e.target.value as 'asc' | 'desc')}
          />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Input
          label="Min Balance"
          type="number"
          placeholder="0.00"
          value={filters.minBalance}
          onChange={(e) => updateFilter('minBalance', e.target.value)}
        />

        <Input
          label="Max Balance"
          type="number"
          placeholder="No limit"
          value={filters.maxBalance}
          onChange={(e) => updateFilter('maxBalance', e.target.value)}
        />
      </div>
    </div>
  );
};
