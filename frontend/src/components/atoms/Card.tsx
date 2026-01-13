/**
 * Card Component (Atom)
 * Based on DESIGN_SYSTEM.md specifications
 */

import type { HTMLAttributes, ReactNode } from 'react';
import { cn } from '@utils/cn';

export interface CardProps extends HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'elevated' | 'outlined';
  header?: ReactNode;
  footer?: ReactNode;
}

export function Card({ className, variant = 'default', header, footer, children, ...props }: CardProps) {
  const baseStyles = 'rounded-lg bg-background';
  
  const variants = {
    default: 'border border-border',
    elevated: 'shadow-md border border-border',
    outlined: 'border-2 border-border',
  };

  return (
    <div className={cn(baseStyles, variants[variant], className)} {...props}>
      {header && (
        <div className="px-6 py-4 border-b border-border">
          {header}
        </div>
      )}
      <div className="px-6 py-4">
        {children}
      </div>
      {footer && (
        <div className="px-6 py-4 border-t border-border">
          {footer}
        </div>
      )}
    </div>
  );
}
