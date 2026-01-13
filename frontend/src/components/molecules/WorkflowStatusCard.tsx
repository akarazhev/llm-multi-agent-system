/**
 * WorkflowStatusCard Component (Molecule)
 * Enhanced workflow card with status visualization
 * Based on OPERATIONAL_DASHBOARD_RESEARCH.md Phase 1.1
 */

import { useState } from 'react';
import { Link } from 'react-router-dom';
import { cn } from '@utils/cn';
import { Badge, Button, Card } from '@components/atoms';
import type { Workflow, WorkflowStatus } from '@/types/workflow';
import { 
  ChevronDown, 
  ChevronUp, 
  Play, 
  Square, 
  RotateCcw, 
  Clock, 
  User,
  CheckCircle2,
  XCircle,
  Loader2,
  AlertCircle,
  Ban
} from 'lucide-react';

export interface WorkflowStatusCardProps {
  workflow: Workflow;
  onStart?: (workflowId: string) => void;
  onStop?: (workflowId: string) => void;
  onCancel?: (workflowId: string) => void;
  onRetry?: (workflowId: string) => void;
  className?: string;
}

const statusConfig: Record<WorkflowStatus, { 
  color: string; 
  bgColor: string; 
  icon: React.ReactNode;
  label: string;
  animate?: boolean;
}> = {
  pending: { 
    color: 'text-gray-600', 
    bgColor: 'bg-gray-100 dark:bg-gray-800',
    icon: <Clock className="h-5 w-5" />,
    label: 'Pending'
  },
  running: { 
    color: 'text-blue-600', 
    bgColor: 'bg-blue-100 dark:bg-blue-900/30',
    icon: <Loader2 className="h-5 w-5 animate-spin" />,
    label: 'Running',
    animate: true
  },
  completed: { 
    color: 'text-green-600', 
    bgColor: 'bg-green-100 dark:bg-green-900/30',
    icon: <CheckCircle2 className="h-5 w-5" />,
    label: 'Completed'
  },
  failed: { 
    color: 'text-red-600', 
    bgColor: 'bg-red-100 dark:bg-red-900/30',
    icon: <XCircle className="h-5 w-5" />,
    label: 'Failed'
  },
  cancelled: { 
    color: 'text-orange-600', 
    bgColor: 'bg-orange-100 dark:bg-orange-900/30',
    icon: <Ban className="h-5 w-5" />,
    label: 'Cancelled'
  },
};

export function WorkflowStatusCard({
  workflow,
  onStart,
  onStop,
  onCancel,
  onRetry,
  className,
}: WorkflowStatusCardProps) {
  const [isExpanded, setIsExpanded] = useState(false);
  const status = statusConfig[workflow.status] || statusConfig.pending;
  
  // Calculate progress percentage based on steps
  const progress = workflow.current_step && workflow.total_steps 
    ? Math.round((workflow.current_step / workflow.total_steps) * 100)
    : 0;

  // Format execution time
  const formatTime = (dateStr?: string) => {
    if (!dateStr) return 'N/A';
    const date = new Date(dateStr);
    return date.toLocaleString();
  };

  const getExecutionDuration = () => {
    if (!workflow.created_at) return null;
    const start = new Date(workflow.created_at);
    const end = workflow.completed_at ? new Date(workflow.completed_at) : new Date();
    const diff = end.getTime() - start.getTime();
    const minutes = Math.floor(diff / 60000);
    const seconds = Math.floor((diff % 60000) / 1000);
    return `${minutes}m ${seconds}s`;
  };

  return (
    <Card 
      variant="elevated" 
      className={cn(
        'p-6 rounded-2xl shadow-lg transition-all duration-300 hover:shadow-xl',
        status.animate && 'ring-2 ring-blue-400/50 ring-offset-2',
        className
      )}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <Link 
            to={`/workflows/${workflow.workflow_id}`}
            className="text-lg font-semibold hover:text-primary transition-colors"
          >
            {workflow.workflow_id}
          </Link>
          {workflow.request_id && (
            <p className="text-sm text-text-secondary mt-1">
              Request: {workflow.request_id}
            </p>
          )}
        </div>
        
        {/* Status Badge - Large */}
        <div className={cn(
          'flex items-center gap-2 px-4 py-2 rounded-full h-10',
          status.bgColor,
          status.color
        )}>
          {status.icon}
          <span className="font-medium">{status.label}</span>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="mb-4">
        <div className="flex items-center justify-between text-sm mb-2">
          <span className="text-text-secondary">Progress</span>
          <span className="font-medium">{progress}%</span>
        </div>
        <div className="h-3 bg-background-tertiary rounded-full overflow-hidden">
          <div 
            className={cn(
              'h-full rounded-full transition-all duration-500',
              workflow.status === 'completed' && 'bg-green-500',
              workflow.status === 'running' && 'bg-blue-500 animate-pulse',
              workflow.status === 'failed' && 'bg-red-500',
              workflow.status === 'pending' && 'bg-gray-400',
              workflow.status === 'cancelled' && 'bg-orange-500',
            )}
            style={{ width: `${progress}%` }}
          />
        </div>
        {workflow.current_step && workflow.total_steps && (
          <p className="text-xs text-text-tertiary mt-1">
            Step {workflow.current_step} of {workflow.total_steps}
          </p>
        )}
      </div>

      {/* Agent Assignment & Time */}
      <div className="flex items-center gap-4 mb-4 text-sm">
        {workflow.current_agent && (
          <div className="flex items-center gap-2 text-text-secondary">
            <User className="h-4 w-4" />
            <span>{workflow.current_agent}</span>
          </div>
        )}
        <div className="flex items-center gap-2 text-text-secondary">
          <Clock className="h-4 w-4" />
          <span>{getExecutionDuration() || 'N/A'}</span>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="flex items-center gap-2 mb-4">
        {workflow.status === 'pending' && onStart && (
          <Button size="sm" variant="primary" onClick={() => onStart(workflow.workflow_id)}>
            <Play className="h-4 w-4 mr-1" />
            Start
          </Button>
        )}
        {workflow.status === 'running' && onStop && (
          <Button size="sm" variant="destructive" onClick={() => onStop(workflow.workflow_id)}>
            <Square className="h-4 w-4 mr-1" />
            Stop
          </Button>
        )}
        {(workflow.status === 'running' || workflow.status === 'pending') && onCancel && (
          <Button size="sm" variant="outline" onClick={() => onCancel(workflow.workflow_id)}>
            <Ban className="h-4 w-4 mr-1" />
            Cancel
          </Button>
        )}
        {workflow.status === 'failed' && onRetry && (
          <Button size="sm" variant="secondary" onClick={() => onRetry(workflow.workflow_id)}>
            <RotateCcw className="h-4 w-4 mr-1" />
            Retry
          </Button>
        )}
        <Link to={`/workflows/${workflow.workflow_id}`}>
          <Button size="sm" variant="ghost">
            View Details
          </Button>
        </Link>
      </div>

      {/* Expandable Details */}
      <div className="border-t border-border pt-4">
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="flex items-center gap-2 text-sm text-text-secondary hover:text-text-primary transition-colors w-full"
        >
          {isExpanded ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
          {isExpanded ? 'Hide Details' : 'Show Details'}
        </button>
        
        {isExpanded && (
          <div className="mt-4 space-y-3 text-sm">
            <div className="flex justify-between">
              <span className="text-text-secondary">Created:</span>
              <span>{formatTime(workflow.created_at)}</span>
            </div>
            {workflow.completed_at && (
              <div className="flex justify-between">
                <span className="text-text-secondary">Completed:</span>
                <span>{formatTime(workflow.completed_at)}</span>
              </div>
            )}
            {workflow.error && (
              <div className="p-3 bg-red-50 dark:bg-red-900/20 rounded-lg">
                <div className="flex items-start gap-2">
                  <AlertCircle className="h-4 w-4 text-red-600 mt-0.5" />
                  <p className="text-red-600">{workflow.error}</p>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </Card>
  );
}
