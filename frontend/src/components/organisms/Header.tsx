/**
 * Header Component (Organism)
 * Modern header bar with breadcrumbs, actions, and user menu
 * Based on SIDEBAR_HEADER_SPECIFICATIONS.md
 */

import { useState, type ReactNode } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { cn } from '@utils/cn';
import { ChevronRight, Sun, Moon, Search, Bell, User, Settings, LogOut } from 'lucide-react';
import { Button } from '@components/atoms';
import { useUIStore } from '@stores/uiStore';

export interface BreadcrumbItem {
  label: string;
  href?: string;
  icon?: ReactNode;
}

export interface ActionButton {
  id: string;
  label: string;
  icon: ReactNode;
  onClick: () => void;
  variant?: 'default' | 'primary' | 'secondary';
  badge?: number;
}

export interface UserMenuItem {
  id: string;
  label: string;
  icon?: ReactNode;
  href?: string;
  onClick?: () => void;
  divider?: boolean;
}

export interface NavItem {
  id: string;
  label: string;
  icon?: ReactNode;
  href: string;
  group?: string;
}

export interface HeaderProps {
  title?: string;
  description?: string;
  breadcrumbs?: BreadcrumbItem[];
  primaryAction?: {
    label: string;
    icon?: ReactNode;
    onClick: () => void;
    variant?: 'primary' | 'secondary';
  };
  actions?: ActionButton[];
  showThemeToggle?: boolean;
  showNavigation?: boolean;
  navigationItems?: NavItem[];
  userMenu?: {
    avatar?: string;
    name?: string;
    email?: string;
    menuItems: UserMenuItem[];
  };
  search?: {
    placeholder?: string;
    value?: string;
    onChange?: (value: string) => void;
  };
  className?: string;
}

export function Header({
  title,
  description,
  breadcrumbs,
  primaryAction,
  actions = [],
  showThemeToggle = true,
  showNavigation = false,
  navigationItems = [],
  userMenu,
  search,
  className,
}: HeaderProps) {
  const location = useLocation();
  const theme = useUIStore((state) => state.theme);
  const toggleTheme = useUIStore((state) => state.toggleTheme);
  const [userMenuOpen, setUserMenuOpen] = useState(false);
  const [searchOpen, setSearchOpen] = useState(false);
  const isDark = theme === 'dark';

  const defaultUserMenu: UserMenuItem[] = userMenu?.menuItems || [
    { id: 'profile', label: 'Profile', icon: <User className="h-4 w-4" />, href: '/profile' },
    { id: 'settings', label: 'Settings', icon: <Settings className="h-4 w-4" />, href: '/settings' },
    { id: 'divider', label: '', divider: true },
    { id: 'logout', label: 'Logout', icon: <LogOut className="h-4 w-4" />, onClick: () => {} },
  ];

  return (
    <header
      className={cn(
        'sticky top-0 z-50 h-20',
        'bg-gradient-to-r from-background via-background to-background-secondary',
        'border-b border-border/50',
        'backdrop-blur-xl',
        isDark ? 'shadow-lg shadow-black/20' : 'shadow-lg shadow-gray-200/50',
        className
      )}
      role="banner"
      aria-label="Site header"
    >
      <div className="h-full px-6 lg:px-8 flex items-center max-w-[1920px] mx-auto relative">
        {/* Left Section: Breadcrumbs/Title */}
        <div className="flex-1 min-w-0">
          {breadcrumbs && breadcrumbs.length > 0 ? (
            <nav className="flex items-center gap-2 text-sm" aria-label="Breadcrumb">
              {breadcrumbs.map((crumb, index) => {
                const isLast = index === breadcrumbs.length - 1;
                return (
                  <div key={index} className="flex items-center gap-2">
                    {index > 0 && <ChevronRight className="h-4 w-4 text-text-tertiary" />}
                    {crumb.href && !isLast ? (
                      <Link
                        to={crumb.href}
                        className="text-text-secondary hover:text-primary transition-colors"
                      >
                        {crumb.icon && <span className="mr-1">{crumb.icon}</span>}
                        {crumb.label}
                      </Link>
                    ) : (
                      <span
                        className={cn(
                          'flex items-center gap-1',
                          isLast ? 'text-text-primary font-semibold' : 'text-text-secondary'
                        )}
                      >
                        {crumb.icon && <span>{crumb.icon}</span>}
                        {crumb.label}
                      </span>
                    )}
                  </div>
                );
              })}
            </nav>
          ) : (
            <div>
              {title && (
                <h1 className="text-2xl font-semibold text-text-primary line-height-tight">{title}</h1>
              )}
              {description && (
                <p className="text-sm text-text-secondary mt-1">{description}</p>
              )}
            </div>
          )}
        </div>

        {/* Center: Horizontal Navigation (absolutely centered) */}
        {showNavigation && navigationItems.length > 0 && (
          <nav 
            className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 flex items-center gap-2" 
            aria-label="Main navigation"
          >
            {navigationItems.map((item) => {
              const isActive = location.pathname === item.href || 
                (item.href !== '/' && location.pathname.startsWith(item.href));
              return (
                <Link
                  key={item.id}
                  to={item.href}
                  className={cn(
                    'flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-semibold transition-all duration-200 whitespace-nowrap',
                    isActive
                      ? 'bg-gradient-to-r from-primary to-primary-dark text-white shadow-lg shadow-primary/30 scale-105'
                      : 'text-text-secondary hover:text-text-primary hover:bg-background-tertiary/50 hover:scale-105'
                  )}
                >
                  {item.icon && <span className="text-lg">{item.icon}</span>}
                  {item.label}
                </Link>
              );
            })}
          </nav>
        )}

        {/* Right Section: Actions */}
        <div className="flex items-center gap-2 flex-1 justify-end">
          {/* Search */}
          {search && (
            <div className="relative">
              {searchOpen ? (
                <div className="flex items-center gap-2">
                  <input
                    type="text"
                    placeholder={search.placeholder || 'Search...'}
                    value={search.value || ''}
                    onChange={(e) => search.onChange?.(e.target.value)}
                    className="w-60 h-10 px-3 rounded-lg bg-background border border-border text-text-primary placeholder:text-text-tertiary focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
                    autoFocus
                    onBlur={() => setTimeout(() => setSearchOpen(false), 200)}
                  />
                </div>
              ) : (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setSearchOpen(true)}
                  className="h-10 w-10 p-0"
                  aria-label="Search"
                >
                  <Search className="h-5 w-5" />
                </Button>
              )}
            </div>
          )}

          {/* Action Buttons */}
          {actions.map((action) => (
            <Button
              key={action.id}
              variant={action.variant === 'primary' ? 'primary' : 'ghost'}
              size="sm"
              onClick={action.onClick}
              className="h-10 w-10 p-0 relative"
              aria-label={action.label}
            >
              <span className="relative">
                {action.icon}
                {action.badge !== undefined && action.badge > 0 && (
                  <span className="absolute -top-1 -right-1 flex items-center justify-center min-w-[18px] h-[18px] px-1 text-xs font-semibold text-white bg-error rounded-full">
                    {action.badge > 99 ? '99+' : action.badge}
                  </span>
                )}
              </span>
            </Button>
          ))}

          {/* Primary Action */}
          {primaryAction && (
            <Button
              variant={primaryAction.variant || 'primary'}
              size="md"
              onClick={primaryAction.onClick}
              className="h-11 px-6 bg-gradient-to-r from-primary to-primary-dark hover:from-primary-dark hover:to-primary shadow-lg shadow-primary/30 font-semibold"
            >
              {primaryAction.icon && <span className="mr-2">{primaryAction.icon}</span>}
              {primaryAction.label}
            </Button>
          )}

          {/* Theme Toggle */}
          {showThemeToggle && (
            <Button
              variant="ghost"
              size="sm"
              onClick={toggleTheme}
              className="h-10 w-10 p-0"
              aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
            >
              {theme === 'light' ? <Moon className="h-5 w-5" /> : <Sun className="h-5 w-5" />}
            </Button>
          )}

          {/* User Menu */}
          {userMenu && (
            <div className="relative">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setUserMenuOpen(!userMenuOpen)}
                className="h-10 w-10 p-0 rounded-full"
                aria-label="User menu"
                aria-expanded={userMenuOpen}
              >
                {userMenu.avatar ? (
                  <img
                    src={userMenu.avatar}
                    alt={userMenu.name || 'User'}
                    className="w-8 h-8 rounded-full"
                  />
                ) : (
                  <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center text-white font-semibold">
                    {userMenu.name?.[0]?.toUpperCase() || 'U'}
                  </div>
                )}
              </Button>

              {/* User Menu Dropdown */}
              {userMenuOpen && (
                <>
                  <div
                    className="fixed inset-0 z-40"
                    onClick={() => setUserMenuOpen(false)}
                    aria-hidden="true"
                  />
                  <div
                    className="absolute right-0 top-12 w-56 bg-background-secondary border border-border rounded-lg shadow-lg z-50 py-2"
                    role="menu"
                  >
                    {userMenu.name && (
                      <div className="px-4 py-2 border-b border-border">
                        <p className="text-sm font-semibold text-text-primary">{userMenu.name}</p>
                        {userMenu.email && (
                          <p className="text-xs text-text-secondary">{userMenu.email}</p>
                        )}
                      </div>
                    )}
                    {defaultUserMenu.map((item) => {
                      if (item.divider) {
                        return <div key={item.id} className="h-px bg-border my-2" />;
                      }

                      const content = (
                        <div className="flex items-center gap-3 px-4 py-2 text-sm text-text-primary hover:bg-background-tertiary cursor-pointer">
                          {item.icon && <span className="text-text-secondary">{item.icon}</span>}
                          <span>{item.label}</span>
                        </div>
                      );

                      if (item.href) {
                        return (
                          <Link
                            key={item.id}
                            to={item.href}
                            onClick={() => {
                              setUserMenuOpen(false);
                              item.onClick?.();
                            }}
                          >
                            {content}
                          </Link>
                        );
                      }

                      return (
                        <div
                          key={item.id}
                          onClick={() => {
                            setUserMenuOpen(false);
                            item.onClick?.();
                          }}
                        >
                          {content}
                        </div>
                      );
                    })}
                  </div>
                </>
              )}
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
