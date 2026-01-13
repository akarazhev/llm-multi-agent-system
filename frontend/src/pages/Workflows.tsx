/**
 * Workflows Page
 * List and manage workflows
 */

import { Layout } from '@components/templates/Layout';
import { WorkflowCard } from '@components/molecules/WorkflowCard';
import { EmptyState, SkeletonList } from '@components/molecules';
import { useWorkflows, useCancelWorkflow } from '@hooks/useWorkflows';
import { useToastContext } from '@lib/toast-provider';
import { useNavigate } from 'react-router-dom';
import { Plus, Workflow as WorkflowIcon, AlertCircle } from 'lucide-react';

export function Workflows() {
  const navigate = useNavigate();
  const toast = useToastContext();
  const { data: workflows, isLoading, error } = useWorkflows();
  const cancelWorkflow = useCancelWorkflow();

  const handleCancel = async (workflowId: string) => {
    if (!confirm('Are you sure you want to cancel this workflow?')) {
      return;
    }

    try {
      await cancelWorkflow.mutateAsync(workflowId);
      toast.success('Workflow cancelled successfully');
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Failed to cancel workflow';
      toast.error(message);
      console.error('Failed to cancel workflow:', error);
    }
  };

  return (
    <Layout
      title="Workflows"
      description="Manage and monitor your workflows"
      primaryAction={{
        label: 'New Workflow',
        icon: <Plus className="h-4 w-4" />,
        onClick: () => navigate('/workflows/new'),
      }}
    >

      {isLoading && (
        <SkeletonList count={6} />
      )}

      {error && (
        <EmptyState
          icon={<AlertCircle className="h-12 w-12" />}
          title="Failed to load workflows"
          description={error.message || 'An error occurred while loading workflows. Please try again.'}
          action={{
            label: 'Retry',
            onClick: () => window.location.reload(),
            variant: 'primary',
          }}
        />
      )}

      {!isLoading && !error && workflows && workflows.length === 0 && (
        <EmptyState
          icon={<WorkflowIcon className="h-16 w-16" />}
          title="No workflows yet"
          description="Get started by creating your first workflow. Define your requirements and let the multi-agent system handle the rest."
          action={{
            label: 'Create Your First Workflow',
            onClick: () => navigate('/workflows/new'),
            variant: 'primary',
          }}
        />
      )}

      {!isLoading && !error && workflows && workflows.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {workflows.map((workflow) => (
            <WorkflowCard
              key={workflow.workflow_id}
              workflow={workflow}
              onCancel={handleCancel}
            />
          ))}
        </div>
      )}
    </Layout>
  );
}
