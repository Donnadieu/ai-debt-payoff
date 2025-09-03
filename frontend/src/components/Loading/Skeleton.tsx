import React, { forwardRef } from 'react';
import type { SkeletonProps } from './Loading.types';

const variantClasses = {
  text: 'rounded-md',
  circular: 'rounded-full',
  rectangular: 'rounded-lg',
};

const animationClasses = {
  pulse: 'animate-pulse',
  wave: 'animate-pulse', // Using pulse as wave is more complex, could be enhanced later
  none: '',
};

const Skeleton = forwardRef<HTMLDivElement, SkeletonProps>(
  (
    {
      variant = 'rectangular',
      animation = 'pulse',
      width,
      height,
      className = '',
      lines = 1,
      ...props
    },
    ref
  ) => {
    const variantClass = variantClasses[variant];
    const animationClass = animationClasses[animation];

    // Style object for dynamic dimensions
    const style: React.CSSProperties = {};
    if (width !== undefined) {
      style.width = typeof width === 'number' ? `${width}px` : width;
    }
    if (height !== undefined) {
      style.height = typeof height === 'number' ? `${height}px` : height;
    }

    // For text variant with multiple lines
    if (variant === 'text' && lines > 1) {
      return (
        <div
          ref={ref}
          className={`space-y-2 ${className}`}
          role='status'
          aria-label='Loading content...'
          {...props}
        >
          {Array.from({ length: lines }, (_, index) => (
            <div
              key={index}
              className={`bg-gray-300 h-4 ${variantClass} ${animationClass} ${
                index === lines - 1 ? 'w-3/4' : 'w-full'
              }`}
              style={index === 0 ? style : undefined}
            />
          ))}
          <span className='sr-only'>Loading content...</span>
        </div>
      );
    }

    // Default dimensions based on variant
    const defaultStyle: React.CSSProperties = {
      ...style,
    };

    if (!width && !height) {
      switch (variant) {
        case 'text':
          defaultStyle.width = '100%';
          defaultStyle.height = '1rem';
          break;
        case 'circular':
          defaultStyle.width = '2.5rem';
          defaultStyle.height = '2.5rem';
          break;
        case 'rectangular':
          defaultStyle.width = '100%';
          defaultStyle.height = '8rem';
          break;
      }
    }

    return (
      <div
        ref={ref}
        className={`bg-gray-300 ${variantClass} ${animationClass} ${className}`}
        style={defaultStyle}
        role='status'
        aria-label='Loading content...'
        {...props}
      >
        <span className='sr-only'>Loading content...</span>
      </div>
    );
  }
);

Skeleton.displayName = 'Skeleton';

export { Skeleton };
export default Skeleton;
