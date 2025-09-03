import { apiClient } from './client';
import {
  CoachingNudge,
  CreateNudgeRequest,
  UpdateNudgeRequest,
  CoachingInsight,
  CoachingGoal,
  CreateGoalRequest,
  UpdateGoalRequest,
  SlipDetection,
  ResolveSlipRequest,
  PaginatedResponse,
  QueryParams,
} from '../../types/api';

export class CoachingService {
  private static readonly BASE_PATH = '/api/coaching';

  /**
   * Get coaching nudges for the current user
   */
  static async getNudges(params?: QueryParams & {
    unread_only?: boolean;
    priority?: string;
  }): Promise<PaginatedResponse<CoachingNudge>> {
    const response = await apiClient.get<PaginatedResponse<CoachingNudge>>(
      `${this.BASE_PATH}/nudges`,
      { params }
    );
    return response.data;
  }

  /**
   * Get a specific nudge by ID
   */
  static async getNudge(nudgeId: string): Promise<CoachingNudge> {
    const response = await apiClient.get<CoachingNudge>(`${this.BASE_PATH}/nudges/${nudgeId}`);
    return response.data;
  }

  /**
   * Mark a nudge as read
   */
  static async markNudgeAsRead(nudgeId: string): Promise<CoachingNudge> {
    const response = await apiClient.patch<CoachingNudge>(
      `${this.BASE_PATH}/nudges/${nudgeId}`,
      { is_read: true } as UpdateNudgeRequest
    );
    return response.data;
  }

  /**
   * Dismiss a nudge
   */
  static async dismissNudge(nudgeId: string): Promise<CoachingNudge> {
    const response = await apiClient.patch<CoachingNudge>(
      `${this.BASE_PATH}/nudges/${nudgeId}`,
      { is_dismissed: true } as UpdateNudgeRequest
    );
    return response.data;
  }

  /**
   * Get coaching insights
   */
  static async getInsights(params?: QueryParams): Promise<PaginatedResponse<CoachingInsight>> {
    const response = await apiClient.get<PaginatedResponse<CoachingInsight>>(
      `${this.BASE_PATH}/insights`,
      { params }
    );
    return response.data;
  }

  /**
   * Get a specific insight by ID
   */
  static async getInsight(insightId: string): Promise<CoachingInsight> {
    const response = await apiClient.get<CoachingInsight>(
      `${this.BASE_PATH}/insights/${insightId}`
    );
    return response.data;
  }

  /**
   * Get coaching goals
   */
  static async getGoals(params?: QueryParams): Promise<PaginatedResponse<CoachingGoal>> {
    const response = await apiClient.get<PaginatedResponse<CoachingGoal>>(
      `${this.BASE_PATH}/goals`,
      { params }
    );
    return response.data;
  }

  /**
   * Create a new coaching goal
   */
  static async createGoal(goalData: CreateGoalRequest): Promise<CoachingGoal> {
    const response = await apiClient.post<CoachingGoal>(`${this.BASE_PATH}/goals`, goalData);
    return response.data;
  }

  /**
   * Update a coaching goal
   */
  static async updateGoal(goalId: string, goalData: UpdateGoalRequest): Promise<CoachingGoal> {
    const response = await apiClient.patch<CoachingGoal>(
      `${this.BASE_PATH}/goals/${goalId}`,
      goalData
    );
    return response.data;
  }

  /**
   * Delete a coaching goal
   */
  static async deleteGoal(goalId: string): Promise<void> {
    await apiClient.delete(`${this.BASE_PATH}/goals/${goalId}`);
  }

  /**
   * Get slip detections
   */
  static async getSlipDetections(params?: QueryParams & {
    unresolved_only?: boolean;
    severity?: string;
  }): Promise<PaginatedResponse<SlipDetection>> {
    const response = await apiClient.get<PaginatedResponse<SlipDetection>>(
      `${this.BASE_PATH}/slips`,
      { params }
    );
    return response.data;
  }

  /**
   * Resolve a slip detection
   */
  static async resolveSlip(slipId: string, resolution: ResolveSlipRequest): Promise<SlipDetection> {
    const response = await apiClient.patch<SlipDetection>(
      `${this.BASE_PATH}/slips/${slipId}/resolve`,
      resolution
    );
    return response.data;
  }

  /**
   * Request personalized coaching advice
   */
  static async getPersonalizedAdvice(context: {
    topic: 'debt_strategy' | 'budgeting' | 'motivation' | 'goal_setting';
    current_situation: string;
    specific_question?: string;
  }): Promise<{
    advice: string;
    action_items: string[];
    resources: Array<{
      title: string;
      url: string;
      type: 'article' | 'video' | 'tool';
    }>;
    follow_up_questions: string[];
  }> {
    const response = await apiClient.post(`${this.BASE_PATH}/advice`, context);
    return response.data;
  }

  /**
   * Get motivational content
   */
  static async getMotivationalContent(): Promise<{
    quote: string;
    tip: string;
    success_story?: string;
    milestone_celebration?: string;
  }> {
    const response = await apiClient.get(`${this.BASE_PATH}/motivation`);
    return response.data;
  }

  /**
   * Generate coaching report
   */
  static async generateReport(period: '7d' | '30d' | '90d' = '30d'): Promise<{
    summary: {
      goals_achieved: number;
      nudges_acted_on: number;
      insights_generated: number;
      progress_score: number;
    };
    achievements: string[];
    areas_for_improvement: string[];
    recommendations: string[];
    next_steps: string[];
  }> {
    const response = await apiClient.get(`${this.BASE_PATH}/report`, {
      params: { period },
    });
    return response.data;
  }

  /**
   * Update coaching preferences
   */
  static async updatePreferences(preferences: {
    nudge_frequency: 'daily' | 'weekly' | 'monthly';
    nudge_types: string[];
    coaching_style: 'encouraging' | 'direct' | 'analytical';
    reminder_time?: string;
  }): Promise<void> {
    await apiClient.patch(`${this.BASE_PATH}/preferences`, preferences);
  }

  /**
   * Get coaching preferences
   */
  static async getPreferences(): Promise<{
    nudge_frequency: string;
    nudge_types: string[];
    coaching_style: string;
    reminder_time?: string;
  }> {
    const response = await apiClient.get(`${this.BASE_PATH}/preferences`);
    return response.data;
  }

  /**
   * Request immediate coaching intervention
   */
  static async requestIntervention(situation: {
    type: 'financial_stress' | 'motivation_loss' | 'strategy_confusion' | 'emergency';
    description: string;
    urgency: 'low' | 'medium' | 'high' | 'critical';
  }): Promise<{
    immediate_advice: string;
    action_plan: string[];
    resources: string[];
    follow_up_scheduled: boolean;
  }> {
    const response = await apiClient.post(`${this.BASE_PATH}/intervention`, situation);
    return response.data;
  }
}

export default CoachingService;
