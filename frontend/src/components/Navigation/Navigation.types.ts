export interface NavigationItem {
  label: string;
  href: string;
  icon?: React.ReactNode;
  isActive?: boolean;
  disabled?: boolean;
}

export interface HeaderProps {
  /** Brand/logo content */
  brand?: React.ReactNode;
  /** Navigation items */
  navigationItems?: NavigationItem[];
  /** User menu content */
  userMenu?: React.ReactNode;
  /** Additional CSS classes */
  className?: string;
}

export interface SidebarProps {
  /** Navigation items */
  navigationItems: NavigationItem[];
  /** Whether the sidebar is collapsed */
  isCollapsed?: boolean;
  /** Function to toggle sidebar collapse */
  onToggleCollapse?: () => void;
  /** Additional CSS classes */
  className?: string;
}

export interface BreadcrumbItem {
  label: string;
  href?: string;
}

export interface BreadcrumbsProps {
  /** Array of breadcrumb items */
  items: BreadcrumbItem[];
  /** Separator between items */
  separator?: React.ReactNode;
  /** Additional CSS classes */
  className?: string;
}
