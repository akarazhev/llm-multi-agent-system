/**
 * Dashboard Page
 * Main operational dashboard with tabbed interface
 * Based on OPERATIONAL_DASHBOARD_RESEARCH.md Phase 4
 */

import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { cn } from '@utils/cn';
import { Layout } from '@components/templates/Layout';
import { Card, Button, Badge } from '@components/atoms';
import { SkeletonCard, EmptyState } from '@components/molecules';
import { WorkflowList, AgentGrid, ChatPanel } from '@components/organisms';
import { useWorkflows } from '@hooks/useWorkflows';
import { useAgents } from '@hooks/useAgents';
import type { ChatMessage } from '@components/molecules/MessageBubble';
import { 
  LayoutDashboard, 
  Workflow, 
  Users, 
  MessageSquare,
  Plus,
  Activity,
  CheckCircle2,
  XCircle
} from 'lucide-react';

type TabType = 'overview' | 'workflows' | 'agents' | 'messages';

// Mock messages for demo
const mockMessages: ChatMessage[] = [
  {
    id: '1',
    type: 'agent',
    sender: 'Agent 1',
    content: 'Started processing workflow req-test-1',
    timestamp: new Date(Date.now() - 300000).toISOString(),
  },
  {
    id: '2',
    type: 'success',
    sender: 'System',
    content: 'Workflow req-test-1 completed successfully',
    timestamp: new Date(Date.now() - 120000).toISOString(),
  },
  {
    id: '3',
    type: 'agent',
    sender: 'Agent 2',
    content: 'Processing requirements analysis...',
    timestamp: new Date(Date.now() - 60000).toISOString(),
  },
];

export default function Dashboard() {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState<TabType>('overview');
  const { data: workflows, isLoading: workflowsLoading, error: workflowsError } = useWorkflows();
  const { data: agents, isLoading: agentsLoading, error: agentsError } = useAgents();

  // Calculate stats
  const stats = {
    totalWorkflows: workflows?.length || 0,
    runningWorkflows: workflows?.filter(w => w.status === 'running').length || 0,
    completedWorkflows: workflows?.filter(w => w.status === 'completed').length || 0,
    failedWorkflows: workflows?.filter(w => w.status === 'failed').length || 0,
    activeAgents: agents?.filter(a => a.status === 'active').length || 0,
    totalAgents: agents?.length || 0,
  };

  const tabs = [
    { id: 'overview' as TabType, label: 'Overview', icon: LayoutDashboard },
    { id: 'workflows' as TabType, label: 'Workflows', icon: Workflow, count: stats.totalWorkflows },
    { id: 'agents' as TabType, label: 'Agents', icon: Users, count: stats.totalAgents },
    { id: 'messages' as TabType, label: 'Messages', icon: MessageSquare, count: mockMessages.length },
  ];

  const getTabDescription = () => {
    switch (activeTab) {
      case 'overview':
        return 'Monitor workflows and agents in real-time';
      case 'workflows':
        return 'View and manage all workflows';
      case 'agents':
        return 'Monitor agent status and activity';
      case 'messages':
        return 'View system messages and notifications';
      default:
        return '';
    }
  };

  return (
    <Layout
      title="Dashboard"
      description="Monitor your workflows and agents in real-time"
      showSidebar={false}
      primaryAction={{
        label: 'New Workflow',
        icon: <Plus className="h-4 w-4" />,
        onClick: () => navigate('/workflows/new'),
      }}
    >
      <div className="space-y-8">
            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {/* Running Workflows */}
              <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-blue-500 to-blue-700 p-6 shadow-xl shadow-blue-500/30 hover:shadow-2xl hover:shadow-blue-500/40 transition-all duration-300 hover:scale-105">
                <div className="absolute top-0 right-0 -mt-4 -mr-4 h-24 w-24 rounded-full bg-white/10 blur-2xl"></div>
                <div className="relative">
                  <div className="flex items-center justify-between mb-4">
                    <div className="p-3 rounded-xl bg-white/20 backdrop-blur-sm">
                      <Activity className="h-7 w-7 text-white" />
                    </div>
                  </div>
                  <p className="text-sm text-blue-100 font-medium mb-1">Running</p>
                  <p className="text-4xl font-bold text-white">{stats.runningWorkflows}</p>
                </div>
              </div>

              {/* Completed Workflows */}
              <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-green-500 to-emerald-700 p-6 shadow-xl shadow-green-500/30 hover:shadow-2xl hover:shadow-green-500/40 transition-all duration-300 hover:scale-105">
                <div className="absolute top-0 right-0 -mt-4 -mr-4 h-24 w-24 rounded-full bg-white/10 blur-2xl"></div>
                <div className="relative">
                  <div className="flex items-center justify-between mb-4">
                    <div className="p-3 rounded-xl bg-white/20 backdrop-blur-sm">
                      <CheckCircle2 className="h-7 w-7 text-white" />
                    </div>
                  </div>
                  <p className="text-sm text-green-100 font-medium mb-1">Completed</p>
                  <p className="text-4xl font-bold text-white">{stats.completedWorkflows}</p>
                </div>
              </div>

              {/* Failed Workflows */}
              <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-red-500 to-rose-700 p-6 shadow-xl shadow-red-500/30 hover:shadow-2xl hover:shadow-red-500/40 transition-all duration-300 hover:scale-105">
                <div className="absolute top-0 right-0 -mt-4 -mr-4 h-24 w-24 rounded-full bg-white/10 blur-2xl"></div>
                <div className="relative">
                  <div className="flex items-center justify-between mb-4">
                    <div className="p-3 rounded-xl bg-white/20 backdrop-blur-sm">
                      <XCircle className="h-7 w-7 text-white" />
                    </div>
                  </div>
                  <p className="text-sm text-red-100 font-medium mb-1">Failed</p>
                  <p className="text-4xl font-bold text-white">{stats.failedWorkflows}</p>
                </div>
              </div>

              {/* Active Agents */}
              <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-purple-500 to-indigo-700 p-6 shadow-xl shadow-purple-500/30 hover:shadow-2xl hover:shadow-purple-500/40 transition-all duration-300 hover:scale-105">
                <div className="absolute top-0 right-0 -mt-4 -mr-4 h-24 w-24 rounded-full bg-white/10 blur-2xl"></div>
                <div className="relative">
                  <div className="flex items-center justify-between mb-4">
                    <div className="p-3 rounded-xl bg-white/20 backdrop-blur-sm">
                      <Users className="h-7 w-7 text-white" />
                    </div>
                  </div>
                  <p className="text-sm text-purple-100 font-medium mb-1">Active Agents</p>
                  <p className="text-4xl font-bold text-white">{stats.activeAgents}<span className="text-2xl text-purple-200">/{stats.totalAgents}</span></p>
                </div>
              </div>
            </div>

            {/* Recent Activity */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Recent Workflows */}
              <div className="lg:col-span-2">
                <Card className="p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h2 className="text-lg font-semibold">Recent Workflows</h2>
                    <Link to="/workflows">
                      <Button variant="ghost" size="sm">View All</Button>
                    </Link>
                  </div>
                  {workflowsLoading ? (
                    <div className="space-y-4">
                      {[1, 2, 3].map((i) => <SkeletonCard key={i} />)}
                    </div>
                  ) : workflowsError ? (
                    <EmptyState
                      icon={<XCircle className="h-12 w-12" />}
                      title="Failed to load workflows"
                      description="Please try again later"
                    />
                  ) : workflows && workflows.length > 0 ? (
                    <div className="space-y-3">
                      {workflows.slice(0, 5).map((workflow) => (
                        <Link
                          key={workflow.workflow_id}
                          to={`/workflows/${workflow.workflow_id}`}
                          className="flex items-center justify-between p-3 rounded-lg hover:bg-background-secondary transition-colors"
                        >
                          <div className="flex items-center gap-3">
                            <div className={cn(
                              'w-2 h-2 rounded-full',
                              workflow.status === 'running' && 'bg-blue-500 animate-pulse',
                              workflow.status === 'completed' && 'bg-green-500',
                              workflow.status === 'failed' && 'bg-red-500',
                              workflow.status === 'pending' && 'bg-gray-400',
                            )} />
                            <div>
                              <p className="font-medium">{workflow.workflow_id}</p>
                              <p className="text-xs text-text-tertiary">{workflow.request_id}</p>
                            </div>
                          </div>
                          <Badge 
                            variant={
                              workflow.status === 'completed' ? 'success' :
                              workflow.status === 'failed' ? 'destructive' :
                              workflow.status === 'running' ? 'default' : 'secondary'
                            }
                          >
                            {workflow.status}
                          </Badge>
                        </Link>
                      ))}
                    </div>
                  ) : (
                    <EmptyState
                      icon={<Workflow className="h-12 w-12" />}
                      title="No workflows yet"
                      description="Create your first workflow to get started"
                      action={{
                        label: 'New Workflow',
                        onClick: () => window.location.href = '/workflows/new',
                      }}
                    />
                  )}
                </Card>
              </div>

              {/* Messages */}
              <Card className="p-0 overflow-hidden">
                <ChatPanel
                  messages={mockMessages}
                  height={350}
                  showFilters={false}
                />
              </Card>
            </div>
          </div>
    </Layout>
  );
}
