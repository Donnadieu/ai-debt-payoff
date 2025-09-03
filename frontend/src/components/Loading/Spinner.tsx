import React, { forwardRef } from 'react';
import { SpinnerProps } from './Loading.types';

const sizeClasses = {
  sm: 'h-4 w-4',
  md: 'h-6 w-6', 
  lg: 'h-8 w-8',
  xl: 'h-12 w-12'
};

const colorClasses = {
  primary: 'text-blue-600',
  secondary: 'text-gray-600',
  white: 'text-white',
  gray: 'text-gray-400'
};

const Spinner = forwardRef<HTMLDivElement, SpinnerProps>(({
  size = 'md',
  color = 'primary',
  className = '',
  'aria-label': ariaLabel = 'Loading...',
  ...props
}, ref) => {
  const sizeClass = sizeClasses[size];
  const colorClass = colorClasses[color];

  return (
    <div
      ref={ref}
      className={`animate-spin inline-block ${sizeClass} ${colorClass} ${className}`}
      role="status"
      aria-label={ariaLabel}
      aria-live="polite"
      {...props}
    >
      <svg
        className="w-full h-full"
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <circle
          className="opacity-25"
          cx="12"
          cy="12"
          r="10"
          stroke="currentColor"
          strokeWidth="4"
        />
        <path
          className="opacity-75"
          fill="currentColor"
          d="M4 12a8 8 0 018-8v8H4z"
        />
      </svg>
      <span className="sr-only">{ariaLabel}</span>
    </div>
  );
});

Spinner.displayName = 'Spinner';

export { Spinner };
export default Spinner;