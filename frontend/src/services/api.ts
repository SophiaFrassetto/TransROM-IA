/**
 * API service layer for handling HTTP requests
 */

import axios, { AxiosInstance, AxiosResponse } from 'axios';
import { config } from '@/config';
import type { ApiResponse } from '@/types';

/**
 * Create axios instance with default configuration
 */
const axiosInstance: AxiosInstance = axios.create({
  baseURL: config.api.baseUrl,
  timeout: config.api.timeout,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Request interceptor for API calls
 */
axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem(config.auth.tokenKey);
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

/**
 * Response interceptor for API calls
 */
axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refreshToken = localStorage.getItem(config.auth.refreshTokenKey);

      try {
        const response = await axiosInstance.post('/auth/refresh', { refreshToken });
        const { token } = response.data;
        localStorage.setItem(config.auth.tokenKey, token);
        originalRequest.headers.Authorization = `Bearer ${token}`;
        return axiosInstance(originalRequest);
      } catch (error) {
        localStorage.removeItem(config.auth.tokenKey);
        localStorage.removeItem(config.auth.refreshTokenKey);
        window.location.href = '/auth/login';
        return Promise.reject(error);
      }
    }

    return Promise.reject(error);
  }
);

/**
 * Generic API request handler
 */
const handleRequest = async <T>(
  request: Promise<AxiosResponse>
): Promise<ApiResponse<T>> => {
  try {
    const response = await request;
    return {
      data: response.data,
      status: response.status,
    };
  } catch (error: any) {
    return {
      data: null as T,
      status: error.response?.status || 500,
      message: error.response?.data?.message || 'An error occurred',
    };
  }
};

/**
 * API service methods
 */
export const api = {
  get: <T>(url: string, params?: object) =>
    handleRequest<T>(axiosInstance.get(url, { params })),

  post: <T>(url: string, data?: object) =>
    handleRequest<T>(axiosInstance.post(url, data)),

  put: <T>(url: string, data?: object) =>
    handleRequest<T>(axiosInstance.put(url, data)),

  delete: <T>(url: string) =>
    handleRequest<T>(axiosInstance.delete(url)),

  patch: <T>(url: string, data?: object) =>
    handleRequest<T>(axiosInstance.patch(url, data)),
}; 