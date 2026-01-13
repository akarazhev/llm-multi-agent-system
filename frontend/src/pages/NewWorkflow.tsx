/**
 * New Workflow Page
 * Create a new workflow
 */

import { Layout } from '@components/templates/Layout';
import { WorkflowForm } from '@components/organisms/WorkflowForm';

export function NewWorkflow() {
  return (
    <Layout
      title="Create Workflow"
      description="Define requirements for a new workflow"
      breadcrumbs={[
        { label: 'Workflows', href: '/workflows' },
        { label: 'New Workflow' },
      ]}
    >
      <WorkflowForm />
    </Layout>
  );
}
