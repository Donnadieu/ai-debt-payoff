import { useState, useMemo } from 'react';
import { Debt } from '../schemas/debt';
import { DebtFiltersType } from '../components/DebtFilters';

const defaultFilters: DebtFiltersType = {
  status: '',
  type: '',
  sortBy: 'balance',
  sortOrder: 'desc',
  minBalance: '',
  maxBalance: '',
  search: '',
};

export const useDebtFilters = (debts: Debt[]) => {
  const [filters, setFilters] = useState<DebtFiltersType>(defaultFilters);

  const filteredDebts = useMemo(() => {
    let filtered = [...debts];

    // Search filter
    if (filters.search) {
      const searchTerm = filters.search.toLowerCase();
      filtered = filtered.filter(debt =>
        debt.name.toLowerCase().includes(searchTerm) ||
        debt.description?.toLowerCase().includes(searchTerm)
      );
    }

    // Status filter
    if (filters.status) {
      filtered = filtered.filter(debt => debt.status === filters.status);
    }

    // Type filter
    if (filters.type) {
      filtered = filtered.filter(debt => debt.type === filters.type);
    }

    // Balance range filter
    if (filters.minBalance) {
      const minBalance = parseFloat(filters.minBalance);
      if (!isNaN(minBalance)) {
        filtered = filtered.filter(debt => debt.balance >= minBalance);
      }
    }

    if (filters.maxBalance) {
      const maxBalance = parseFloat(filters.maxBalance);
      if (!isNaN(maxBalance)) {
        filtered = filtered.filter(debt => debt.balance <= maxBalance);
      }
    }

    // Sorting
    filtered.sort((a, b) => {
      let aValue: any;
      let bValue: any;

      switch (filters.sortBy) {
        case 'name':
          aValue = a.name.toLowerCase();
          bValue = b.name.toLowerCase();
          break;
        case 'balance':
          aValue = a.balance;
          bValue = b.balance;
          break;
        case 'apr':
          aValue = a.apr;
          bValue = b.apr;
          break;
        case 'minimumPayment':
          aValue = a.minimumPayment;
          bValue = b.minimumPayment;
          break;
        case 'created':
          aValue = a.createdAt || 0;
          bValue = b.createdAt || 0;
          break;
        default:
          aValue = a.balance;
          bValue = b.balance;
      }

      if (aValue < bValue) {
        return filters.sortOrder === 'asc' ? -1 : 1;
      }
      if (aValue > bValue) {
        return filters.sortOrder === 'asc' ? 1 : -1;
      }
      return 0;
    });

    return filtered;
  }, [debts, filters]);

  const updateFilters = (newFilters: DebtFiltersType) => {
    setFilters(newFilters);
  };

  const resetFilters = () => {
    setFilters(defaultFilters);
  };

  return {
    filters,
    filteredDebts,
    updateFilters,
    resetFilters,
  };
};
