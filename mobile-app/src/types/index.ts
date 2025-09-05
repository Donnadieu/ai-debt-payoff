// Type definitions for the debt payoff mobile app

export interface Debt {
  id: string;
  name: string;
  balance: number;
  interest_rate: number;
  minimum_payment: number;
  due_date: number;
  created_at: string;
  updated_at: string;
}

export interface PayoffPlan {
  strategy: 'snowball' | 'avalanche';
  total_debt: number;
  total_months: number;
  monthly_payment: number;
  total_interest: number;
  debts: Debt[];
}

export interface Nudge {
  id: string;
  title: string;
  message: string;
  nudge_type: string;
  priority: number;
  user_id: string;
  created_at: string;
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
}