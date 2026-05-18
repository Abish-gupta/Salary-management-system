import { api } from "@/lib/api";
import { CountrySalaryChart, DepartmentSalaryChart } from "@/components/DashboardCharts";
import { Banknote, Users, TrendingUp, Building2 } from "lucide-react";

export const dynamic = 'force-dynamic';

export default async function Dashboard() {
  // Fetch analytics data server-side
  const [globalStats, countryStats, departmentStats] = await Promise.all([
    api.getGlobalStats().catch(() => ({ total_employees: 0, avg_salary: 0, max_salary: 0 })),
    api.getCountryStats().catch(() => []),
    api.getDepartmentStats().catch(() => [])
  ]);

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div>
        <h1 className="text-3xl font-bold tracking-tight text-white">Analytics Overview</h1>
        <p className="text-zinc-400 mt-2">Salary insights and company-wide distributions.</p>
      </div>

      {/* Global Stats Row */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <div className="card-glass rounded-xl p-6 relative overflow-hidden group">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-zinc-400">Total Employees</p>
              <p className="text-3xl font-bold text-white mt-2">
                {globalStats.total_employees.toLocaleString()}
              </p>
            </div>
            <div className="h-12 w-12 rounded-full bg-emerald-500/10 flex items-center justify-center">
              <Users className="h-6 w-6 text-emerald-500" />
            </div>
          </div>
          <div className="absolute -bottom-4 -right-4 h-24 w-24 bg-emerald-500/10 rounded-full blur-2xl group-hover:bg-emerald-500/20 transition-all duration-500" />
        </div>

        <div className="card-glass rounded-xl p-6 relative overflow-hidden group">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-zinc-400">Average Salary</p>
              <p className="text-3xl font-bold text-white mt-2">
                ${Number(globalStats.avg_salary).toLocaleString(undefined, { maximumFractionDigits: 0 })}
              </p>
            </div>
            <div className="h-12 w-12 rounded-full bg-blue-500/10 flex items-center justify-center">
              <Banknote className="h-6 w-6 text-blue-500" />
            </div>
          </div>
          <div className="absolute -bottom-4 -right-4 h-24 w-24 bg-blue-500/10 rounded-full blur-2xl group-hover:bg-blue-500/20 transition-all duration-500" />
        </div>

        <div className="card-glass rounded-xl p-6 relative overflow-hidden group">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-zinc-400">Highest Salary</p>
              <p className="text-3xl font-bold text-white mt-2">
                ${Number(globalStats.max_salary).toLocaleString()}
              </p>
            </div>
            <div className="h-12 w-12 rounded-full bg-purple-500/10 flex items-center justify-center">
              <TrendingUp className="h-6 w-6 text-purple-500" />
            </div>
          </div>
          <div className="absolute -bottom-4 -right-4 h-24 w-24 bg-purple-500/10 rounded-full blur-2xl group-hover:bg-purple-500/20 transition-all duration-500" />
        </div>

        <div className="card-glass rounded-xl p-6 relative overflow-hidden group">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-zinc-400">Departments</p>
              <p className="text-3xl font-bold text-white mt-2">
                {departmentStats.length}
              </p>
            </div>
            <div className="h-12 w-12 rounded-full bg-amber-500/10 flex items-center justify-center">
              <Building2 className="h-6 w-6 text-amber-500" />
            </div>
          </div>
          <div className="absolute -bottom-4 -right-4 h-24 w-24 bg-amber-500/10 rounded-full blur-2xl group-hover:bg-amber-500/20 transition-all duration-500" />
        </div>
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <div className="card-glass rounded-xl p-6">
          <h2 className="text-lg font-semibold text-white">Average Salary by Country</h2>
          <p className="text-sm text-zinc-400">Geographic compensation distribution.</p>
          {countryStats.length > 0 ? (
            <CountrySalaryChart data={countryStats} />
          ) : (
            <div className="h-80 flex items-center justify-center text-zinc-500">No data available</div>
          )}
        </div>

        <div className="card-glass rounded-xl p-6">
          <h2 className="text-lg font-semibold text-white">Salary by Department</h2>
          <p className="text-sm text-zinc-400">Average vs Maximum salary comparison.</p>
          {departmentStats.length > 0 ? (
            <DepartmentSalaryChart data={departmentStats} />
          ) : (
            <div className="h-80 flex items-center justify-center text-zinc-500">No data available</div>
          )}
        </div>
      </div>
    </div>
  );
}
