import React, { forwardRef } from 'react';
import type { InputProps, InputSize, InputVariant } from './Input.types';
import type { Size } from '../Button/Button.types';

// Input validation state styles
const validationStateStyles: Record<ValidationState, string> = {
  default: 'border-neutral-300 focus:border-primary-500 focus:ring-primary-500',
  error: 'border-danger-300 focus:border-danger-500 focus:ring-danger-500',
  success: 'border-success-300 focus:border-success-500 focus:ring-success-500',
};

// Input size styles
const sizeStyles: Record<Size, string> = {
  sm: 'px-3 py-1.5 text-sm',
  md: 'px-3 py-2 text-base',
  lg: 'px-4 py-3 text-lg',
};

// Base input styles
const baseStyles =
  'block rounded-lg border transition-colors focus:outline-none focus:ring-2 focus:ring-offset-1 disabled:opacity-50 disabled:cursor-not-allowed placeholder:text-neutral-400';

export const Input = forwardRef<HTMLInputElement, InputProps>(
  (
    {
      type = 'text',
      size = 'md',
      validationState = 'default',
      fullWidth = false,
      disabled = false,
      className = '',
      error,
      required = false,
      helperText,
      'aria-describedby': ariaDescribedBy,
      ...props
    },
    ref
  ) => {
    // Determine validation state based on error prop
    const effectiveValidationState = error ? 'error' : validationState;

    const inputClasses = [
      baseStyles,
      sizeStyles[size],
      validationStateStyles[effectiveValidationState],
      fullWidth ? 'w-full' : '',
      className,
    ]
      .filter(Boolean)
      .join(' ');

    // Generate unique IDs for accessibility
    const inputId =
      props.id || `input-${Math.random().toString(36).substr(2, 9)}`;
    const errorId = error ? `${inputId}-error` : undefined;
    const helperTextId = helperText ? `${inputId}-helper` : undefined;

    // Combine aria-describedby with our generated IDs
    const describedBy =
      [ariaDescribedBy, errorId, helperTextId].filter(Boolean).join(' ') ||
      undefined;

    return (
      <div className={fullWidth ? 'w-full' : ''}>
        <input
          ref={ref}
          id={inputId}
          type={type}
          className={inputClasses}
          disabled={disabled}
          aria-disabled={disabled}
          aria-required={required}
          aria-invalid={effectiveValidationState === 'error'}
          aria-describedby={describedBy}
          {...props}
        />

        {/* Error message */}
        {error && (
          <p
            id={errorId}
            className='mt-1 text-sm text-danger-600'
            role='alert'
            aria-live='polite'
          >
            {error}
          </p>
        )}

        {/* Helper text */}
        {helperText && !error && (
          <p id={helperTextId} className='mt-1 text-sm text-neutral-500'>
            {helperText}
          </p>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';
