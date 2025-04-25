import { useEffect } from 'react';
import { useRouter } from 'next/router';
import { useAuth } from '../../contexts/AuthContext';
import { Box, CircularProgress, Typography } from '@mui/material';

export default function AuthCallback() {
  const router = useRouter();
  const { login } = useAuth();

  useEffect(() => {
    const { code } = router.query;

    if (code) {
      handleGoogleCallback(code as string);
    }
  }, [router.query]);

  const handleGoogleCallback = async (code: string) => {
    try {
      const response = await fetch(`http://localhost:8000/auth/google/token?code=${code}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        }
      });

      if (!response.ok) {
        throw new Error('Failed to authenticate with Google');
      }

      const data = await response.json();
      login(data.access_token);
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
      }}
    >
      <CircularProgress />
      <Typography sx={{ mt: 2 }}>
        Processing authentication...
      </Typography>
    </Box>
  );
} 