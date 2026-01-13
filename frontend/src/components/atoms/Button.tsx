/**
 * Button Component (Atom)
 * Based on DESIGN_SYSTEM.md specifications
 */

import type { ButtonHTMLAttributes, ReactNode } from 'react';
import { cn } from '@utils/cn';
import { Loader2 } from 'lucide-react';

export type ButtonVariant = 'primary' | 'secondary' | 'outline' | 'ghost' | 'destructive';
export type ButtonSize = 'sm' | 'md' | 'lg';

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
  isLoading?: boolean;
  children: ReactNode;
}

const variantClasses: Record<ButtonVariant, string> = {
  primary: 'bg-gradient-to-r from-primary to-primary-dark text-white hover:from-primary-dark hover:to-primary shadow-lg shadow-primary/30 hover:shadow-xl hover:shadow-primary/40',
  secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80 shadow-md',
  outline: 'border border-border bg-transparent hover:bg-accent hover:text-accent-foreground',
  ghost: 'hover:bg-accent hover:text-accent-foreground',
  destructive: 'bg-gradient-to-r from-error to-error-dark text-white hover:from-error-dark hover:to-error shadow-lg shadow-error/30 hover:shadow-xl hover:shadow-error/40',
};

const sizeClasses: Record<ButtonSize, string> = {
  sm: 'h-8 px-3 text-sm rounded-xl',
  md: 'h-10 px-4 text-base rounded-xl',
  lg: 'h-12 px-6 text-lg rounded-2xl',
};

export function Button({
  variant = 'primary',
  size = 'md',
  isLoading = false,
  disabled,
  className,
  children,
  ...props
}: ButtonProps) {
  return (
    <button
      type="button"
      className={cn(
        'inline-flex items-center justify-center font-medium transition-all duration-200',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-border-focus focus-visible:ring-offset-2',
        'disabled:pointer-events-none disabled:opacity-50',
        'hover:scale-105 active:scale-95',
        variantClasses[variant],
        sizeClasses[size],
        className
      )}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading && <Loader2 className="h-4 w-4 mr-2 animate-spin" />}
      {children}
    </button>
  );
}

export default Button;
