/**
 * Typography configuration for MUI theme
 * Based on existing Tailwind font configuration
 */

export const typography = {
  fontFamily: '"Inter", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
  fontSize: 16,
  fontWeightLight: 300,
  fontWeightRegular: 400,
  fontWeightMedium: 500,
  fontWeightBold: 700,
  
  // Heading styles
  h1: {
    fontSize: '3rem', // 48px - 3xl
    fontWeight: 700,
    lineHeight: 1.2,
    letterSpacing: '-0.025em',
  },
  h2: {
    fontSize: '2.25rem', // 36px - 2xl
    fontWeight: 600,
    lineHeight: 1.25,
    letterSpacing: '-0.025em',
  },
  h3: {
    fontSize: '1.875rem', // 30px - xl
    fontWeight: 600,
    lineHeight: 1.3,
    letterSpacing: '-0.025em',
  },
  h4: {
    fontSize: '1.5rem', // 24px - lg
    fontWeight: 600,
    lineHeight: 1.35,
    letterSpacing: '-0.025em',
  },
  h5: {
    fontSize: '1.25rem', // 20px - base+
    fontWeight: 600,
    lineHeight: 1.4,
  },
  h6: {
    fontSize: '1.125rem', // 18px - sm+
    fontWeight: 600,
    lineHeight: 1.4,
  },
  
  // Body text styles
  body1: {
    fontSize: '1rem', // 16px - base
    fontWeight: 400,
    lineHeight: 1.5,
  },
  body2: {
    fontSize: '0.875rem', // 14px - sm
    fontWeight: 400,
    lineHeight: 1.4,
  },
  
  // Subtitle styles
  subtitle1: {
    fontSize: '1rem', // 16px
    fontWeight: 500,
    lineHeight: 1.4,
  },
  subtitle2: {
    fontSize: '0.875rem', // 14px
    fontWeight: 500,
    lineHeight: 1.4,
  },
  
  // Caption and overline
  caption: {
    fontSize: '0.75rem', // 12px - xs
    fontWeight: 400,
    lineHeight: 1.4,
  },
  overline: {
    fontSize: '0.75rem', // 12px
    fontWeight: 600,
    lineHeight: 1.4,
    textTransform: 'uppercase' as const,
    letterSpacing: '0.08em',
  },
  
  // Button text
  button: {
    fontSize: '0.875rem', // 14px
    fontWeight: 500,
    lineHeight: 1.4,
    textTransform: 'none' as const,
  },
};