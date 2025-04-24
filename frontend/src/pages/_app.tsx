import React from 'react';
import { AppProps } from 'next/app';
import { ThemeProvider, createTheme, responsiveFontSizes } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Head from 'next/head';

let theme = createTheme({
  breakpoints: {
    values: {
      xs: 0,
      sm: 600,
      md: 900,
      lg: 1200,
      xl: 1536,
    },
  },
  palette: {
    primary: {
      main: '#FF6B6B', // Retro Red
      light: '#FF8E8E',
      dark: '#FF5252',
    },
    secondary: {
      main: '#4ECDC4', // Retro Teal
      light: '#7FE5DD',
      dark: '#3DBEB6',
    },
    background: {
      default: '#F7F7F7',
      paper: '#FFFFFF',
    },
    text: {
      primary: '#2D3436', // Dark Gray
      secondary: '#636E72', // Medium Gray
    },
    error: {
      main: '#FF7675', // Soft Red
    },
    warning: {
      main: '#FFA502', // Retro Orange
    },
    success: {
      main: '#00B894', // Retro Green
    },
  },
  typography: {
    fontFamily: '"Share Tech Mono", "VT323", "Roboto", "Arial", sans-serif',
    h1: {
      fontSize: { xs: '1.5rem', sm: '2rem', md: '2.5rem' },
      fontWeight: 400,
      letterSpacing: '0.5px',
    },
    h2: {
      fontSize: { xs: '1.25rem', sm: '1.5rem', md: '2rem' },
      fontWeight: 400,
      letterSpacing: '0.5px',
    },
    h3: {
      fontSize: { xs: '1.1rem', sm: '1.25rem', md: '1.75rem' },
      fontWeight: 400,
      letterSpacing: '0.5px',
    },
    body1: {
      fontSize: { xs: '0.875rem', sm: '1rem', md: '1.125rem' },
      letterSpacing: '0.3px',
    },
    button: {
      textTransform: 'none',
      fontWeight: 400,
      letterSpacing: '0.5px',
      fontSize: { xs: '0.75rem', sm: '0.875rem', md: '1rem' },
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: '4px',
          padding: { xs: '6px 12px', sm: '8px 16px' },
          boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
          transition: 'all 0.3s ease',
          '&:hover': {
            transform: 'translateY(-2px)',
            boxShadow: '0 6px 8px rgba(0,0,0,0.2)',
          },
          '&:active': {
            transform: 'translateY(0)',
            boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
          },
        },
        contained: {
          background: 'linear-gradient(45deg, #FF6B6B 30%, #FF8E8E 90%)',
          border: '2px solid #FF5252',
          '&:hover': {
            background: 'linear-gradient(45deg, #FF5252 30%, #FF6B6B 90%)',
          },
        },
        outlined: {
          border: '2px solid #2D3436',
          '&:hover': {
            border: '2px solid #FF6B6B',
            background: 'rgba(255, 255, 255, 0.1)',
          },
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: '4px',
          boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: '4px',
          boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: '4px',
          fontWeight: 400,
        },
      },
    },
    MuiLinearProgress: {
      styleOverrides: {
        root: {
          borderRadius: '4px',
          height: '8px',
        },
      },
    },
    MuiSelect: {
      styleOverrides: {
        root: {
          borderRadius: '4px',
        },
      },
    },
    MuiGrid: {
      styleOverrides: {
        container: {
          margin: 0,
          width: '100%',
        },
      },
    },
  },
});

// Make the theme responsive
theme = responsiveFontSizes(theme);

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <ThemeProvider theme={theme}>
      <Head>
        <link
          href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=VT323&display=swap"
          rel="stylesheet"
        />
      </Head>
      <CssBaseline />
      <Component {...pageProps} />
    </ThemeProvider>
  );
}

export default MyApp; 