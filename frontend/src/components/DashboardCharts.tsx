/* eslint-disable @typescript-eslint/no-explicit-any */
'use client';

import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  LineChart, Line
} from 'recharts';

const CustomBarTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="card-glass p-3 rounded-lg border border-border bg-popover text-popover-foreground">
        <p className="text-sm font-medium mb-1">{label}</p>
        {payload.map((entry: any, index: number) => (
          <p key={index} className="text-sm font-semibold" style={{ color: entry.color }}>
            {entry.name}: ${Number(entry.value).toLocaleString()}
          </p>
        ))}
      </div>
    );
  }
  return null;
};

export function CountrySalaryChart({ data }: { data: any[] }) {

  return (
    <div className="h-80 w-full mt-4">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={data}
          margin={{ top: 20, right: 30, left: 20, bottom: 40 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" vertical={false} />
          <XAxis 
            dataKey="country" 
            stroke="var(--color-muted-foreground)" 
            fontSize={12}
            tickLine={false}
            axisLine={false}
            interval={0}
            angle={-45}
            textAnchor="end"
            dy={10}
          />
          <YAxis 
            stroke="var(--color-muted-foreground)" 
            fontSize={12}
            tickLine={false}
            axisLine={false}
            tickFormatter={(value) => `$${value / 1000}k`}
          />
          <Tooltip content={<CustomBarTooltip />} cursor={{ fill: 'var(--color-border)', opacity: 0.4 }} />
          <Bar dataKey="avg_salary" name="Avg Salary" fill="var(--color-primary)" radius={[4, 4, 0, 0]} barSize={30} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

const CustomLineTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="card-glass p-3 rounded-lg border border-border bg-popover text-popover-foreground">
        <p className="text-sm font-medium mb-1">{label}</p>
        {payload.map((entry: any, index: number) => (
          <p key={index} className="text-sm font-semibold" style={{ color: entry.color }}>
            {entry.name}: ${Number(entry.value).toLocaleString()}
          </p>
        ))}
      </div>
    );
  }
  return null;
};

export function DepartmentSalaryChart({ data }: { data: any[] }) {

  return (
    <div className="h-80 w-full mt-4">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart
          data={data}
          margin={{ top: 20, right: 30, left: 20, bottom: 40 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" vertical={false} />
          <XAxis 
            dataKey="department" 
            stroke="var(--color-muted-foreground)" 
            fontSize={12}
            tickLine={false}
            axisLine={false}
            interval={0}
            angle={-45}
            textAnchor="end"
            dy={10}
          />
          <YAxis 
            stroke="var(--color-muted-foreground)" 
            fontSize={12}
            tickLine={false}
            axisLine={false}
            tickFormatter={(value) => `$${value / 1000}k`}
          />
          <Tooltip content={<CustomLineTooltip />} cursor={{ stroke: 'var(--color-border)', strokeWidth: 2 }} />
          <Line 
            type="monotone" 
            dataKey="max_salary" 
            name="Max Salary" 
            stroke="#3b82f6" 
            strokeWidth={3}
            dot={{ r: 4, fill: '#3b82f6', strokeWidth: 0 }}
            activeDot={{ r: 6 }}
          />
          <Line 
            type="monotone" 
            dataKey="avg_salary" 
            name="Avg Salary" 
            stroke="var(--color-primary)" 
            strokeWidth={3}
            dot={{ r: 4, fill: 'var(--color-primary)', strokeWidth: 0 }}
            activeDot={{ r: 6 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
