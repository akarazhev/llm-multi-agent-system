/**
 * Workflow Detail Page
 * View workflow details and progress
 */

import { useParams, useNavigate } from 'react-router-dom';
import { Layout } from '@components/templates/Layout';
import { PageTitle } from '@components/molecules/PageTitle';
import { Card, Button } from '@components/atoms';
import { StatusBadge } from '@components/molecules/StatusBadge';
import { useWorkflowStatus, useCancelWorkflow } from '@hooks/useWorkflows';
import { useToastContext } from '@lib/toast-provider';
import { format } from 'date-fns';
import { ArrowLeft, X, Loader2 } from 'lucide-react';

export function WorkflowDetail() {
  const { workflowId } = useParams<{ workflowId: string }>();
  const navigate = useNavigate();
  const toast = useToastContext();
  const { data: workflow, isLoading, error } = useWorkflowStatus(workflowId || null);
  const cancelWorkflow = useCancelWorkflow();

  const handleCancel = async () => {
    if (!workflowId || !confirm('Are you sure you want to cancel this workflow?')) {
      return;
    }

    try {
      await cancelWorkflow.mutateAsync(workflowId);
      toast.success('Workflow cancelled successfully');
      navigate('/workflows');
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Failed to cancel workflow';
      toast.error(message);
      console.error('Failed to cancel workflow:', error);
    }
  };

  if (isLoading) {
    return (
      <Layout>
        <PageTitle title="Workflow Details" description="Loading workflow information" />
        <div className="flex items-center justify-center py-12">
          <Loader2 className="h-8 w-8 animate-spin text-text-secondary" />
        </div>
      </Layout>
    );
  }

  if (error) {
    return (
      <Layout>
        <PageTitle title="Error" description="Failed to load workflow" />
        <div className="text-center py-12">
          <p className="text-destructive font-medium mb-2">Failed to load workflow</p>
          <p className="text-sm text-destructive/80 mb-4">{error.message}</p>
          <Button variant="primary" onClick={() => navigate('/workflows')}>
            Back to Workflows
          </Button>
        </div>
      </Layout>
    );
  }

  if (!workflow) {
    return (
      <Layout>
        <PageTitle title="Not Found" description="Workflow not found" />
        <div className="text-center py-12">
          <p className="text-text-secondary mb-4">Workflow not found</p>
          <Button variant="primary" onClick={() => navigate('/workflows')}>
            Back to Workflows
          </Button>
        </div>
      </Layout>
    );
  }

  const canCancel = workflow.status === 'pending' || workflow.status === 'running';

  return (
    <Layout>
      <PageTitle 
        title={`Workflow ${workflow.workflow_id}`}
        description={`View details and progress for workflow ${workflow.workflow_id}`}
      />
      <div className="space-y-6">
        <div className="flex items-center gap-4">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => navigate('/workflows')}
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back
          </Button>
          <div className="flex-1">
            <h2 className="text-3xl font-bold mb-2">Workflow Details</h2>
            <p className="text-text-secondary">Workflow ID: {workflow.workflow_id}</p>
          </div>
          <StatusBadge status={workflow.status} type="workflow" />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            <Card variant="elevated">
              <h3 className="text-xl font-semibold mb-4">Status Information</h3>
              <div className="space-y-4">
                <div>
                  <p className="text-sm text-text-secondary mb-1">Status</p>
                  <StatusBadge status={workflow.status} type="workflow" />
                </div>
                {workflow.current_step && (
                  <div>
                    <p className="text-sm text-text-secondary mb-1">Current Step</p>
                    <p className="text-base font-medium">{workflow.current_step}</p>
                  </div>
                )}
                {workflow.message && (
                  <div>
                    <p className="text-sm text-text-secondary mb-1">Message</p>
                    <p className="text-base">{workflow.message}</p>
                  </div>
                )}
              </div>
            </Card>

            {workflow.message && (
              <Card variant="elevated">
                <h3 className="text-xl font-semibold mb-4">Details</h3>
                <p className="text-base whitespace-pre-wrap">{workflow.message}</p>
              </Card>
            )}
          </div>

          <div className="space-y-6">
            <Card variant="elevated">
              <h3 className="text-xl font-semibold mb-4">Actions</h3>
              <div className="space-y-2">
                {canCancel && (
                  <Button
                    variant="destructive"
                    size="sm"
                    onClick={handleCancel}
                    isLoading={cancelWorkflow.isPending}
                    disabled={cancelWorkflow.isPending}
                    className="w-full"
                  >
                    <X className="h-4 w-4 mr-2" />
                    Cancel Workflow
                  </Button>
                )}
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => navigate('/workflows')}
                  className="w-full"
                >
                  Back to List
                </Button>
              </div>
            </Card>

            <Card variant="elevated">
              <h3 className="text-xl font-semibold mb-4">Information</h3>
              <div className="space-y-3 text-sm">
                <div>
                  <p className="text-text-secondary">Request ID</p>
                  <p className="font-medium">{workflow.request_id}</p>
                </div>
                <div>
                  <p className="text-text-secondary">Workflow ID</p>
                  <p className="font-medium font-mono text-xs">{workflow.workflow_id}</p>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </div>
    </Layout>
  );
}
