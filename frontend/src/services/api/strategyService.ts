import { apiClient } from './client';
import {
  PayoffStrategy,
  CreateStrategyRequest,
  UpdateStrategyRequest,
  StrategyComparison,
  StrategyResult,
  StrategyAnalysis,
  PaginatedResponse,
  QueryParams,
} from '../../types/api';

export class StrategyService {
  private static readonly BASE_PATH = '/api/strategies';

  /**
   * Get all strategies for the current user
   */
  static async getStrategies(params?: QueryParams): Promise<PaginatedResponse<PayoffStrategy>> {
    const response = await apiClient.get<PaginatedResponse<PayoffStrategy>>(this.BASE_PATH, {
      params,
    });
    return response.data;
  }

  /**
   * Get a specific strategy by ID
   */
  static async getStrategy(strategyId: string): Promise<PayoffStrategy> {
    const response = await apiClient.get<PayoffStrategy>(`${this.BASE_PATH}/${strategyId}`);
    return response.data;
  }

  /**
   * Create a new payoff strategy
   */
  static async createStrategy(strategyData: CreateStrategyRequest): Promise<PayoffStrategy> {
    const response = await apiClient.post<PayoffStrategy>(this.BASE_PATH, strategyData);
    return response.data;
  }

  /**
   * Update an existing strategy
   */
  static async updateStrategy(
    strategyId: string,
    strategyData: UpdateStrategyRequest
  ): Promise<PayoffStrategy> {
    const response = await apiClient.patch<PayoffStrategy>(
      `${this.BASE_PATH}/${strategyId}`,
      strategyData
    );
    return response.data;
  }

  /**
   * Delete a strategy
   */
  static async deleteStrategy(strategyId: string): Promise<void> {
    await apiClient.delete(`${this.BASE_PATH}/${strategyId}`);
  }

  /**
   * Get the currently active strategy
   */
  static async getActiveStrategy(): Promise<PayoffStrategy | null> {
    const response = await apiClient.get<PayoffStrategy | null>(`${this.BASE_PATH}/active`);
    return response.data;
  }

  /**
   * Set a strategy as active
   */
  static async setActiveStrategy(strategyId: string): Promise<PayoffStrategy> {
    const response = await apiClient.post<PayoffStrategy>(
      `${this.BASE_PATH}/${strategyId}/activate`
    );
    return response.data;
  }

  /**
   * Compare different payoff strategies
   */
  static async compareStrategies(
    extraPayment: number,
    customOrder?: string[]
  ): Promise<StrategyComparison> {
    const response = await apiClient.post<StrategyComparison>(`${this.BASE_PATH}/compare`, {
      extra_payment: extraPayment,
      custom_order: customOrder,
    });
    return response.data;
  }

  /**
   * Get detailed analysis for a specific strategy
   */
  static async getStrategyAnalysis(strategyId: string): Promise<StrategyAnalysis> {
    const response = await apiClient.get<StrategyAnalysis>(
      `${this.BASE_PATH}/${strategyId}/analysis`
    );
    return response.data;
  }

  /**
   * Calculate strategy results without saving
   */
  static async calculateStrategy(
    strategyType: string,
    extraPayment: number,
    customOrder?: string[]
  ): Promise<StrategyResult> {
    const response = await apiClient.post<StrategyResult>(`${this.BASE_PATH}/calculate`, {
      strategy_type: strategyType,
      extra_payment: extraPayment,
      custom_order: customOrder,
    });
    return response.data;
  }

  /**
   * Get strategy recommendations based on user's debt profile
   */
  static async getRecommendations(): Promise<{
    recommended_strategy: string;
    reasons: string[];
    projected_savings: number;
    alternative_strategies: Array<{
      strategy_type: string;
      pros: string[];
      cons: string[];
    }>;
  }> {
    const response = await apiClient.get(`${this.BASE_PATH}/recommendations`);
    return response.data;
  }

  /**
   * Simulate "what if" scenarios
   */
  static async simulateScenario(params: {
    extra_payment_change: number;
    new_debt_amount?: number;
    payment_frequency_change?: 'monthly' | 'bi-weekly' | 'weekly';
    target_date?: string;
  }): Promise<{
    original_result: StrategyResult;
    modified_result: StrategyResult;
    impact_summary: {
      time_difference_months: number;
      interest_difference: number;
      payment_difference: number;
    };
  }> {
    const response = await apiClient.post(`${this.BASE_PATH}/simulate`, params);
    return response.data;
  }

  /**
   * Export strategy data and projections
   */
  static async exportStrategy(
    strategyId: string,
    format: 'csv' | 'json' | 'pdf' = 'csv'
  ): Promise<Blob> {
    const response = await apiClient.get(`${this.BASE_PATH}/${strategyId}/export`, {
      params: { format },
      responseType: 'blob',
    });
    return response.data;
  }
}

export default StrategyService;
