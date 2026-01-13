/**
 * WorkflowList Component (Organism)
 * Sortable, filterable workflow list with search
 * Based on OPERATIONAL_DASHBOARD_RESEARCH.md Phase 1.3
 */

import { useState, useMemo } from 'react';
import { cn } from '@utils/cn';
import { Button, Input, Badge } from '@components/atoms';
import { WorkflowStatusCard } from '@components/molecules/WorkflowStatusCard';
import { EmptyState } from '@components/molecules';
import type { Workflow, WorkflowStatus } from '@/types/workflow';
import { 
  Search, 
  Filter, 
  Grid3X3, 
  List, 
  ChevronUp, 
  ChevronDown,
  X,
  Workflow as WorkflowIcon
} from 'lucide-react';

export interface WorkflowListProps {
  workflows: Workflow[];
  isLoading?: boolean;
  onStart?: (workflowId: string) => void;
  onStop?: (workflowId: string) => void;
  onCancel?: (workflowId: string) => void;
  onRetry?: (workflowId: string) => void;
  className?: string;
}

type SortField = 'created_at' | 'status' | 'workflow_id';
type SortDirection = 'asc' | 'desc';
type ViewMode = 'list' | 'grid';

const statusFilters: { value: WorkflowStatus | 'all'; label: string }[] = [
  { value: 'all', label: 'All' },
  { value: 'running', label: 'Running' },
  { value: 'pending', label: 'Pending' },
  { value: 'completed', label: 'Completed' },
  { value: 'failed', label: 'Failed' },
  { value: 'cancelled', label: 'Cancelled' },
];

export function WorkflowList({
  workflows,
  isLoading,
  onStart,
  onStop,
  onCancel,
  onRetry,
  className,
}: WorkflowListProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState<WorkflowStatus | 'all'>('all');
  const [sortField, setSortField] = useState<SortField>('created_at');
  const [sortDirection, setSortDirection] = useState<SortDirection>('desc');
  const [viewMode, setViewMode] = useState<ViewMode>('grid');
  const [showFilters, setShowFilters] = useState(false);

  // Filter and sort workflows
  const filteredWorkflows = useMemo(() => {
    let result = [...workflows];

    // Search filter
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      result = result.filter(
        (w) =>
          w.workflow_id.toLowerCase().includes(query) ||
          w.request_id?.toLowerCase().includes(query)
      );
    }

    // Status filter
    if (statusFilter !== 'all') {
      result = result.filter((w) => w.status === statusFilter);
    }

    // Sort
    result.sort((a, b) => {
      let comparison = 0;
      
      switch (sortField) {
        case 'created_at':
          comparison = new Date(a.created_at || 0).getTime() - new Date(b.created_at || 0).getTime();
          break;
        case 'status':
          comparison = a.status.localeCompare(b.status);
          break;
        case 'workflow_id':
          comparison = a.workflow_id.localeCompare(b.workflow_id);
          break;
      }

      return sortDirection === 'asc' ? comparison : -comparison;
    });

    return result;
  }, [workflows, searchQuery, statusFilter, sortField, sortDirection]);

  const clearFilters = () => {
    setSearchQuery('');
    setStatusFilter('all');
  };

  const hasActiveFilters = searchQuery || statusFilter !== 'all';

  return (
    <div className={cn('space-y-6', className)}>
      {/* Search and Controls */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        {/* Search */}
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-text-tertiary" />
          <Input
            type="text"
            placeholder="Search workflows..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10"
          />
          {searchQuery && (
            <button
              onClick={() => setSearchQuery('')}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-text-tertiary hover:text-text-primary"
            >
              <X className="h-4 w-4" />
            </button>
          )}
        </div>

        {/* Controls */}
        <div className="flex items-center gap-2">
          {/* Filter Toggle */}
          <Button
            variant={showFilters ? 'secondary' : 'outline'}
            size="sm"
            onClick={() => setShowFilters(!showFilters)}
          >
            <Filter className="h-4 w-4 mr-2" />
            Filters
            {hasActiveFilters && (
              <Badge variant="primary" className="ml-2">
                {(searchQuery ? 1 : 0) + (statusFilter !== 'all' ? 1 : 0)}
              </Badge>
            )}
          </Button>

          {/* View Toggle */}
          <div className="flex items-center border border-border rounded-lg overflow-hidden">
            <button
              onClick={() => setViewMode('grid')}
              className={cn(
                'p-2 transition-colors',
                viewMode === 'grid' 
                  ? 'bg-primary text-white' 
                  : 'bg-background hover:bg-background-secondary'
              )}
              aria-label="Grid view"
            >
              <Grid3X3 className="h-4 w-4" />
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={cn(
                'p-2 transition-colors',
                viewMode === 'list' 
                  ? 'bg-primary text-white' 
                  : 'bg-background hover:bg-background-secondary'
              )}
              aria-label="List view"
            >
              <List className="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Filters Panel */}
      {showFilters && (
        <div className="p-4 bg-background-secondary rounded-lg border border-border">
          <div className="flex flex-wrap items-center gap-4">
            {/* Status Filter */}
            <div className="flex items-center gap-2">
              <span className="text-sm text-text-secondary">Status:</span>
              <div className="flex flex-wrap gap-2">
                {statusFilters.map((filter) => (
                  <button
                    key={filter.value}
                    onClick={() => setStatusFilter(filter.value)}
                    className={cn(
                      'px-3 py-1 text-sm rounded-full transition-colors',
                      statusFilter === filter.value
                        ? 'bg-primary text-white'
                        : 'bg-background border border-border hover:bg-background-tertiary'
                    )}
                  >
                    {filter.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Sort */}
            <div className="flex items-center gap-2 ml-auto">
              <span className="text-sm text-text-secondary">Sort by:</span>
              <select
                value={sortField}
                onChange={(e) => setSortField(e.target.value as SortField)}
                className="px-3 py-1.5 text-sm rounded-lg border border-border bg-background"
              >
                <option value="created_at">Date</option>
                <option value="status">Status</option>
                <option value="workflow_id">ID</option>
              </select>
              <button
                onClick={() => setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc')}
                className="p-1.5 rounded-lg border border-border hover:bg-background-secondary"
              >
                {sortDirection === 'asc' ? (
                  <ChevronUp className="h-4 w-4" />
                ) : (
                  <ChevronDown className="h-4 w-4" />
                )}
              </button>
            </div>

            {/* Clear Filters */}
            {hasActiveFilters && (
              <Button size="sm" variant="ghost" onClick={clearFilters}>
                <X className="h-4 w-4 mr-1" />
                Clear
              </Button>
            )}
          </div>
        </div>
      )}

      {/* Results Count */}
      <div className="text-sm text-text-secondary">
        Showing {filteredWorkflows.length} of {workflows.length} workflows
      </div>

      {/* Workflow Grid/List */}
      {filteredWorkflows.length === 0 ? (
        <EmptyState
          icon={<WorkflowIcon className="h-16 w-16" />}
          title="No workflows found"
          description={
            hasActiveFilters
              ? 'Try adjusting your filters or search query'
              : 'Create your first workflow to get started'
          }
          action={
            hasActiveFilters
              ? { label: 'Clear Filters', onClick: clearFilters, variant: 'outline' }
              : undefined
          }
        />
      ) : (
        <div
          className={cn(
            viewMode === 'grid'
              ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6'
              : 'flex flex-col gap-4'
          )}
        >
          {filteredWorkflows.map((workflow) => (
            <WorkflowStatusCard
              key={workflow.workflow_id}
              workflow={workflow}
              onStart={onStart}
              onStop={onStop}
              onCancel={onCancel}
              onRetry={onRetry}
            />
          ))}
        </div>
      )}
    </div>
  );
}
