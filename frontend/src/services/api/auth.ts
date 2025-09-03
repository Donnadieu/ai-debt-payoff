import { apiClient } from './client';
import { LoginRequest, RegisterRequest, AuthResponse, RefreshTokenRequest } from '../../types/auth';

export class AuthService {
  private static readonly TOKEN_KEY = 'access_token';
  private static readonly REFRESH_TOKEN_KEY = 'refresh_token';
  private static readonly USER_KEY = 'user';

  /**
   * Login user with email and password
   */
  static async login(credentials: LoginRequest): Promise<AuthResponse> {
    const response = await apiClient.post<AuthResponse>('/auth/login', credentials);
    const authData = response.data;
    
    this.storeAuthData(authData);
    return authData;
  }

  /**
   * Register new user
   */
  static async register(userData: RegisterRequest): Promise<AuthResponse> {
    const response = await apiClient.post<AuthResponse>('/auth/register', userData);
    const authData = response.data;
    
    this.storeAuthData(authData);
    return authData;
  }

  /**
   * Refresh authentication token
   */
  static async refreshToken(): Promise<AuthResponse> {
    const refreshToken = this.getRefreshToken();
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    const response = await apiClient.post<AuthResponse>('/auth/refresh', {
      refresh_token: refreshToken,
    } as RefreshTokenRequest);
    
    const authData = response.data;
    this.storeAuthData(authData);
    return authData;
  }

  /**
   * Logout user and clear stored data
   */
  static async logout(): Promise<void> {
    try {
      // Call logout endpoint if token exists
      const token = this.getAccessToken();
      if (token) {
        await apiClient.post('/auth/logout');
      }
    } catch (error) {
      // Continue with logout even if API call fails
      console.warn('Logout API call failed:', error);
    } finally {
      this.clearAuthData();
    }
  }

  /**
   * Get current user profile
   */
  static async getCurrentUser() {
    const response = await apiClient.get('/auth/me');
    const user = response.data;
    
    // Update stored user data
    localStorage.setItem(this.USER_KEY, JSON.stringify(user));
    return user;
  }

  /**
   * Check if user is authenticated
   */
  static isAuthenticated(): boolean {
    const token = this.getAccessToken();
    if (!token) return false;

    try {
      // Basic token expiration check (if JWT)
      const payload = JSON.parse(atob(token.split('.')[1]));
      const currentTime = Date.now() / 1000;
      return payload.exp > currentTime;
    } catch {
      // If token parsing fails, consider it invalid
      return false;
    }
  }

  /**
   * Get stored access token
   */
  static getAccessToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
  }

  /**
   * Get stored refresh token
   */
  static getRefreshToken(): string | null {
    return localStorage.getItem(this.REFRESH_TOKEN_KEY);
  }

  /**
   * Get stored user data
   */
  static getStoredUser() {
    const userData = localStorage.getItem(this.USER_KEY);
    return userData ? JSON.parse(userData) : null;
  }

  /**
   * Store authentication data
   */
  private static storeAuthData(authData: AuthResponse): void {
    localStorage.setItem(this.TOKEN_KEY, authData.access_token);
    localStorage.setItem(this.REFRESH_TOKEN_KEY, authData.refresh_token);
    localStorage.setItem(this.USER_KEY, JSON.stringify(authData.user));
    
    // Set token in API client
    apiClient.setAuthToken(authData.access_token);
  }

  /**
   * Clear all authentication data
   */
  private static clearAuthData(): void {
    localStorage.removeItem(this.TOKEN_KEY);
    localStorage.removeItem(this.REFRESH_TOKEN_KEY);
    localStorage.removeItem(this.USER_KEY);
    
    // Clear token from API client
    apiClient.clearAuthToken();
  }

  /**
   * Initialize auth state on app startup
   */
  static initializeAuth(): boolean {
    const token = this.getAccessToken();
    if (token && this.isAuthenticated()) {
      apiClient.setAuthToken(token);
      return true;
    } else {
      this.clearAuthData();
      return false;
    }
  }
}

export default AuthService;
