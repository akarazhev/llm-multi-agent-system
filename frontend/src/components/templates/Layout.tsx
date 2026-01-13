/**
 * Layout Component (Template)
 * Modern layout with Sidebar and Header
 * Based on SIDEBAR_HEADER_SPECIFICATIONS.md
 */

import { useState, type ReactNode } from 'react';
import { useLocation } from 'react-router-dom';
import { LayoutDashboard, Workflow, Users } from 'lucide-react';
import { Sidebar, Header } from '@components/organisms';
import type { NavItem } from '@components/organisms/Header';
import type { NavItem as SidebarNavItem } from '@components/organisms/Sidebar';
import { cn } from '@utils/cn';

interface LayoutProps {
  children: ReactNode;
  title?: string;
  description?: string;
  breadcrumbs?: Array<{ label: string; href?: string }>;
  primaryAction?: {
    label: string;
    icon?: ReactNode;
    onClick: () => void;
  };
  showSidebar?: boolean;
}

export function Layout({ 
  children, 
  title, 
  description, 
  breadcrumbs, 
  primaryAction,
  showSidebar = false 
}: LayoutProps) {
  const location = useLocation();
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  const navItems: SidebarNavItem[] = [
    {
      id: 'dashboard',
      label: 'Dashboard',
      icon: <LayoutDashboard className="h-5 w-5" />,
      href: '/',
      group: 'main',
    },
    {
      id: 'workflows',
      label: 'Workflows',
      icon: <Workflow className="h-5 w-5" />,
      href: '/workflows',
      group: 'main',
    },
    {
      id: 'agents',
      label: 'Agents',
      icon: <Users className="h-5 w-5" />,
      href: '/agents',
      group: 'main',
    },
  ];

  // Auto-generate title from route if not provided
  const pageTitle = title || (() => {
    const route = location.pathname;
    if (route === '/') return 'Dashboard';
    if (route.startsWith('/workflows')) return 'Workflows';
    if (route.startsWith('/agents')) return 'Agents';
    return 'LLM Multi-Agent System';
  })();

  // Auto-generate breadcrumbs if not provided
  const pageBreadcrumbs = breadcrumbs || (() => {
    const route = location.pathname;
    if (route === '/') return [{ label: 'Dashboard' }];
    if (route.startsWith('/workflows')) {
      if (route === '/workflows/new') {
        return [
          { label: 'Workflows', href: '/workflows' },
          { label: 'New Workflow' },
        ];
      }
      if (route.match(/^\/workflows\/[^/]+$/)) {
        return [
          { label: 'Workflows', href: '/workflows' },
          { label: 'Workflow Details' },
        ];
      }
      return [{ label: 'Workflows' }];
    }
    if (route.startsWith('/agents')) {
      return [{ label: 'Agents' }];
    }
    return [];
  })();

  return (
    <div className="min-h-screen bg-background text-text-primary transition-colors">
      {showSidebar && (
        <Sidebar
          items={navItems}
          appName="LLM Multi-Agent System"
          collapsed={sidebarCollapsed}
          onCollapseChange={setSidebarCollapsed}
        />
      )}
      <div className={cn(
        'transition-all duration-300',
        showSidebar && (sidebarCollapsed ? 'lg:ml-16' : 'lg:ml-60')
      )}>
        <Header
          title={pageTitle}
          description={description}
          breadcrumbs={pageBreadcrumbs.map((bc) => ({
            label: bc.label,
            href: bc.href,
          }))}
          primaryAction={primaryAction}
          showThemeToggle={true}
          showNavigation={true}
          navigationItems={navItems}
          userMenu={{
            name: 'User',
            email: 'user@example.com',
            menuItems: [
              { id: 'profile', label: 'Profile', href: '/profile' },
              { id: 'settings', label: 'Settings', href: '/settings' },
              { id: 'divider', label: '', divider: true },
              { id: 'logout', label: 'Logout', onClick: () => {} },
            ],
          }}
        />
        <main className="container mx-auto px-6 py-8 lg:px-8 max-w-[1920px]">
          <div className="space-y-8">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}
