import React from 'react';
import { ThemeProvider as MuiThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { theme } from './theme';

interface ThemeProviderProps {
  children: React.ReactNode;
}

/**
 * Custom ThemeProvider component that wraps the MUI ThemeProvider
 * Provides the custom theme configuration to all MUI components
 * and includes CssBaseline for consistent styling
 */
export const ThemeProvider: React.FC<ThemeProviderProps> = ({ children }) => {
  return (
    <MuiThemeProvider theme={theme}>
      {/* CssBaseline provides consistent baseline styles across browsers */}
      <CssBaseline />
      {children}
    </MuiThemeProvider>
  );
};

export default ThemeProvider;