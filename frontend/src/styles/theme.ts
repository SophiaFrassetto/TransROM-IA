/**
 * Theme configuration for Material-UI with subtle retro gaming aesthetics
 */

import { createTheme, Theme } from '@mui/material/styles';

declare module '@mui/material/styles' {
  interface Palette {
    custom: {
      background: string;
      border: string;
      hover: string;
      pixelBorder: string;
      accent: string;
    };
  }
  interface PaletteOptions {
    custom?: {
      background: string;
      border: string;
      hover: string;
      pixelBorder: string;
      accent: string;
    };
  }
}

export const theme = createTheme({
  palette: {
    primary: {
      main: '#4A90E2', // Soft blue
      light: '#74A9E6',
      dark: '#2171CD',
      contrastText: '#FFFFFF',
    },
    secondary: {
      main: '#9B51E0', // Soft purple
      light: '#B37BE8',
      dark: '#7B3AB3',
      contrastText: '#FFFFFF',
    },
    error: {
      main: '#E86C6C', // Soft red
      light: '#EE8E8E',
      dark: '#D14343',
    },
    warning: {
      main: '#F5B041', // Soft orange
      light: '#F7C068',
      dark: '#D4932C',
    },
    success: {
      main: '#66BB6A', // Soft green
      light: '#81C784',
      dark: '#4CAF50',
    },
    background: {
      default: '#F8F9FA', // Light gray background
      paper: '#FFFFFF',
    },
    text: {
      primary: '#2C3E50', // Dark blue-gray
      secondary: '#5D6D7E',
    },
    custom: {
      background: '#F8F9FA',
      border: '#E2E8F0',
      hover: '#EDF2F7',
      pixelBorder: '#CBD5E0',
      accent: '#4A90E2',
    },
  },
  typography: {
    fontFamily: [
      '"Share Tech Mono"',
      '"Inconsolata"',
      'monospace'
    ].join(','),
    h1: {
      fontSize: '2rem',
      fontWeight: 600,
      lineHeight: 1.5,
      letterSpacing: '0.05em',
    },
    h2: {
      fontSize: '1.75rem',
      fontWeight: 600,
      lineHeight: 1.5,
      letterSpacing: '0.05em',
    },
    h3: {
      fontSize: '1.5rem',
      fontWeight: 600,
      lineHeight: 1.5,
      letterSpacing: '0.05em',
    },
    h4: {
      fontSize: '1.25rem',
      fontWeight: 600,
      lineHeight: 1.5,
      letterSpacing: '0.05em',
    },
    h5: {
      fontSize: '1rem',
      fontWeight: 600,
      lineHeight: 1.5,
      letterSpacing: '0.05em',
    },
    h6: {
      fontSize: '0.875rem',
      fontWeight: 600,
      lineHeight: 1.5,
      letterSpacing: '0.05em',
    },
    body1: {
      fontSize: '1rem',
      lineHeight: 1.6,
      letterSpacing: '0.03em',
    },
    body2: {
      fontSize: '0.875rem',
      lineHeight: 1.6,
      letterSpacing: '0.03em',
    },
  },
  shape: {
    borderRadius: 4, // Subtle rounded corners
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          fontWeight: 500,
          borderWidth: '2px',
          '&:hover': {
            backgroundColor: '#EDF2F7',
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          border: '1px solid #E2E8F0',
          boxShadow: '0 2px 4px rgba(0,0,0,0.05)',
          backgroundColor: '#FFFFFF',
        },
      },
    },
    MuiDrawer: {
      styleOverrides: {
        paper: {
          borderRight: '1px solid #E2E8F0',
          backgroundColor: '#FFFFFF',
        },
      },
    },
  },
});

export type AppTheme = Theme;
