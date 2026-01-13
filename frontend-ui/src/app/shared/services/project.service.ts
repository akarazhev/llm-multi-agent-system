import { Injectable, signal } from '@angular/core';
import { Observable, of, delay } from 'rxjs';
import { Project, ProjectFormData } from '../../core/interfaces/project.interface';
import { mockProjects } from '../../mocks/mock-projects';

@Injectable({
  providedIn: 'root'
})
export class ProjectService {
  // Signal for reactive projects list - initialize with mock data
  projects = signal<Project[]>(mockProjects);
  loading = signal<boolean>(false);

  constructor() {
    // Projects are already loaded from mock data
  }

  /**
   * Load all projects
   */
  loadProjects(): void {
    this.loading.set(true);
    this.getProjects().subscribe(projects => {
      this.projects.set(projects);
      this.loading.set(false);
    });
  }

  /**
   * Get all projects
   */
  getProjects(): Observable<Project[]> {
    // Return mock data for now
    return of(mockProjects).pipe(delay(300));
  }

  /**
   * Get project by ID
   */
  getProjectById(id: string): Observable<Project | undefined> {
    const project = this.projects().find(p => p.id === id);
    return of(project).pipe(delay(100));
  }

  /**
   * Create new project
   */
  createProject(data: ProjectFormData): Observable<Project> {
    const newProject: Project = {
      id: `proj-${Date.now()}`,
      ...data,
      ownerId: 'current-user',
      teamMembers: [],
      aiAgents: [],
      integrations: {},
      stats: {
        totalWorkflows: 0,
        activeWorkflows: 0,
        completedWorkflows: 0,
        failedWorkflows: 0,
        teamSize: 1,
        aiAgentsCount: 0,
        filesGenerated: 0,
        linesOfCode: 0
      },
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };

    return of(newProject).pipe(delay(500));
  }

  /**
   * Update project
   */
  updateProject(id: string, data: Partial<Project>): Observable<Project> {
    const projects = this.projects();
    const index = projects.findIndex(p => p.id === id);
    
    if (index !== -1) {
      const updatedProject = {
        ...projects[index],
        ...data,
        updatedAt: new Date().toISOString()
      };
      
      projects[index] = updatedProject;
      this.projects.set([...projects]);
      
      return of(updatedProject).pipe(delay(300));
    }
    
    throw new Error('Project not found');
  }

  /**
   * Delete project
   */
  deleteProject(id: string): Observable<boolean> {
    const projects = this.projects().filter(p => p.id !== id);
    this.projects.set(projects);
    return of(true).pipe(delay(300));
  }

  /**
   * Get projects by status
   */
  getProjectsByStatus(status: string): Project[] {
    return this.projects().filter(p => p.status === status);
  }

  /**
   * Get user's active projects
   */
  getActiveProjects(): Project[] {
    return this.projects().filter(p => p.status === 'active');
  }
}
