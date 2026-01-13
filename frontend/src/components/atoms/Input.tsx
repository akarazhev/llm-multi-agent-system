/**
 * Input Component (Atom)
 * Based on DESIGN_SYSTEM.md specifications
 */

import type { InputHTMLAttributes } from 'react';
import { forwardRef } from 'react';
import { cn } from '@utils/cn';

export interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  error?: boolean;
  helperText?: string;
  errorMessage?: string;
}

const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ className, type = 'text', error, helperText, errorMessage, ...props }, ref) => {
    const baseStyles = 'flex h-10 w-full rounded-xl border bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-text-tertiary focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-border-focus focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 shadow-sm focus:shadow-md transition-all duration-200';
    
    const errorStyles = error ? 'border-error focus-visible:ring-error' : 'border-border';

    return (
      <div className="w-full">
        <input
          type={type}
          className={cn(baseStyles, errorStyles, className)}
          ref={ref}
          aria-invalid={error}
          aria-describedby={error ? 'error-message' : helperText ? 'helper-text' : undefined}
          {...props}
        />
        {helperText && !error && (
          <p id="helper-text" className="mt-1 text-xs text-text-secondary">
            {helperText}
          </p>
        )}
        {error && errorMessage && (
          <p id="error-message" className="mt-1 text-xs text-error" role="alert">
            {errorMessage}
          </p>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';

export default Input;
