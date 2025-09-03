import type { ButtonHTMLAttributes, ReactNode } from 'react';
import type { BaseProps, ClickableProps, SizedProps } from '../../types/common';

// Shared size variants that other components can use
export type Size = 'sm' | 'md' | 'lg';

// Shared variant types that other components can use
export type Variant = 'primary' | 'secondary' | 'danger' | 'outline';

// Base props that many components will share
export interface BaseComponentProps {
  /**
   * Additional CSS classes to apply
   */
  className?: string;
  /**
   * Whether the component is disabled
   */
  disabled?: boolean;
  /**
   * Size variant
   */
  size?: Size;
}

// Button-specific props
export interface ButtonProps
  extends BaseComponentProps,
    Omit<ButtonHTMLAttributes<HTMLButtonElement>, 'size'> {
  /**
   * Button variant style
   */
  variant?: Variant;
  /**
   * Content to display inside the button
   */
  children: ReactNode;
  /**
   * Whether the button should take full width
   */
  fullWidth?: boolean;
  /**
   * Whether the button is in a loading state
   */
  loading?: boolean;
  /**
   * Icon to display before the text
   */
  startIcon?: ReactNode;
  /**
   * Icon to display after the text
   */
  endIcon?: ReactNode;
}
