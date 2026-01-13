/**
 * AgentGrid Component (Organism)
 * Responsive grid of agent cards
 * Based on OPERATIONAL_DASHBOARD_RESEARCH.md Phase 2.2
 */

import { cn } from '@utils/cn';
import { AgentStatusCard } from '@components/molecules/AgentStatusCard';
import { EmptyState, SkeletonCard } from '@components/molecules';
import type { AgentInfo } from '@/types/agent';
import { Users } from 'lucide-react';

export interface AgentGridProps {
  agents: AgentInfo[];
  isLoading?: boolean;
  onAgentClick?: (agentId: string) => void;
  className?: string;
}

export function AgentGrid({ agents, isLoading, onAgentClick, className }: AgentGridProps) {
  if (isLoading) {
    return (
      <div className={cn(
        'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6',
        className
      )}>
        {[1, 2, 3, 4].map((i) => (
          <SkeletonCard key={i} />
        ))}
      </div>
    );
  }

  if (!agents || agents.length === 0) {
    return (
      <EmptyState
        icon={<Users className="h-16 w-16" />}
        title="No agents found"
        description="Agents will appear here once they are registered with the system."
        className={className}
      />
    );
  }

  return (
    <div className={cn(
      'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6',
      className
    )}>
      {agents.map((agent) => (
        <AgentStatusCard
          key={agent.agent_id}
          agent={agent}
          onClick={onAgentClick}
        />
      ))}
    </div>
  );
}
