import React, { forwardRef } from 'react';
import { Button as MuiButton, CircularProgress, ButtonProps as MuiButtonProps } from '@mui/material';
import type { ButtonProps, Size, Variant } from './Button.types';

// Map our custom sizes to MUI sizes
const getMuiSize = (size: Size): 'small' | 'medium' | 'large' => {
  const sizeMap = {
    sm: 'small' as const,
    md: 'medium' as const,
    lg: 'large' as const,
  };
  return sizeMap[size];
};

// Map our custom variants to MUI variants and colors
const getMuiVariantAndColor = (variant: Variant): { variant: MuiButtonProps['variant']; color: MuiButtonProps['color'] } => {
  switch (variant) {
    case 'primary':
      return { variant: 'contained', color: 'primary' };
    case 'secondary':
      return { variant: 'contained', color: 'secondary' };
    case 'danger':
      return { variant: 'contained', color: 'error' };
    case 'outline':
      return { variant: 'outlined', color: 'primary' };
    default:
      return { variant: 'contained', color: 'primary' };
  }
};

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
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
    },
    ref
  ) => {
    const { variant: muiVariant, color: muiColor } = getMuiVariantAndColor(variant);
    const muiSize = getMuiSize(size);
    const isDisabled = disabled || loading;

    return (
      <MuiButton
        ref={ref}
        variant={muiVariant}
        color={muiColor}
        size={muiSize}
        fullWidth={fullWidth}
        disabled={isDisabled}
        className={className}
        startIcon={loading ? <CircularProgress size={16} color="inherit" /> : startIcon}
        endIcon={!loading ? endIcon : undefined}
        {...props}
      >
        {loading ? 'Loading...' : children}
      </MuiButton>
    );
  }
);

Button.displayName = 'Button';
