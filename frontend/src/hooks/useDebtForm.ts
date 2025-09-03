import { useState } from 'react';
import { DebtFormData } from '../schemas/debt';
import { useCreateDebt, useUpdateDebt } from '../services/api/debts';

interface UseDebtFormOptions {
  debtId?: string;
  onSuccess?: () => void;
  onError?: (error: Error) => void;
}

export const useDebtForm = ({ debtId, onSuccess, onError }: UseDebtFormOptions = {}) => {
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const createDebtMutation = useCreateDebt();
  const updateDebtMutation = useUpdateDebt();

  const handleSubmit = async (data: DebtFormData) => {
    setIsSubmitting(true);
    
    try {
      if (debtId) {
        await updateDebtMutation.mutateAsync({ id: debtId, ...data });
      } else {
        await createDebtMutation.mutateAsync(data);
      }
      
      onSuccess?.();
    } catch (error) {
      const errorMessage = error instanceof Error ? error : new Error('Failed to save debt');
      onError?.(errorMessage);
      throw errorMessage;
    } finally {
      setIsSubmitting(false);
    }
  };

  return {
    handleSubmit,
    isSubmitting: isSubmitting || createDebtMutation.isPending || updateDebtMutation.isPending,
    isLoading: createDebtMutation.isPending || updateDebtMutation.isPending,
    error: createDebtMutation.error || updateDebtMutation.error,
  };
};
