/**
 * Authentication service for handling API calls related to authentication
 */

import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
}

export interface User {
  email: string;
  name: string;
  picture?: string;
  is_active: boolean;
  is_superuser: boolean;
}

/**
 * Retrieves the Google OAuth URL from the backend
 * @returns {Promise<string>} The Google OAuth URL
 * @throws {Error} If the request fails
 */
export async function getGoogleAuthUrl(): Promise<string> {
  try {
    const response = await axios.get(`${API_URL}/api/v1/auth/google/authorize`);
    return response.data.authorization_url;
  } catch (error) {
    console.error('Error getting Google auth URL:', error);
    throw new Error('Failed to get Google authorization URL');
  }
}

/**
 * Exchanges the Google authorization code for access and refresh tokens
 * @param {string} code - The authorization code from Google
 * @returns {Promise<{ tokens: AuthTokens; user: User }>} Object containing tokens and user data
 * @throws {Error} If the token exchange fails
 */
export async function exchangeGoogleCode(code: string): Promise<{ tokens: AuthTokens; user: User }> {
  try {
    const response = await axios.post(`${API_URL}/api/v1/auth/google/callback`, { code });
    return {
      tokens: {
        access_token: response.data.access_token,
        refresh_token: response.data.refresh_token
      },
      user: response.data.user
    };
  } catch (error) {
    console.error('Error exchanging Google code:', error);
    throw new Error('Failed to exchange Google authorization code');
  }
}

/**
 * Refreshes the access token using a refresh token
 * @param {string} refreshToken - The refresh token
 * @returns {Promise<AuthTokens>} Object containing new access and refresh tokens
 * @throws {Error} If the token refresh fails
 */
export async function refreshAccessToken(refreshToken: string): Promise<AuthTokens> {
  try {
    const response = await axios.post(`${API_URL}/api/v1/auth/refresh`, {
      refresh_token: refreshToken
    });
    return response.data;
  } catch (error) {
    console.error('Error refreshing token:', error);
    throw new Error('Failed to refresh access token');
  }
}

/**
 * Logs out the user by invalidating their refresh token
 * @param {string} refreshToken - The refresh token to invalidate
 * @returns {Promise<void>}
 * @throws {Error} If the logout request fails
 */
export async function logout(refreshToken: string): Promise<void> {
  try {
    await axios.post(`${API_URL}/api/v1/auth/logout`, {
      refresh_token: refreshToken
    });
  } catch (error) {
    console.error('Error during logout:', error);
    throw new Error('Failed to logout');
  }
}

/**
 * Gets the current user's information
 * @param {string} accessToken - The access token
 * @returns {Promise<User>} The user's information
 * @throws {Error} If the request fails
 */
export async function getCurrentUser(accessToken: string): Promise<User> {
  try {
    const response = await axios.get(`${API_URL}/api/v1/users/me`, {
      headers: {
        Authorization: `Bearer ${accessToken}`
      }
    });
    return response.data;
  } catch (error) {
    console.error('Error getting current user:', error);
    throw new Error('Failed to get current user information');
  }
}

/**
 * Updates the current user's profile information
 * @param {string} accessToken - The access token
 * @param {Partial<User>} userData - The user data to update
 * @returns {Promise<User>} The updated user information
 * @throws {Error} If the update request fails
 */
export async function updateUserProfile(
  accessToken: string,
  userData: Partial<User>
): Promise<User> {
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
    return response.data;
  } catch (error) {
    console.error('Error updating user profile:', error);
    throw new Error('Failed to update user profile');
  }
} 