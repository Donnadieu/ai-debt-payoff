import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { DebtService } from '../../services/api';
import {
  Debt,
  CreateDebtRequest,
  UpdateDebtRequest,
  DebtPayment,
  CreatePaymentRequest,
  DebtSummary,
  QueryParams,
} from '../../types/api';

// Query keys
export const debtKeys = {
  all: ['debts'] as const,
  lists: () => [...debtKeys.all, 'list'] as const,
  list: (params?: QueryParams) => [...debtKeys.lists(), params] as const,
  details: () => [...debtKeys.all, 'detail'] as const,
  detail: (id: string) => [...debtKeys.details(), id] as const,
  summary: () => [...debtKeys.all, 'summary'] as const,
  payments: (debtId?: string) => [...debtKeys.all, 'payments', debtId] as const,
};

// Hooks for debts
export const useDebts = (params?: QueryParams) => {
  return useQuery({
    queryKey: debtKeys.list(params),
    queryFn: () => DebtService.getDebts(params),
  });
};

export const useDebt = (debtId: string) => {
  return useQuery({
    queryKey: debtKeys.detail(debtId),
    queryFn: () => DebtService.getDebt(debtId),
    enabled: !!debtId,
  });
};

export const useDebtSummary = () => {
  return useQuery({
    queryKey: debtKeys.summary(),
    queryFn: () => DebtService.getDebtSummary(),
  });
};

export const useDebtPayments = (debtId: string, params?: QueryParams) => {
  return useQuery({
    queryKey: debtKeys.payments(debtId),
    queryFn: () => DebtService.getDebtPayments(debtId, params),
    enabled: !!debtId,
  });
};

export const useAllPayments = (params?: QueryParams) => {
  return useQuery({
    queryKey: [...debtKeys.all, 'all-payments', params],
    queryFn: () => DebtService.getAllPayments(params),
  });
};

// Mutations for debts
export const useCreateDebt = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (debtData: CreateDebtRequest) => DebtService.createDebt(debtData),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: debtKeys.lists() });
      queryClient.invalidateQueries({ queryKey: debtKeys.summary() });
    },
  });
};

export const useUpdateDebt = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ debtId, data }: { debtId: string; data: UpdateDebtRequest }) =>
      DebtService.updateDebt(debtId, data),
    onSuccess: (updatedDebt) => {
      queryClient.invalidateQueries({ queryKey: debtKeys.lists() });
      queryClient.invalidateQueries({ queryKey: debtKeys.summary() });
      queryClient.setQueryData(debtKeys.detail(updatedDebt.id), updatedDebt);
    },
  });
};

export const useDeleteDebt = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (debtId: string) => DebtService.deleteDebt(debtId),
    onSuccess: (_, debtId) => {
      queryClient.invalidateQueries({ queryKey: debtKeys.lists() });
      queryClient.invalidateQueries({ queryKey: debtKeys.summary() });
      queryClient.removeQueries({ queryKey: debtKeys.detail(debtId) });
      queryClient.removeQueries({ queryKey: debtKeys.payments(debtId) });
    },
  });
};

export const useRecordPayment = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (paymentData: CreatePaymentRequest) => DebtService.recordPayment(paymentData),
    onSuccess: (payment) => {
      queryClient.invalidateQueries({ queryKey: debtKeys.lists() });
      queryClient.invalidateQueries({ queryKey: debtKeys.summary() });
      queryClient.invalidateQueries({ queryKey: debtKeys.detail(payment.debt_id) });
      queryClient.invalidateQueries({ queryKey: debtKeys.payments(payment.debt_id) });
      queryClient.invalidateQueries({ queryKey: [...debtKeys.all, 'all-payments'] });
    },
  });
};

export const useUpdatePayment = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ paymentId, data }: { paymentId: string; data: Partial<CreatePaymentRequest> }) =>
      DebtService.updatePayment(paymentId, data),
    onSuccess: (payment) => {
      queryClient.invalidateQueries({ queryKey: debtKeys.payments(payment.debt_id) });
      queryClient.invalidateQueries({ queryKey: [...debtKeys.all, 'all-payments'] });
    },
  });
};

export const useDeletePayment = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (paymentId: string) => DebtService.deletePayment(paymentId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: debtKeys.all });
    },
  });
};

export const useBulkCreateDebts = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (debts: CreateDebtRequest[]) => DebtService.bulkCreateDebts(debts),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: debtKeys.lists() });
      queryClient.invalidateQueries({ queryKey: debtKeys.summary() });
    },
  });
};

export const useExportDebts = () => {
  return useMutation({
    mutationFn: (format: 'csv' | 'json' = 'csv') => DebtService.exportDebts(format),
  });
};
