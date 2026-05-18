import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Sidebar } from "@/components/Sidebar";
import { ThemeProvider } from "@/components/ThemeProvider";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Salary Management System",
  description: "A premium dashboard for analyzing employee salaries.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.className} flex h-screen overflow-hidden`}>
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem disableTransitionOnChange>
          <Sidebar />
          <main className="flex-1 overflow-y-auto bg-black/5 dark:bg-black/20 p-8">
            <div className="mx-auto max-w-7xl">
              {children}
            </div>
          </main>
        </ThemeProvider>
      </body>
    </html>
  );
}
