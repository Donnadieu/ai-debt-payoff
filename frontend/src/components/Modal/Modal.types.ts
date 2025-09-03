export interface ModalProps {
  /** Whether the modal is open */
  isOpen: boolean;
  /** Function to call when the modal should be closed */
  onClose: () => void;
  /** Optional title for the modal */
  title?: string;
  /** Modal content */
  children: React.ReactNode;
  /** Size of the modal */
  size?: 'sm' | 'md' | 'lg' | 'xl';
  /** Whether to show the close button in the header */
  showCloseButton?: boolean;
  /** Whether clicking the overlay should close the modal */
  closeOnOverlayClick?: boolean;
  /** Whether pressing Escape should close the modal */
  closeOnEscape?: boolean;
  /** Additional CSS classes */
  className?: string;
}
