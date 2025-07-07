/**
 * Authentication service for handling API calls related to authentication
 */

import axios from 'axios';
import { User } from '@/types/user';
import { ApiResponse } from '@/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface AuthTokens {
  access_token: string;
  token_type: string;
}

/**
 * Retrieves the Google OAuth URL from the backend
 * @returns {Promise<ApiResponse<{ url: string }>>} The Google OAuth URL
 */
export async function getGoogleAuthUrl(): Promise<ApiResponse<{ url: string }>> {
  try {
    const response = await axios.get(`${API_URL}/api/v1/auth/google/url`);
    return {
      data: { url: response.data.url },
      status: response.status,
      message: 'Successfully retrieved Google authorization URL'
    };
  } catch (error: any) {
    return {
      data: undefined as unknown as { url: string },
      status: error.response?.status || 500,
      message: 'Failed to get Google authorization URL',
      error: error.response?.data?.error || error.message
    };
  }
}

/**
 * Exchanges the Google authorization code for access and refresh tokens
 * @param {string} code - The authorization code from Google
 * @returns {Promise<ApiResponse<AuthTokens>>} Object containing tokens
 */
export async function exchangeGoogleCode(code: string): Promise<ApiResponse<AuthTokens>> {
  try {
    const response = await axios.post(`${API_URL}/api/v1/auth/google/token`, { code });
    return {
      data: {
        access_token: response.data.access_token,
        token_type: response.data.token_type
      },
      status: response.status,
      message: 'Successfully authenticated with Google'
    };
  } catch (error: any) {
    return {
      data: undefined as unknown as AuthTokens,
      status: error.response?.status || 500,
      message: 'Failed to exchange Google authorization code',
      error: error.response?.data?.error || error.message
    };
  }
}

/**
 * Refreshes the access token using a refresh token
 * @param {string} refreshToken - The refresh token
 * @returns {Promise<ApiResponse<AuthTokens>>} Object containing new access and refresh tokens
 */
export async function refreshAccessToken(refreshToken: string): Promise<ApiResponse<AuthTokens>> {
  try {
    const response = await axios.post(`${API_URL}/api/v1/auth/refresh`, {
      refresh_token: refreshToken
    });
    return {
      data: response.data,
      status: response.status,
      message: 'Successfully refreshed access token'
    };
  } catch (error: any) {
    return {
      data: null,
      status: error.response?.status || 500,
      message: 'Failed to refresh access token',
      error: error.response?.data?.error || error.message
    };
  }
}

/**
 * Logs out the user by invalidating their refresh token
 * @returns {Promise<ApiResponse<void>>}
 */
export async function logout(): Promise<ApiResponse<void>> {
  try {
    const response = await axios.post(`${API_URL}/api/v1/auth/logout`);
    return {
      data: undefined,
      status: response.status,
      message: 'Successfully logged out'
    };
  } catch (error: any) {
    return {
      data: undefined,
      status: error.response?.status || 500,
      message: 'Failed to logout',
      error: error.response?.data?.error || error.message
    };
  }
}

/**
 * Gets the current user's information
 * @param {string} accessToken - The access token
 * @returns {Promise<ApiResponse<User>>} The user's information
 */
export async function getCurrentUser(accessToken: string): Promise<ApiResponse<User>> {
  try {
    const response = await axios.get(`${API_URL}/api/v1/users/me`, {
      headers: {
        Authorization: `Bearer ${accessToken}`
      }
    });
    return {
      data: response.data,
      status: response.status,
      message: 'Successfully retrieved user information'
    };
  } catch (error: any) {
    return {
      data: undefined as unknown as User,
      status: error.response?.status || 500,
      message: 'Failed to get current user information',
      error: error.response?.data?.error || error.message
    };
  }
}

/**
 * Updates the current user's profile information
 * @param {string} accessToken - The access token
 * @param {Partial<User>} userData - The user data to update
 * @returns {Promise<ApiResponse<User>>} The updated user information
 */
export async function updateUserProfile(
  accessToken: string,
  userData: Partial<User>
): Promise<ApiResponse<User>> {
  try {
    const response = await axios.patch(
      `${API_URL}/api/v1/users/me`,
      userData,
      {
        headers: {
          Authorization: `Bearer ${accessToken}`
        }
      }
    );
    return {
      data: response.data,
      status: response.status,
      message: 'Successfully updated user profile'
    };
  } catch (error: any) {
    return {
      data: undefined as unknown as User,
      status: error.response?.status || 500,
      message: 'Failed to update user profile',
      error: error.response?.data?.error || error.message
    };
  }
}
