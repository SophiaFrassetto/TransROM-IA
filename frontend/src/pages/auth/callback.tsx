import { useEffect } from 'react';
import { useRouter } from 'next/router';
import { useAuth } from '../../contexts/AuthContext';
import { Box, CircularProgress, Typography } from '@mui/material';

export default function AuthCallback() {
  const router = useRouter();
  const { login } = useAuth();

  useEffect(() => {
    const { code, error } = router.query;

    if (error) {
      console.error('Google OAuth error:', error);
      router.push('/login?error=google_auth_failed');
      return;
    }

    if (code) {
      handleGoogleCallback(code as string);
    }
  }, [router.query]);

  const handleGoogleCallback = async (code: string) => {
    try {
      const baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${baseUrl}/api/v1/auth/google/token?code=${code}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        console.error('Authentication error:', errorData);
        throw new Error(errorData.detail || 'Failed to authenticate with Google');
      }

      const data = await response.json();
      await login({
        access_token: data.access_token,
        refresh_token: data.refresh_token
      });
      router.push('/');
    } catch (error) {
      console.error('Authentication error:', error);
      router.push('/login?error=auth_failed');
    }
  };

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        height: '100vh',
        gap: 2,
      }}
    >
      <CircularProgress />
      <Typography variant="h6" textAlign="center">
        Processing authentication...
      </Typography>
      <Typography variant="body2" color="text.secondary" textAlign="center">
        Please wait while we complete your sign-in
      </Typography>
    </Box>
  );
} 