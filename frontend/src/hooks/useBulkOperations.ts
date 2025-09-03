import { useState } from 'react';
import type { Debt } from '../schemas/debt';
// import { useDeleteDebt, useUpdateDebt } from '../services/api/debts';

interface UseBulkOperationsOptions {
  onSuccess?: () => void;
  onError?: (error: Error) => void;
}

export const useBulkOperations = ({ onSuccess, onError }: UseBulkOperationsOptions = {}) => {
  const [isLoading, setIsLoading] = useState(false);
  const [selectedDebts, setSelectedDebts] = useState<Set<string>>(new Set());
  
  // TODO: Implement when API hooks are available
  // const deleteDebtMutation = useDeleteDebt();
  // const updateDebtMutation = useUpdateDebt();

  const selectDebt = (debtId: string, selected: boolean) => {
    const newSelected = new Set(selectedDebts);
    if (selected) {
      newSelected.add(debtId);
    } else {
      newSelected.delete(debtId);
    }
    setSelectedDebts(newSelected);
  };

  const selectAll = (debts: Debt[]) => {
    setSelectedDebts(new Set(debts.map(debt => debt.id!)));
  };

  const clearSelection = () => {
    setSelectedDebts(new Set());
  };

  const bulkDelete = async (debts: Debt[]) => {
    setIsLoading(true);
    
    try {
      // TODO: Implement API calls when hooks are available
      // Delete debts sequentially to avoid overwhelming the API
      // for (const debt of debts) {
      //   await deleteDebtMutation.mutateAsync(debt.id!);
      // }
      
      console.log('Bulk delete:', debts.map(d => d.name));
      clearSelection();
      onSuccess?.();
    } catch (error) {
      const errorMessage = error instanceof Error ? error : new Error('Failed to delete debts');
      onError?.(errorMessage);
      throw errorMessage;
    } finally {
      setIsLoading(false);
    }
  };

  const bulkStatusChange = async (debts: Debt[], newStatus: string) => {
    setIsLoading(true);
    
    try {
      // TODO: Implement API calls when hooks are available
      // Update debts sequentially to avoid overwhelming the API
      // for (const debt of debts) {
      //   await updateDebtMutation.mutateAsync({
      //     id: debt.id!,
      //     ...debt,
      //     status: newStatus as any
      //   });
      // }
      
      console.log('Bulk status change:', debts.map(d => d.name), 'to', newStatus);
      clearSelection();
      onSuccess?.();
    } catch (error) {
      const errorMessage = error instanceof Error ? error : new Error('Failed to update debt status');
      onError?.(errorMessage);
      throw errorMessage;
    } finally {
      setIsLoading(false);
    }
  };

  const getSelectedDebts = (allDebts: Debt[]): Debt[] => {
    return allDebts.filter(debt => selectedDebts.has(debt.id!));
  };

  return {
    selectedDebts,
    selectedCount: selectedDebts.size,
    isLoading: isLoading, // || deleteDebtMutation.isPending || updateDebtMutation.isPending,
    selectDebt,
    selectAll,
    clearSelection,
    bulkDelete,
    bulkStatusChange,
    getSelectedDebts,
    error: null, // deleteDebtMutation.error || updateDebtMutation.error,
  };
};
