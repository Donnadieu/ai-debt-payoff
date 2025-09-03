import { createTheme } from '@mui/material/styles';
import { colors } from './colors';
import { typography } from './typography';
import { breakpoints } from './breakpoints';
import { spacing } from './spacing';

/**
 * Custom MUI theme configuration
 * Integrates existing Tailwind design tokens with MUI components
 */
export const theme = createTheme({
  // Color palette
  palette: {
    mode: 'light',
    primary: {
      main: colors.primary[600],
      light: colors.primary[400],
      dark: colors.primary[700],
      contrastText: colors.common.white,
    },
    secondary: {
      main: colors.secondary[600],
      light: colors.secondary[400],
      dark: colors.secondary[700],
      contrastText: colors.common.white,
    },
    error: {
      main: colors.error[600],
      light: colors.error[400],
      dark: colors.error[700],
      contrastText: colors.common.white,
    },
    warning: {
      main: colors.warning[600],
      light: colors.warning[400],
      dark: colors.warning[700],
      contrastText: colors.common.white,
    },
    success: {
      main: colors.success[600],
      light: colors.success[400],
      dark: colors.success[700],
      contrastText: colors.common.white,
    },
    grey: colors.grey,
    text: colors.text,
    background: colors.background,
    action: colors.action,
    divider: colors.divider,
    common: colors.common,
  },

  // Typography
  typography,

  // Breakpoints
  breakpoints,

  // Spacing function
  spacing,

  // Component overrides
  components: {
    // Button component customization
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: '0.5rem', // rounded-lg equivalent
          textTransform: 'none',
          fontWeight: 500,
          transition: 'all 0.2s ease-in-out',
          '&:focus': {
            outline: `2px solid ${colors.primary[500]}`,
            outlineOffset: '2px',
          },
        },
        contained: {
          boxShadow: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
          '&:hover': {
            boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
          },
        },
        outlined: {
          borderWidth: '1px',
          '&:hover': {
            borderWidth: '1px',
          },
        },
        sizeSmall: {
          padding: '6px 12px',
          fontSize: '0.875rem',
        },
        sizeMedium: {
          padding: '8px 16px',
          fontSize: '1rem',
        },
        sizeLarge: {
          padding: '12px 24px',
          fontSize: '1.125rem',
        },
      },
    },

    // TextField component customization
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            borderRadius: '0.5rem',
            '&:hover .MuiOutlinedInput-notchedOutline': {
              borderColor: colors.primary[400],
            },
            '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
              borderColor: colors.primary[600],
              borderWidth: '2px',
            },
            '&.Mui-error .MuiOutlinedInput-notchedOutline': {
              borderColor: colors.error[600],
            },
          },
        },
      },
    },

    // Select component customization
    MuiSelect: {
      styleOverrides: {
        root: {
          borderRadius: '0.5rem',
        },
      },
    },

    // Card component customization
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: '1rem', // rounded-xl equivalent
          boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        },
      },
    },

    // Paper component customization
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: '0.75rem',
        },
        elevation1: {
          boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
        },
        elevation2: {
          boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        },
        elevation3: {
          boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
        },
      },
    },

    // Input component customization
    MuiInputBase: {
      styleOverrides: {
        root: {
          '&.Mui-focused': {
            '& .MuiOutlinedInput-notchedOutline': {
              borderColor: colors.primary[600],
            },
          },
        },
      },
    },

    // FormLabel customization
    MuiFormLabel: {
      styleOverrides: {
        root: {
          color: colors.text.secondary,
          '&.Mui-focused': {
            color: colors.primary[600],
          },
        },
      },
    },

    // IconButton customization
    MuiIconButton: {
      styleOverrides: {
        root: {
          borderRadius: '0.5rem',
          transition: 'all 0.2s ease-in-out',
          '&:hover': {
            backgroundColor: colors.action.hover,
          },
        },
      },
    },
  },

  // Shape configuration
  shape: {
    borderRadius: 8, // 0.5rem equivalent
  },

  // Shadows
  shadows: [
    'none',
    '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)', // shadow-sm
    '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)', // shadow
    '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)', // shadow-md
    '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)', // shadow-lg
    '0 25px 50px -12px rgba(0, 0, 0, 0.25)', // shadow-xl
    '0 35px 60px -12px rgba(0, 0, 0, 0.25)', // shadow-2xl
    // Additional shadows as needed by MUI
    ...Array(18).fill('0 35px 60px -12px rgba(0, 0, 0, 0.25)'),
  ] as const,
});