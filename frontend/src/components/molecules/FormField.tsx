/**
 * FormField Component (Molecule)
 * Based on DESIGN_SYSTEM.md specifications
 */

import type { ReactNode } from 'react';

export interface FormFieldProps {
  id: string;
  label: string;
  required?: boolean;
  error?: boolean;
  errorMessage?: string;
  helperText?: string;
  children: ReactNode;
}

export function FormField({
  id,
  label,
  required = false,
  error = false,
  errorMessage,
  helperText,
  children,
}: FormFieldProps) {
  return (
    <div className="space-y-2">
      <label
        htmlFor={id}
        className="text-sm font-medium text-text-primary"
      >
        {label}
        {required && <span className="text-destructive ml-1">*</span>}
      </label>
      {children}
      {error && errorMessage && (
        <p className="text-sm text-destructive" id={`${id}-error`}>
          {errorMessage}
        </p>
      )}
      {!error && helperText && (
        <p className="text-sm text-text-secondary" id={`${id}-helper`}>
          {helperText}
        </p>
      )}
    </div>
  );
}
