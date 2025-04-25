import { useState } from 'react';
import { useRouter } from 'next/router';
import { useAuth } from '../contexts/AuthContext';
import { getGoogleAuthUrl, exchangeGoogleCode } from '../services/auth';

interface UseGoogleAuthReturn {
    isLoading: boolean;
    error: string | null;
    initiateGoogleLogin: () => Promise<void>;
    handleGoogleCallback: (code: string) => Promise<void>;
}

/**
 * Custom hook to handle Google OAuth authentication flow
 * @returns {UseGoogleAuthReturn} Object containing loading state, error state, and auth methods
 * @example
 * ```tsx
 * function LoginPage() {
 *   const { isLoading, error, initiateGoogleLogin } = useGoogleAuth();
 *   return (
 *     <button onClick={initiateGoogleLogin} disabled={isLoading}>
 *       {isLoading ? 'Loading...' : 'Login with Google'}
 *     </button>
 *   );
 * }
 * ```
 */
export function useGoogleAuth(): UseGoogleAuthReturn {
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const { login } = useAuth();
    const router = useRouter();

    const initiateGoogleLogin = async () => {
        try {
            setIsLoading(true);
            setError(null);
            const authUrl = await getGoogleAuthUrl();
            window.location.href = authUrl;
        } catch (err) {
            setError('Failed to initiate Google login');
            console.error('Google login error:', err);
        } finally {
            setIsLoading(false);
        }
    };

    const handleGoogleCallback = async (code: string) => {
        try {
            setIsLoading(true);
            setError(null);
            const tokens = await exchangeGoogleCode(code);
            login(tokens);
            await router.push('/'); // Redirect to home page after successful login
        } catch (err) {
            setError('Failed to complete Google authentication');
            console.error('Google callback error:', err);
            await router.push('/auth/login'); // Redirect back to login page on error
        } finally {
            setIsLoading(false);
        }
    };

    return {
        isLoading,
        error,
        initiateGoogleLogin,
        handleGoogleCallback
    };
} 