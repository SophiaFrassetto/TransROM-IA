import React, { createContext, useCallback, useContext, useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { config } from '@/config';
import { api } from '@/services/api';
import { User } from '@/types/user';
import * as authService from '@/services/auth';

interface AuthContextData {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  signIn: (accessToken: string) => Promise<void>;
  signOut: () => void;
}

export const AuthContext = createContext<AuthContextData>({} as AuthContextData);

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
export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  const signIn = useCallback(async (accessToken: string) => {
    try {
      localStorage.setItem(config.auth.accessTokenKey, accessToken);
      api.setAuthToken(accessToken);

      const response = await authService.getCurrentUser(accessToken);
      if (response.error) {
        throw new Error(response.error);
      }
      setUser(response.data);
    } catch (error) {
      console.error('Error during sign in:', error);
      signOut();
      throw error;
    }
  }, []);

  const signOut = useCallback(() => {
    localStorage.removeItem(config.auth.accessTokenKey);
    setUser(null);
    api.clearAuthToken();
    router.push('/auth/login');
  }, [router]);

  useEffect(() => {
    const initializeAuth = async () => {
      try {
        const storedToken = localStorage.getItem(config.auth.accessTokenKey);

        if (storedToken) {
          api.setAuthToken(storedToken);

          try {
            const response = await authService.getCurrentUser(storedToken);
            if (response.error) {
              throw new Error(response.error);
            }
            setUser(response.data);
          } catch (error) {
            console.error('Error getting user info:', error);
            signOut();
          }
        }
      } catch (error) {
        console.error('Error initializing auth:', error);
        signOut();
      } finally {
        setIsLoading(false);
      }
    };

    initializeAuth();
  }, [signOut]);

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        isLoading,
        signIn,
        signOut,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

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
export function useAuth(): AuthContextData {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
} 