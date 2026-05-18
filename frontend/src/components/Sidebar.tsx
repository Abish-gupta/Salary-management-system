'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { LayoutDashboard, Users, Settings, Building2 } from 'lucide-react';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function Sidebar() {
  const pathname = usePathname();

  const navigation = [
    { name: 'Dashboard', href: '/', icon: LayoutDashboard },
    { name: 'Employees', href: '/employees', icon: Users },
  ];

  return (
    <div className="flex h-screen w-64 flex-col glass border-r">
      <div className="flex h-16 shrink-0 items-center px-6 border-b border-white/5">
        <Building2 className="h-6 w-6 text-emerald-500 mr-2" />
        <span className="text-lg font-semibold tracking-tight text-white">Incubyte</span>
      </div>
      <div className="flex flex-1 flex-col overflow-y-auto">
        <nav className="flex-1 space-y-1 px-4 py-6">
          {navigation.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.name}
                href={item.href}
                className={cn(
                  isActive
                    ? 'bg-emerald-500/10 text-emerald-500'
                    : 'text-zinc-400 hover:bg-white/5 hover:text-white',
                  'group flex items-center rounded-lg px-3 py-2.5 text-sm font-medium transition-all duration-200'
                )}
              >
                <item.icon
                  className={cn(
                    isActive ? 'text-emerald-500' : 'text-zinc-400 group-hover:text-white',
                    'mr-3 h-5 w-5 flex-shrink-0 transition-colors duration-200'
                  )}
                  aria-hidden="true"
                />
                {item.name}
              </Link>
            );
          })}
        </nav>
      </div>
      <div className="border-t border-white/5 p-4">
        <div className="flex items-center gap-x-3 rounded-lg px-3 py-2 text-sm font-medium text-zinc-400 hover:bg-white/5 hover:text-white cursor-pointer transition-colors duration-200">
          <Settings className="h-5 w-5 shrink-0" />
          Settings
        </div>
      </div>
    </div>
  );
}
