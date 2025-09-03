import React from 'react';
import { HeaderProps } from './Navigation.types';
import { Button } from '../Button/Button';

export const Header: React.FC<HeaderProps> = ({
  brand,
  navigationItems = [],
  userMenu,
  className = '',
}) => {
  return (
    <header className={`bg-white shadow-sm border-b border-neutral-200 ${className}`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Brand/Logo */}
          <div className="flex-shrink-0">
            {brand || (
              <div className="text-xl font-bold text-primary-600">
                Debt Payoff
              </div>
            )}
          </div>

          {/* Navigation */}
          <nav className="hidden md:flex space-x-8">
            {navigationItems.map((item, index) => (
              <a
                key={index}
                href={item.href}
                className={`inline-flex items-center px-1 pt-1 text-sm font-medium transition-colors ${
                  item.isActive
                    ? 'text-primary-600 border-b-2 border-primary-600'
                    : 'text-neutral-500 hover:text-neutral-700 hover:border-neutral-300'
                } ${item.disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
                aria-current={item.isActive ? 'page' : undefined}
                aria-disabled={item.disabled}
              >
                {item.icon && (
                  <span className="mr-2" aria-hidden="true">
                    {item.icon}
                  </span>
                )}
                {item.label}
              </a>
            ))}
          </nav>

          {/* User Menu */}
          <div className="flex items-center space-x-4">
            {userMenu || (
              <Button variant="outline" size="sm">
                Sign In
              </Button>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <Button
              variant="outline"
              size="sm"
              aria-label="Open mobile menu"
            >
              <svg
                className="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                aria-hidden="true"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 6h16M4 12h16M4 18h16"
                />
              </svg>
            </Button>
          </div>
        </div>
      </div>
    </header>
  );
};
