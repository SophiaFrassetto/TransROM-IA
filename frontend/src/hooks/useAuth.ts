/**
 * Custom hook for handling authentication state and operations
 */

import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/router';
import { api } from '@/services/api';
import { config } from '@/config';
import type { User } from '@/types';

interface LoginCredentials {
  email: string;
  password: string;
}

interface RegisterData extends LoginCredentials {
  username: string;
}

interface AuthResponse {
  token: string;
  refreshToken: string;
  user: User;
}

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  /**
   * Load user data from token
   */
  const loadUser = useCallback(async () => {
    try {
      const token = localStorage.getItem(config.auth.tokenKey);
      if (!token) {
        setLoading(false);
        return;
      }

      const response = await api.get<User>('/auth/me');
      if (response.status === 200 && response.data) {
        setUser(response.data);
      } else {
        localStorage.removeItem(config.auth.tokenKey);
        localStorage.removeItem(config.auth.refreshTokenKey);
      }
    } catch (error) {
      localStorage.removeItem(config.auth.tokenKey);
      localStorage.removeItem(config.auth.refreshTokenKey);
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * Initialize auth state
   */
  useEffect(() => {
    loadUser();
  }, [loadUser]);

  /**
   * Login user
   */
  const login = async (credentials: LoginCredentials) => {
    try {
      const response = await api.post<AuthResponse>('/auth/login', credentials);
      
      if (response.status === 200 && response.data) {
        const { token, refreshToken, user } = response.data;
        localStorage.setItem(config.auth.tokenKey, token);
        localStorage.setItem(config.auth.refreshTokenKey, refreshToken);
        setUser(user);
        return { success: true };
      }
      
      return {
        success: false,
        error: response.message || 'Login failed',
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.message || 'Login failed',
      };
    }
  };

  /**
   * Register new user
   */
  const register = async (data: RegisterData) => {
    try {
      const response = await api.post<AuthResponse>('/auth/register', data);
      
      if (response.status === 201 && response.data) {
        const { token, refreshToken, user } = response.data;
        localStorage.setItem(config.auth.tokenKey, token);
        localStorage.setItem(config.auth.refreshTokenKey, refreshToken);
        setUser(user);
        return { success: true };
      }
      
      return {
        success: false,
        error: response.message || 'Registration failed',
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.message || 'Registration failed',
      };
    }
  };

  /**
   * Logout user
   */
  const logout = useCallback(async () => {
    try {
      await api.post('/auth/logout');
    } finally {
      localStorage.removeItem(config.auth.tokenKey);
      localStorage.removeItem(config.auth.refreshTokenKey);
      setUser(null);
      router.push('/auth/login');
    }
  }, [router]);

  return {
    user,
    loading,
    isAuthenticated: !!user,
    login,
    register,
    logout,
  };
} 