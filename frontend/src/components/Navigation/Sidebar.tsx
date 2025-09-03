import React from 'react';
import { SidebarProps } from './Navigation.types';
import { Button } from '../Button/Button';

export const Sidebar: React.FC<SidebarProps> = ({
  navigationItems,
  isCollapsed = false,
  onToggleCollapse,
  className = '',
}) => {
  return (
    <aside className={`bg-neutral-50 border-r border-neutral-200 transition-all duration-300 ${
      isCollapsed ? 'w-16' : 'w-64'
    } ${className}`}>
      <div className="flex flex-col h-full">
        {/* Toggle Button */}
        {onToggleCollapse && (
          <div className="p-4 border-b border-neutral-200">
            <Button
              variant="outline"
              size="sm"
              onClick={onToggleCollapse}
              className="w-full justify-center"
              aria-label={isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
            >
              <svg
                className={`w-4 h-4 transition-transform ${isCollapsed ? 'rotate-180' : ''}`}
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                aria-hidden="true"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M11 19l-7-7 7-7m8 14l-7-7 7-7"
                />
              </svg>
            </Button>
          </div>
        )}

        {/* Navigation */}
        <nav className="flex-1 p-4 space-y-2">
          {navigationItems.map((item, index) => (
            <a
              key={index}
              href={item.href}
              className={`flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors ${
                item.isActive
                  ? 'bg-primary-100 text-primary-700'
                  : 'text-neutral-600 hover:bg-neutral-100 hover:text-neutral-900'
              } ${item.disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
              aria-current={item.isActive ? 'page' : undefined}
              aria-disabled={item.disabled}
              title={isCollapsed ? item.label : undefined}
            >
              {item.icon && (
                <span className={`flex-shrink-0 ${isCollapsed ? '' : 'mr-3'}`} aria-hidden="true">
                  {item.icon}
                </span>
              )}
              {!isCollapsed && (
                <span className="truncate">{item.label}</span>
              )}
            </a>
          ))}
        </nav>
      </div>
    </aside>
  );
};
