import React, { useState } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  Checkbox,
  FormControl,
  FormControlLabel,
  FormGroup,
  Grid,
  IconButton,
  InputLabel,
  LinearProgress,
  MenuItem,
  Select,
  TextField,
  Typography,
  Chip,
  Divider,
  Stack,
  Paper,
} from '@mui/material';
import { styled } from '@mui/material/styles';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import VideogameAssetIcon from '@mui/icons-material/VideogameAsset';
import LanguageIcon from '@mui/icons-material/Language';
import TextFieldsIcon from '@mui/icons-material/TextFields';
import AudiotrackIcon from '@mui/icons-material/Audiotrack';
import ImageIcon from '@mui/icons-material/Image';
import Layout from '@/components/layout/Layout';

const VisuallyHiddenInput = styled('input')({
  clip: 'rect(0 0 0 0)',
  clipPath: 'inset(50%)',
  height: 1,
  overflow: 'hidden',
  position: 'absolute',
  bottom: 0,
  left: 0,
  whiteSpace: 'nowrap',
  width: 1,
});

const OptionCard = styled(Card)(({ theme }) => ({
  transition: 'all 0.3s ease',
  '&:hover': {
    transform: 'translateY(-2px)',
    boxShadow: theme.shadows[4],
  },
}));

const RomUploader = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [targetLanguage, setTargetLanguage] = useState('en');
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [translationOptions, setTranslationOptions] = useState({
    text: true,
    audio: false,
    image: false,
  });

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setSelectedFile(event.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setIsUploading(true);
    setUploadProgress(0);

    // Simulate upload progress
    const interval = setInterval(() => {
      setUploadProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          setIsUploading(false);
          return 100;
        }
        return prev + 10;
      });
    }, 500);
  };

  const handleTranslationOptionChange = (option: keyof typeof translationOptions) => {
    setTranslationOptions(prev => ({
      ...prev,
      [option]: !prev[option]
    }));
  };

  return (
    <Layout>
      <Box sx={{ flexGrow: 1 }}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Paper sx={{ p: 4, textAlign: 'center' }} className="retro-border">
              <Typography variant="h3" component="h1" gutterBottom className="pixel-text">
                Upload ROM
              </Typography>
              <Typography variant="body1" paragraph className="pixel-text">
                Select your ROM file and configure the translation settings
              </Typography>
            </Paper>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card className="retro-border">
              <CardContent>
                <Stack spacing={3}>
                  <Button
                    component="label"
                    variant="contained"
                    startIcon={<CloudUploadIcon />}
                    className="retro-button"
                    fullWidth
                    sx={{ py: 2 }}
                  >
                    Select ROM File
                    <VisuallyHiddenInput type="file" onChange={handleFileChange} />
                  </Button>

                  {selectedFile && (
                    <Chip
                      icon={<VideogameAssetIcon />}
                      label={`${selectedFile.name} (${(selectedFile.size / 1024 / 1024).toFixed(2)} MB)`}
                      onDelete={() => setSelectedFile(null)}
                      className="retro-border"
                      sx={{ 
                        maxWidth: '100%',
                        '& .MuiChip-label': {
                          overflow: 'hidden',
                          textOverflow: 'ellipsis',
                        }
                      }}
                    />
                  )}

                  <FormControl fullWidth>
                    <InputLabel id="target-language-label" className="pixel-text">
                      <LanguageIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                      Target Language
                    </InputLabel>
                    <Select
                      labelId="target-language-label"
                      value={targetLanguage}
                      label="Target Language"
                      onChange={(e) => setTargetLanguage(e.target.value)}
                      className="retro-border"
                    >
                      <MenuItem value="en">English</MenuItem>
                      <MenuItem value="es">Spanish</MenuItem>
                      <MenuItem value="fr">French</MenuItem>
                      <MenuItem value="de">German</MenuItem>
                      <MenuItem value="it">Italian</MenuItem>
                      <MenuItem value="pt">Portuguese</MenuItem>
                      <MenuItem value="ru">Russian</MenuItem>
                      <MenuItem value="ja">Japanese</MenuItem>
                      <MenuItem value="zh">Chinese</MenuItem>
                      <MenuItem value="ko">Korean</MenuItem>
                    </Select>
                  </FormControl>

                  <FormGroup>
                    <Typography variant="subtitle1" className="pixel-text" sx={{ mb: 1 }}>
                      Translation Options
                    </Typography>
                    <Stack spacing={1}>
                      <FormControlLabel
                        control={
                          <Checkbox
                            checked={translationOptions.text}
                            onChange={() => handleTranslationOptionChange('text')}
                            icon={<TextFieldsIcon />}
                            checkedIcon={<TextFieldsIcon />}
                          />
                        }
                        label="Text Translation"
                        className="pixel-text"
                      />
                      <FormControlLabel
                        control={
                          <Checkbox
                            checked={translationOptions.audio}
                            onChange={() => handleTranslationOptionChange('audio')}
                            icon={<AudiotrackIcon />}
                            checkedIcon={<AudiotrackIcon />}
                            disabled
                          />
                        }
                        label={
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <span>Audio Dubbing</span>
                            <Chip 
                              label="Coming Soon" 
                              size="small" 
                              color="primary" 
                              variant="outlined"
                              sx={{ 
                                fontSize: '0.7rem',
                                height: '20px',
                                '& .MuiChip-label': { px: 1 }
                              }}
                            />
                          </Box>
                        }
                        className="pixel-text"
                      />
                      <FormControlLabel
                        control={
                          <Checkbox
                            checked={translationOptions.image}
                            onChange={() => handleTranslationOptionChange('image')}
                            icon={<ImageIcon />}
                            checkedIcon={<ImageIcon />}
                            disabled
                          />
                        }
                        label={
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <span>Image Translation</span>
                            <Chip 
                              label="Coming Soon" 
                              size="small" 
                              color="primary" 
                              variant="outlined"
                              sx={{ 
                                fontSize: '0.7rem',
                                height: '20px',
                                '& .MuiChip-label': { px: 1 }
                              }}
                            />
                          </Box>
                        }
                        className="pixel-text"
                      />
                    </Stack>
                  </FormGroup>

                  {isUploading && (
                    <Box sx={{ width: '100%' }}>
                      <LinearProgress 
                        variant="determinate" 
                        value={uploadProgress}
                        sx={{ 
                          height: 8,
                          borderRadius: 4,
                          backgroundColor: 'rgba(0,0,0,0.1)',
                          '& .MuiLinearProgress-bar': {
                            borderRadius: 4,
                          }
                        }}
                      />
                      <Typography 
                        variant="body2" 
                        color="text.secondary" 
                        className="pixel-text"
                        sx={{ mt: 1, textAlign: 'center' }}
                      >
                        {`${uploadProgress}%`}
                      </Typography>
                    </Box>
                  )}

                  <Button
                    variant="contained"
                    onClick={handleUpload}
                    disabled={!selectedFile || isUploading}
                    className="retro-button"
                    fullWidth
                    sx={{ py: 2 }}
                  >
                    {isUploading ? 'Uploading...' : 'Start Translation'}
                  </Button>
                </Stack>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card className="retro-border">
              <CardContent>
                <Typography 
                  variant="h6" 
                  gutterBottom 
                  className="pixel-text"
                  sx={{ mb: 3, textAlign: 'center' }}
                >
                  Translation Details
                </Typography>
                <Stack spacing={3}>
                  <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 2 }}>
                    <TextFieldsIcon 
                      sx={{ 
                        fontSize: 32,
                        color: translationOptions.text ? 'primary.main' : 'text.secondary',
                        transition: 'color 0.3s ease',
                        mt: 0.5
                      }} 
                    />
                    <Box>
                      <Typography variant="subtitle1" className="pixel-text">
                        Text Translation
                      </Typography>
                      <Typography variant="body2" color="text.secondary" className="pixel-text">
                        Translates all in-game text including menus, dialogues, and descriptions. 
                        <br />
                        <strong>Estimated time:</strong> 5-10 minutes per 1000 characters
                      </Typography>
                    </Box>
                  </Box>

                  <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 2 }}>
                    <AudiotrackIcon 
                      sx={{ 
                        fontSize: 32,
                        color: translationOptions.audio ? 'primary.main' : 'text.secondary',
                        transition: 'color 0.3s ease',
                        mt: 0.5
                      }} 
                    />
                    <Box>
                      <Typography variant="subtitle1" className="pixel-text">
                        Audio Dubbing
                      </Typography>
                      <Typography variant="body2" color="text.secondary" className="pixel-text">
                        Generate voice-overs for cutscenes and character dialogues.
                        <br />
                        <strong>Estimated time:</strong> Coming Soon
                      </Typography>
                    </Box>
                  </Box>

                  <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 2 }}>
                    <ImageIcon 
                      sx={{ 
                        fontSize: 32,
                        color: translationOptions.image ? 'primary.main' : 'text.secondary',
                        transition: 'color 0.3s ease',
                        mt: 0.5
                      }} 
                    />
                    <Box>
                      <Typography variant="subtitle1" className="pixel-text">
                        Image Translation
                      </Typography>
                      <Typography variant="body2" color="text.secondary" className="pixel-text">
                        Translate text embedded in images, logos, and UI elements.
                        <br />
                        <strong>Estimated time:</strong> Coming Soon
                      </Typography>
                    </Box>
                  </Box>
                </Stack>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Box>
    </Layout>
  );
};

export default RomUploader; 