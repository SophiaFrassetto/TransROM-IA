import React, { createContext, useContext, useState, useEffect } from 'react';
import { refreshAccessToken, AuthTokens, logout, getCurrentUser, User } from '../services/auth';

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  accessToken: string | null;
  refreshToken: string | null;
  login: (tokens: AuthTokens) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

/**
 * Provider component that wraps the app and makes auth object available to any
 * child component that calls useAuth().
 * @param {object} props - Component props
 * @param {React.ReactNode} props.children - Child components
 * @returns {JSX.Element} AuthProvider component
 * @example
 * ```tsx
 * function App() {
 *   return (
 *     <AuthProvider>
 *       <YourApp />
 *     </AuthProvider>
 *   );
 * }
 * ```
 */
export function AuthProvider({ children }: { children: React.ReactNode }): JSX.Element {
  const [user, setUser] = useState<User | null>(null);
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [refreshToken, setRefreshToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Fetch user profile when access token changes
  useEffect(() => {
    const fetchUserProfile = async () => {
      if (!accessToken) {
        setUser(null);
        return;
      }

      try {
        const userData = await getCurrentUser(accessToken);
        setUser(userData);
      } catch (error) {
        console.error('Failed to fetch user profile:', error);
        // If we fail to fetch the user profile, we should probably log out
        handleLogout();
      }
    };

    fetchUserProfile();
  }, [accessToken]);

  useEffect(() => {
    // Check for stored tokens on mount
    const storedAccessToken = localStorage.getItem('accessToken');
    const storedRefreshToken = localStorage.getItem('refreshToken');
    
    if (storedAccessToken && storedRefreshToken) {
      setAccessToken(storedAccessToken);
      setRefreshToken(storedRefreshToken);
    }
    
    setIsLoading(false);
  }, []);

  // Set up automatic token refresh
  useEffect(() => {
    if (!refreshToken) return;

    const REFRESH_INTERVAL = 14 * 60 * 1000; // 14 minutes
    const refreshTokens = async () => {
      try {
        const tokens = await refreshAccessToken(refreshToken);
        setAccessToken(tokens.access_token);
        setRefreshToken(tokens.refresh_token);
        localStorage.setItem('accessToken', tokens.access_token);
        localStorage.setItem('refreshToken', tokens.refresh_token);
      } catch (error) {
        console.error('Failed to refresh token:', error);
        handleLogout();
      }
    };

    const intervalId = setInterval(refreshTokens, REFRESH_INTERVAL);
    return () => clearInterval(intervalId);
  }, [refreshToken]);

  const handleLogin = async (tokens: AuthTokens) => {
    setAccessToken(tokens.access_token);
    setRefreshToken(tokens.refresh_token);
    localStorage.setItem('accessToken', tokens.access_token);
    localStorage.setItem('refreshToken', tokens.refresh_token);
  };

  const handleLogout = async () => {
    try {
      if (refreshToken) {
        await logout(refreshToken);
      }
    } catch (error) {
      console.error('Error during logout:', error);
    } finally {
      setUser(null);
      setAccessToken(null);
      setRefreshToken(null);
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
    }
  };

  const value = {
    user,
    isAuthenticated: !!user,
    isLoading,
    accessToken,
    refreshToken,
    login: handleLogin,
    logout: handleLogout
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

/**
 * Hook for accessing the authentication context
 * @returns {AuthContextType} The authentication context
 * @throws {Error} If used outside of AuthProvider
 * @example
 * ```tsx
 * function MyComponent() {
 *   const { user, isAuthenticated, logout } = useAuth();
 *   
 *   if (isAuthenticated) {
 *     return <div>Welcome {user?.name}!</div>;
 *   }
 *   return <div>Please log in</div>;
 * }
 * ```
 */
export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
} 