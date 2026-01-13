/**
 * WorkflowCard Component (Molecule)
 * Enhanced for Operational Dashboard with progress bar, agent assignment, expandable details
 * Based on OPERATIONAL_DASHBOARD_RESEARCH.md Phase 1.1 specifications
 */

import { useState } from 'react';
import { Card } from '@components/atoms/Card';
import { StatusBadge } from './StatusBadge';
import Button from '@components/atoms/Button';
import type { Workflow } from '@/types/workflow';
import { format } from 'date-fns';
import { 
  X, 
  Clock, 
  User, 
  ChevronDown, 
  ChevronUp,
  Play,
  Square,
  RotateCcw,
  Eye
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { cn } from '@utils/cn';

export interface WorkflowCardProps {
  workflow: Workflow;
  onStart?: (workflowId: string) => void;
  onStop?: (workflowId: string) => void;
  onCancel?: (workflowId: string) => void;
  onRetry?: (workflowId: string) => void;
  showExpandedDetails?: boolean;
}

export function WorkflowCard({ 
  workflow, 
  onStart,
  onStop,
  onCancel,
  onRetry,
  showExpandedDetails = false 
}: WorkflowCardProps) {
  const navigate = useNavigate();
  const [isExpanded, setIsExpanded] = useState(showExpandedDetails);
  
  // Calculate progress percentage (mock - should come from backend)
  const progress = workflow.status === 'completed' ? 100 
    : workflow.status === 'failed' ? 0
    : workflow.status === 'running' ? 65
    : workflow.status === 'pending' ? 0
    : 0;

  // Extract agent from current_step or workflow data (mock)
  const currentStepStr = workflow.current_step ? String(workflow.current_step) : '';
  const assignedAgent = currentStepStr.includes('Agent') 
    ? currentStepStr.split(' ')[0]
    : 'Agent-1';

  // Calculate execution time
  const executionTime = workflow.created_at 
    ? (() => {
        const start = new Date(workflow.created_at);
        const now = new Date();
        const diffMs = now.getTime() - start.getTime();
        const diffMins = Math.floor(diffMs / 60000);
        const diffHours = Math.floor(diffMins / 60);
        
        if (diffHours > 0) return `${diffHours}h ${diffMins % 60}m`;
        if (diffMins > 0) return `${diffMins}m`;
        return 'Just now';
      })()
    : null;

  // Quick action availability
  const canStart = workflow.status === 'pending';
  const canStop = workflow.status === 'running';
  const canCancel = workflow.status === 'pending' || workflow.status === 'running';
  const canRetry = workflow.status === 'failed' || workflow.status === 'cancelled';

  return (
    <Card 
      variant="elevated" 
      className={cn(
        'hover:shadow-xl transition-all duration-200',
        'border-l-4',
        workflow.status === 'running' && 'border-l-blue-500',
        workflow.status === 'completed' && 'border-l-green-500',
        workflow.status === 'failed' && 'border-l-red-500',
        workflow.status === 'pending' && 'border-l-amber-500',
        workflow.status === 'cancelled' && 'border-l-gray-500'
      )}
    >
      <div className="p-6">
        {/* Header: Title + Status Badge */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1 min-w-0">
            <h3 className="text-lg font-semibold mb-1 truncate">
              {workflow.request_id || workflow.workflow_id}
            </h3>
            <p className="text-xs text-text-tertiary font-mono truncate">
              {workflow.workflow_id}
            </p>
          </div>
          <StatusBadge status={workflow.status} type="workflow" />
        </div>

        {/* Progress Bar */}
        {(workflow.status === 'running' || workflow.status === 'completed') && (
          <div className="mb-4">
            <div className="flex items-center justify-between text-xs text-text-secondary mb-1">
              <span>Progress</span>
              <span className="font-medium">{progress}%</span>
            </div>
            <div className="h-2 bg-background-tertiary rounded-full overflow-hidden">
              <div 
                className={cn(
                  'h-full rounded-full transition-all duration-500',
                  workflow.status === 'running' && 'bg-blue-500 animate-pulse',
                  workflow.status === 'completed' && 'bg-green-500'
                )}
                style={{ width: `${progress}%` }}
              />
            </div>
          </div>
        )}

        {/* Agent Assignment */}
        {(workflow.status === 'running' || workflow.status === 'completed') && (
          <div className="flex items-center gap-2 mb-3 text-sm">
            <User className="h-4 w-4 text-text-tertiary" />
            <span className="text-text-secondary">Assigned to:</span>
            <span className="font-medium text-primary">{assignedAgent}</span>
          </div>
        )}

        {/* Current Step / Message */}
        {workflow.current_step && (
          <div className="flex items-center gap-2 mb-3 text-sm text-text-secondary">
            <Clock className="h-4 w-4" />
            <span className="line-clamp-1">{workflow.current_step}</span>
          </div>
        )}

        {/* Execution Time */}
        {executionTime && (
          <div className="text-xs text-text-tertiary mb-4">
            {workflow.status === 'running' ? 'Running for: ' : 'Created: '}
            {executionTime}
          </div>
        )}

        {/* Expandable Details */}
        {workflow.message && (
          <div className="mb-4">
            <button
              onClick={() => setIsExpanded(!isExpanded)}
              className="flex items-center gap-1 text-sm text-primary hover:underline mb-2"
            >
              {isExpanded ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
              {isExpanded ? 'Hide Details' : 'Show Details'}
            </button>
            {isExpanded && (
              <div className="p-3 bg-background-secondary rounded-lg text-sm text-text-secondary border border-border">
                {workflow.message}
              </div>
            )}
          </div>
        )}

        {/* Quick Action Buttons */}
        <div className="flex flex-wrap gap-2">
          {/* View Details Button */}
          <Button
            variant="outline"
            size="sm"
            onClick={() => navigate(`/workflows/${workflow.workflow_id}`)}
            className="flex-1 min-w-[100px]"
          >
            <Eye className="h-4 w-4 mr-1" />
            View
          </Button>

          {/* Start Button */}
          {canStart && onStart && (
            <Button
              variant="primary"
              size="sm"
              onClick={() => onStart(workflow.workflow_id)}
            >
              <Play className="h-4 w-4" />
            </Button>
          )}

          {/* Stop Button */}
          {canStop && onStop && (
            <Button
              variant="secondary"
              size="sm"
              onClick={() => onStop(workflow.workflow_id)}
            >
              <Square className="h-4 w-4" />
            </Button>
          )}

          {/* Retry Button */}
          {canRetry && onRetry && (
            <Button
              variant="secondary"
              size="sm"
              onClick={() => onRetry(workflow.workflow_id)}
            >
              <RotateCcw className="h-4 w-4" />
            </Button>
          )}

          {/* Cancel Button */}
          {canCancel && onCancel && (
            <Button
              variant="destructive"
              size="sm"
              onClick={() => onCancel(workflow.workflow_id)}
            >
              <X className="h-4 w-4" />
            </Button>
          )}
        </div>
      </div>
    </Card>
  );
}
