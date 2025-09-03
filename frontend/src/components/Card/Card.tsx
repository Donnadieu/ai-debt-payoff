import React, { forwardRef } from 'react';
import { cn } from '../../utils';
import {
  CardProps,
  CardHeaderProps,
  CardBodyProps,
  CardFooterProps,
  CardPadding,
  CardBorder,
  CardShadow,
  CardHoverEffect,
} from './Card.types';

/**
 * Get padding classes based on padding variant
 */
const getPaddingClasses = (padding: CardPadding): string => {
  switch (padding) {
    case 'none':
      return '';
    case 'sm':
      return 'p-3';
    case 'md':
      return 'p-4';
    case 'lg':
      return 'p-6';
    default:
      return 'p-4';
  }
};

/**
 * Get border classes based on border variant
 */
const getBorderClasses = (border: CardBorder): string => {
  switch (border) {
    case 'none':
      return '';
    case 'sm':
      return 'border border-gray-200';
    case 'md':
      return 'border-2 border-gray-200';
    case 'lg':
      return 'border-4 border-gray-200';
    default:
      return 'border border-gray-200';
  }
};

/**
 * Get shadow classes based on shadow variant
 */
const getShadowClasses = (shadow: CardShadow): string => {
  switch (shadow) {
    case 'none':
      return '';
    case 'sm':
      return 'shadow-sm';
    case 'md':
      return 'shadow-md';
    case 'lg':
      return 'shadow-lg';
    case 'xl':
      return 'shadow-xl';
    default:
      return 'shadow-sm';
  }
};

/**
 * Get hover effect classes based on hover effect variant
 */
const getHoverEffectClasses = (hoverEffect: CardHoverEffect): string => {
  switch (hoverEffect) {
    case 'none':
      return '';
    case 'lift':
      return 'hover:shadow-lg hover:-translate-y-1 transition-all duration-200';
    case 'glow':
      return 'hover:shadow-lg hover:shadow-blue-500/25 transition-all duration-200';
    case 'scale':
      return 'hover:scale-105 transition-transform duration-200';
    default:
      return '';
  }
};

/**
 * Get background classes based on background variant
 */
const getBackgroundClasses = (background: string): string => {
  switch (background) {
    case 'subtle':
      return 'bg-gray-50';
    case 'accent':
      return 'bg-blue-50';
    default:
      return 'bg-white';
  }
};

/**
 * CardHeader component for card headers
 */
export const CardHeader = forwardRef<HTMLDivElement, CardHeaderProps>(
  (
    {
      className,
      title,
      subtitle,
      actions,
      divider = false,
      children,
      ...props
    },
    ref
  ) => {
    return (
      <div
        ref={ref}
        className={cn(
          'flex items-start justify-between',
          divider && 'border-b border-gray-200 pb-4 mb-4',
          className
        )}
        {...props}
      >
        <div className='flex-1'>
          {title && (
            <h3 className='text-lg font-semibold text-gray-900 mb-1'>
              {title}
            </h3>
          )}
          {subtitle && <p className='text-sm text-gray-500'>{subtitle}</p>}
          {children}
        </div>
        {actions && (
          <div className='flex items-center space-x-2 ml-4'>{actions}</div>
        )}
      </div>
    );
  }
);

CardHeader.displayName = 'CardHeader';

/**
 * CardBody component for card content
 */
export const CardBody = forwardRef<HTMLDivElement, CardBodyProps>(
  ({ className, children, padding, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(
          'flex-1',
          padding && getPaddingClasses(padding),
          className
        )}
        {...props}
      >
        {children}
      </div>
    );
  }
);

CardBody.displayName = 'CardBody';

/**
 * CardFooter component for card footers
 */
export const CardFooter = forwardRef<HTMLDivElement, CardFooterProps>(
  (
    { className, children, actions, divider = false, align = 'left', ...props },
    ref
  ) => {
    const alignClasses = {
      left: 'justify-start',
      center: 'justify-center',
      right: 'justify-end',
      between: 'justify-between',
    };

    return (
      <div
        ref={ref}
        className={cn(
          'flex items-center',
          alignClasses[align],
          divider && 'border-t border-gray-200 pt-4 mt-4',
          className
        )}
        {...props}
      >
        <div className='flex-1'>{children}</div>
        {actions && (
          <div className='flex items-center space-x-2 ml-4'>{actions}</div>
        )}
      </div>
    );
  }
);

CardFooter.displayName = 'CardFooter';

/**
 * Loading skeleton component for cards
 */
const CardSkeleton: React.FC<{ className?: string }> = ({ className }) => {
  return (
    <div className={cn('animate-pulse', className)}>
      <div className='h-4 bg-gray-200 rounded w-3/4 mb-3'></div>
      <div className='h-3 bg-gray-200 rounded w-1/2 mb-4'></div>
      <div className='space-y-2'>
        <div className='h-3 bg-gray-200 rounded'></div>
        <div className='h-3 bg-gray-200 rounded w-5/6'></div>
        <div className='h-3 bg-gray-200 rounded w-4/6'></div>
      </div>
    </div>
  );
};

/**
 * Card component for content containers
 */
export const Card = forwardRef<HTMLDivElement, CardProps>(
  (
    {
      className,
      id,
      children,
      header,
      footer,
      padding = 'md',
      border = 'sm',
      shadow = 'sm',
      hoverEffect = 'none',
      selected = false,
      clickable = false,
      background = 'default',
      loading = false,
      onClick,
      'data-testid': dataTestId,
      ...props
    },
    ref
  ) => {
    const isClickable = clickable || !!onClick;

    const cardClasses = cn(
      // Base styles
      'rounded-lg overflow-hidden transition-all duration-200',

      // Background
      getBackgroundClasses(background),

      // Border
      getBorderClasses(border),

      // Shadow
      getShadowClasses(shadow),

      // Padding
      getPaddingClasses(padding),

      // Hover effects
      getHoverEffectClasses(hoverEffect),

      // Clickable styles
      isClickable && 'cursor-pointer',

      // Selected state
      selected && 'ring-2 ring-blue-500 ring-opacity-50 border-blue-300',

      // Focus styles for accessibility
      isClickable &&
        'focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50',

      className
    );

    const handleClick = (event: React.MouseEvent<HTMLDivElement>) => {
      if (onClick && !loading) {
        onClick(event);
      }
    };

    const handleKeyDown = (event: React.KeyboardEvent<HTMLDivElement>) => {
      if (
        isClickable &&
        !loading &&
        (event.key === 'Enter' || event.key === ' ')
      ) {
        event.preventDefault();
        const mouseEvent = new MouseEvent('click', {
          bubbles: true,
          cancelable: true,
        });
        handleClick(mouseEvent as React.MouseEvent<HTMLDivElement>);
      }
    };

    return (
      <div
        ref={ref}
        id={id}
        className={cardClasses}
        onClick={handleClick}
        onKeyDown={handleKeyDown}
        tabIndex={isClickable ? 0 : undefined}
        role={isClickable ? 'button' : undefined}
        aria-pressed={isClickable && selected ? selected : undefined}
        aria-disabled={loading}
        data-testid={dataTestId}
        {...props}
      >
        {loading ? (
          <CardSkeleton />
        ) : (
          <>
            {header && <CardHeader>{header}</CardHeader>}

            <CardBody>{children}</CardBody>

            {footer && <CardFooter>{footer}</CardFooter>}
          </>
        )}
      </div>
    );
  }
);

Card.displayName = 'Card';

// Export all components
export { CardHeader, CardBody, CardFooter };
export default Card;
