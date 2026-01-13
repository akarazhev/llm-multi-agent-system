/**
 * Sidebar Component (Organism)
 * Modern sidebar navigation with glassmorphism effect
 * Based on SIDEBAR_HEADER_SPECIFICATIONS.md
 */

import { useState, type ReactNode } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { cn } from '@utils/cn';
import { ChevronLeft, ChevronRight, Menu, X } from 'lucide-react';
import { Button } from '@components/atoms';
import { useUIStore } from '@stores/uiStore';

export interface NavItem {
  id: string;
  label: string;
  icon: ReactNode;
  href: string;
  badge?: number;
  active?: boolean;
  group?: string;
  onClick?: () => void;
}

export interface SidebarProps {
  items: NavItem[];
  activeRoute?: string;
  collapsed?: boolean;
  onCollapseChange?: (collapsed: boolean) => void;
  logo?: ReactNode;
  appName?: string;
  showCollapseButton?: boolean;
  className?: string;
}

export function Sidebar({
  items,
  activeRoute,
  collapsed: controlledCollapsed,
  onCollapseChange,
  logo,
  appName = 'LLM Multi-Agent System',
  showCollapseButton = true,
  className,
}: SidebarProps) {
  const location = useLocation();
  const [internalCollapsed, setInternalCollapsed] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const theme = useUIStore((state) => state.theme);

  const isCollapsed = controlledCollapsed !== undefined ? controlledCollapsed : internalCollapsed;
  const isDark = theme === 'dark';

  const handleCollapse = () => {
    const newCollapsed = !isCollapsed;
    if (onCollapseChange) {
      onCollapseChange(newCollapsed);
    } else {
      setInternalCollapsed(newCollapsed);
    }
  };

  const handleMobileClose = () => {
    setMobileOpen(false);
  };

  // Determine active route
  const currentRoute = activeRoute || location.pathname;

  // Group items by group property
  const groupedItems = items.reduce((acc, item) => {
    const group = item.group || 'main';
    if (!acc[group]) {
      acc[group] = [];
    }
    acc[group].push(item);
    return acc;
  }, {} as Record<string, NavItem[]>);

  const sidebarContent = (
    <>
      {/* Header Section */}
      <div className="h-16 flex items-center justify-between px-4 border-b border-border">
        {!isCollapsed && (
          <div className="flex items-center gap-3">
            {logo && <div className="w-8 h-8">{logo}</div>}
            <span className="text-xl font-semibold text-text-primary">{appName}</span>
          </div>
        )}
        {isCollapsed && logo && <div className="w-8 h-8 mx-auto">{logo}</div>}
        {showCollapseButton && (
          <Button
            variant="ghost"
            size="sm"
            onClick={handleCollapse}
            className="h-8 w-8 p-0"
            aria-label={isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
          >
            {isCollapsed ? <ChevronRight className="h-4 w-4" /> : <ChevronLeft className="h-4 w-4" />}
          </Button>
        )}
      </div>

      {/* Navigation Items */}
      <nav className="flex-1 overflow-y-auto px-2 py-4" role="navigation" aria-label="Main navigation">
        {Object.entries(groupedItems).map(([group, groupItems]) => (
          <div key={group} className="mb-4">
            {group !== 'main' && !isCollapsed && (
              <div className="px-3 py-2 text-xs font-medium text-text-tertiary uppercase tracking-wider">
                {group}
              </div>
            )}
            <div className="space-y-1">
              {groupItems.map((item) => {
                const isActive = item.active !== undefined ? item.active : currentRoute === item.href;

                return (
                  <Link
                    key={item.id}
                    to={item.href}
                    onClick={() => {
                      if (item.onClick) item.onClick();
                      setMobileOpen(false);
                    }}
                    className={cn(
                      'flex items-center gap-3 h-10 px-3 rounded-lg text-sm font-medium transition-all duration-200',
                      'hover:bg-background-tertiary',
                      isActive
                        ? 'bg-primary/10 text-primary border-l-3 border-primary font-semibold'
                        : 'text-text-secondary hover:text-text-primary',
                      isCollapsed && 'justify-center px-2'
                    )}
                    aria-current={isActive ? 'page' : undefined}
                  >
                    <span className={cn('h-5 w-5 flex-shrink-0 flex items-center justify-center', isActive && 'text-primary')}>
                      {item.icon}
                    </span>
                    {!isCollapsed && (
                      <>
                        <span className="flex-1">{item.label}</span>
                        {item.badge !== undefined && item.badge > 0 && (
                          <span className="flex items-center justify-center min-w-[18px] h-[18px] px-1.5 text-xs font-semibold text-white bg-error rounded-full">
                            {item.badge > 99 ? '99+' : item.badge}
                          </span>
                        )}
                      </>
                    )}
                    {isCollapsed && item.badge !== undefined && item.badge > 0 && (
                      <span className="absolute top-1 right-1 w-2 h-2 bg-error rounded-full" />
                    )}
                  </Link>
                );
              })}
            </div>
          </div>
        ))}
      </nav>

      {/* Footer Section (optional) */}
      {showCollapseButton && !isCollapsed && (
        <div className="border-t border-border p-2">
          <Button
            variant="ghost"
            size="sm"
            onClick={handleCollapse}
            className="w-full justify-start"
            aria-label="Collapse sidebar"
          >
            <ChevronLeft className="h-4 w-4 mr-2" />
            Collapse
          </Button>
        </div>
      )}
    </>
  );

  return (
    <>
      {/* Mobile Hamburger Button */}
      <div className="lg:hidden fixed top-4 left-4 z-50">
        <Button
          variant="ghost"
          size="sm"
          onClick={() => setMobileOpen(true)}
          className="h-10 w-10 p-0"
          aria-label="Open navigation menu"
        >
          <Menu className="h-5 w-5" />
        </Button>
      </div>

      {/* Mobile Overlay */}
      {mobileOpen && (
        <div
          className="lg:hidden fixed inset-0 bg-black/50 z-40 backdrop-blur-sm"
          onClick={handleMobileClose}
          aria-hidden="true"
        />
      )}

      {/* Sidebar */}
      <aside
        className={cn(
          'fixed left-0 top-0 h-screen z-40',
          'bg-background-secondary border-r border-border',
          'backdrop-blur-xl',
          isDark ? 'bg-white/5' : 'bg-white/80',
          'shadow-md',
          'transition-all duration-300 ease-in-out',
          isCollapsed ? 'w-16' : 'w-60',
          'lg:translate-x-0',
          mobileOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0',
          className
        )}
        role="complementary"
        aria-label="Sidebar navigation"
      >
        <div className="flex flex-col h-full">
          {/* Close button for mobile */}
          {mobileOpen && (
            <div className="lg:hidden flex items-center justify-end p-4 border-b border-border">
              <Button
                variant="ghost"
                size="sm"
                onClick={handleMobileClose}
                className="h-8 w-8 p-0"
                aria-label="Close navigation menu"
              >
                <X className="h-5 w-5" />
              </Button>
            </div>
          )}
          {sidebarContent}
        </div>
      </aside>

      {/* Spacer for desktop */}
      <div className={cn('hidden lg:block transition-all duration-300', isCollapsed ? 'w-16' : 'w-60')} />
    </>
  );
}
