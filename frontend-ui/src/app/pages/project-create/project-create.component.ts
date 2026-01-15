import { Component, signal, ChangeDetectionStrategy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { MatStepperModule } from '@angular/material/stepper';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatChipsModule } from '@angular/material/chips';
import { MatCardModule } from '@angular/material/card';
import { ProjectService } from '../../shared/services/project.service';
import { ProjectFormData, ProjectType, ProjectStatus } from '../../core/interfaces/project.interface';

@Component({
  selector: 'app-project-create',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatStepperModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatButtonModule,
    MatIconModule,
    MatChipsModule,
    MatCardModule
  ],
  templateUrl: './project-create.component.html',
  styleUrl: './project-create.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ProjectCreateComponent {
  basicInfoForm: FormGroup;
  techStackForm: FormGroup;
  integrationsForm: FormGroup;
  
  creating = signal(false);
  
  projectTypes: { value: ProjectType; label: string; icon: string }[] = [
    { value: 'web_app', label: 'Web Application', icon: '🌐' },
    { value: 'mobile_app', label: 'Mobile App', icon: '📱' },
    { value: 'api', label: 'API/Backend', icon: '⚙️' },
    { value: 'infrastructure', label: 'Infrastructure', icon: '🔧' },
    { value: 'data', label: 'Data/Analytics', icon: '📊' },
    { value: 'custom', label: 'Custom', icon: '🎯' }
  ];

  projectStatuses: { value: ProjectStatus; label: string }[] = [
    { value: 'planning', label: 'Planning' },
    { value: 'active', label: 'Active' },
  ];

  // Common tech options
  languageOptions = ['TypeScript', 'JavaScript', 'Python', 'Java', 'Kotlin', 'Go', 'Rust', 'C#', 'PHP', 'Ruby'];
  frameworkOptions = ['Angular', 'React', 'Vue.js', 'Next.js', 'Express.js', 'FastAPI', 'Spring Boot', 'Django', 'Flask'];
  databaseOptions = ['PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'SQLite', 'Elasticsearch', 'DynamoDB'];
  toolOptions = ['Docker', 'Kubernetes', 'Jest', 'Cypress', 'Webpack', 'Vite', 'ESLint', 'Prettier'];
  gitPlatforms = ['github', 'gitlab', 'bitbucket'];

  selectedLanguages = signal<string[]>([]);
  selectedFrameworks = signal<string[]>([]);
  selectedDatabases = signal<string[]>([]);
  selectedTools = signal<string[]>([]);

  constructor(
    private fb: FormBuilder,
    private projectService: ProjectService,
    private router: Router
  ) {
    this.basicInfoForm = this.fb.group({
      name: ['', [Validators.required, Validators.minLength(3)]],
      description: ['', [Validators.required, Validators.minLength(10)]],
      icon: ['📁'],
      type: ['web_app', Validators.required],
      status: ['planning', Validators.required]
    });

    this.techStackForm = this.fb.group({
      languages: [[]],
      frameworks: [[]],
      databases: [[]],
      tools: [[]]
    });

    this.integrationsForm = this.fb.group({
      gitPlatform: ['github'],
      gitUrl: [''],
      gitBranch: ['main'],
      confluenceUrl: [''],
      confluenceSpaceKey: ['']
    });
  }

  toggleLanguage(lang: string): void {
    const current = this.selectedLanguages();
    if (current.includes(lang)) {
      this.selectedLanguages.set(current.filter(l => l !== lang));
    } else {
      this.selectedLanguages.set([...current, lang]);
    }
    this.techStackForm.patchValue({ languages: this.selectedLanguages() });
  }

  toggleFramework(fw: string): void {
    const current = this.selectedFrameworks();
    if (current.includes(fw)) {
      this.selectedFrameworks.set(current.filter(f => f !== fw));
    } else {
      this.selectedFrameworks.set([...current, fw]);
    }
    this.techStackForm.patchValue({ frameworks: this.selectedFrameworks() });
  }

  toggleDatabase(db: string): void {
    const current = this.selectedDatabases();
    if (current.includes(db)) {
      this.selectedDatabases.set(current.filter(d => d !== db));
    } else {
      this.selectedDatabases.set([...current, db]);
    }
    this.techStackForm.patchValue({ databases: this.selectedDatabases() });
  }

  toggleTool(tool: string): void {
    const current = this.selectedTools();
    if (current.includes(tool)) {
      this.selectedTools.set(current.filter(t => t !== tool));
    } else {
      this.selectedTools.set([...current, tool]);
    }
    this.techStackForm.patchValue({ tools: this.selectedTools() });
  }

  isSelected(item: string, list: string[]): boolean {
    return list.includes(item);
  }

  createProject(): void {
    if (this.basicInfoForm.invalid) {
      return;
    }

    this.creating.set(true);

    const formData: ProjectFormData = {
      ...this.basicInfoForm.value,
      techStack: {
        languages: this.selectedLanguages(),
        frameworks: this.selectedFrameworks(),
        databases: this.selectedDatabases(),
        tools: this.selectedTools()
      },
      integrations: this.buildIntegrationsPayload()
    };

    this.projectService.createProject(formData).subscribe({
      next: (project) => {
        if (project) {
          this.router.navigate(['/projects', project.id]);
        }
      },
      error: (error) => {
        console.error('Error creating project:', error);
        this.creating.set(false);
      }
    });
  }

  cancel(): void {
    this.router.navigate(['/projects']);
  }

  private buildIntegrationsPayload(): ProjectFormData['integrations'] {
    const gitUrl = (this.integrationsForm.get('gitUrl')?.value as string || '').trim();
    const confluenceUrl = (this.integrationsForm.get('confluenceUrl')?.value as string || '').trim();
    const confluenceSpaceKey = (this.integrationsForm.get('confluenceSpaceKey')?.value as string || '').trim();

    const gitPayload = gitUrl
      ? {
          platform: this.integrationsForm.get('gitPlatform')?.value as string,
          url: gitUrl,
          branch: (this.integrationsForm.get('gitBranch')?.value as string || 'main').trim(),
          connected: true
        }
      : undefined;

    const confluencePayload = confluenceUrl || confluenceSpaceKey
      ? {
          url: confluenceUrl,
          spaceKey: confluenceSpaceKey,
          connected: true
        }
      : undefined;

    if (!gitPayload && !confluencePayload) {
      return undefined;
    }

    return {
      git: gitPayload,
      confluence: confluencePayload
    };
  }

  getProjectTypeIcon(type: ProjectType): string {
    return this.projectTypes.find(t => t.value === type)?.icon || '📁';
  }
}
