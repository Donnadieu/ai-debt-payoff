import { BaseEntity } from './common';

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

export enum NudgeType {
  PAYMENT_REMINDER = 'payment_reminder',
  STRATEGY_SUGGESTION = 'strategy_suggestion',
  MILESTONE_CELEBRATION = 'milestone_celebration',
  SLIP_DETECTION = 'slip_detection',
  MOTIVATION = 'motivation',
  EDUCATIONAL = 'educational',
  GOAL_ADJUSTMENT = 'goal_adjustment',
}

export enum NudgePriority {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  URGENT = 'urgent',
}

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

export enum InsightType {
  SPENDING_PATTERN = 'spending_pattern',
  PAYMENT_BEHAVIOR = 'payment_behavior',
  STRATEGY_EFFECTIVENESS = 'strategy_effectiveness',
  GOAL_PROGRESS = 'goal_progress',
  RISK_ASSESSMENT = 'risk_assessment',
  OPPORTUNITY = 'opportunity',
}

export enum ImpactLevel {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  CRITICAL = 'critical',
}

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

export enum GoalType {
  DEBT_FREE_DATE = 'debt_free_date',
  TOTAL_INTEREST_SAVINGS = 'total_interest_savings',
  MONTHLY_PAYMENT_REDUCTION = 'monthly_payment_reduction',
  EMERGENCY_FUND = 'emergency_fund',
  CREDIT_SCORE_IMPROVEMENT = 'credit_score_improvement',
  DEBT_TO_INCOME_RATIO = 'debt_to_income_ratio',
}

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

export enum SlipType {
  MISSED_PAYMENT = 'missed_payment',
  REDUCED_PAYMENT = 'reduced_payment',
  NEW_DEBT_ADDED = 'new_debt_added',
  STRATEGY_ABANDONED = 'strategy_abandoned',
  GOAL_REGRESSION = 'goal_regression',
}

export enum SlipSeverity {
  MINOR = 'minor',
  MODERATE = 'moderate',
  MAJOR = 'major',
  CRITICAL = 'critical',
}

export interface ResolveSlipRequest {
  resolution_notes: string;
  action_taken: string;
}
