/**
 * Breakpoint configuration for MUI theme
 * Based on common responsive design patterns
 */

export const breakpoints = {
  values: {
    xs: 0,     // Extra small devices (phones)
    sm: 640,   // Small devices (tablets)
    md: 768,   // Medium devices (small laptops)
    lg: 1024,  // Large devices (laptops/desktops)
    xl: 1280,  // Extra large devices (large desktops)
  },
};

// Helper functions for media queries
export const breakpointHelpers = {
  up: (key: keyof typeof breakpoints.values) => `@media (min-width: ${breakpoints.values[key]}px)`,
  down: (key: keyof typeof breakpoints.values) => {
    const value = breakpoints.values[key];
    return value === 0 ? '@media (max-width: 0px)' : `@media (max-width: ${value - 0.05}px)`;
  },
  between: (start: keyof typeof breakpoints.values, end: keyof typeof breakpoints.values) => {
    const startValue = breakpoints.values[start];
    const endValue = breakpoints.values[end];
    return `@media (min-width: ${startValue}px) and (max-width: ${endValue - 0.05}px)`;
  },
};