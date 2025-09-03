import React from 'react';
import {
  Select as MuiSelect,
  FormControl,
  InputLabel,
  MenuItem,
  FormHelperText,
  SelectChangeEvent,
} from '@mui/material';

export interface SelectOption {
  value: string;
  label: string;
}

export interface SelectProps {
  options: SelectOption[];
  label?: string;
  error?: string;
  placeholder?: string;
  value?: string | string[];
  multiple?: boolean;
  fullWidth?: boolean;
  disabled?: boolean;
  required?: boolean;
  size?: 'small' | 'medium';
  variant?: 'outlined' | 'filled' | 'standard';
  onChange?: (event: SelectChangeEvent<string | string[]>) => void;
  className?: string;
  id?: string;
  name?: string;
}

export const Select = React.forwardRef<HTMLSelectElement, SelectProps>(
  ({
    options,
    label,
    error,
    placeholder,
    value = '',
    multiple = false,
    fullWidth = true,
    disabled = false,
    required = false,
    size = 'medium',
    variant = 'outlined',
    onChange,
    className = '',
    id,
    name,
    ...props
  }, ref) => {
    // Generate a unique ID if not provided
    const selectId = id || `select-${Math.random().toString(36).substr(2, 9)}`;
    const labelId = label ? `${selectId}-label` : undefined;

    return (
      <FormControl
        fullWidth={fullWidth}
        disabled={disabled}
        required={required}
        error={Boolean(error)}
        size={size}
        variant={variant}
        className={className}
      >
        {label && (
          <InputLabel id={labelId}>
            {label}
          </InputLabel>
        )}
        <MuiSelect
          ref={ref}
          id={selectId}
          name={name}
          labelId={labelId}
          label={label}
          value={value}
          multiple={multiple}
          displayEmpty={Boolean(placeholder)}
          onChange={onChange}
          {...props}
        >
          {placeholder && (
            <MenuItem value="" disabled>
              <em>{placeholder}</em>
            </MenuItem>
          )}
          {options.map((option) => (
            <MenuItem key={option.value} value={option.value}>
              {option.label}
            </MenuItem>
          ))}
        </MuiSelect>
        {error && (
          <FormHelperText>{error}</FormHelperText>
        )}
      </FormControl>
    );
  }
);

Select.displayName = 'Select';
