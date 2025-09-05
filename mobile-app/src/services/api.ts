// API service for connecting to the debt payoff backend

const API_BASE_URL = 'http://localhost:5000'; // This will be updated for production

export class ApiService {
  private static baseUrl = API_BASE_URL;

  static async get<T>(endpoint: string): Promise<T> {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  static async post<T>(endpoint: string, data: any): Promise<T> {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  static async put<T>(endpoint: string, data: any): Promise<T> {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  static async delete<T>(endpoint: string): Promise<T> {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  // Health check endpoint
  static async checkHealth() {
    return this.get('/health');
  }

  // Debt management endpoints
  static async getDebts() {
    return this.get('/api/v1/debts');
  }

  static async createDebt(debtData: any) {
    return this.post('/api/v1/debts', debtData);
  }

  // Payoff planning endpoints
  static async calculatePayoffPlan(planData: any) {
    return this.post('/plan', planData);
  }

  // Nudge endpoints
  static async generateNudge(nudgeData: any) {
    return this.post('/nudge/generate', nudgeData);
  }
}