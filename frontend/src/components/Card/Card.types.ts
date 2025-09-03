import React from 'react';
import { BaseProps, ClickableProps, SizedProps } from '../../types/common';

/**
 * Card padding variants
 */
export type CardPadding = 'none' | 'sm' | 'md' | 'lg';

/**
 * Card border variants
 */
export type CardBorder = 'none' | 'sm' | 'md' | 'lg';

/**
 * Card shadow variants
 */
export type CardShadow = 'none' | 'sm' | 'md' | 'lg' | 'xl';

/**
 * Card hover effect variants
 */
export type CardHoverEffect = 'none' | 'lift' | 'glow' | 'scale';

/**
 * Props for the Card component
 */
export interface CardProps extends BaseProps, ClickableProps, SizedProps {
  /**
   * Card header content (optional)
   */
  header?: React.ReactNode;
  
  /**
   * Card footer content (optional)
   */
  footer?: React.ReactNode;
  
  /**
   * Card body content
   */
  children: React.ReactNode;
  
  /**
   * Card padding variant
   * @default 'md'
   */
  padding?: CardPadding;
  
  /**
   * Card border variant
   * @default 'sm'
   */
  border?: CardBorder;
  
  /**
   * Card shadow variant
   * @default 'sm'
   */
  shadow?: CardShadow;
  
  /**
   * Card hover effect variant
   * @default 'none'
   */
  hoverEffect?: CardHoverEffect;
  
  /**
   * Whether the card is selected/active
   */
  selected?: boolean;
  
  /**
   * Whether the card is clickable (shows pointer cursor)
   */
  clickable?: boolean;
  
  /**
   * Card background color variant
   */
  background?: 'default' | 'subtle' | 'accent';
  
  /**
   * Whether to show a loading skeleton
   */
  loading?: boolean;
}

/**
 * Props for the CardHeader component
 */
export interface CardHeaderProps extends BaseProps {
  /**
   * Header title
   */
  title?: React.ReactNode;
  
  /**
   * Header subtitle
   */
  subtitle?: React.ReactNode;
  
  /**
   * Action buttons or elements for the header
   */
  actions?: React.ReactNode;
  
  /**
   * Whether to show a divider below the header
   */
  divider?: boolean;
}

/**
 * Props for the CardBody component
 */
export interface CardBodyProps extends BaseProps {
  /**
   * Body content
   */
  children: React.ReactNode;
  
  /**
   * Custom padding override
   */
  padding?: CardPadding;
}

/**
 * Props for the CardFooter component
 */
export interface CardFooterProps extends BaseProps {
  /**
   * Footer content
   */
  children: React.ReactNode;
  
  /**
   * Footer actions (typically buttons)
   */
  actions?: React.ReactNode;
  
  /**
   * Whether to show a divider above the footer
   */
  divider?: boolean;
  
  /**
   * Footer alignment
   */
  align?: 'left' | 'center' | 'right' | 'between';
}