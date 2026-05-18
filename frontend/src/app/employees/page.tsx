'use client';

import { useEffect, useState } from 'react';
import { api, type Employee, type PaginatedResponse } from '@/lib/api';
import { Search, Plus, Loader2 } from 'lucide-react';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export default function EmployeesPage() {
  const [data, setData] = useState<PaginatedResponse<Employee> | null>(null);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(1);
  const limit = 10;

  useEffect(() => {
    const fetchEmployees = async () => {
      setLoading(true);
      try {
        const skip = (page - 1) * limit;
        const res = await api.getEmployees(skip, limit, search);
        setData(res);
      } catch (error) {
        console.error("Failed to fetch employees", error);
      } finally {
        setLoading(false);
      }
    };

    // Add a small debounce for typing search
    const timer = setTimeout(() => {
      fetchEmployees();
    }, 300);

    return () => clearTimeout(timer);
  }, [page, limit, search]);

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white">Employees</h1>
          <p className="text-zinc-400 mt-1">Manage your workforce data.</p>
        </div>
        
        <button className="flex items-center justify-center rounded-lg bg-emerald-500 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-emerald-400 transition-colors">
          <Plus className="mr-2 h-4 w-4" />
          Add Employee
        </button>
      </div>

      <div className="card-glass rounded-xl overflow-hidden">
        {/* Toolbar */}
        <div className="p-4 border-b border-zinc-800 flex items-center gap-4 bg-zinc-900/50">
          <div className="relative flex-1 max-w-md">
            <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
              <Search className="h-5 w-5 text-zinc-500" aria-hidden="true" />
            </div>
            <input
              type="text"
              name="search"
              id="search"
              value={search}
              onChange={(e) => {
                setSearch(e.target.value);
                setPage(1); // reset to page 1 on new search
              }}
              className="block w-full rounded-md border-0 py-2 pl-10 bg-black/40 text-white shadow-sm ring-1 ring-inset ring-zinc-800 placeholder:text-zinc-500 focus:ring-2 focus:ring-inset focus:ring-emerald-500 sm:text-sm sm:leading-6 transition-all"
              placeholder="Search by name, department, or country..."
            />
          </div>
        </div>

        {/* Table */}
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-zinc-800">
            <thead className="bg-zinc-900/50">
              <tr>
                <th scope="col" className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-white sm:pl-6">Name</th>
                <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-white">Title</th>
                <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-white">Department</th>
                <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-white">Country</th>
                <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-white">Salary</th>
                <th scope="col" className="relative py-3.5 pl-3 pr-4 sm:pr-6">
                  <span className="sr-only">Edit</span>
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-800 bg-transparent">
              {loading && !data ? (
                <tr>
                  <td colSpan={6} className="py-10 text-center">
                    <Loader2 className="h-6 w-6 text-emerald-500 animate-spin mx-auto" />
                  </td>
                </tr>
              ) : data?.items.length === 0 ? (
                <tr>
                  <td colSpan={6} className="py-10 text-center text-zinc-500">
                    No employees found.
                  </td>
                </tr>
              ) : (
                data?.items.map((person) => (
                  <tr key={person.id} className="hover:bg-white/[0.02] transition-colors">
                    <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm sm:pl-6">
                      <div className="font-medium text-white">{person.full_name}</div>
                      <div className="text-zinc-500">{person.email}</div>
                    </td>
                    <td className="whitespace-nowrap px-3 py-4 text-sm text-zinc-300">{person.job_title}</td>
                    <td className="whitespace-nowrap px-3 py-4 text-sm text-zinc-300">
                      <span className="inline-flex items-center rounded-md bg-zinc-400/10 px-2 py-1 text-xs font-medium text-zinc-400 ring-1 ring-inset ring-zinc-400/20">
                        {person.department}
                      </span>
                    </td>
                    <td className="whitespace-nowrap px-3 py-4 text-sm text-zinc-300">{person.country}</td>
                    <td className="whitespace-nowrap px-3 py-4 text-sm text-zinc-300 font-mono">
                      ${person.salary.toLocaleString()}
                    </td>
                    <td className="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-6">
                      <button className="text-emerald-500 hover:text-emerald-400 transition-colors">
                        Edit
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        {data && data.total_pages > 1 && (
          <div className="border-t border-zinc-800 bg-zinc-900/50 px-4 py-3 flex items-center justify-between sm:px-6">
            <div className="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
              <div>
                <p className="text-sm text-zinc-400">
                  Showing <span className="font-medium text-white">{((page - 1) * limit) + 1}</span> to{' '}
                  <span className="font-medium text-white">
                    {Math.min(page * limit, data.total)}
                  </span>{' '}
                  of <span className="font-medium text-white">{data.total}</span> results
                </p>
              </div>
              <div>
                <nav className="isolate inline-flex -space-x-px rounded-md shadow-sm" aria-label="Pagination">
                  <button
                    onClick={() => setPage(p => Math.max(1, p - 1))}
                    disabled={page === 1 || loading}
                    className="relative inline-flex items-center rounded-l-md px-2 py-2 text-zinc-400 ring-1 ring-inset ring-zinc-800 hover:bg-zinc-800 disabled:opacity-50 transition-colors"
                  >
                    Previous
                  </button>
                  <button
                    onClick={() => setPage(p => Math.min(data.total_pages, p + 1))}
                    disabled={page === data.total_pages || loading}
                    className="relative inline-flex items-center rounded-r-md px-2 py-2 text-zinc-400 ring-1 ring-inset ring-zinc-800 hover:bg-zinc-800 disabled:opacity-50 transition-colors"
                  >
                    Next
                  </button>
                </nav>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
