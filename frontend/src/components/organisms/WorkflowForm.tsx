/**
 * WorkflowForm Component (Organism)
 * Based on DESIGN_SYSTEM.md specifications
 */

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FormField } from '@components/molecules/FormField';
import { Button, Card } from '@components/atoms';
import { useStartWorkflow } from '@hooks/useWorkflows';
import { useToastContext } from '@lib/toast-provider';
import type { WorkflowRequest } from '@/types/workflow';
import { X } from 'lucide-react';

export interface WorkflowFormProps {
  onCancel?: () => void;
}

export function WorkflowForm({ onCancel }: WorkflowFormProps) {
  const navigate = useNavigate();
  const toast = useToastContext();
  const startWorkflow = useStartWorkflow();
  const [requirements, setRequirements] = useState('');
  const [requestId, setRequestId] = useState('');
  const [errors, setErrors] = useState<{ requirements?: string }>({});

  const validate = (): boolean => {
    const newErrors: { requirements?: string } = {};
    
    if (!requirements.trim()) {
      newErrors.requirements = 'Requirements are required';
    } else if (requirements.trim().length < 10) {
      newErrors.requirements = 'Requirements must be at least 10 characters';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validate()) {
      return;
    }

    try {
      const request: WorkflowRequest = {
        requirements: requirements.trim(),
        ...(requestId.trim() && { request_id: requestId.trim() }),
      };

      const response = await startWorkflow.mutateAsync(request);
      toast.success('Workflow created successfully');
      navigate(`/workflows/${response.workflow_id}`);
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Failed to start workflow';
      toast.error(message);
      setErrors({
        requirements: message,
      });
      console.error('Failed to start workflow:', error);
    }
  };

  const handleCancel = () => {
    if (onCancel) {
      onCancel();
    } else {
      navigate('/workflows');
    }
  };

  return (
    <Card variant="elevated" className="max-w-2xl mx-auto">
      <div className="px-6 py-4 border-b border-border flex items-center justify-between">
        <h2 className="text-2xl font-bold">Create New Workflow</h2>
        {onCancel && (
          <Button
            variant="ghost"
            size="sm"
            onClick={handleCancel}
            aria-label="Close form"
          >
            <X className="h-5 w-5" />
          </Button>
        )}
      </div>

      <form onSubmit={handleSubmit} className="px-6 py-4 space-y-6">
        <FormField
          id="requirements"
          label="Requirements"
          required
          error={!!errors.requirements}
          errorMessage={errors.requirements}
          helperText="Describe what you want the workflow to accomplish (minimum 10 characters)"
        >
          <textarea
            id="requirements"
            value={requirements}
            onChange={(e) => {
              setRequirements(e.target.value);
              if (errors.requirements) {
                setErrors({});
              }
            }}
            rows={8}
            className="w-full rounded-md border border-border bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-text-tertiary focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-border-focus focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
            placeholder="Enter workflow requirements here..."
            aria-invalid={!!errors.requirements}
            aria-describedby={errors.requirements ? 'requirements-error' : 'requirements-helper'}
          />
        </FormField>

        <FormField
          id="request-id"
          label="Request ID (Optional)"
          helperText="Optional: Provide a custom request ID for tracking"
        >
          <input
            id="request-id"
            type="text"
            value={requestId}
            onChange={(e) => setRequestId(e.target.value)}
            className="w-full rounded-md border border-border bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-text-tertiary focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-border-focus focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
            placeholder="e.g., REQ-2026-001"
          />
        </FormField>

        <div className="flex gap-4 pt-4 border-t border-border">
          <Button
            type="submit"
            variant="primary"
            isLoading={startWorkflow.isPending}
            disabled={startWorkflow.isPending}
            className="flex-1"
          >
            {startWorkflow.isPending ? 'Creating...' : 'Create Workflow'}
          </Button>
          <Button
            type="button"
            variant="outline"
            onClick={handleCancel}
            disabled={startWorkflow.isPending}
          >
            Cancel
          </Button>
        </div>
      </form>
    </Card>
  );
}
