"use client"

import * as React from "react"
import { Moon, Sun } from "lucide-react"
import { useTheme } from "next-themes"

export function ThemeToggle({ isCollapsed }: { isCollapsed?: boolean }) {
  const [mounted, setMounted] = React.useState(false)
  const { theme, setTheme, resolvedTheme } = useTheme()

  React.useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setMounted(true)
  }, [])

  if (!mounted) {
    return (
      <button className="flex items-center justify-center gap-x-3 rounded-lg px-3 py-2 text-sm font-medium text-muted-foreground w-full h-10">
        <div className="h-5 w-5 rounded-full bg-muted animate-pulse" />
      </button>
    )
  }

  const currentTheme = theme === 'system' ? resolvedTheme : theme;

  return (
    <button
      onClick={() => setTheme(currentTheme === "dark" ? "light" : "dark")}
      className={`flex items-center rounded-lg px-3 py-2 text-sm font-medium text-muted-foreground hover:bg-secondary hover:text-foreground cursor-pointer transition-colors duration-200 w-full ${isCollapsed ? 'justify-center' : 'gap-x-3'}`}
      title="Toggle Theme"
    >
      <div className="relative h-5 w-5 shrink-0 flex items-center justify-center">
        <Sun className="absolute h-5 w-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
        <Moon className="absolute h-5 w-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
      </div>
      {!isCollapsed && <span>Toggle Theme</span>}
    </button>
  )
}
