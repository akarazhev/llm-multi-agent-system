/**
 * AgentCard Component (Molecule)
 * Based on DESIGN_SYSTEM.md specifications
 */

import { Card } from '@components/atoms/Card';
import { StatusBadge } from './StatusBadge';
import type { AgentInfo } from '@/types/agent';

export interface AgentCardProps {
  agent: AgentInfo;
}

export function AgentCard({ agent }: AgentCardProps) {
  return (
    <Card variant="elevated" className="hover:shadow-lg transition-shadow">
      <div className="p-6">
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <h3 className="text-lg font-semibold mb-2">{agent.agent_name}</h3>
            <p className="text-sm text-text-secondary mb-2">{agent.agent_id}</p>
          </div>
          <StatusBadge status={agent.status || 'idle'} type="agent" />
        </div>

        {agent.tools && agent.tools.length > 0 && (
          <div className="mb-4">
            <p className="text-xs font-medium text-text-secondary mb-2">Tools:</p>
            <div className="flex flex-wrap gap-2">
              {agent.tools.map((tool: { name: string; description?: string }, index: number) => (
                <span
                  key={index}
                  className="text-xs px-2 py-1 bg-background-secondary rounded-md text-text-secondary"
                >
                  {tool.name}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </Card>
  );
}
