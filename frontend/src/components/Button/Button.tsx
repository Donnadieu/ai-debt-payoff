import React, { forwardRef } from 'react';
import { ButtonProps, Size, Variant } from './Button.types';

// Button variant styles using Tailwind classes
const variantStyles: Record<Variant, string> = {
  primary: 'bg-primary-600 hover:bg-primary-700 focus:ring-primary-500 text-white border-transparent',
  secondary: 'bg-neutral-100 hover:bg-neutral-200 focus:ring-neutral-500 text-neutral-900 border-neutral-300',
  danger: 'bg-danger-600 hover:bg-danger-700 focus:ring-danger-500 text-white border-transparent',
  outline: 'bg-transparent hover:bg-neutral-50 focus:ring-primary-500 text-primary-600 border-primary-600 hover:border-primary-700',
};

// Button size styles
const sizeStyles: Record<Size, string> = {
  sm: 'px-3 py-1.5 text-sm',
  md: 'px-4 py-2 text-base',
  lg: 'px-6 py-3 text-lg',
};

// Base button styles
const baseStyles = 'inline-flex items-center justify-center font-medium rounded-lg border transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed';

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(({
  variant = 'primary',
  size = 'md',
  fullWidth = false,
  loading = false,
  disabled = false,
  className = '',
  children,
  startIcon,
  endIcon,
  ...props
}, ref) => {
  const buttonClasses = [
    baseStyles,
    variantStyles[variant],
    sizeStyles[size],
    fullWidth ? 'w-full' : '',
    className,
  ].filter(Boolean).join(' ');

  const isDisabled = disabled || loading;

  return (
    <button
      ref={ref}
      className={buttonClasses}
      disabled={isDisabled}
      aria-disabled={isDisabled}
      {...props}
    >
      {loading ? (
        <>
          {/* Loading spinner */}
          <svg
            className="animate-spin -ml-1 mr-2 h-4 w-4"
            fill="none"
            viewBox="0 0 24 24"
            aria-hidden="true"
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
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
          Loading...
        </>
      ) : (
        <>
          {startIcon && (
            <span className="mr-2 flex-shrink-0" aria-hidden="true">
              {startIcon}
            </span>
          )}
          {children}
          {endIcon && (
            <span className="ml-2 flex-shrink-0" aria-hidden="true">
              {endIcon}
            </span>
          )}
        </>
      )}
    </button>
  );
});

Button.displayName = 'Button';