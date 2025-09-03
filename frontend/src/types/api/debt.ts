import type { BaseEntity } from './common';

export interface Debt extends BaseEntity {
  name: string;
  balance: number;
  minimum_payment: number;
  apr: number;
  debt_type: DebtType;
  user_id: string;
}

export const DebtType = {
  CREDIT_CARD: 'credit_card',
  STUDENT_LOAN: 'student_loan',
  MORTGAGE: 'mortgage',
  AUTO_LOAN: 'auto_loan',
  PERSONAL_LOAN: 'personal_loan',
  OTHER: 'other',
} as const;

export type DebtType = typeof DebtType[keyof typeof DebtType];

export interface CreateDebtRequest {
  name: string;
  balance: number;
  minimum_payment: number;
  apr: number;
  debt_type: DebtType;
}

export interface UpdateDebtRequest {
  name?: string;
  balance?: number;
  minimum_payment?: number;
  apr?: number;
  debt_type?: DebtType;
}

export interface DebtPayment extends BaseEntity {
  debt_id: string;
  amount: number;
  payment_date: string;
  payment_type: PaymentType;
  notes?: string;
}

export const PaymentType = {
  MINIMUM: 'minimum',
  EXTRA: 'extra',
  LUMP_SUM: 'lump_sum',
} as const;

export type PaymentType = typeof PaymentType[keyof typeof PaymentType];

export interface CreatePaymentRequest {
  debt_id: string;
  amount: number;
  payment_date: string;
  payment_type: PaymentType;
  notes?: string;
}

export interface DebtSummary {
  total_balance: number;
  total_minimum_payment: number;
  total_debts: number;
  average_apr: number;
  highest_apr_debt: Debt | null;
  lowest_balance_debt: Debt | null;
}
