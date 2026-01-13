/**
 * Toast Component (Molecule)
 * Notification messages for user feedback
 */

import { useEffect } from 'react';
import { Card } from '@components/atoms/Card';
import { cn } from '@utils/cn';
import { X, CheckCircle, AlertCircle, Info, AlertTriangle } from 'lucide-react';
import Button from '@components/atoms/Button';

export type ToastType = 'success' | 'error' | 'info' | 'warning';

export interface ToastProps {
  id: string;
  type: ToastType;
  message: string;
  duration?: number;
  onClose: (id: string) => void;
}

const typeConfig: Record<ToastType, { icon: typeof CheckCircle; bgColor: string; iconColor: string }> = {
  success: {
    icon: CheckCircle,
    bgColor: 'bg-success/10 border-success',
    iconColor: 'text-success',
  },
  error: {
    icon: AlertCircle,
    bgColor: 'bg-error/10 border-error',
    iconColor: 'text-error',
  },
  warning: {
    icon: AlertTriangle,
    bgColor: 'bg-warning/10 border-warning',
    iconColor: 'text-warning',
  },
  info: {
    icon: Info,
    bgColor: 'bg-info/10 border-info',
    iconColor: 'text-info',
  },
};

export function Toast({ id, type, message, duration = 5000, onClose }: ToastProps) {
  const config = typeConfig[type];
  const Icon = config.icon;

  useEffect(() => {
    if (duration > 0) {
      const timer = setTimeout(() => {
        onClose(id);
      }, duration);

      return () => clearTimeout(timer);
    }
  }, [id, duration, onClose]);

  return (
    <Card
      variant="elevated"
      className={cn(
        'min-w-[300px] max-w-[500px] border-l-4 shadow-lg',
        config.bgColor
      )}
    >
      <div className="flex items-start gap-3 p-4">
        <Icon className={cn('h-5 w-5 mt-0.5 flex-shrink-0', config.iconColor)} />
        <p className="flex-1 text-sm text-text-primary">{message}</p>
        <Button
          variant="ghost"
          size="sm"
          onClick={() => onClose(id)}
          className="h-6 w-6 p-0 flex-shrink-0"
          aria-label="Close notification"
        >
          <X className="h-4 w-4" />
        </Button>
      </div>
    </Card>
  );
}
