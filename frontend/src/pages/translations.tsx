import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  CardActions,
  LinearProgress,
  Chip,
  Tabs,
  Tab,
  Container,
  Tooltip,
} from '@mui/material';
import DownloadIcon from '@mui/icons-material/Download';
import TextFieldsIcon from '@mui/icons-material/TextFields';
import AudiotrackIcon from '@mui/icons-material/Audiotrack';
import ImageIcon from '@mui/icons-material/Image';
import Layout from '@/components/layout/Layout';
import { ProtectedRoute } from '../components/ProtectedRoute';

interface RomTranslation {
  id: string;
  name: string;
  consoleType: string;
  targetLanguage: string;
  status: 'queued' | 'processing' | 'completed' | 'failed';
  progress: number;
  date: string;
  estimatedTime?: string;
  options: {
    text: boolean;
    audio: boolean;
    image: boolean;
  };
}

// Mock data - replace with actual API calls
const mockTranslations: RomTranslation[] = [
  {
    id: '1',
    name: 'Pokemon Emerald.gba',
    consoleType: 'gba',
    targetLanguage: 'es',
    status: 'completed',
    progress: 100,
    date: '2023-05-15',
    estimatedTime: '45 minutes',
    options: {
      text: true,
      audio: false,
      image: false,
    },
  },
  {
    id: '2',
    name: 'Zelda - Minish Cap.gba',
    consoleType: 'gba',
    targetLanguage: 'fr',
    status: 'processing',
    progress: 45,
    date: '2023-05-16',
    estimatedTime: '1 hour',
    options: {
      text: true,
      audio: true,
      image: false,
    },
  },
  {
    id: '3',
    name: 'Super Mario World.sfc',
    consoleType: 'snes',
    targetLanguage: 'pt',
    status: 'queued',
    progress: 0,
    date: '2023-05-17',
    estimatedTime: '30 minutes',
    options: {
      text: true,
      audio: false,
      image: true,
    },
  },
  {
    id: '4',
    name: 'Final Fantasy VI.sfc',
    consoleType: 'snes',
    targetLanguage: 'de',
    status: 'completed',
    progress: 100,
    date: '2023-05-18',
    estimatedTime: '2 hours',
    options: {
      text: true,
      audio: true,
      image: true,
    },
  },
  {
    id: '5',
    name: 'Metroid Fusion.gba',
    consoleType: 'gba',
    targetLanguage: 'it',
    status: 'processing',
    progress: 75,
    date: '2023-05-19',
    estimatedTime: '1 hour',
    options: {
      text: true,
      audio: false,
      image: false,
    },
  },
  {
    id: '6',
    name: 'Chrono Trigger.sfc',
    consoleType: 'snes',
    targetLanguage: 'es',
    status: 'queued',
    progress: 0,
    date: '2023-05-20',
    estimatedTime: '1.5 hours',
    options: {
      text: true,
      audio: true,
      image: false,
    },
  },
  {
    id: '7',
    name: 'Castlevania - Aria of Sorrow.gba',
    consoleType: 'gba',
    targetLanguage: 'fr',
    status: 'completed',
    progress: 100,
    date: '2023-05-21',
    estimatedTime: '50 minutes',
    options: {
      text: true,
      audio: false,
      image: true,
    },
  },
  {
    id: '8',
    name: 'EarthBound.sfc',
    consoleType: 'snes',
    targetLanguage: 'pt',
    status: 'processing',
    progress: 30,
    date: '2023-05-22',
    estimatedTime: '2.5 hours',
    options: {
      text: true,
      audio: true,
      image: true,
    },
  },
];

const TranslationsPage: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const getStatusColor = (status: RomTranslation['status']) => {
    switch (status) {
      case 'completed':
        return 'success';
      case 'processing':
        return 'primary';
      case 'queued':
        return 'default';
      case 'failed':
        return 'error';
      default:
        return 'default';
    }
  };

  const filteredTranslations = mockTranslations.filter((translation) => {
    if (tabValue === 0) return true; // All
    if (tabValue === 1) return translation.status === 'queued';
    if (tabValue === 2) return translation.status === 'processing';
    if (tabValue === 3) return translation.status === 'completed';
    return true;
  });

  return (
    <ProtectedRoute>
      <Layout>
        <Box sx={{ 
          display: 'flex', 
          flexDirection: 'column',
          minHeight: '100vh',
        }}>
          <Container maxWidth="lg" sx={{ flex: 1, py: 4 }}>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Paper sx={{ p: 4, textAlign: 'center' }} className="retro-border">
                  <Typography variant="h3" component="h1" gutterBottom className="pixel-text">
                    Translations
                  </Typography>
                  <Typography variant="body1" paragraph className="pixel-text">
                    Track your ROM translations and download completed files
                  </Typography>
                </Paper>
              </Grid>

              <Grid item xs={12}>
                <Paper sx={{ p: 2 }} className="retro-border">
                  <Tabs
                    value={tabValue}
                    onChange={handleTabChange}
                    indicatorColor="primary"
                    textColor="primary"
                    centered
                  >
                    <Tab label="All" className="pixel-text" />
                    <Tab label="Queued" className="pixel-text" />
                    <Tab label="Processing" className="pixel-text" />
                    <Tab label="Completed" className="pixel-text" />
                  </Tabs>
                </Paper>
              </Grid>

              <Grid container spacing={3} sx={{ mt: 0 }}>
                {filteredTranslations.map((translation) => (
                  <Grid item xs={12} md={6} key={translation.id}>
                    <Card className="retro-border">
                      <CardContent>
                        <Typography variant="h6" gutterBottom className="pixel-text">
                          {translation.name}
                        </Typography>
                        <Box sx={{ display: 'flex', gap: 1, mb: 2, flexWrap: 'wrap', alignItems: 'center' }}>
                          <Chip
                            label={translation.consoleType.toUpperCase()}
                            size="small"
                            color="secondary"
                            className="pixel-text"
                          />
                          <Chip
                            label={translation.targetLanguage.toUpperCase()}
                            size="small"
                            className="pixel-text"
                          />
                          <Chip
                            label={translation.status}
                            size="small"
                            color={getStatusColor(translation.status)}
                            className="pixel-text"
                          />
                          <Box sx={{ display: 'flex', gap: 0.5, ml: 1 }}>
                            <Tooltip title="Text Translation">
                              <Box sx={{ 
                                display: 'flex', 
                                alignItems: 'center', 
                                justifyContent: 'center',
                                width: 24,
                                height: 24,
                                borderRadius: '50%',
                                bgcolor: translation.options.text ? 'primary.main' : 'action.disabledBackground',
                                color: translation.options.text ? 'primary.contrastText' : 'action.disabled',
                              }}>
                                <TextFieldsIcon sx={{ fontSize: 16 }} />
                              </Box>
                            </Tooltip>
                            <Tooltip title="Audio Dubbing">
                              <Box sx={{ 
                                display: 'flex', 
                                alignItems: 'center', 
                                justifyContent: 'center',
                                width: 24,
                                height: 24,
                                borderRadius: '50%',
                                bgcolor: translation.options.audio ? 'primary.main' : 'action.disabledBackground',
                                color: translation.options.audio ? 'primary.contrastText' : 'action.disabled',
                              }}>
                                <AudiotrackIcon sx={{ fontSize: 16 }} />
                              </Box>
                            </Tooltip>
                            <Tooltip title="Image Translation">
                              <Box sx={{ 
                                display: 'flex', 
                                alignItems: 'center', 
                                justifyContent: 'center',
                                width: 24,
                                height: 24,
                                borderRadius: '50%',
                                bgcolor: translation.options.image ? 'primary.main' : 'action.disabledBackground',
                                color: translation.options.image ? 'primary.contrastText' : 'action.disabled',
                              }}>
                                <ImageIcon sx={{ fontSize: 16 }} />
                              </Box>
                            </Tooltip>
                          </Box>
                          {translation.estimatedTime && (
                            <Chip
                              label={`Est. Time: ${translation.estimatedTime}`}
                              size="small"
                              variant="outlined"
                              className="pixel-text"
                            />
                          )}
                        </Box>
                        <Typography variant="body2" color="text.secondary" gutterBottom className="pixel-text">
                          Uploaded: {translation.date}
                        </Typography>
                        {translation.status === 'processing' && (
                          <Box sx={{ mt: 2 }}>
                            <LinearProgress
                              variant="determinate"
                              value={translation.progress}
                              sx={{ 
                                height: 8, 
                                borderRadius: 4,
                                backgroundColor: 'rgba(0,0,0,0.1)',
                                '& .MuiLinearProgress-bar': {
                                  borderRadius: 4,
                                }
                              }}
                            />
                            <Typography variant="body2" color="text.secondary" align="right" className="pixel-text">
                              {translation.progress}%
                            </Typography>
                          </Box>
                        )}
                      </CardContent>
                      <CardActions>
                        {translation.status === 'completed' ? (
                          <Button
                            variant="contained"
                            startIcon={<DownloadIcon />}
                            fullWidth
                            className="retro-button"
                          >
                            Download Translated ROM
                          </Button>
                        ) : (
                          <Button
                            variant="outlined"
                            disabled
                            fullWidth
                            className="retro-button"
                          >
                            {translation.status === 'processing'
                              ? 'Translation in Progress'
                              : 'Waiting in Queue'}
                          </Button>
                        )}
                      </CardActions>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            </Grid>
          </Container>
        </Box>
      </Layout>
    </ProtectedRoute>
  );
};

export default TranslationsPage; 