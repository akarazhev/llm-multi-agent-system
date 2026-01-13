import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'dashboard',
    pathMatch: 'full'
  },
  {
    path: 'dashboard',
    loadComponent: () => import('./pages/dashboard/dashboard.component').then(m => m.DashboardComponent)
  },
  {
    path: 'workflows',
    loadComponent: () => import('./pages/workflows/workflows.component').then(m => m.WorkflowsComponent)
  },
  {
    path: 'workflows/:id',
    loadComponent: () => import('./pages/workflow-detail/workflow-detail.component').then(m => m.WorkflowDetailComponent)
  },
  {
    path: 'agents',
    loadComponent: () => import('./pages/agents/agents.component').then(m => m.AgentsComponent)
  },
  {
    path: '**',
    redirectTo: 'dashboard'
  }
];
