import { apiClient } from './client';
import type {
  Debt,
  CreateDebtRequest,
  UpdateDebtRequest,
  DebtPayment,
  CreatePaymentRequest,
  DebtSummary,
  PaginatedResponse,
  QueryParams,
} from '../../types/api';

export class DebtService {
  private static readonly BASE_PATH = '/api/debts';

  /**
   * Get all debts for the current user
   */
  static async getDebts(params?: QueryParams): Promise<PaginatedResponse<Debt>> {
    const response = await apiClient.get<PaginatedResponse<Debt>>(this.BASE_PATH, {
      params,
    });
    return response.data;
  }

  /**
   * Get a specific debt by ID
   */
  static async getDebt(debtId: string): Promise<Debt> {
    const response = await apiClient.get<Debt>(`${this.BASE_PATH}/${debtId}`);
    return response.data;
  }

  /**
   * Create a new debt
   */
  static async createDebt(debtData: CreateDebtRequest): Promise<Debt> {
    const response = await apiClient.post<Debt>(this.BASE_PATH, debtData);
    return response.data;
  }

  /**
   * Update an existing debt
   */
  static async updateDebt(debtId: string, debtData: UpdateDebtRequest): Promise<Debt> {
    const response = await apiClient.patch<Debt>(`${this.BASE_PATH}/${debtId}`, debtData);
    return response.data;
  }

  /**
   * Delete a debt
   */
  static async deleteDebt(debtId: string): Promise<void> {
    await apiClient.delete(`${this.BASE_PATH}/${debtId}`);
  }

  /**
   * Get debt summary statistics
   */
  static async getDebtSummary(): Promise<DebtSummary> {
    const response = await apiClient.get<DebtSummary>(`${this.BASE_PATH}/summary`);
    return response.data;
  }

  /**
   * Get payments for a specific debt
   */
  static async getDebtPayments(
    debtId: string,
    params?: QueryParams
  ): Promise<PaginatedResponse<DebtPayment>> {
    const response = await apiClient.get<PaginatedResponse<DebtPayment>>(
      `${this.BASE_PATH}/${debtId}/payments`,
      { params }
    );
    return response.data;
  }

  /**
   * Record a payment for a debt
   */
  static async recordPayment(paymentData: CreatePaymentRequest): Promise<DebtPayment> {
    const response = await apiClient.post<DebtPayment>(
      `${this.BASE_PATH}/${paymentData.debt_id}/payments`,
      paymentData
    );
    return response.data;
  }

  /**
   * Get all payments across all debts
   */
  static async getAllPayments(params?: QueryParams): Promise<PaginatedResponse<DebtPayment>> {
    const response = await apiClient.get<PaginatedResponse<DebtPayment>>(
      '/api/payments',
      { params }
    );
    return response.data;
  }

  /**
   * Update a payment
   */
  static async updatePayment(
    paymentId: string,
    paymentData: Partial<CreatePaymentRequest>
  ): Promise<DebtPayment> {
    const response = await apiClient.patch<DebtPayment>(
      `/api/payments/${paymentId}`,
      paymentData
    );
    return response.data;
  }

  /**
   * Delete a payment
   */
  static async deletePayment(paymentId: string): Promise<void> {
    await apiClient.delete(`/api/payments/${paymentId}`);
  }

  /**
   * Bulk create debts from CSV or array
   */
  static async bulkCreateDebts(debts: CreateDebtRequest[]): Promise<Debt[]> {
    const response = await apiClient.post<Debt[]>(`${this.BASE_PATH}/bulk`, {
      debts,
    });
    return response.data;
  }

  /**
   * Export debts data
   */
  static async exportDebts(format: 'csv' | 'json' = 'csv'): Promise<Blob> {
    const response = await apiClient.get(`${this.BASE_PATH}/export`, {
      params: { format },
      responseType: 'blob',
    });
    return response.data;
  }
}

export default DebtService;
