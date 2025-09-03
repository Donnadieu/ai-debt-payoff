import { apiClient } from './client';
import type {
  AnalyticsEvent,
  CreateEventRequest,
  UserSession,
  AnalyticsDashboard,
  PerformanceMetrics,
  PaginatedResponse,
  QueryParams,
} from '../../types/api';

export class AnalyticsService {
  private static readonly BASE_PATH = '/api/analytics';

  /**
   * Track an analytics event
   */
  static async trackEvent(eventData: CreateEventRequest): Promise<AnalyticsEvent> {
    const response = await apiClient.post<AnalyticsEvent>(`${this.BASE_PATH}/events`, eventData);
    return response.data;
  }

  /**
   * Get analytics events for the current user
   */
  static async getEvents(params?: QueryParams): Promise<PaginatedResponse<AnalyticsEvent>> {
    const response = await apiClient.get<PaginatedResponse<AnalyticsEvent>>(
      `${this.BASE_PATH}/events`,
      { params }
    );
    return response.data;
  }

  /**
   * Get user sessions
   */
  static async getSessions(params?: QueryParams): Promise<PaginatedResponse<UserSession>> {
    const response = await apiClient.get<PaginatedResponse<UserSession>>(
      `${this.BASE_PATH}/sessions`,
      { params }
    );
    return response.data;
  }

  /**
   * Start a new user session
   */
  static async startSession(deviceInfo?: any): Promise<UserSession> {
    const response = await apiClient.post<UserSession>(`${this.BASE_PATH}/sessions`, {
      device_info: deviceInfo,
    });
    return response.data;
  }

  /**
   * End the current session
   */
  static async endSession(sessionId: string): Promise<UserSession> {
    const response = await apiClient.patch<UserSession>(
      `${this.BASE_PATH}/sessions/${sessionId}/end`
    );
    return response.data;
  }

  /**
   * Get analytics dashboard data
   */
  static async getDashboard(dateRange?: {
    start_date: string;
    end_date: string;
  }): Promise<AnalyticsDashboard> {
    const response = await apiClient.get<AnalyticsDashboard>(`${this.BASE_PATH}/dashboard`, {
      params: dateRange,
    });
    return response.data;
  }

  /**
   * Get performance metrics
   */
  static async getPerformanceMetrics(timeframe: '1h' | '24h' | '7d' | '30d' = '24h'): Promise<PerformanceMetrics> {
    const response = await apiClient.get<PerformanceMetrics>(`${this.BASE_PATH}/performance`, {
      params: { timeframe },
    });
    return response.data;
  }

  /**
   * Get user behavior insights
   */
  static async getUserInsights(): Promise<{
    most_active_hours: number[];
    preferred_features: string[];
    usage_patterns: Record<string, any>;
    engagement_score: number;
  }> {
    const response = await apiClient.get(`${this.BASE_PATH}/insights/user`);
    return response.data;
  }

  /**
   * Get debt management insights
   */
  static async getDebtInsights(): Promise<{
    payment_consistency: number;
    strategy_effectiveness: number;
    goal_progress: number;
    risk_factors: string[];
    recommendations: string[];
  }> {
    const response = await apiClient.get(`${this.BASE_PATH}/insights/debt`);
    return response.data;
  }

  /**
   * Track page view
   */
  static async trackPageView(page: string, additionalData?: Record<string, any>): Promise<void> {
    await this.trackEvent({
      event_type: 'page_view' as any,
      event_data: {
        page,
        timestamp: new Date().toISOString(),
        ...additionalData,
      },
    });
  }

  /**
   * Track user action
   */
  static async trackAction(
    action: string,
    category: string,
    data?: Record<string, any>
  ): Promise<void> {
    await this.trackEvent({
      event_type: action as any,
      event_data: {
        category,
        action,
        timestamp: new Date().toISOString(),
        ...data,
      },
    });
  }

  /**
   * Batch track multiple events
   */
  static async trackBatchEvents(events: CreateEventRequest[]): Promise<AnalyticsEvent[]> {
    const response = await apiClient.post<AnalyticsEvent[]>(`${this.BASE_PATH}/events/batch`, {
      events,
    });
    return response.data;
  }

  /**
   * Get event aggregations
   */
  static async getEventAggregations(params: {
    event_types?: string[];
    group_by: 'hour' | 'day' | 'week' | 'month';
    start_date: string;
    end_date: string;
  }): Promise<Array<{
    period: string;
    event_type: string;
    count: number;
    unique_users: number;
  }>> {
    const response = await apiClient.get(`${this.BASE_PATH}/events/aggregations`, {
      params,
    });
    return response.data;
  }

  /**
   * Export analytics data
   */
  static async exportData(
    type: 'events' | 'sessions' | 'insights',
    format: 'csv' | 'json' = 'csv',
    dateRange?: { start_date: string; end_date: string }
  ): Promise<Blob> {
    const response = await apiClient.get(`${this.BASE_PATH}/export/${type}`, {
      params: { format, ...dateRange },
      responseType: 'blob',
    });
    return response.data;
  }
}

export default AnalyticsService;
