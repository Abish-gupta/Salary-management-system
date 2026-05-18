'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { LayoutDashboard, Users, Building2, PanelLeftClose, PanelLeftOpen } from 'lucide-react';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function Sidebar() {
  const pathname = usePathname();
  const [isCollapsed, setIsCollapsed] = useState(false);

  const navigation = [
    { name: 'Dashboard', href: '/', icon: LayoutDashboard },
    { name: 'Employees', href: '/employees', icon: Users },
  ];

  return (
    <div className={cn("flex h-screen flex-col glass border-r bg-card/50 transition-all duration-300 relative", isCollapsed ? "w-20" : "w-64")}>
      <div className={cn("flex h-16 shrink-0 items-center border-b border-border", isCollapsed ? "justify-center px-0" : "px-6")}>
        <Building2 className={cn("h-6 w-6 text-primary", !isCollapsed && "mr-2")} />
        {!isCollapsed && <span className="text-lg font-semibold tracking-tight text-foreground">Incubyte</span>}
      </div>
      
      <button 
        onClick={() => setIsCollapsed(!isCollapsed)}
        className="absolute -right-3 top-5 bg-background border border-border text-foreground rounded-full p-1 shadow-sm hover:bg-secondary transition-colors z-10"
      >
        {isCollapsed ? <PanelLeftOpen className="w-4 h-4" /> : <PanelLeftClose className="w-4 h-4" />}
      </button>

      <div className="flex flex-1 flex-col overflow-y-auto overflow-x-hidden">
        <nav className={cn("flex-1 space-y-2 py-6", isCollapsed ? "px-2" : "px-4")}>
          {navigation.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.name}
                href={item.href}
                title={isCollapsed ? item.name : undefined}
                className={cn(
                  isActive
                    ? 'bg-primary/10 text-primary'
                    : 'text-muted-foreground hover:bg-secondary hover:text-foreground',
                  'group flex items-center rounded-lg py-2.5 text-sm font-medium transition-all duration-200',
                  isCollapsed ? 'justify-center px-0' : 'px-3'
                )}
              >
                <item.icon
                  className={cn(
                    isActive ? 'text-primary' : 'text-muted-foreground group-hover:text-foreground',
                    'h-5 w-5 flex-shrink-0 transition-colors duration-200',
                    !isCollapsed && 'mr-3'
                  )}
                  aria-hidden="true"
                />
                {!isCollapsed && item.name}
              </Link>
            );
          })}
        </nav>
      </div>
    </div>
  );
}
