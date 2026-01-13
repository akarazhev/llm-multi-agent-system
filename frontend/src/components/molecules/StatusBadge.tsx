/**
 * StatusBadge Component (Molecule)
 * Based on DESIGN_SYSTEM.md specifications
 */

import { Badge } from '@components/atoms/Badge';
import type { WorkflowStatus } from '@/types/workflow';

export interface StatusBadgeProps {
  status: WorkflowStatus | 'active' | 'idle' | 'error';
  type?: 'workflow' | 'agent';
}

const statusConfig: Record<string, { variant: 'default' | 'success' | 'warning' | 'destructive' | 'secondary'; label: string }> = {
  // Workflow statuses
  pending: { variant: 'secondary', label: 'Pending' },
  running: { variant: 'default', label: 'Running' },
  completed: { variant: 'success', label: 'Completed' },
  failed: { variant: 'destructive', label: 'Failed' },
  cancelled: { variant: 'secondary', label: 'Cancelled' },
  // Agent statuses
  active: { variant: 'success', label: 'Active' },
  idle: { variant: 'secondary', label: 'Idle' },
  error: { variant: 'destructive', label: 'Error' },
};

export function StatusBadge({ status }: StatusBadgeProps) {
  const config = statusConfig[status] || { variant: 'secondary' as const, label: status };
  
  return (
    <Badge variant={config.variant}>
      {config.label}
    </Badge>
  );
}
