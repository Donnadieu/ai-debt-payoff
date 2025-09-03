import { InputHTMLAttributes } from 'react';
import { BaseComponentProps } from '../Button/Button.types';

// Input-specific types
export type InputType = 'text' | 'number' | 'email' | 'password' | 'tel' | 'url';
export type ValidationState = 'default' | 'error' | 'success';

// Input props extending base props and native input attributes
export interface InputProps extends BaseComponentProps, Omit<InputHTMLAttributes<HTMLInputElement>, 'size'> {
  /**
   * Input type
   */
  type?: InputType;
  /**
   * Input validation state
   */
  validationState?: ValidationState;
  /**
   * Placeholder text
   */
  placeholder?: string;
  /**
   * Whether the input should take full width
   */
  fullWidth?: boolean;
  /**
   * Error message to display
   */
  error?: string;
  /**
   * Whether the input is required
   */
  required?: boolean;
  /**
   * Help text to display below the input
   */
  helperText?: string;
}