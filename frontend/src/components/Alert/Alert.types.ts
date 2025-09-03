// Alert component type definitions

export type AlertVariant = 'success' | 'error' | 'warning' | 'info';
export type AlertSize = 'sm' | 'md' | 'lg';

export interface AlertProps {
  variant?: AlertVariant;
  size?: AlertSize;
  title?: string;
  children: React.ReactNode;
  dismissible?: boolean;
  onDismiss?: () => void;
  className?: string;
  icon?: React.ReactNode | boolean; // Custom icon or true for default variant icon
}

// For programmatic alerts/notifications
export interface NotificationConfig {
  id?: string;
  variant: AlertVariant;
  title?: string;
  message: string;
  duration?: number; // Auto-dismiss after this many ms, 0 or undefined = no auto-dismiss
  dismissible?: boolean;
  action?: {
    label: string;
    onClick: () => void;
  };
}

export interface NotificationState {
  notifications: NotificationConfig[];
}
