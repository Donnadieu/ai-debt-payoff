// Common types shared across components

import React from 'react';

/**
 * Base size variants used across components
 */
export type Size = 'sm' | 'md' | 'lg';

/**
 * Common color variants for UI components
 */
export type Variant = 'primary' | 'secondary' | 'danger' | 'success' | 'warning' | 'outline';

/**
 * Common props that many components will extend
 */
export interface BaseProps {
  /**
   * Additional CSS class names to apply
   */
  className?: string;
  
  /**
   * Unique identifier for the element
   */
  id?: string;
  
  /**
   * React children elements
   */
  children?: React.ReactNode;
  
  /**
   * Test ID for automated testing
   */
  'data-testid'?: string;
}

/**
 * Props for components that can be disabled
 */
export interface DisableableProps {
  /**
   * Whether the component is disabled
   */
  disabled?: boolean;
}

/**
 * Props for components with loading states
 */
export interface LoadingProps {
  /**
   * Whether the component is in a loading state
   */
  loading?: boolean;
}

/**
 * Props for components that can be clicked
 */
export interface ClickableProps {
  /**
   * Click event handler
   */
  onClick?: (event: React.MouseEvent<HTMLElement>) => void;
}

/**
 * Props for components that need size variants
 */
export interface SizedProps {
  /**
   * Component size variant
   */
  size?: Size;
}

/**
 * Props for components with visual variants
 */
export interface VariantProps {
  /**
   * Component visual variant
   */
  variant?: Variant;
}