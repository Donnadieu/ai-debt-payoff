import { BaseEntity } from './common';

export interface AnalyticsEvent extends BaseEntity {
  user_id: string;
  event_type: EventType;
  event_data: Record<string, any>;
  session_id?: string;
  timestamp: string;
}

export enum EventType {
  PAGE_VIEW = 'page_view',
  DEBT_CREATED = 'debt_created',
  DEBT_UPDATED = 'debt_updated',
  DEBT_DELETED = 'debt_deleted',
  PAYMENT_RECORDED = 'payment_recorded',
  STRATEGY_CREATED = 'strategy_created',
  STRATEGY_UPDATED = 'strategy_updated',
  STRATEGY_COMPARED = 'strategy_compared',
  GOAL_SET = 'goal_set',
  MILESTONE_REACHED = 'milestone_reached',
  EXPORT_DATA = 'export_data',
  COACHING_VIEWED = 'coaching_viewed',
}

export interface CreateEventRequest {
  event_type: EventType;
  event_data: Record<string, any>;
  session_id?: string;
}

export interface UserSession extends BaseEntity {
  user_id: string;
  session_start: string;
  session_end?: string;
  duration_seconds?: number;
  page_views: number;
  events_count: number;
  device_info?: DeviceInfo;
}

export interface DeviceInfo {
  user_agent: string;
  screen_resolution: string;
  browser: string;
  os: string;
  device_type: 'desktop' | 'tablet' | 'mobile';
}

export interface AnalyticsDashboard {
  user_stats: UserStats;
  debt_stats: DebtStats;
  strategy_stats: StrategyStats;
  engagement_stats: EngagementStats;
  recent_events: AnalyticsEvent[];
}

export interface UserStats {
  total_users: number;
  active_users_today: number;
  active_users_week: number;
  active_users_month: number;
  new_users_today: number;
  retention_rate: number;
}

export interface DebtStats {
  total_debts: number;
  total_debt_amount: number;
  average_debt_per_user: number;
  most_common_debt_type: string;
  total_payments_recorded: number;
  total_amount_paid: number;
}

export interface StrategyStats {
  total_strategies: number;
  most_popular_strategy: string;
  average_extra_payment: number;
  strategies_by_type: Record<string, number>;
  average_payoff_time_months: number;
}

export interface EngagementStats {
  average_session_duration: number;
  average_page_views_per_session: number;
  bounce_rate: number;
  most_viewed_pages: PageView[];
  peak_usage_hours: number[];
}

export interface PageView {
  page: string;
  views: number;
  unique_visitors: number;
  average_time_on_page: number;
}

export interface PerformanceMetrics {
  api_response_times: ResponseTimeMetrics;
  error_rates: ErrorRateMetrics;
  system_health: SystemHealthMetrics;
}

export interface ResponseTimeMetrics {
  average_response_time: number;
  p95_response_time: number;
  p99_response_time: number;
  slowest_endpoints: EndpointMetric[];
}

export interface ErrorRateMetrics {
  total_errors: number;
  error_rate_percentage: number;
  errors_by_type: Record<string, number>;
  errors_by_endpoint: Record<string, number>;
}

export interface SystemHealthMetrics {
  uptime_percentage: number;
  cpu_usage: number;
  memory_usage: number;
  disk_usage: number;
  active_connections: number;
}

export interface EndpointMetric {
  endpoint: string;
  average_response_time: number;
  request_count: number;
  error_count: number;
}
