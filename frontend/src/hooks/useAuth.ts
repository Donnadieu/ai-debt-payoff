import { useState, useEffect, useCallback } from 'react';
import { AuthService } from '../services/api/auth';
import { AuthState, LoginRequest, RegisterRequest, User } from '../types/auth';

export const useAuth = () => {
  const [state, setState] = useState<AuthState>({
    user: null,
    isAuthenticated: false,
    isLoading: true,
    error: null,
  });

  // Initialize auth state on mount
  useEffect(() => {
    const initializeAuth = async () => {
      try {
        const isAuthenticated = AuthService.initializeAuth();
        
        if (isAuthenticated) {
          const user = AuthService.getStoredUser();
          setState({
            user,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          });
          
          // Optionally refresh user data from server
          try {
            const currentUser = await AuthService.getCurrentUser();
            setState(prev => ({ ...prev, user: currentUser }));
          } catch (error) {
            // If fetching current user fails, keep stored user data
            console.warn('Failed to fetch current user:', error);
          }
        } else {
          setState({
            user: null,
            isAuthenticated: false,
            isLoading: false,
            error: null,
          });
        }
      } catch (error) {
        setState({
          user: null,
          isAuthenticated: false,
          isLoading: false,
          error: error instanceof Error ? error.message : 'Authentication initialization failed',
        });
      }
    };

    initializeAuth();

    // Listen for auth events
    const handleAuthLogout = () => {
      setState({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
      });
    };

    window.addEventListener('auth:logout', handleAuthLogout);
    return () => window.removeEventListener('auth:logout', handleAuthLogout);
  }, []);

  const login = useCallback(async (credentials: LoginRequest) => {
    setState(prev => ({ ...prev, isLoading: true, error: null }));
    
    try {
      const authResponse = await AuthService.login(credentials);
      setState({
        user: authResponse.user,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      });
    } catch (error) {
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: error instanceof Error ? error.message : 'Login failed',
      }));
      throw error;
    }
  }, []);

  const register = useCallback(async (userData: RegisterRequest) => {
    setState(prev => ({ ...prev, isLoading: true, error: null }));
    
    try {
      const authResponse = await AuthService.register(userData);
      setState({
        user: authResponse.user,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      });
    } catch (error) {
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: error instanceof Error ? error.message : 'Registration failed',
      }));
      throw error;
    }
  }, []);

  const logout = useCallback(async () => {
    setState(prev => ({ ...prev, isLoading: true }));
    
    try {
      await AuthService.logout();
      setState({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
      });
    } catch (error) {
      // Even if logout API call fails, clear local state
      setState({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
      });
      console.warn('Logout error:', error);
    }
  }, []);

  const refreshToken = useCallback(async () => {
    try {
      const authResponse = await AuthService.refreshToken();
      setState(prev => ({
        ...prev,
        user: authResponse.user,
        isAuthenticated: true,
        error: null,
      }));
    } catch (error) {
      // If refresh fails, logout user
      setState({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: error instanceof Error ? error.message : 'Token refresh failed',
      });
      throw error;
    }
  }, []);

  const clearError = useCallback(() => {
    setState(prev => ({ ...prev, error: null }));
  }, []);

  return {
    ...state,
    login,
    register,
    logout,
    refreshToken,
    clearError,
  };
};
