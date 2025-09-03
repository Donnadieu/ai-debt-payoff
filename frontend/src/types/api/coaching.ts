import type { BaseEntity } from './common';

export interface CoachingNudge extends BaseEntity {
  user_id: string;
  nudge_type: NudgeType;
  title: string;
  message: string;
  priority: NudgePriority;
  is_read: boolean;
  is_dismissed: boolean;
  expires_at?: string;
  action_url?: string;
  action_text?: string;
  context_data?: Record<string, any>;
}

export const NudgeType = {
  MOTIVATIONAL: 'motivational',
  REMINDER: 'reminder',
  WARNING: 'warning',
  CELEBRATION: 'celebration',
  TIP: 'tip',
  CHALLENGE: 'challenge',
  MILESTONE: 'milestone',
  SLIP_PREVENTION: 'slip_prevention',
} as const;

export type NudgeType = typeof NudgeType[keyof typeof NudgeType];

export const NudgePriority = {
  LOW: 'low',
  MEDIUM: 'medium',
  HIGH: 'high',
  URGENT: 'urgent',
} as const;

export type NudgePriority = typeof NudgePriority[keyof typeof NudgePriority];

export interface CreateNudgeRequest {
  nudge_type: NudgeType;
  title: string;
  message: string;
  priority: NudgePriority;
  expires_at?: string;
  action_url?: string;
  action_text?: string;
  context_data?: Record<string, any>;
}

export interface UpdateNudgeRequest {
  is_read?: boolean;
  is_dismissed?: boolean;
}

export interface CoachingInsight extends BaseEntity {
  user_id: string;
  insight_type: InsightType;
  title: string;
  description: string;
  recommendations: string[];
  data_points: DataPoint[];
  confidence_score: number;
  impact_level: ImpactLevel;
}

export const InsightType = {
  SPENDING_PATTERN: 'spending_pattern',
  PROGRESS_UPDATE: 'progress_update',
  OPTIMIZATION: 'optimization',
  BEHAVIORAL: 'behavioral',
  FINANCIAL_HEALTH: 'financial_health',
} as const;

export type InsightType = typeof InsightType[keyof typeof InsightType];

export const ImpactLevel = {
  LOW: 'low',
  MEDIUM: 'medium',
  HIGH: 'high',
} as const;

export type ImpactLevel = typeof ImpactLevel[keyof typeof ImpactLevel];

export interface DataPoint {
  label: string;
  value: number | string;
  trend?: 'up' | 'down' | 'stable';
  comparison?: string;
}

export interface CoachingGoal extends BaseEntity {
  user_id: string;
  goal_type: GoalType;
  title: string;
  description: string;
  target_value: number;
  current_value: number;
  target_date: string;
  is_achieved: boolean;
  progress_percentage: number;
}

export const GoalType = {
  DEBT_PAYOFF: 'debt_payoff',
  SAVINGS: 'savings',
  SPENDING_REDUCTION: 'spending_reduction',
  INCOME_INCREASE: 'income_increase',
  EMERGENCY_FUND: 'emergency_fund',
} as const;

export type GoalType = typeof GoalType[keyof typeof GoalType];

export interface CreateGoalRequest {
  goal_type: GoalType;
  title: string;
  description: string;
  target_value: number;
  target_date: string;
}

export interface UpdateGoalRequest {
  title?: string;
  description?: string;
  target_value?: number;
  target_date?: string;
  current_value?: number;
}

export interface SlipDetection extends BaseEntity {
  user_id: string;
  slip_type: SlipType;
  severity: SlipSeverity;
  detected_at: string;
  description: string;
  contributing_factors: string[];
  recommendations: string[];
  is_resolved: boolean;
  resolution_notes?: string;
}

export const SlipType = {
  OVERSPENDING: 'overspending',
  MISSED_PAYMENT: 'missed_payment',
  NEW_DEBT: 'new_debt',
  GOAL_ABANDONMENT: 'goal_abandonment',
} as const;

export type SlipType = typeof SlipType[keyof typeof SlipType];

export const SlipSeverity = {
  MINOR: 'minor',
  MODERATE: 'moderate',
  MAJOR: 'major',
  CRITICAL: 'critical',
} as const;

export type SlipSeverity = typeof SlipSeverity[keyof typeof SlipSeverity];

export interface ResolveSlipRequest {
  resolution_notes: string;
  action_taken: string;
}
