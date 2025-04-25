import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  Grid,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  LinearProgress,
  Chip,
  Tabs,
  Tab,
  Container,
  Tooltip,
  Divider,
  Stack,
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

              <Grid item xs={12}>
                <Paper className="retro-border">
                  <List>
                    {filteredTranslations.map((translation, index) => (
                      <React.Fragment key={translation.id}>
                        {index > 0 && <Divider />}
                        <ListItem
                          sx={{
                            py: 3,
                            px: 4,
                            display: 'flex',
                            flexDirection: { xs: 'column', sm: 'row' },
                            alignItems: { xs: 'flex-start', sm: 'center' },
                            gap: 2,
                          }}
                        >
                          <Box sx={{ flex: 1, minWidth: 0 }}>
                            <Typography variant="h6" className="pixel-text" sx={{ mb: 1 }}>
                              {translation.name}
                            </Typography>
                            
                            <Stack direction="row" spacing={1} sx={{ mb: 2, flexWrap: 'wrap', gap: 1 }}>
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
                              {translation.estimatedTime && (
                                <Chip
                                  label={`Est. Time: ${translation.estimatedTime}`}
                                  size="small"
                                  variant="outlined"
                                  className="pixel-text"
                                />
                              )}
                            </Stack>

                            <Stack direction="row" spacing={2} alignItems="center" sx={{ mb: 2 }}>
                              <Tooltip title="Text Translation">
                                <Box sx={{ 
                                  display: 'flex', 
                                  alignItems: 'center', 
                                  gap: 1,
                                  color: translation.options.text ? 'primary.main' : 'text.disabled',
                                }}>
                                  <TextFieldsIcon fontSize="small" />
                                  <Typography variant="body2" className="pixel-text">Text</Typography>
                                </Box>
                              </Tooltip>
                              <Tooltip title="Audio Dubbing">
                                <Box sx={{ 
                                  display: 'flex', 
                                  alignItems: 'center', 
                                  gap: 1,
                                  color: translation.options.audio ? 'primary.main' : 'text.disabled',
                                }}>
                                  <AudiotrackIcon fontSize="small" />
                                  <Typography variant="body2" className="pixel-text">Audio</Typography>
                                </Box>
                              </Tooltip>
                              <Tooltip title="Image Translation">
                                <Box sx={{ 
                                  display: 'flex', 
                                  alignItems: 'center', 
                                  gap: 1,
                                  color: translation.options.image ? 'primary.main' : 'text.disabled',
                                }}>
                                  <ImageIcon fontSize="small" />
                                  <Typography variant="body2" className="pixel-text">Image</Typography>
                                </Box>
                              </Tooltip>
                            </Stack>

                            {translation.status === 'processing' && (
                              <Box sx={{ width: '100%' }}>
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
                                <Typography variant="body2" color="text.secondary" align="right" className="pixel-text" sx={{ mt: 0.5 }}>
                                  {translation.progress}%
                                </Typography>
                              </Box>
                            )}
                          </Box>

                          <Box sx={{ 
                            display: 'flex',
                            flexDirection: { xs: 'column', sm: 'row' },
                            alignItems: 'center',
                            gap: 2,
                            minWidth: { xs: '100%', sm: 'auto' }
                          }}>
                            <Typography variant="body2" color="text.secondary" className="pixel-text" sx={{ whiteSpace: 'nowrap' }}>
                              Uploaded: {translation.date}
                            </Typography>
                            {translation.status === 'completed' ? (
                              <Button
                                variant="contained"
                                startIcon={<DownloadIcon />}
                                className="retro-button"
                                sx={{ whiteSpace: 'nowrap' }}
                              >
                                Download ROM
                              </Button>
                            ) : (
                              <Button
                                variant="outlined"
                                disabled
                                className="retro-button"
                                sx={{ whiteSpace: 'nowrap' }}
                              >
                                {translation.status === 'processing'
                                  ? 'In Progress'
                                  : 'Queued'}
                              </Button>
                            )}
                          </Box>
                        </ListItem>
                      </React.Fragment>
                    ))}
                  </List>
                </Paper>
              </Grid>
            </Grid>
          </Container>
        </Box>
      </Layout>
    </ProtectedRoute>
  );
};

export default TranslationsPage; 