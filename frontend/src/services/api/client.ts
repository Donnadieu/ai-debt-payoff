import axios from 'axios';
import type { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';

export interface ApiConfig {
  baseURL: string;
  timeout: number;
  retries: number;
  retryDelay: number;
}

const defaultConfig: ApiConfig = {
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 10000,
  retries: 3,
  retryDelay: 1000,
};

class ApiClient {
  private client: AxiosInstance;
  private config: ApiConfig;

  constructor(config: Partial<ApiConfig> = {}) {
    this.config = { ...defaultConfig, ...config };
    this.client = this.createClient();
    this.setupInterceptors();
  }

  private createClient(): AxiosInstance {
    return axios.create({
      baseURL: this.config.baseURL,
      timeout: this.config.timeout,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  private setupInterceptors(): void {
    // Request interceptor for auth token
    this.client.interceptors.request.use(
      (config) => {
        const token = this.getAuthToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        
        // Add request logging in development
        if (import.meta.env.DEV) {
          console.log(`[API Request] ${config.method?.toUpperCase()} ${config.url}`, {
            params: config.params,
            data: config.data,
          });
        }
        
        return config;
      },
      (error) => {
        console.error('[API Request Error]', error);
        return Promise.reject(error);
      }
    );

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => {
        // Log successful responses in development
        if (import.meta.env.DEV) {
          console.log(`[API Response] ${response.status} ${response.config.url}`, response.data);
        }
        return response;
      },
      async (error) => {
        const originalRequest = error.config;

        // Handle 401 errors with token refresh
        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;
          
          try {
            await this.refreshAuthToken();
            const token = this.getAuthToken();
            if (token) {
              originalRequest.headers.Authorization = `Bearer ${token}`;
              return this.client(originalRequest);
            }
          } catch (refreshError) {
            this.handleAuthFailure();
            return Promise.reject(refreshError);
          }
        }

        // Retry logic for network errors
        if (this.shouldRetry(error) && !originalRequest._retryCount) {
          originalRequest._retryCount = 0;
        }

        if (originalRequest._retryCount < this.config.retries) {
          originalRequest._retryCount++;
          await this.delay(this.config.retryDelay * originalRequest._retryCount);
          return this.client(originalRequest);
        }

        console.error('[API Response Error]', error.response?.data || error.message);
        return Promise.reject(error);
      }
    );
  }

  private getAuthToken(): string | null {
    return localStorage.getItem('access_token');
  }

  private async refreshAuthToken(): Promise<void> {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    const response = await axios.post(`${this.config.baseURL}/auth/refresh`, {
      refresh_token: refreshToken,
    });

    const { access_token, refresh_token: newRefreshToken } = response.data;
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', newRefreshToken);
  }

  private handleAuthFailure(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.dispatchEvent(new CustomEvent('auth:logout'));
  }

  private shouldRetry(error: any): boolean {
    return (
      !error.response ||
      error.code === 'NETWORK_ERROR' ||
      error.code === 'TIMEOUT' ||
      (error.response.status >= 500 && error.response.status < 600)
    );
  }

  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  // Public API methods
  public get<T = any>(url: string, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> {
    return this.client.get(url, config);
  }

  public post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> {
    return this.client.post(url, data, config);
  }

  public put<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> {
    return this.client.put(url, data, config);
  }

  public patch<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> {
    return this.client.patch(url, data, config);
  }

  public delete<T = any>(url: string, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> {
    return this.client.delete(url, config);
  }

  public setAuthToken(token: string): void {
    localStorage.setItem('access_token', token);
  }

  public clearAuthToken(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }
}

// Create and export singleton instance
export const apiClient = new ApiClient();
export default apiClient;
