/**
 * Agents Page
 * List and view agent information
 */

import { Layout } from '@components/templates/Layout';
import { AgentCard } from '@components/molecules/AgentCard';
import { EmptyState, SkeletonList } from '@components/molecules';
import { useAgents } from '@hooks/useAgents';
import { Users, AlertCircle } from 'lucide-react';

export function Agents() {
  const { data: agents, isLoading, error } = useAgents();

  return (
    <Layout 
      title="Agents"
      description="View available agents and their status"
    >
      {isLoading && (
        <SkeletonList count={6} />
      )}

      {error && (
        <EmptyState
          icon={<AlertCircle className="h-12 w-12" />}
          title="Failed to load agents"
          description={error.message || 'An error occurred while loading agents. Please try again.'}
          action={{
            label: 'Retry',
            onClick: () => window.location.reload(),
            variant: 'primary',
          }}
        />
      )}

      {!isLoading && !error && agents && agents.length === 0 && (
        <EmptyState
          icon={<Users className="h-16 w-16" />}
          title="No agents found"
          description="Agents will appear here once they are registered with the system. Agents are automatically discovered and registered when they connect."
        />
      )}

      {!isLoading && !error && agents && agents.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {agents.map((agent) => (
            <AgentCard key={agent.agent_id} agent={agent} />
          ))}
        </div>
      )}
    </Layout>
  );
}
