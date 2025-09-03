import React, { forwardRef } from 'react';
import { TextField, TextFieldProps as MuiTextFieldProps } from '@mui/material';
import type { InputProps, ValidationState } from './Input.types';
import type { Size } from '../Button/Button.types';

// Map our custom sizes to MUI sizes
const getMuiSize = (size: Size): 'small' | 'medium' => {
  return size === 'sm' ? 'small' : 'medium';
};

// Map our custom validation state to MUI color and error state
const getMuiProps = (validationState: ValidationState, error?: string): {
  error: boolean;
  color: MuiTextFieldProps['color'];
} => {
  if (error || validationState === 'error') {
    return { error: true, color: 'primary' };
  }
  if (validationState === 'success') {
    return { error: false, color: 'success' };
  }
  return { error: false, color: 'primary' };
};

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
      placeholder,
      ...props
    },
    ref
  ) => {
    const muiSize = getMuiSize(size);
    const { error: hasError, color } = getMuiProps(validationState, error);

    // Determine helper text to display
    const displayHelperText = error || helperText;

    return (
      <TextField
        inputRef={ref}
        type={type}
        size={muiSize}
        fullWidth={fullWidth}
        disabled={disabled}
        required={required}
        error={hasError}
        color={color}
        placeholder={placeholder}
        helperText={displayHelperText}
        className={className}
        variant="outlined"
        {...props}
      />
    );
  }
);

Input.displayName = 'Input';
