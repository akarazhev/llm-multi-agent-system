/**
 * AgentStatusCard Component (Molecule)
 * Enhanced agent card with status indicator
 * Based on OPERATIONAL_DASHBOARD_RESEARCH.md Phase 2.1
 */

import { cn } from '@utils/cn';
import { Badge, Card } from '@components/atoms';
import type { AgentInfo } from '@/types/agent';
import { 
  User, 
  Clock, 
  Wrench,
  Activity,
  CheckCircle2,
  Circle,
  Loader2
} from 'lucide-react';

export interface AgentStatusCardProps {
  agent: AgentInfo;
  onClick?: (agentId: string) => void;
  className?: string;
}

type AgentStatus = 'active' | 'idle' | 'busy' | 'offline';

const statusConfig: Record<AgentStatus, {
  color: string;
  bgColor: string;
  ringColor: string;
  icon: React.ReactNode;
  label: string;
  animate?: boolean;
}> = {
  active: {
    color: 'text-green-600',
    bgColor: 'bg-green-500',
    ringColor: 'ring-green-400/50',
    icon: <CheckCircle2 className="h-5 w-5" />,
    label: 'Active',
    animate: true,
  },
  idle: {
    color: 'text-gray-500',
    bgColor: 'bg-gray-400',
    ringColor: 'ring-gray-300/50',
    icon: <Circle className="h-5 w-5" />,
    label: 'Idle',
  },
  busy: {
    color: 'text-blue-600',
    bgColor: 'bg-blue-500',
    ringColor: 'ring-blue-400/50',
    icon: <Loader2 className="h-5 w-5 animate-spin" />,
    label: 'Busy',
    animate: true,
  },
  offline: {
    color: 'text-red-500',
    bgColor: 'bg-red-400',
    ringColor: 'ring-red-300/50',
    icon: <Circle className="h-5 w-5" />,
    label: 'Offline',
  },
};

export function AgentStatusCard({ agent, onClick, className }: AgentStatusCardProps) {
  // Determine status based on agent info
  const getAgentStatus = (): AgentStatus => {
    if (!agent.status || agent.status === 'offline') return 'offline';
    if (agent.current_task) return 'busy';
    if (agent.status === 'active' || agent.status === 'available') return 'active';
    return 'idle';
  };

  const agentStatus = getAgentStatus();
  const config = statusConfig[agentStatus];

  return (
    <Card
      variant="elevated"
      className={cn(
        'p-6 rounded-2xl cursor-pointer transition-all duration-300',
        'hover:shadow-xl hover:scale-[1.02]',
        config.animate && `ring-2 ${config.ringColor}`,
        className
      )}
      onClick={() => onClick?.(agent.agent_id)}
    >
      {/* Header with Status Indicator */}
      <div className="flex items-start gap-4 mb-4">
        {/* Large Status Indicator (48px) */}
        <div className={cn(
          'relative w-12 h-12 rounded-full flex items-center justify-center',
          config.bgColor
        )}>
          <User className="h-6 w-6 text-white" />
          {config.animate && (
            <span className={cn(
              'absolute inset-0 rounded-full animate-ping opacity-75',
              config.bgColor
            )} />
          )}
        </div>

        <div className="flex-1">
          <h3 className="font-semibold text-lg">{agent.name || agent.agent_id}</h3>
          <div className={cn('flex items-center gap-1 text-sm', config.color)}>
            {config.icon}
            <span>{config.label}</span>
          </div>
        </div>

        {/* Activity Indicator */}
        <Activity className={cn(
          'h-5 w-5',
          config.animate ? 'text-green-500 animate-pulse' : 'text-text-tertiary'
        )} />
      </div>

      {/* Current Task */}
      {agent.current_task && (
        <div className="mb-4 p-3 bg-background-secondary rounded-lg">
          <p className="text-sm text-text-secondary mb-1">Current Task</p>
          <p className="font-medium truncate">{agent.current_task}</p>
        </div>
      )}

      {/* Tools */}
      {agent.tools && agent.tools.length > 0 && (
        <div className="mb-4">
          <div className="flex items-center gap-2 text-sm text-text-secondary mb-2">
            <Wrench className="h-4 w-4" />
            <span>Tools</span>
          </div>
          <div className="flex flex-wrap gap-1">
            {agent.tools.slice(0, 4).map((tool, index) => (
              <Badge key={index} variant="secondary" size="sm">
                {tool}
              </Badge>
            ))}
            {agent.tools.length > 4 && (
              <Badge variant="default" size="sm">
                +{agent.tools.length - 4}
              </Badge>
            )}
          </div>
        </div>
      )}

      {/* Execution Time */}
      {agent.execution_time && (
        <div className="flex items-center gap-2 text-sm text-text-secondary">
          <Clock className="h-4 w-4" />
          <span>Running for {agent.execution_time}</span>
        </div>
      )}
    </Card>
  );
}
