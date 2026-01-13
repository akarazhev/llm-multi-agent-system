/**
 * WorkflowTimeline Component (Molecule)
 * Vertical timeline showing workflow steps
 * Based on OPERATIONAL_DASHBOARD_RESEARCH.md Phase 1.2
 */

import { useState } from 'react';
import { cn } from '@utils/cn';
import { 
  CheckCircle2, 
  Circle, 
  Loader2, 
  XCircle, 
  ChevronDown,
  ChevronUp,
  User,
  Clock
} from 'lucide-react';

export interface WorkflowStep {
  id: string;
  name: string;
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
  agent?: string;
  startTime?: string;
  endTime?: string;
  duration?: string;
  details?: string;
  error?: string;
}

export interface WorkflowTimelineProps {
  steps: WorkflowStep[];
  className?: string;
}

const stepStatusConfig = {
  pending: {
    icon: <Circle className="h-6 w-6" />,
    color: 'text-gray-400',
    bgColor: 'bg-gray-100 dark:bg-gray-800',
    lineColor: 'bg-gray-300 dark:bg-gray-700',
  },
  in_progress: {
    icon: <Loader2 className="h-6 w-6 animate-spin" />,
    color: 'text-blue-600',
    bgColor: 'bg-blue-100 dark:bg-blue-900/30',
    lineColor: 'bg-blue-400',
  },
  completed: {
    icon: <CheckCircle2 className="h-6 w-6" />,
    color: 'text-green-600',
    bgColor: 'bg-green-100 dark:bg-green-900/30',
    lineColor: 'bg-green-500',
  },
  failed: {
    icon: <XCircle className="h-6 w-6" />,
    color: 'text-red-600',
    bgColor: 'bg-red-100 dark:bg-red-900/30',
    lineColor: 'bg-red-500',
  },
};

function TimelineStep({ 
  step, 
  isLast 
}: { 
  step: WorkflowStep; 
  isLast: boolean;
}) {
  const [isExpanded, setIsExpanded] = useState(false);
  const config = stepStatusConfig[step.status];

  const formatTime = (dateStr?: string) => {
    if (!dateStr) return null;
    return new Date(dateStr).toLocaleTimeString();
  };

  return (
    <div className="relative pl-10">
      {/* Timeline Line */}
      {!isLast && (
        <div 
          className={cn(
            'absolute left-3 top-8 w-0.5 h-full -ml-px',
            config.lineColor
          )} 
        />
      )}

      {/* Step Indicator */}
      <div 
        className={cn(
          'absolute left-0 top-0 flex items-center justify-center w-6 h-6 rounded-full',
          config.bgColor,
          config.color
        )}
      >
        {config.icon}
      </div>

      {/* Step Content */}
      <div className="pb-6">
        <div 
          className={cn(
            'p-4 rounded-lg border border-border bg-background-secondary',
            'hover:shadow-md transition-all duration-200',
            step.status === 'in_progress' && 'ring-2 ring-blue-400/50'
          )}
        >
          {/* Step Header */}
          <div className="flex items-start justify-between">
            <div>
              <h4 className="font-medium text-text-primary">{step.name}</h4>
              <div className="flex items-center gap-4 mt-2 text-sm text-text-secondary">
                {step.agent && (
                  <div className="flex items-center gap-1">
                    <User className="h-4 w-4" />
                    <span>{step.agent}</span>
                  </div>
                )}
                {step.duration && (
                  <div className="flex items-center gap-1">
                    <Clock className="h-4 w-4" />
                    <span>{step.duration}</span>
                  </div>
                )}
              </div>
            </div>
            
            {/* Status Badge */}
            <span className={cn(
              'text-xs font-medium px-2 py-1 rounded-full',
              config.bgColor,
              config.color
            )}>
              {step.status.replace('_', ' ').toUpperCase()}
            </span>
          </div>

          {/* Time Info */}
          {(step.startTime || step.endTime) && (
            <div className="mt-3 text-xs text-text-tertiary flex gap-4">
              {step.startTime && <span>Started: {formatTime(step.startTime)}</span>}
              {step.endTime && <span>Ended: {formatTime(step.endTime)}</span>}
            </div>
          )}

          {/* Error Display */}
          {step.error && (
            <div className="mt-3 p-2 bg-red-50 dark:bg-red-900/20 rounded text-sm text-red-600">
              {step.error}
            </div>
          )}

          {/* Expandable Details */}
          {step.details && (
            <div className="mt-3">
              <button
                onClick={() => setIsExpanded(!isExpanded)}
                className="flex items-center gap-1 text-sm text-primary hover:underline"
              >
                {isExpanded ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
                {isExpanded ? 'Hide Details' : 'Show Details'}
              </button>
              {isExpanded && (
                <div className="mt-2 p-3 bg-background-tertiary rounded text-sm">
                  {step.details}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export function WorkflowTimeline({ steps, className }: WorkflowTimelineProps) {
  if (!steps || steps.length === 0) {
    return (
      <div className={cn('text-center py-8 text-text-secondary', className)}>
        No steps available
      </div>
    );
  }

  return (
    <div className={cn('relative', className)}>
      {steps.map((step, index) => (
        <TimelineStep 
          key={step.id} 
          step={step} 
          isLast={index === steps.length - 1} 
        />
      ))}
    </div>
  );
}
