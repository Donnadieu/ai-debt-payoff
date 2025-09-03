import React from 'react';
import type { FormFieldProps } from './FormField.types';

export const FormField: React.FC<FormFieldProps> = ({
  label,
  required = false,
  error,
  helperText,
  children,
  htmlFor,
  labelContent,
  className = '',
  disabled = false,
}) => {
  // Generate unique IDs for accessibility
  const fieldId = htmlFor || `field-${Math.random().toString(36).substr(2, 9)}`;
  const errorId = error ? `${fieldId}-error` : undefined;
  const helperTextId = helperText ? `${fieldId}-helper` : undefined;

  const wrapperClasses = ['space-y-1', className].filter(Boolean).join(' ');

  return (
    <div className={wrapperClasses}>
      {/* Label */}
      {(label || labelContent) && (
        <label
          htmlFor={fieldId}
          className={`block text-sm font-medium ${
            disabled ? 'text-neutral-400' : 'text-neutral-700'
          }`}
        >
          {labelContent || label}
          {required && (
            <span className='ml-1 text-danger-500' aria-label='required'>
              *
            </span>
          )}
        </label>
      )}

      {/* Form control */}
      <div>
        {React.Children.map(children, child => {
          if (React.isValidElement(child)) {
            // Clone the child element and pass down the necessary props
            return React.cloneElement(child, {
              id: fieldId,
              'aria-describedby':
                [child.props['aria-describedby'], errorId, helperTextId]
                  .filter(Boolean)
                  .join(' ') || undefined,
              'aria-required': required,
              'aria-invalid': !!error,
              disabled: disabled || child.props.disabled,
            } as React.HTMLAttributes<HTMLElement>);
          }
          return child;
        })}
      </div>

      {/* Error message */}
      {error && (
        <p
          id={errorId}
          className='text-sm text-danger-600'
          role='alert'
          aria-live='polite'
        >
          {error}
        </p>
      )}

      {/* Helper text */}
      {helperText && !error && (
        <p id={helperTextId} className='text-sm text-neutral-500'>
          {helperText}
        </p>
      )}
    </div>
  );
};

FormField.displayName = 'FormField';
