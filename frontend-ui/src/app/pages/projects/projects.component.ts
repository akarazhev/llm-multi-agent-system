import { Component, OnInit, computed, ChangeDetectionStrategy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterLink } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatChipsModule } from '@angular/material/chips';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { ProjectService } from '../../shared/services/project.service';
import { Project, ProjectStatus } from '../../core/interfaces/project.interface';

@Component({
  selector: 'app-projects',
  standalone: true,
  imports: [
    CommonModule,
    RouterLink,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatChipsModule,
    MatProgressSpinnerModule,
    MatTooltipModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule
  ],
  templateUrl: './projects.component.html',
  styleUrl: './projects.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ProjectsComponent implements OnInit {
  projects = computed(() => this.projectService.projects());
  loading = computed(() => this.projectService.loading());
  
  searchQuery = '';
  statusFilter: ProjectStatus | 'all' = 'all';

  filteredProjects = computed(() => {
    let projects = this.projects();
    
    // Filter by status
    if (this.statusFilter !== 'all') {
      projects = projects.filter(p => p.status === this.statusFilter);
    }
    
    // Filter by search query
    if (this.searchQuery) {
      const query = this.searchQuery.toLowerCase();
      projects = projects.filter(p => 
        p.name.toLowerCase().includes(query) ||
        p.description.toLowerCase().includes(query)
      );
    }
    
    return projects;
  });

  constructor(
    private projectService: ProjectService,
    private router: Router
  ) {}

  ngOnInit(): void {
    // Projects are automatically loaded in service constructor
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

  getTechStackDisplay(project: Project): string[] {
    const stack: string[] = [];
    
    if (project.techStack.languages.length > 0) {
      stack.push(...project.techStack.languages.slice(0, 3));
    }
    
    if (project.techStack.frameworks.length > 0 && stack.length < 3) {
      stack.push(...project.techStack.frameworks.slice(0, 3 - stack.length));
    }
    
    return stack;
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
    if (seconds < 2592000) return `${Math.floor(seconds / 604800)}w ago`;
    return `${Math.floor(seconds / 2592000)}mo ago`;
  }

  openProject(projectId: string): void {
    this.router.navigate(['/projects', projectId]);
  }

  createNewProject(): void {
    this.router.navigate(['/projects/new']);
  }

  onSearchChange(event: Event): void {
    const input = event.target as HTMLInputElement;
    this.searchQuery = input.value;
  }

  onStatusFilterChange(status: ProjectStatus | 'all'): void {
    this.statusFilter = status;
  }

  trackByProjectId(index: number, project: Project): string {
    return project.id;
  }
}
