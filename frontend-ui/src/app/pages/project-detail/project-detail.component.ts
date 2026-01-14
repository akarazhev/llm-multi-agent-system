import { Component, OnInit, signal, ChangeDetectionStrategy, computed, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatTabsModule } from '@angular/material/tabs';
import { MatCardModule } from '@angular/material/card';
import { MatChipsModule } from '@angular/material/chips';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatDividerModule } from '@angular/material/divider';
import { MatListModule } from '@angular/material/list';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { ProjectService } from '../../shared/services/project.service';
import { Project, ProjectStatus } from '../../core/interfaces/project.interface';
import { AssignAgentsDialogComponent } from './assign-agents-dialog/assign-agents-dialog.component';

@Component({
  selector: 'app-project-detail',
  standalone: true,
  imports: [
    CommonModule,
    RouterLink,
    MatButtonModule,
    MatIconModule,
    MatTabsModule,
    MatCardModule,
    MatChipsModule,
    MatProgressSpinnerModule,
    MatTooltipModule,
    MatDividerModule,
    MatListModule,
    MatDialogModule,
    MatSnackBarModule
  ],
  templateUrl: './project-detail.component.html',
  styleUrl: './project-detail.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ProjectDetailComponent implements OnInit {
  project = signal<Project | undefined>(undefined);
  loading = signal(true);

  projectExists = computed(() => !!this.project());

  private dialog = inject(MatDialog);
  private snackBar = inject(MatSnackBar);

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private projectService: ProjectService
  ) {}

  ngOnInit(): void {
    const projectId = this.route.snapshot.paramMap.get('id');
    if (projectId) {
      this.loadProject(projectId);
    }
  }

  loadProject(id: string): void {
    this.loading.set(true);
    this.projectService.getProjectById(id).subscribe(project => {
      this.project.set(project);
      this.loading.set(false);
    });
  }

  goBack(): void {
    this.router.navigate(['/projects']);
  }

  getStatusColor(status: ProjectStatus): string {
    const colors: Record<ProjectStatus, string> = {
      active: 'primary',
      planning: 'accent',
      on_hold: 'warn',
      archived: '',
      completed: 'primary'
    };
    return colors[status] || '';
  }

  getStatusIcon(status: ProjectStatus): string {
    const icons: Record<ProjectStatus, string> = {
      active: 'play_circle',
      planning: 'schedule',
      on_hold: 'pause_circle',
      archived: 'archive',
      completed: 'check_circle'
    };
    return icons[status];
  }

  getProjectTypeLabel(type: string): string {
    const labels: Record<string, string> = {
      web_app: 'Web Application',
      mobile_app: 'Mobile App',
      api: 'API/Backend',
      infrastructure: 'Infrastructure',
      data: 'Data/Analytics',
      custom: 'Custom'
    };
    return labels[type] || type;
  }

  getTimeAgo(dateString?: string): string {
    if (!dateString) return 'Never';
    
    const date = new Date(dateString);
    const now = new Date();
    const seconds = Math.floor((now.getTime() - date.getTime()) / 1000);
    
    if (seconds < 60) return 'Just now';
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
    if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
    if (seconds < 604800) return `${Math.floor(seconds / 86400)}d ago`;
    return date.toLocaleDateString();
  }

  editProject(): void {
    // TODO: Navigate to edit page
    console.log('Edit project');
  }

  archiveProject(): void {
    // TODO: Archive project
    console.log('Archive project');
  }

  configureAgents(): void {
    const dialogRef = this.dialog.open(AssignAgentsDialogComponent, {
      width: '700px',
      maxWidth: '90vw',
      data: {
        projectId: this.project()!.id,
        projectName: this.project()!.name,
        currentlyAssignedAgentIds: this.project()!.aiAgents
      }
    });

    dialogRef.afterClosed().subscribe((selectedAgentIds: string[]) => {
      if (selectedAgentIds) {
        this.projectService.assignAgents(this.project()!.id, selectedAgentIds).subscribe(project => {
          if (project) {
            this.loadProject(this.project()!.id);
            this.snackBar.open('Agent assignments updated successfully!', 'Close', {
              duration: 3000,
              horizontalPosition: 'end',
              verticalPosition: 'top'
            });
          }
        });
      }
    });
  }
}
