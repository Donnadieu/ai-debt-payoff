import { ReactNode } from 'react';
import { BaseComponentProps } from '../Button/Button.types';

// FormField props for wrapping form inputs with labels and help text
export interface FormFieldProps extends BaseComponentProps {
  /**
   * Label text for the form field
   */
  label?: string;
  /**
   * Whether the field is required (shows asterisk)
   */
  required?: boolean;
  /**
   * Error message to display
   */
  error?: string;
  /**
   * Help text to display below the field
   */
  helperText?: string;
  /**
   * The form control element (input, textarea, select, etc.)
   */
  children: ReactNode;
  /**
   * ID of the form control for accessibility
   */
  htmlFor?: string;
  /**
   * Custom label content (overrides label prop)
   */
  labelContent?: ReactNode;
}