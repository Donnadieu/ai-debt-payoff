import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { CoachingService } from '../../services/api';
import {
  CoachingNudge,
  CoachingInsight,
  CoachingGoal,
  CreateGoalRequest,
  UpdateGoalRequest,
  SlipDetection,
  ResolveSlipRequest,
  QueryParams,
} from '../../types/api';

// Query keys
export const coachingKeys = {
  all: ['coaching'] as const,
  nudges: () => [...coachingKeys.all, 'nudges'] as const,
  nudgesList: (params?: QueryParams & { unread_only?: boolean; priority?: string }) => 
    [...coachingKeys.nudges(), 'list', params] as const,
  nudge: (id: string) => [...coachingKeys.nudges(), id] as const,
  insights: () => [...coachingKeys.all, 'insights'] as const,
  insightsList: (params?: QueryParams) => [...coachingKeys.insights(), 'list', params] as const,
  insight: (id: string) => [...coachingKeys.insights(), id] as const,
  goals: () => [...coachingKeys.all, 'goals'] as const,
  goalsList: (params?: QueryParams) => [...coachingKeys.goals(), 'list', params] as const,
  slips: () => [...coachingKeys.all, 'slips'] as const,
  slipsList: (params?: QueryParams & { unresolved_only?: boolean; severity?: string }) => 
    [...coachingKeys.slips(), 'list', params] as const,
  preferences: () => [...coachingKeys.all, 'preferences'] as const,
  motivation: () => [...coachingKeys.all, 'motivation'] as const,
  report: (period: string) => [...coachingKeys.all, 'report', period] as const,
};

// Hooks for nudges
export const useCoachingNudges = (params?: QueryParams & { unread_only?: boolean; priority?: string }) => {
  return useQuery({
    queryKey: coachingKeys.nudgesList(params),
    queryFn: () => CoachingService.getNudges(params),
  });
};

export const useCoachingNudge = (nudgeId: string) => {
  return useQuery({
    queryKey: coachingKeys.nudge(nudgeId),
    queryFn: () => CoachingService.getNudge(nudgeId),
    enabled: !!nudgeId,
  });
};

// Hooks for insights
export const useCoachingInsights = (params?: QueryParams) => {
  return useQuery({
    queryKey: coachingKeys.insightsList(params),
    queryFn: () => CoachingService.getInsights(params),
  });
};

export const useCoachingInsight = (insightId: string) => {
  return useQuery({
    queryKey: coachingKeys.insight(insightId),
    queryFn: () => CoachingService.getInsight(insightId),
    enabled: !!insightId,
  });
};

// Hooks for goals
export const useCoachingGoals = (params?: QueryParams) => {
  return useQuery({
    queryKey: coachingKeys.goalsList(params),
    queryFn: () => CoachingService.getGoals(params),
  });
};

// Hooks for slip detections
export const useSlipDetections = (params?: QueryParams & { unresolved_only?: boolean; severity?: string }) => {
  return useQuery({
    queryKey: coachingKeys.slipsList(params),
    queryFn: () => CoachingService.getSlipDetections(params),
  });
};

// Hooks for preferences and content
export const useCoachingPreferences = () => {
  return useQuery({
    queryKey: coachingKeys.preferences(),
    queryFn: () => CoachingService.getPreferences(),
  });
};

export const useMotivationalContent = () => {
  return useQuery({
    queryKey: coachingKeys.motivation(),
    queryFn: () => CoachingService.getMotivationalContent(),
    staleTime: 30 * 60 * 1000, // 30 minutes
  });
};

export const useCoachingReport = (period: '7d' | '30d' | '90d' = '30d') => {
  return useQuery({
    queryKey: coachingKeys.report(period),
    queryFn: () => CoachingService.generateReport(period),
  });
};

// Mutations for nudges
export const useMarkNudgeAsRead = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (nudgeId: string) => CoachingService.markNudgeAsRead(nudgeId),
    onSuccess: (updatedNudge) => {
      queryClient.invalidateQueries({ queryKey: coachingKeys.nudges() });
      queryClient.setQueryData(coachingKeys.nudge(updatedNudge.id), updatedNudge);
    },
  });
};

export const useDismissNudge = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (nudgeId: string) => CoachingService.dismissNudge(nudgeId),
    onSuccess: (updatedNudge) => {
      queryClient.invalidateQueries({ queryKey: coachingKeys.nudges() });
      queryClient.setQueryData(coachingKeys.nudge(updatedNudge.id), updatedNudge);
    },
  });
};

// Mutations for goals
export const useCreateGoal = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (goalData: CreateGoalRequest) => CoachingService.createGoal(goalData),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: coachingKeys.goals() });
    },
  });
};

export const useUpdateGoal = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ goalId, data }: { goalId: string; data: UpdateGoalRequest }) =>
      CoachingService.updateGoal(goalId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: coachingKeys.goals() });
    },
  });
};

export const useDeleteGoal = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (goalId: string) => CoachingService.deleteGoal(goalId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: coachingKeys.goals() });
    },
  });
};

// Mutations for slip detections
export const useResolveSlip = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ slipId, resolution }: { slipId: string; resolution: ResolveSlipRequest }) =>
      CoachingService.resolveSlip(slipId, resolution),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: coachingKeys.slips() });
    },
  });
};

// Mutations for advice and preferences
export const useGetPersonalizedAdvice = () => {
  return useMutation({
    mutationFn: (context: {
      topic: 'debt_strategy' | 'budgeting' | 'motivation' | 'goal_setting';
      current_situation: string;
      specific_question?: string;
    }) => CoachingService.getPersonalizedAdvice(context),
  });
};

export const useUpdatePreferences = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (preferences: {
      nudge_frequency: 'daily' | 'weekly' | 'monthly';
      nudge_types: string[];
      coaching_style: 'encouraging' | 'direct' | 'analytical';
      reminder_time?: string;
    }) => CoachingService.updatePreferences(preferences),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: coachingKeys.preferences() });
    },
  });
};

export const useRequestIntervention = () => {
  return useMutation({
    mutationFn: (situation: {
      type: 'financial_stress' | 'motivation_loss' | 'strategy_confusion' | 'emergency';
      description: string;
      urgency: 'low' | 'medium' | 'high' | 'critical';
    }) => CoachingService.requestIntervention(situation),
  });
};
