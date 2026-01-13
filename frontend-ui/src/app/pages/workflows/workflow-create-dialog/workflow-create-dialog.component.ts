import { Component, inject, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatDialogRef, MatDialogModule } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatStepperModule } from '@angular/material/stepper';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatChipsModule } from '@angular/material/chips';
import { MatCardModule } from '@angular/material/card';
import { WorkflowType, WorkflowPriority, WorkflowTemplate } from '../../../core/interfaces/workflow.interface';
import { WorkflowService } from '../../../shared/services/workflow.service';
import { ProjectService } from '../../../shared/services/project.service';
import { AgentService } from '../../../shared/services/agent.service';

@Component({
  selector: 'app-workflow-create-dialog',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatDialogModule,
    MatButtonModule,
    MatIconModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatStepperModule,
    MatTooltipModule,
    MatChipsModule,
    MatCardModule
  ],
  templateUrl: './workflow-create-dialog.component.html',
  styleUrl: './workflow-create-dialog.component.scss'
})
export class WorkflowCreateDialogComponent implements OnInit {
  private readonly fb = inject(FormBuilder);
  private readonly dialogRef = inject(MatDialogRef<WorkflowCreateDialogComponent>);
  private readonly workflowService = inject(WorkflowService);
  private readonly projectService = inject(ProjectService);
  private readonly agentService = inject(AgentService);

  // Forms
  templateForm!: FormGroup;
  detailsForm!: FormGroup;
  configurationForm!: FormGroup;

  // Data
  templates = this.workflowService.templatesSignal;
  projects = this.projectService.projects;
  agents = this.agentService.agentsSignal;

  // State
  selectedTemplate = signal<WorkflowTemplate | undefined>(undefined);

  // Enums
  readonly WorkflowType = WorkflowType;
  readonly WorkflowPriority = WorkflowPriority;

  ngOnInit(): void {
    this.initForms();
  }

  private initForms(): void {
    this.templateForm = this.fb.group({
      template: ['']
    });

    this.detailsForm = this.fb.group({
      name: ['', Validators.required],
      description: [''],
      requirement: ['', Validators.required],
      workflow_type: ['', Validators.required],
      priority: [WorkflowPriority.MEDIUM, Validators.required]
    });

    this.configurationForm = this.fb.group({
      project_id: [''],
      assigned_agents: [[]],
      tags: [[]]
    });

    // Watch template selection
    this.templateForm.get('template')?.valueChanges.subscribe(templateId => {
      const template = this.templates().find(t => t.template_id === templateId);
      this.selectedTemplate.set(template);
      if (template) {
        this.applyTemplate(template);
      }
    });
  }

  private applyTemplate(template: WorkflowTemplate): void {
    this.detailsForm.patchValue({
      name: template.name,
      description: template.description,
      workflow_type: template.workflow_type
    });
    this.configurationForm.patchValue({
      assigned_agents: template.recommended_agents
    });
  }

  onCancel(): void {
    this.dialogRef.close();
  }

  onCreate(): void {
    if (this.detailsForm.valid) {
      const workflowData = {
        ...this.detailsForm.value,
        ...this.configurationForm.value
      };
      this.dialogRef.close(workflowData);
    } else {
      this.detailsForm.markAllAsTouched();
    }
  }

  getTemplateIcon(type: WorkflowType): string {
    return this.workflowService.getTypeIcon(type);
  }
}
