import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Grid,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Switch,
  FormControlLabel,
  Button,
  Divider,
  Avatar,
} from '@mui/material';
import Layout from '@/components/layout/Layout';

const SettingsPage: React.FC = () => {
  const [language, setLanguage] = useState('en');
  const [notifications, setNotifications] = useState(true);
  const [darkMode, setDarkMode] = useState(false);

  return (
    <Layout>
      <Box sx={{ flexGrow: 1 }}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Paper sx={{ p: 4, textAlign: 'center' }}>
              <Typography variant="h3" component="h1" gutterBottom>
                Settings
              </Typography>
              <Typography variant="body1" paragraph>
                Customize your TransROM-IA experience
              </Typography>
            </Paper>
          </Grid>

          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h5" gutterBottom>
                Profile Settings
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                <Avatar
                  sx={{
                    width: 64,
                    height: 64,
                    bgcolor: 'secondary.main',
                    mr: 2,
                  }}
                >
                  U
                </Avatar>
                <Button variant="outlined" color="primary">
                  Change Avatar
                </Button>
              </Box>
              <TextField
                fullWidth
                label="Username"
                defaultValue="User123"
                margin="normal"
              />
              <TextField
                fullWidth
                label="Email"
                defaultValue="user@example.com"
                margin="normal"
              />
              <Button
                variant="contained"
                color="primary"
                fullWidth
                sx={{ mt: 2 }}
              >
                Save Profile Changes
              </Button>
            </Paper>
          </Grid>

          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h5" gutterBottom>
                Preferences
              </Typography>
              <FormControl fullWidth margin="normal">
                <InputLabel>Default Language</InputLabel>
                <Select
                  value={language}
                  label="Default Language"
                  onChange={(e) => setLanguage(e.target.value)}
                >
                  <MenuItem value="en">English</MenuItem>
                  <MenuItem value="es">Spanish</MenuItem>
                  <MenuItem value="fr">French</MenuItem>
                  <MenuItem value="de">German</MenuItem>
                  <MenuItem value="it">Italian</MenuItem>
                  <MenuItem value="pt">Portuguese</MenuItem>
                  <MenuItem value="ja">Japanese</MenuItem>
                </Select>
              </FormControl>
              <FormControlLabel
                control={
                  <Switch
                    checked={notifications}
                    onChange={(e) => setNotifications(e.target.checked)}
                  />
                }
                label="Enable Notifications"
                sx={{ mt: 2 }}
              />
              <FormControlLabel
                control={
                  <Switch
                    checked={darkMode}
                    onChange={(e) => setDarkMode(e.target.checked)}
                  />
                }
                label="Dark Mode"
                sx={{ mt: 2 }}
              />
            </Paper>
          </Grid>

          <Grid item xs={12}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h5" gutterBottom>
                Account Settings
              </Typography>
              <Button
                variant="outlined"
                color="error"
                sx={{ mr: 2 }}
              >
                Delete Account
              </Button>
              <Button
                variant="outlined"
                color="primary"
              >
                Export Data
              </Button>
            </Paper>
          </Grid>
        </Grid>
      </Box>
    </Layout>
  );
};

export default SettingsPage; 