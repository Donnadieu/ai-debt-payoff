import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { AnalyticsService } from '../../services/api';
import {
  AnalyticsEvent,
  CreateEventRequest,
  UserSession,
  AnalyticsDashboard,
  PerformanceMetrics,
  QueryParams,
} from '../../types/api';

// Query keys
export const analyticsKeys = {
  all: ['analytics'] as const,
  events: () => [...analyticsKeys.all, 'events'] as const,
  eventsList: (params?: QueryParams) => [...analyticsKeys.events(), 'list', params] as const,
  sessions: () => [...analyticsKeys.all, 'sessions'] as const,
  sessionsList: (params?: QueryParams) => [...analyticsKeys.sessions(), 'list', params] as const,
  dashboard: (dateRange?: { start_date: string; end_date: string }) => 
    [...analyticsKeys.all, 'dashboard', dateRange] as const,
  performance: (timeframe: string) => [...analyticsKeys.all, 'performance', timeframe] as const,
  insights: (type: string) => [...analyticsKeys.all, 'insights', type] as const,
};

// Hooks for analytics
export const useAnalyticsEvents = (params?: QueryParams) => {
  return useQuery({
    queryKey: analyticsKeys.eventsList(params),
    queryFn: () => AnalyticsService.getEvents(params),
  });
};

export const useAnalyticsSessions = (params?: QueryParams) => {
  return useQuery({
    queryKey: analyticsKeys.sessionsList(params),
    queryFn: () => AnalyticsService.getSessions(params),
  });
};

export const useAnalyticsDashboard = (dateRange?: { start_date: string; end_date: string }) => {
  return useQuery({
    queryKey: analyticsKeys.dashboard(dateRange),
    queryFn: () => AnalyticsService.getDashboard(dateRange),
  });
};

export const usePerformanceMetrics = (timeframe: '1h' | '24h' | '7d' | '30d' = '24h') => {
  return useQuery({
    queryKey: analyticsKeys.performance(timeframe),
    queryFn: () => AnalyticsService.getPerformanceMetrics(timeframe),
  });
};

export const useUserInsights = () => {
  return useQuery({
    queryKey: analyticsKeys.insights('user'),
    queryFn: () => AnalyticsService.getUserInsights(),
  });
};

export const useDebtInsights = () => {
  return useQuery({
    queryKey: analyticsKeys.insights('debt'),
    queryFn: () => AnalyticsService.getDebtInsights(),
  });
};

// Mutations for analytics
export const useTrackEvent = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (eventData: CreateEventRequest) => AnalyticsService.trackEvent(eventData),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: analyticsKeys.events() });
    },
  });
};

export const useStartSession = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (deviceInfo?: any) => AnalyticsService.startSession(deviceInfo),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: analyticsKeys.sessions() });
    },
  });
};

export const useEndSession = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (sessionId: string) => AnalyticsService.endSession(sessionId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: analyticsKeys.sessions() });
    },
  });
};

export const useTrackBatchEvents = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (events: CreateEventRequest[]) => AnalyticsService.trackBatchEvents(events),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: analyticsKeys.events() });
    },
  });
};

export const useExportAnalytics = () => {
  return useMutation({
    mutationFn: ({ type, format, dateRange }: {
      type: 'events' | 'sessions' | 'insights';
      format?: 'csv' | 'json';
      dateRange?: { start_date: string; end_date: string };
    }) => AnalyticsService.exportData(type, format, dateRange),
  });
};

// Convenience hooks for common tracking
export const usePageTracking = () => {
  const trackEvent = useTrackEvent();

  return {
    trackPageView: (page: string, additionalData?: Record<string, any>) => {
      return AnalyticsService.trackPageView(page, additionalData);
    },
    trackAction: (action: string, category: string, data?: Record<string, any>) => {
      return AnalyticsService.trackAction(action, category, data);
    },
  };
};
