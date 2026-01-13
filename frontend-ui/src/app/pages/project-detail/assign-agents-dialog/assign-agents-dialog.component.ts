import { Component, inject, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatDialogModule, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatChipsModule } from '@angular/material/chips';
import { MatDividerModule } from '@angular/material/divider';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { AgentService } from '../../../shared/services/agent.service';
import { Agent } from '../../../core/interfaces/agent.interface';

export interface AssignAgentsDialogData {
  projectId: string;
  projectName: string;
  currentlyAssignedAgentIds: string[];
}

@Component({
  selector: 'app-assign-agents-dialog',
  standalone: true,
  imports: [
    CommonModule,
    MatDialogModule,
    MatButtonModule,
    MatIconModule,
    MatCheckboxModule,
    MatChipsModule,
    MatDividerModule,
    MatProgressSpinnerModule
  ],
  templateUrl: './assign-agents-dialog.component.html',
  styleUrl: './assign-agents-dialog.component.scss'
})
export class AssignAgentsDialogComponent {
  private dialogRef = inject(MatDialogRef<AssignAgentsDialogComponent>);
  readonly data = inject<AssignAgentsDialogData>(MAT_DIALOG_DATA);
  private agentService = inject(AgentService);

  readonly agents = this.agentService.agentsSignal;
  readonly selectedAgentIds = signal<Set<string>>(new Set(this.data.currentlyAssignedAgentIds));
  readonly saving = signal(false);

  readonly selectedCount = computed(() => this.selectedAgentIds().size);
  readonly hasChanges = computed(() => {
    const current = new Set(this.data.currentlyAssignedAgentIds);
    const selected = this.selectedAgentIds();
    if (current.size !== selected.size) return true;
    for (const id of selected) {
      if (!current.has(id)) return true;
    }
    return false;
  });

  isSelected(agentId: string): boolean {
    return this.selectedAgentIds().has(agentId);
  }

  toggleAgent(agent: Agent): void {
    const selected = new Set(this.selectedAgentIds());
    if (selected.has(agent.agent_id)) {
      selected.delete(agent.agent_id);
    } else {
      selected.add(agent.agent_id);
    }
    this.selectedAgentIds.set(selected);
  }

  cancel(): void {
    this.dialogRef.close();
  }

  save(): void {
    if (!this.hasChanges()) {
      this.dialogRef.close();
      return;
    }

    this.saving.set(true);

    // Update agent assignments
    const currentIds = new Set(this.data.currentlyAssignedAgentIds);
    const selectedIds = this.selectedAgentIds();

    // Assign newly selected agents
    for (const agentId of selectedIds) {
      if (!currentIds.has(agentId)) {
        this.agentService.assignToProject(agentId, this.data.projectId);
      }
    }

    // Unassign deselected agents
    for (const agentId of currentIds) {
      if (!selectedIds.has(agentId)) {
        this.agentService.unassignFromProject(agentId, this.data.projectId);
      }
    }

    // Simulate API call
    setTimeout(() => {
      this.saving.set(false);
      this.dialogRef.close(Array.from(selectedIds));
    }, 500);
  }

  getRoleIcon(agent: Agent): string {
    return this.agentService.getRoleIcon(agent.role);
  }

  getRoleDisplayName(agent: Agent): string {
    return this.agentService.getRoleDisplayName(agent.role);
  }
}
