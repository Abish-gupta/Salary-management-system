"use client"

import { useState, useEffect } from "react"
import { api } from "@/lib/api"
import { Banknote, TrendingUp, TrendingDown, Briefcase } from "lucide-react"

interface JobTitleStat {
  job_title: string;
  avg_salary: number;
}

interface CountryStats {
  country: string;
  total_employees: number;
  min_salary: number;
  max_salary: number;
  avg_salary: number;
  job_titles: JobTitleStat[];
}

export function CountryFilterDashboard({ countries }: { countries: string[] }) {
  const [selectedCountry, setSelectedCountry] = useState<string>("")
  const [stats, setStats] = useState<CountryStats | null>(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (!selectedCountry) {
      // eslint-disable-next-line react-hooks/set-state-in-effect
      setStats(null)
      return
    }
    
    setLoading(true)
    api.getSpecificCountryAnalytics(selectedCountry)
      .then((data) => setStats(data))
      .catch((err) => console.error("Failed to fetch country stats", err))
      .finally(() => setLoading(false))
  }, [selectedCountry])

  return (
    <div className="card-glass rounded-xl p-6 mt-8">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6">
        <div>
          <h2 className="text-lg font-semibold text-foreground">Country Deep Dive</h2>
          <p className="text-sm text-muted-foreground">Detailed salary insights by region and job title.</p>
        </div>
        
        <div className="mt-4 sm:mt-0">
          <select
            value={selectedCountry}
            onChange={(e) => setSelectedCountry(e.target.value)}
            className="w-48 bg-background border border-border text-foreground text-sm rounded-lg focus:ring-primary focus:border-primary block p-2.5 outline-none"
          >
            <option value="">Select a country...</option>
            {countries.map((c) => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
        </div>
      </div>

      {loading && (
        <div className="py-12 flex justify-center text-muted-foreground">
          Loading analytics...
        </div>
      )}

      {!loading && !stats && selectedCountry && (
        <div className="py-12 flex justify-center text-muted-foreground">
          No data available
        </div>
      )}

      {!loading && !selectedCountry && (
        <div className="py-12 flex justify-center text-muted-foreground">
          Select a country to view detailed analytics.
        </div>
      )}

      {!loading && stats && (
        <div className="space-y-6 animate-in fade-in duration-300">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-secondary/50 rounded-lg p-4 border border-border">
              <p className="text-sm font-medium text-muted-foreground flex items-center gap-2">
                <TrendingDown className="w-4 h-4 text-rose-500" />
                Minimum Salary
              </p>
              <p className="text-2xl font-bold mt-2 text-foreground">
                ${Number(stats.min_salary).toLocaleString()}
              </p>
            </div>
            
            <div className="bg-secondary/50 rounded-lg p-4 border border-border">
              <p className="text-sm font-medium text-muted-foreground flex items-center gap-2">
                <Banknote className="w-4 h-4 text-blue-500" />
                Average Salary
              </p>
              <p className="text-2xl font-bold mt-2 text-foreground">
                ${Number(stats.avg_salary).toLocaleString(undefined, { maximumFractionDigits: 0 })}
              </p>
            </div>
            
            <div className="bg-secondary/50 rounded-lg p-4 border border-border">
              <p className="text-sm font-medium text-muted-foreground flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-emerald-500" />
                Maximum Salary
              </p>
              <p className="text-2xl font-bold mt-2 text-foreground">
                ${Number(stats.max_salary).toLocaleString()}
              </p>
            </div>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-foreground mb-3 flex items-center gap-2">
              <Briefcase className="w-4 h-4 text-primary" />
              Average Salary by Job Title
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
              {stats.job_titles.map((job) => (
                <div key={job.job_title} className="flex justify-between items-center p-3 rounded-md bg-secondary/30 border border-border hover:bg-secondary/50 transition-colors">
                  <span className="text-sm font-medium text-foreground">{job.job_title}</span>
                  <span className="text-sm font-semibold text-primary">
                    ${Number(job.avg_salary).toLocaleString(undefined, { maximumFractionDigits: 0 })}
                  </span>
                </div>
              ))}
              {stats.job_titles.length === 0 && (
                <div className="col-span-full text-sm text-muted-foreground">No job title data found.</div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
