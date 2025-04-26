import React, { useEffect, useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Grid,
  Typography,
  Chip,
  LinearProgress,
  IconButton,
  Stack,
  Paper,
  Tooltip,
} from '@mui/material';
import DownloadIcon from '@mui/icons-material/Download';
import DeleteIcon from '@mui/icons-material/Delete';
import TextFieldsIcon from '@mui/icons-material/TextFields';
import AudiotrackIcon from '@mui/icons-material/Audiotrack';
import ImageIcon from '@mui/icons-material/Image';
import LanguageIcon from '@mui/icons-material/Language';
import PendingIcon from '@mui/icons-material/Pending';
import AutorenewIcon from '@mui/icons-material/Autorenew';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';
import Layout from '@/components/layout/Layout';
import { ProtectedRoute } from '../components/ProtectedRoute';
import { api } from '@/services/api';

interface TranslationJob {
  id: number;
  original_filename: string;
  file_size: number;
  target_language: string;
  translation_options: {
    text: boolean;
    audio: boolean;
    image: boolean;
  };
  status: string;
  created_at: string;
  updated_at: string;
}

const statusConfig = {
  pending: {
    color: '#FFA726',
    bgColor: '#FFF3E0',
    icon: <PendingIcon fontSize="small" />,
    label: 'Pending'
  },
  processing: {
    color: '#29B6F6',
    bgColor: '#E1F5FE',
    icon: <AutorenewIcon fontSize="small" className="rotating-icon" />,
    label: 'In Progress'
  },
  completed: {
    color: '#66BB6A',
    bgColor: '#E8F5E9',
    icon: <CheckCircleIcon fontSize="small" />,
    label: 'Completed'
  },
  failed: {
    color: '#EF5350',
    bgColor: '#FFEBEE',
    icon: <ErrorIcon fontSize="small" />,
    label: 'Failed'
  }
};

const TranslationsPage = () => {
  const [translations, setTranslations] = useState<TranslationJob[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchTranslations();
  }, []);

  const fetchTranslations = async () => {
    try {
      const response = await api.get('/api/v1/translations/jobs');
      setTranslations(response.data);
      setError(null);
    } catch (err) {
      console.error('Failed to fetch translations:', err);
      setError('Failed to load translation jobs');
    } finally {
      setLoading(false);
    }
  };

  const formatFileSize = (bytes: number) => {
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    if (bytes === 0) return '0 Byte';
    const i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)).toString());
    return Math.round((bytes / Math.pow(1024, i)) * 100) / 100 + ' ' + sizes[i];
  };

  return (
    <ProtectedRoute>
      <Layout>
        <Box sx={{ flexGrow: 1 }}>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Paper sx={{ p: 4, textAlign: 'center' }} className="retro-border">
                <Typography variant="h3" component="h1" gutterBottom className="pixel-text">
                  Translation Jobs
                </Typography>
                <Typography variant="body1" paragraph className="pixel-text">
                  View and manage your ROM translation jobs
                </Typography>
              </Paper>
            </Grid>

            {loading ? (
              <Grid item xs={12}>
                <LinearProgress />
              </Grid>
            ) : error ? (
              <Grid item xs={12}>
                <Paper sx={{ p: 2, textAlign: 'center', bgcolor: 'error.light' }}>
                  <Typography color="error">{error}</Typography>
                </Paper>
              </Grid>
            ) : translations.length === 0 ? (
              <Grid item xs={12}>
                <Paper sx={{ p: 4, textAlign: 'center' }}>
                  <Typography variant="h6" className="pixel-text">
                    No translation jobs yet
                  </Typography>
                  <Typography variant="body1" className="pixel-text">
                    Upload a ROM to start translating
                  </Typography>
                </Paper>
              </Grid>
            ) : (
              translations.map((job) => (
                <Grid item xs={12} key={job.id}>
                  <Card className="retro-border">
                    <CardContent>
                      <Stack spacing={2}>
                        {/* Primeira linha: Nome do arquivo e Status */}
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                          <Box sx={{ minWidth: 0, flex: 1 }}>
                            <Typography variant="h6" className="pixel-text" noWrap>
                              {job.original_filename}
                              <Typography
                                component="span"
                                variant="body2"
                                color="text.secondary"
                                sx={{ ml: 1 }}
                              >
                                ({formatFileSize(job.file_size)})
                              </Typography>
                            </Typography>
                          </Box>
                          <Chip
                            icon={statusConfig[job.status as keyof typeof statusConfig].icon}
                            label={statusConfig[job.status as keyof typeof statusConfig].label}
                            sx={{
                              backgroundColor: statusConfig[job.status as keyof typeof statusConfig].bgColor,
                              color: statusConfig[job.status as keyof typeof statusConfig].color,
                              borderColor: statusConfig[job.status as keyof typeof statusConfig].color,
                              '& .MuiChip-icon': {
                                color: 'inherit'
                              },
                              fontWeight: 'medium',
                              border: 1,
                            }}
                          />
                        </Box>

                        {/* Segunda linha: Tags e Botões */}
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                          <Stack direction="row" spacing={1} alignItems="center">
                            <Chip
                              icon={<LanguageIcon />}
                              label={job.target_language.toUpperCase()}
                              size="small"
                              sx={{
                                backgroundColor: '#E3F2FD',
                                color: '#1976D2',
                                borderColor: '#1976D2',
                                border: 1,
                              }}
                            />
                            <Chip
                              icon={<TextFieldsIcon />}
                              label="Text"
                              size="small"
                              sx={{
                                backgroundColor: job.translation_options.text ? '#E8F5E9' : '#F5F5F5',
                                color: job.translation_options.text ? '#2E7D32' : '#9E9E9E',
                                borderColor: job.translation_options.text ? '#2E7D32' : '#9E9E9E',
                                border: 1,
                              }}
                            />
                            <Chip
                              icon={<AudiotrackIcon />}
                              label="Audio"
                              size="small"
                              sx={{
                                backgroundColor: job.translation_options.audio ? '#E8F5E9' : '#F5F5F5',
                                color: job.translation_options.audio ? '#2E7D32' : '#9E9E9E',
                                borderColor: job.translation_options.audio ? '#2E7D32' : '#9E9E9E',
                                border: 1,
                              }}
                            />
                            <Chip
                              icon={<ImageIcon />}
                              label="Image"
                              size="small"
                              sx={{
                                backgroundColor: job.translation_options.image ? '#E8F5E9' : '#F5F5F5',
                                color: job.translation_options.image ? '#2E7D32' : '#9E9E9E',
                                borderColor: job.translation_options.image ? '#2E7D32' : '#9E9E9E',
                                border: 1,
                              }}
                            />
                          </Stack>
                          <Stack direction="row" spacing={1}>
                            <Tooltip title={job.status !== 'completed' ? 'Available after completion' : 'Download'}>
                              <span>
                                <IconButton
                                  size="small"
                                  sx={{
                                    color: job.status === 'completed' ? '#1976D2' : '#9E9E9E',
                                    backgroundColor: job.status === 'completed' ? '#E3F2FD' : '#F5F5F5',
                                    '&:hover': {
                                      backgroundColor: job.status === 'completed' ? '#BBDEFB' : '#F5F5F5',
                                    }
                                  }}
                                  disabled={job.status !== 'completed'}
                                >
                                  <DownloadIcon fontSize="small" />
                                </IconButton>
                              </span>
                            </Tooltip>
                            <Tooltip title={job.status !== 'completed' ? 'Available after completion' : 'Delete'}>
                              <span>
                                <IconButton
                                  size="small"
                                  sx={{
                                    color: job.status === 'completed' ? '#D32F2F' : '#9E9E9E',
                                    backgroundColor: job.status === 'completed' ? '#FFEBEE' : '#F5F5F5',
                                    '&:hover': {
                                      backgroundColor: job.status === 'completed' ? '#FFCDD2' : '#F5F5F5',
                                    }
                                  }}
                                  disabled={job.status !== 'completed'}
                                >
                                  <DeleteIcon fontSize="small" />
                                </IconButton>
                              </span>
                            </Tooltip>
                          </Stack>
                        </Box>
                      </Stack>
                    </CardContent>
                  </Card>
                </Grid>
              ))
            )}
          </Grid>
        </Box>
      </Layout>
    </ProtectedRoute>
  );
};

export default TranslationsPage;

// Adicione este CSS global ao seu arquivo de estilos
// .rotating-icon {
//   animation: spin 2s linear infinite;
// }
// @keyframes spin {
//   100% { transform: rotate(360deg); }
// } 