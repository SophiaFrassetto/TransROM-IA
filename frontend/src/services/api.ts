/**
 * API service layer for handling HTTP requests
 */

import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse, AxiosError } from 'axios';
import { ApiResponse } from '@/types';
import { config } from '@/config';

// Define custom API interface extending AxiosInstance
interface CustomAPI extends AxiosInstance {
  setAuthToken: (token: string) => void;
  clearAuthToken: () => void;
  upload: (endpoint: string, formData: FormData, onProgress?: (progress: number) => void) => Promise<any>;
}

// Create axios instance with default config
const axiosInstance = axios.create({
  baseURL: config.api.baseUrl,
  timeout: config.api.timeout,
}) as CustomAPI;

// Add request interceptor for adding authorization token
axiosInstance.interceptors.request.use(
  (axiosConfig) => {
    const token = localStorage.getItem(config.auth.accessTokenKey);
    if (token) {
      axiosConfig.headers.Authorization = `Bearer ${token}`;
    }
    return axiosConfig;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor for handling errors
axiosInstance.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    if (error.response?.status === 401) {
      // Clear auth tokens and redirect to login
      localStorage.removeItem(config.auth.accessTokenKey);
      window.location.href = '/auth/login';
    }
    return Promise.reject(error);
  }
);

// Add custom methods to axios instance
axiosInstance.setAuthToken = (token: string) => {
  axiosInstance.defaults.headers.common.Authorization = `Bearer ${token}`;
};

axiosInstance.clearAuthToken = () => {
  delete axiosInstance.defaults.headers.common.Authorization;
};

axiosInstance.upload = async (endpoint: string, formData: FormData, onProgress?: (progress: number) => void) => {
  const response = await axiosInstance.post(endpoint, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress: (progressEvent) => {
      if (onProgress && progressEvent.total) {
        const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
        onProgress(progress);
      }
    },
  });
  return response;
};

export const api = axiosInstance;

/**
 * Generic function to handle API requests
 * @param requestFn - Function that returns a promise with the API request
 * @returns ApiResponse with data, status, message, and optional error
 */
async function handleRequest<T>(
  requestFn: () => Promise<AxiosResponse>
): Promise<ApiResponse<T>> {
  try {
    const response = await requestFn();
    return {
      data: response.data,
      status: response.status,
      message: 'Request successful'
    };
  } catch (error: any) {
    const errorResponse: ApiResponse<T> = {
      data: undefined as unknown as T,
      status: error.response?.status || 500,
      message: error.response?.data?.message || 'Request failed',
      error: error.response?.data?.error || error.message
    };
    return errorResponse;
  }
}

/**
 * GET request
 * @param endpoint - API endpoint
 * @param config - Axios request configuration
 */
export function get<T>(endpoint: string, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
  return handleRequest<T>(() => api.get(endpoint, config));
}

/**
 * POST request
 * @param endpoint - API endpoint
 * @param data - Request body
 * @param config - Axios request configuration
 */
export function post<T>(
  endpoint: string,
  data?: any,
  config?: AxiosRequestConfig
): Promise<ApiResponse<T>> {
  return handleRequest<T>(() => api.post(endpoint, data, config));
}

/**
 * PUT request
 * @param endpoint - API endpoint
 * @param data - Request body
 * @param config - Axios request configuration
 */
export function put<T>(
  endpoint: string,
  data?: any,
  config?: AxiosRequestConfig
): Promise<ApiResponse<T>> {
  return handleRequest<T>(() => api.put(endpoint, data, config));
}

/**
 * DELETE request
 * @param endpoint - API endpoint
 * @param config - Axios request configuration
 */
export function del<T>(endpoint: string, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
  return handleRequest<T>(() => api.delete(endpoint, config));
}

/**
 * PATCH request
 * @param endpoint - API endpoint
 * @param data - Request body
 * @param config - Axios request configuration
 */
export function patch<T>(
  endpoint: string,
  data?: any,
  config?: AxiosRequestConfig
): Promise<ApiResponse<T>> {
  return handleRequest<T>(() => api.patch(endpoint, data, config));
}

/**
 * File upload request
 * @param endpoint - API endpoint
 * @param file - File to upload
 * @param config - Axios request configuration
 */
export function upload<T>(
  endpoint: string,
  file: File,
  config?: AxiosRequestConfig
): Promise<ApiResponse<T>> {
  const formData = new FormData();
  formData.append('file', file);

  const uploadConfig: AxiosRequestConfig = {
    ...config,
    headers: {
      ...config?.headers,
      'Content-Type': 'multipart/form-data'
    }
  };

  return handleRequest<T>(() => api.post(endpoint, formData, uploadConfig));
} 