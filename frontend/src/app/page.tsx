'use client';

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { CountrySalaryChart, DepartmentSalaryChart } from "@/components/DashboardCharts";
import { CountryFilterDashboard } from "@/components/CountryFilterDashboard";
import { Banknote, Users, TrendingUp, Building2, Loader2, Database, Wifi } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

interface GlobalStats {
  total_employees: number;
  avg_salary: number;
  max_salary: number;
}

export default function Dashboard() {
  const [globalStats, setGlobalStats] = useState<GlobalStats>({ total_employees: 0, avg_salary: 0, max_salary: 0 });
  const [countryStats, setCountryStats] = useState<any[]>([]);
  const [departmentStats, setDepartmentStats] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [isSleeping, setIsSleeping] = useState(false);
  const [wakingProgress, setWakingProgress] = useState(0);
  const [currentTipIndex, setCurrentTipIndex] = useState(0);

  const tips = [
    "Spinning up the Render FastAPI server containers...",
    "Waking up the SQLite backend database...",
    "Compiling 10,000+ employee record schemas...",
    "Calculating global average salary metrics...",
    "Generating Recharts visual analytics..."
  ];

  useEffect(() => {
    let sleepTimer: NodeJS.Timeout;
    let progressInterval: NodeJS.Timeout;
    let tipInterval: NodeJS.Timeout;

    // Start a timer to detect if server is in deep sleep (Render Free Plan)
    // If it takes more than 2 seconds, we flag it as sleeping and show the wake-up progress bar
    sleepTimer = setTimeout(() => {
      setIsSleeping(true);
      // Start progress simulation over ~45 seconds
      progressInterval = setInterval(() => {
        setWakingProgress((prev) => {
          if (prev >= 98) return prev;
          return prev + 1;
        });
      }, 450);

      // Rotate tips every 8 seconds
      tipInterval = setInterval(() => {
        setCurrentTipIndex((prev) => (prev + 1) % tips.length);
      }, 7000);
    }, 2000);

    const fetchData = async () => {
      try {
        const [stats, countries, depts] = await Promise.all([
          api.getGlobalStats(),
          api.getCountryStats(),
          api.getDepartmentStats()
        ]);
        setGlobalStats(stats);
        setCountryStats(countries);
        setDepartmentStats(depts);
      } catch (err) {
        console.error("Failed to fetch dashboard data", err);
      } finally {
        clearTimeout(sleepTimer);
        clearInterval(progressInterval);
        clearInterval(tipInterval);
        setLoading(false);
        setIsSleeping(false);
      }
    };

    fetchData();

    return () => {
      clearTimeout(sleepTimer);
      if (progressInterval) clearInterval(progressInterval);
      if (tipInterval) clearInterval(tipInterval);
    };
  }, []);

  const uniqueCountries = countryStats.map((c: { country: string }) => c.country).sort();

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div>
        <h1 className="text-3xl font-bold tracking-tight text-foreground">Analytics Overview</h1>
        <p className="text-muted-foreground mt-2">Salary insights and company-wide distributions.</p>
      </div>

      <AnimatePresence mode="wait">
        {loading ? (
          <motion.div
            key="loading"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="flex flex-col items-center justify-center min-h-[400px] p-8 card-glass rounded-2xl border border-border"
          >
            {isSleeping ? (
              <div className="w-full max-w-md text-center space-y-6">
                <div className="flex justify-center relative">
                  <div className="absolute -inset-1 rounded-full bg-emerald-500/20 blur-lg animate-pulse" />
                  <div className="h-16 w-16 rounded-full bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center relative z-10 animate-bounce">
                    <Database className="h-8 w-8 text-emerald-500" />
                  </div>
                </div>

                <div className="space-y-2">
                  <h3 className="text-lg font-bold text-foreground flex items-center justify-center gap-2">
                    <Wifi className="w-4 h-4 text-emerald-500 animate-pulse" />
                    Waking Up Render Server...
                  </h3>
                  <p className="text-sm text-muted-foreground">
                    This project uses Render's free tier, which auto-sleeps after 15 minutes of inactivity. We are spinning it up now (takes ~45s)!
                  </p>
                </div>

                <div className="space-y-2">
                  <div className="w-full bg-secondary/60 h-2 rounded-full overflow-hidden border border-border">
                    <motion.div 
                      className="bg-emerald-500 h-full rounded-full"
                      initial={{ width: "0%" }}
                      animate={{ width: `${wakingProgress}%` }}
                      transition={{ ease: "easeOut" }}
                    />
                  </div>
                  <div className="flex justify-between text-xs text-muted-foreground">
                    <span>Starting backend containers...</span>
                    <span>{wakingProgress}%</span>
                  </div>
                </div>

                <div className="h-8 flex items-center justify-center">
                  <motion.p 
                    key={currentTipIndex}
                    initial={{ opacity: 0, y: 5 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -5 }}
                    className="text-xs font-medium text-emerald-500/80 italic"
                  >
                    {tips[currentTipIndex]}
                  </motion.p>
                </div>
              </div>
            ) : (
              <div className="flex flex-col items-center gap-4">
                <Loader2 className="h-8 w-8 text-emerald-500 animate-spin" />
                <p className="text-sm text-muted-foreground font-medium">Connecting to API service...</p>
              </div>
            )}
          </motion.div>
        ) : (
          <motion.div
            key="dashboard-content"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="space-y-8"
          >
            {/* Global Stats Row */}
            <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
              <div className="card-glass rounded-xl p-6 relative overflow-hidden group">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-muted-foreground">Total Employees</p>
                    <p className="text-3xl font-bold text-foreground mt-2">
                      {globalStats.total_employees.toLocaleString()}
                    </p>
                  </div>
                  <div className="h-12 w-12 rounded-full bg-primary/10 flex items-center justify-center">
                    <Users className="h-6 w-6 text-primary" />
                  </div>
                </div>
                <div className="absolute -bottom-4 -right-4 h-24 w-24 bg-primary/10 rounded-full blur-2xl group-hover:bg-primary/20 transition-all duration-500" />
              </div>

              <div className="card-glass rounded-xl p-6 relative overflow-hidden group">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-muted-foreground">Average Salary</p>
                    <p className="text-3xl font-bold text-foreground mt-2">
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
                    <p className="text-sm font-medium text-muted-foreground">Highest Salary</p>
                    <p className="text-3xl font-bold text-foreground mt-2">
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
                    <p className="text-sm font-medium text-muted-foreground">Departments</p>
                    <p className="text-3xl font-bold text-foreground mt-2">
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
                <h2 className="text-lg font-semibold text-foreground">Average Salary by Country</h2>
                <p className="text-sm text-muted-foreground">Geographic compensation distribution.</p>
                {countryStats.length > 0 ? (
                  <CountrySalaryChart data={countryStats} />
                ) : (
                  <div className="h-80 flex items-center justify-center text-muted-foreground">No data available</div>
                )}
              </div>

              <div className="card-glass rounded-xl p-6">
                <h2 className="text-lg font-semibold text-foreground">Salary by Department</h2>
                <p className="text-sm text-muted-foreground">Average vs Maximum salary comparison.</p>
                {departmentStats.length > 0 ? (
                  <DepartmentSalaryChart data={departmentStats} />
                ) : (
                  <div className="h-80 flex items-center justify-center text-muted-foreground">No data available</div>
                )}
              </div>
            </div>

            {/* Deep Dive Row */}
            <CountryFilterDashboard countries={uniqueCountries} />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

