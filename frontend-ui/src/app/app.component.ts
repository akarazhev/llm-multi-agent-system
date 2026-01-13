import { Component, computed, signal, ChangeDetectionStrategy } from '@angular/core';
import { RouterOutlet, RouterLink } from '@angular/router';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatListModule } from '@angular/material/list';
import { MatTooltipModule } from '@angular/material/tooltip';
import { NgOptimizedImage } from '@angular/common';
import { Router } from '@angular/router';
import { ThemeService } from './shared/services/theme.service';

interface NavItem {
  label: string;
  icon: string;
  route: string;
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    RouterOutlet,
    RouterLink,
    MatToolbarModule,
    MatButtonModule,
    MatIconModule,
    MatSidenavModule,
    MatListModule,
    MatTooltipModule,
    NgOptimizedImage
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class AppComponent {
  title = 'LLM Multi-Agent System';
  
  menuCollapsed = signal(false);
  
  sideNavWidth = computed(() =>
    this.menuCollapsed() ? '5rem' : 'max-content'
  );
  
  sideNavOffset = computed(() =>
    this.menuCollapsed() ? '5rem' : '13rem'
  );

  navItems: NavItem[] = [
    { label: 'Dashboard', icon: 'dashboard', route: '/dashboard' },
    { label: 'Projects', icon: 'folder', route: '/projects' },
    { label: 'Workflows', icon: 'account_tree', route: '/workflows' },
    { label: 'Agents', icon: 'smart_toy', route: '/agents' },
  ];

  constructor(
    private router: Router,
    public themeService: ThemeService
  ) {}

  isActive(route: string): boolean {
    return this.router.url.startsWith(route);
  }

  getSpgLogo(): string {
    if (this.themeService.isDark()) {
      return 'images/spg_logo.png';
    } else {
      return 'images/spg_logo_black.svg';
    }
  }

  toggleTheme(): void {
    this.themeService.toggleTheme();
  }

  getThemeIcon(): string {
    return this.themeService.isDark() ? 'light_mode' : 'dark_mode';
  }

  getThemeTooltip(): string {
    return this.themeService.isDark() ? 'Switch to light mode' : 'Switch to dark mode';
  }
}
