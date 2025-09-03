import { DebtFormData } from '../schemas/debt';

export const formatCurrency = (amount: number): string => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(amount);
};

export const formatPercentage = (rate: number): string => {
  return `${rate.toFixed(2)}%`;
};

export const validateDebtRatio = (balance: number, minimumPayment: number): boolean => {
  // Minimum payment should not exceed 50% of balance (reasonable check)
  return minimumPayment <= balance * 0.5;
};

export const calculateMonthsToPayoff = (balance: number, apr: number, payment: number): number => {
  if (payment <= 0 || balance <= 0) return 0;
  
  const monthlyRate = apr / 100 / 12;
  if (monthlyRate === 0) {
    return Math.ceil(balance / payment);
  }
  
  // Check if payment covers interest
  const monthlyInterest = balance * monthlyRate;
  if (payment <= monthlyInterest) {
    return Infinity; // Will never pay off
  }
  
  const months = -Math.log(1 - (balance * monthlyRate) / payment) / Math.log(1 + monthlyRate);
  return Math.ceil(months);
};

export const validateFormData = (data: DebtFormData): string[] => {
  const errors: string[] = [];
  
  const balance = parseFloat(data.balance);
  const minimumPayment = parseFloat(data.minimumPayment);
  const apr = parseFloat(data.apr);
  
  if (!validateDebtRatio(balance, minimumPayment)) {
    errors.push('Minimum payment seems unusually high compared to balance');
  }
  
  if (apr > 0 && minimumPayment > 0) {
    const monthlyInterest = balance * (apr / 100 / 12);
    if (minimumPayment < monthlyInterest) {
      errors.push('Minimum payment is less than monthly interest - debt will grow');
    }
  }
  
  return errors;
};
