// Component exports will be added here as components are created
// Example:
// export { Button } from './ui/Button';
// export { Layout } from './layout/Layout';
// export { DebtCard } from './debt/DebtCard';

// UI Components
export { Button } from './Button';
export type { ButtonProps, Size, Variant, BaseComponentProps } from './Button';

export { Input } from './Input';
export type { InputProps, InputType, ValidationState } from './Input';

export { Select } from './Select';
export type { SelectProps, SelectOption } from './Select';

export { Card } from './Card/Card';
export type { CardProps } from './Card/Card.types';

export { Modal } from './Modal/Modal';
export type { ModalProps } from './Modal/Modal.types';

export { FormField } from './FormField/FormField';
export type { FormFieldProps } from './FormField/FormField.types';

// Loading Components
export { Spinner } from './Loading/Spinner';
export { Skeleton } from './Loading/Skeleton';

// Alert Components
export { Alert } from './Alert/Alert';
export type { AlertProps } from './Alert/Alert.types';

// Navigation Components
export { Header } from './Navigation/Header';
export { Sidebar } from './Navigation/Sidebar';
export { Breadcrumbs } from './Navigation/Breadcrumbs';
export type {
  HeaderProps,
  SidebarProps,
  BreadcrumbsProps,
  NavigationItem,
  BreadcrumbItem,
} from './Navigation/Navigation.types';

export {};
