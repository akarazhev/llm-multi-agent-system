import { Component, inject, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatDialogModule, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatSliderModule } from '@angular/material/slider';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatChipsModule } from '@angular/material/chips';
import { MatStepperModule } from '@angular/material/stepper';
import { AgentTemplate, AgentRole, CreateAgentRequest } from '../../../core/interfaces/agent.interface';

export interface AgentConfigDialogData {
  template?: AgentTemplate;
  mode: 'create' | 'edit';
  agentId?: string;
}

@Component({
  selector: 'app-agent-config-dialog',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatSliderModule,
    MatSlideToggleModule,
    MatButtonModule,
    MatIconModule,
    MatChipsModule,
    MatStepperModule
  ],
  templateUrl: './agent-config-dialog.component.html',
  styleUrl: './agent-config-dialog.component.scss'
})
export class AgentConfigDialogComponent {
  private fb = inject(FormBuilder);
  private dialogRef = inject(MatDialogRef<AgentConfigDialogComponent>);
  readonly data = inject<AgentConfigDialogData>(MAT_DIALOG_DATA);

  readonly creating = signal(false);

  // Form groups
  readonly basicInfoForm: FormGroup;
  readonly configForm: FormGroup;

  // Available models
  readonly availableModels = [
    { value: 'llama3-70b', label: 'Llama 3 70B (Recommended)' },
    { value: 'llama3-8b', label: 'Llama 3 8B (Faster)' },
    { value: 'gpt-4', label: 'GPT-4 (External API)' },
    { value: 'gpt-3.5-turbo', label: 'GPT-3.5 Turbo (External API)' }
  ];

  // Available roles
  readonly availableRoles = Object.values(AgentRole).map(role => ({
    value: role,
    label: this.getRoleDisplayName(role)
  }));

  constructor() {
    const template = this.data.template;

    // Initialize basic info form
    this.basicInfoForm = this.fb.group({
      name: ['', [Validators.required, Validators.minLength(3)]],
      role: [template?.role || '', Validators.required],
      description: [template?.description || '']
    });

    // Initialize config form
    this.configForm = this.fb.group({
      model: [template?.default_configuration.model || 'llama3-70b', Validators.required],
      temperature: [template?.default_configuration.temperature || 0.5, [Validators.min(0), Validators.max(1)]],
      max_tokens: [template?.default_configuration.max_tokens || 4000, [Validators.min(100), Validators.max(16000)]],
      auto_approve: [template?.default_configuration.auto_approve || false],
      max_retries: [template?.default_configuration.max_retries || 3, [Validators.min(1), Validators.max(5)]]
    });
  }

  cancel(): void {
    this.dialogRef.close();
  }

  create(): void {
    if (this.basicInfoForm.invalid || this.configForm.invalid) {
      this.basicInfoForm.markAllAsTouched();
      this.configForm.markAllAsTouched();
      return;
    }

    this.creating.set(true);

    const request: CreateAgentRequest = {
      name: this.basicInfoForm.value.name,
      role: this.basicInfoForm.value.role,
      description: this.basicInfoForm.value.description,
      template_id: this.data.template?.template_id,
      configuration: {
        model: this.configForm.value.model,
        temperature: this.configForm.value.temperature,
        max_tokens: this.configForm.value.max_tokens,
        tools_enabled: this.data.template?.default_configuration.tools_enabled || [],
        auto_approve: this.configForm.value.auto_approve,
        max_retries: this.configForm.value.max_retries
      }
    };

    // Simulate API call
    setTimeout(() => {
      this.creating.set(false);
      this.dialogRef.close(request);
    }, 1000);
  }

  getRoleDisplayName(role: AgentRole): string {
    const names: Record<AgentRole, string> = {
      [AgentRole.BUSINESS_ANALYST]: 'Business Analyst',
      [AgentRole.DEVELOPER]: 'Developer',
      [AgentRole.QA_ENGINEER]: 'QA Engineer',
      [AgentRole.DEVOPS_ENGINEER]: 'DevOps Engineer',
      [AgentRole.TECHNICAL_WRITER]: 'Technical Writer',
      [AgentRole.ARCHITECT]: 'Architect',
      [AgentRole.PRODUCT_MANAGER]: 'Product Manager',
      [AgentRole.SECURITY_ENGINEER]: 'Security Engineer'
    };
    return names[role] || role;
  }

  formatTemperature(value: number): string {
    return value.toFixed(2);
  }

  formatTokens(value: number): string {
    if (value >= 1000) return `${(value / 1000).toFixed(1)}K`;
    return value.toString();
  }
}
