import { BaseEntity } from './common';
import { Debt } from './debt';

export interface PayoffStrategy extends BaseEntity {
  name: string;
  strategy_type: StrategyType;
  user_id: string;
  extra_payment: number;
  target_date?: string;
  is_active: boolean;
}

export enum StrategyType {
  SNOWBALL = 'snowball',
  AVALANCHE = 'avalanche',
  CUSTOM = 'custom',
}

export interface CreateStrategyRequest {
  name: string;
  strategy_type: StrategyType;
  extra_payment: number;
  target_date?: string;
  custom_order?: string[]; // debt IDs in custom order
}

export interface UpdateStrategyRequest {
  name?: string;
  extra_payment?: number;
  target_date?: string;
  custom_order?: string[];
  is_active?: boolean;
}

export interface StrategyComparison {
  strategies: StrategyResult[];
  recommended_strategy: StrategyType;
  savings_difference: number;
  time_difference_months: number;
}

export interface StrategyResult {
  strategy_type: StrategyType;
  total_interest: number;
  total_payments: number;
  payoff_date: string;
  months_to_payoff: number;
  payment_schedule: PaymentScheduleItem[];
}

export interface PaymentScheduleItem {
  month: number;
  date: string;
  debt_payments: DebtPaymentItem[];
  remaining_balance: number;
  total_payment: number;
  interest_paid: number;
}

export interface DebtPaymentItem {
  debt_id: string;
  debt_name: string;
  payment_amount: number;
  remaining_balance: number;
  is_final_payment: boolean;
}

export interface StrategyAnalysis {
  current_strategy: PayoffStrategy | null;
  projected_payoff_date: string;
  total_interest_savings: number;
  monthly_progress: MonthlyProgress[];
  milestones: Milestone[];
}

export interface MonthlyProgress {
  month: string;
  total_balance: number;
  total_payment: number;
  interest_paid: number;
  principal_paid: number;
  debts_remaining: number;
}

export interface Milestone {
  date: string;
  type: MilestoneType;
  description: string;
  amount?: number;
  debt_name?: string;
}

export enum MilestoneType {
  DEBT_PAID_OFF = 'debt_paid_off',
  HALFWAY_POINT = 'halfway_point',
  FINAL_PAYMENT = 'final_payment',
  SAVINGS_MILESTONE = 'savings_milestone',
}
