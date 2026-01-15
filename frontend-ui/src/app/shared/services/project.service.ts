import { Injectable, signal, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, catchError, finalize, map, of, tap } from 'rxjs';
import { Project, ProjectFormData } from '../../core/interfaces/project.interface';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ProjectService {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = environment.apiUrl;
  // Signal for reactive projects list - initialize with mock data
  projects = signal<Project[]>([]);
  loading = signal<boolean>(false);

  constructor() {
    this.loadProjects();
  }

  /**
   * Load all projects
   */
  loadProjects(): void {
    this.loading.set(true);
    this.getProjects().pipe(
      finalize(() => this.loading.set(false))
    ).subscribe(projects => this.projects.set(projects));
  }

  /**
   * Get all projects
   */
  getProjects(): Observable<Project[]> {
    return this.http.get<Project[]>(`${this.apiUrl}/projects`).pipe(
      catchError(() => of([]))
    );
  }

  /**
   * Get project by ID
   */
  getProjectById(id: string): Observable<Project | undefined> {
    return this.http.get<Project>(`${this.apiUrl}/projects/${id}`).pipe(
      catchError(() => of(undefined))
    );
  }

  /**
   * Create new project
   */
  createProject(data: ProjectFormData): Observable<Project> {
    return this.http.post<Project>(`${this.apiUrl}/projects`, data).pipe(
      tap(project => this.projects.update(projects => [...projects, project])),
      catchError(() => of(undefined as unknown as Project))
    );
  }

  /**
   * Update project
   */
  updateProject(id: string, data: Partial<Project>): Observable<Project> {
    const current = this.projects().find(p => p.id === id);
    if (!current) {
      return of(undefined as unknown as Project);
    }

    const payload: ProjectFormData = {
      name: data.name ?? current.name,
      description: data.description ?? current.description,
      icon: data.icon ?? current.icon,
      status: data.status ?? current.status,
      type: data.type ?? current.type,
      techStack: data.techStack ?? current.techStack,
      integrations: data.integrations ?? current.integrations
    };

    return this.http.put<Project>(`${this.apiUrl}/projects/${id}`, payload).pipe(
      tap(project => {
        this.projects.update(projects =>
          projects.map(p => p.id === id ? project : p)
        );
      }),
      catchError(() => of(undefined as unknown as Project))
    );
  }

  assignAgents(projectId: string, agentIds: string[]): Observable<Project> {
    return this.http.post<Project>(`${this.apiUrl}/projects/${projectId}/agents`, {
      agent_ids: agentIds
    }).pipe(
      tap(project => {
        this.projects.update(projects =>
          projects.map(p => p.id === projectId ? project : p)
        );
      }),
      catchError(() => of(undefined as unknown as Project))
    );
  }

  /**
   * Delete project
   */
  deleteProject(id: string): Observable<boolean> {
    return this.http.delete(`${this.apiUrl}/projects/${id}`).pipe(
      tap(() => this.projects.update(projects => projects.filter(p => p.id !== id))),
      map(() => true),
      catchError(() => of(false))
    ) as Observable<boolean>;
  }

  createDemoProject(): Observable<{ projectId: string; workflowId: string } | undefined> {
    return this.http.post<{ projectId: string; workflowId: string }>(`${this.apiUrl}/demo/inventory`, {}).pipe(
      catchError(() => of(undefined))
    );
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
