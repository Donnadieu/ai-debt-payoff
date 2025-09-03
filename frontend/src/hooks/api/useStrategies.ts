import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { StrategyService } from '../../services/api';
import {
  PayoffStrategy,
  CreateStrategyRequest,
  UpdateStrategyRequest,
  StrategyComparison,
  StrategyAnalysis,
  QueryParams,
} from '../../types/api';

// Query keys
export const strategyKeys = {
  all: ['strategies'] as const,
  lists: () => [...strategyKeys.all, 'list'] as const,
  list: (params?: QueryParams) => [...strategyKeys.lists(), params] as const,
  details: () => [...strategyKeys.all, 'detail'] as const,
  detail: (id: string) => [...strategyKeys.details(), id] as const,
  active: () => [...strategyKeys.all, 'active'] as const,
  comparison: (extraPayment: number, customOrder?: string[]) => 
    [...strategyKeys.all, 'comparison', extraPayment, customOrder] as const,
  analysis: (id: string) => [...strategyKeys.all, 'analysis', id] as const,
  recommendations: () => [...strategyKeys.all, 'recommendations'] as const,
};

// Hooks for strategies
export const useStrategies = (params?: QueryParams) => {
  return useQuery({
    queryKey: strategyKeys.list(params),
    queryFn: () => StrategyService.getStrategies(params),
  });
};

export const useStrategy = (strategyId: string) => {
  return useQuery({
    queryKey: strategyKeys.detail(strategyId),
    queryFn: () => StrategyService.getStrategy(strategyId),
    enabled: !!strategyId,
  });
};

export const useActiveStrategy = () => {
  return useQuery({
    queryKey: strategyKeys.active(),
    queryFn: () => StrategyService.getActiveStrategy(),
  });
};

export const useStrategyComparison = (extraPayment: number, customOrder?: string[]) => {
  return useQuery({
    queryKey: strategyKeys.comparison(extraPayment, customOrder),
    queryFn: () => StrategyService.compareStrategies(extraPayment, customOrder),
    enabled: extraPayment > 0,
  });
};

export const useStrategyAnalysis = (strategyId: string) => {
  return useQuery({
    queryKey: strategyKeys.analysis(strategyId),
    queryFn: () => StrategyService.getStrategyAnalysis(strategyId),
    enabled: !!strategyId,
  });
};

export const useStrategyRecommendations = () => {
  return useQuery({
    queryKey: strategyKeys.recommendations(),
    queryFn: () => StrategyService.getRecommendations(),
  });
};

// Mutations for strategies
export const useCreateStrategy = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (strategyData: CreateStrategyRequest) => StrategyService.createStrategy(strategyData),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: strategyKeys.lists() });
    },
  });
};

export const useUpdateStrategy = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ strategyId, data }: { strategyId: string; data: UpdateStrategyRequest }) =>
      StrategyService.updateStrategy(strategyId, data),
    onSuccess: (updatedStrategy) => {
      queryClient.invalidateQueries({ queryKey: strategyKeys.lists() });
      queryClient.setQueryData(strategyKeys.detail(updatedStrategy.id), updatedStrategy);
      if (updatedStrategy.is_active) {
        queryClient.invalidateQueries({ queryKey: strategyKeys.active() });
      }
    },
  });
};

export const useDeleteStrategy = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (strategyId: string) => StrategyService.deleteStrategy(strategyId),
    onSuccess: (_, strategyId) => {
      queryClient.invalidateQueries({ queryKey: strategyKeys.lists() });
      queryClient.invalidateQueries({ queryKey: strategyKeys.active() });
      queryClient.removeQueries({ queryKey: strategyKeys.detail(strategyId) });
      queryClient.removeQueries({ queryKey: strategyKeys.analysis(strategyId) });
    },
  });
};

export const useSetActiveStrategy = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (strategyId: string) => StrategyService.setActiveStrategy(strategyId),
    onSuccess: (activeStrategy) => {
      queryClient.invalidateQueries({ queryKey: strategyKeys.lists() });
      queryClient.setQueryData(strategyKeys.active(), activeStrategy);
    },
  });
};

export const useCalculateStrategy = () => {
  return useMutation({
    mutationFn: ({ strategyType, extraPayment, customOrder }: {
      strategyType: string;
      extraPayment: number;
      customOrder?: string[];
    }) => StrategyService.calculateStrategy(strategyType, extraPayment, customOrder),
  });
};

export const useSimulateScenario = () => {
  return useMutation({
    mutationFn: (params: {
      extra_payment_change: number;
      new_debt_amount?: number;
      payment_frequency_change?: 'monthly' | 'bi-weekly' | 'weekly';
      target_date?: string;
    }) => StrategyService.simulateScenario(params),
  });
};

export const useExportStrategy = () => {
  return useMutation({
    mutationFn: ({ strategyId, format }: { strategyId: string; format?: 'csv' | 'json' | 'pdf' }) =>
      StrategyService.exportStrategy(strategyId, format),
  });
};
