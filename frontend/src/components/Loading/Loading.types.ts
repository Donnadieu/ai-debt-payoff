// Loading component type definitions

export type SpinnerSize = 'sm' | 'md' | 'lg' | 'xl';
export type SpinnerColor = 'primary' | 'secondary' | 'white' | 'gray';

export interface SpinnerProps {
  size?: SpinnerSize;
  color?: SpinnerColor;
  className?: string;
  'aria-label'?: string;
}

export type SkeletonVariant = 'text' | 'circular' | 'rectangular';
export type SkeletonAnimation = 'pulse' | 'wave' | 'none';

export interface SkeletonProps {
  variant?: SkeletonVariant;
  animation?: SkeletonAnimation;
  width?: string | number;
  height?: string | number;
  className?: string;
  lines?: number; // For text variant - number of lines to show
}

// Common loading state interface for consistency across components
export interface LoadingState<T = unknown> {
  isLoading: boolean;
  error?: string | null;
  data?: T;
}
