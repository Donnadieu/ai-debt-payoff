import { BaseEntity } from './common';

export interface Debt extends BaseEntity {
  name: string;
  balance: number;
  minimum_payment: number;
  apr: number;
  debt_type: DebtType;
  user_id: string;
}

export enum DebtType {
  CREDIT_CARD = 'credit_card',
  STUDENT_LOAN = 'student_loan',
  MORTGAGE = 'mortgage',
  PERSONAL_LOAN = 'personal_loan',
  AUTO_LOAN = 'auto_loan',
  OTHER = 'other',
}

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

export enum PaymentType {
  MINIMUM = 'minimum',
  EXTRA = 'extra',
  LUMP_SUM = 'lump_sum',
}

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
