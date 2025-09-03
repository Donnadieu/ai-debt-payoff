import React from 'react';
import { BreadcrumbsProps } from './Navigation.types';

export const Breadcrumbs: React.FC<BreadcrumbsProps> = ({
  items,
  separator,
  className = '',
}) => {
  const defaultSeparator = (
    <svg
      className="w-4 h-4 text-neutral-400"
      fill="currentColor"
      viewBox="0 0 20 20"
      aria-hidden="true"
    >
      <path
        fillRule="evenodd"
        d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
        clipRule="evenodd"
      />
    </svg>
  );

  return (
    <nav className={`flex ${className}`} aria-label="Breadcrumb">
      <ol className="flex items-center space-x-2">
        {items.map((item, index) => (
          <li key={index} className="flex items-center">
            {index > 0 && (
              <span className="mx-2" aria-hidden="true">
                {separator || defaultSeparator}
              </span>
            )}
            {item.href ? (
              <a
                href={item.href}
                className="text-sm font-medium text-neutral-500 hover:text-neutral-700 transition-colors"
              >
                {item.label}
              </a>
            ) : (
              <span
                className="text-sm font-medium text-neutral-900"
                aria-current="page"
              >
                {item.label}
              </span>
            )}
          </li>
        ))}
      </ol>
    </nav>
  );
};
