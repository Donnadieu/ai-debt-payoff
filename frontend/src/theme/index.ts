/**
 * Theme module exports
 * Centralized exports for all theme-related configurations
 */

export { theme } from './theme';
export { colors } from './colors';
export { typography } from './typography';
export { breakpoints, breakpointHelpers } from './breakpoints';
export { spacing, spacingValues } from './spacing';
export { ThemeProvider } from './ThemeProvider';

// Re-export MUI types for convenience
export type { Theme } from '@mui/material/styles';
export type { PaletteOptions, TypographyOptions } from '@mui/material/styles';