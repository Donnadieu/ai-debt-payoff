/**
 * Spacing configuration for MUI theme
 * Based on existing Tailwind spacing system (4px base unit)
 */

export const spacing = (factor: number): string => `${factor * 4}px`;

// Common spacing values for quick reference
export const spacingValues = {
  0: '0px',      // 0
  1: '4px',      // 1
  2: '8px',      // 2
  3: '12px',     // 3
  4: '16px',     // 4
  5: '20px',     // 5
  6: '24px',     // 6
  7: '28px',     // 7
  8: '32px',     // 8
  9: '36px',     // 9
  10: '40px',    // 10
  12: '48px',    // 12
  16: '64px',    // 16
  20: '80px',    // 20
  24: '96px',    // 24
  32: '128px',   // 32
  40: '160px',   // 40
  48: '192px',   // 48
  56: '224px',   // 56
  64: '256px',   // 64
};