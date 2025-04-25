import { useEffect } from 'react';
import {
  Box,
  Container,
  Typography,
  Paper,
  Avatar,
  Grid,
  Divider,
} from '@mui/material';
import { useAuth } from '../contexts/AuthContext';
import { useRouter } from 'next/router';
import { ProtectedRoute } from '../components/ProtectedRoute';

export default function Settings() {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !user) {
      router.push('/login');
    }
  }, [user, loading, router]);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
        <Typography>Loading...</Typography>
      </Box>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <ProtectedRoute>
      <Container maxWidth="md">
        <Typography variant="h4" component="h1" gutterBottom>
          Settings
        </Typography>
        <Paper elevation={3} sx={{ p: 4, mt: 4 }}>
          <Grid container spacing={4}>
            <Grid item xs={12} md={4} sx={{ display: 'flex', justifyContent: 'center' }}>
              <Avatar
                src={user.picture || undefined}
                alt={user.name || user.email}
                sx={{
                  width: 150,
                  height: 150,
                  border: '4px solid #fff',
                  boxShadow: '0 0 10px rgba(0,0,0,0.2)',
                }}
              >
                {!user.picture && (user.name?.[0] || user.email[0]).toUpperCase()}
              </Avatar>
            </Grid>
            <Grid item xs={12} md={8}>
              <Typography variant="h5" gutterBottom>
                Profile Information
              </Typography>
              <Divider sx={{ mb: 2 }} />
              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="text.secondary">
                  Name
                </Typography>
                <Typography variant="body1">{user.name || 'Not provided'}</Typography>
              </Box>
              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="text.secondary">
                  Email
                </Typography>
                <Typography variant="body1">{user.email}</Typography>
              </Box>
              <Box>
                <Typography variant="subtitle2" color="text.secondary">
                  Account Type
                </Typography>
                <Typography variant="body1">
                  {user.is_superuser ? 'Administrator' : 'User'}
                </Typography>
              </Box>
            </Grid>
          </Grid>
        </Paper>
      </Container>
    </ProtectedRoute>
  );
} 