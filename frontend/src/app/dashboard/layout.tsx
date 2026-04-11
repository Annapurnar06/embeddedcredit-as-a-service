"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import {
  LayoutDashboard,
  FileText,
  CheckSquare,
  Grid3X3,
  Activity,
  BarChart3,
  Bot,
  Search,
  Bell,
} from "lucide-react";

const navItems = [
  { label: "Pipeline", href: "/dashboard", icon: LayoutDashboard },
  { label: "Loans", href: "/dashboard/loans", icon: FileText },
  { label: "Approvals", href: "/dashboard/approvals", icon: CheckSquare },
  { label: "Segments", href: "/dashboard/segments", icon: Grid3X3 },
  { label: "Monitoring", href: "/dashboard/monitoring", icon: Activity },
  { label: "Analytics", href: "/dashboard/analytics", icon: BarChart3 },
  { label: "Agent", href: "/dashboard/agent", icon: Bot },
];

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();

  return (
    <div className="flex h-screen overflow-hidden">
      {/* Sidebar */}
      <aside className="flex w-64 flex-col bg-sidebar text-sidebar-foreground">
        {/* Logo */}
        <div className="flex h-16 items-center gap-2 px-6 border-b border-white/10">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary">
            <span className="text-sm font-bold text-white">EC</span>
          </div>
          <span className="text-lg font-semibold tracking-tight">
            EmbeddedCredit
          </span>
        </div>

        {/* Navigation */}
        <nav className="flex-1 space-y-1 px-3 py-4">
          {navItems.map((item) => {
            const isActive =
              item.href === "/dashboard"
                ? pathname === "/dashboard"
                : pathname.startsWith(item.href);
            const Icon = item.icon;

            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors",
                  isActive
                    ? "bg-sidebar-active text-white border-l-2 border-primary"
                    : "text-sidebar-foreground/70 hover:bg-sidebar-hover hover:text-sidebar-foreground"
                )}
              >
                <Icon className="h-5 w-5 shrink-0" />
                {item.label}
              </Link>
            );
          })}
        </nav>

        {/* Lender info */}
        <div className="border-t border-white/10 px-6 py-4">
          <div className="flex items-center gap-3">
            <div className="flex h-8 w-8 items-center justify-center rounded-full bg-sidebar-active text-xs font-medium">
              DN
            </div>
            <div>
              <p className="text-sm font-medium">Demo NBFC</p>
              <p className="text-xs text-sidebar-foreground/50">Lender</p>
            </div>
          </div>
        </div>
      </aside>

      {/* Main area */}
      <div className="flex flex-1 flex-col overflow-hidden">
        {/* Topbar */}
        <header className="flex h-16 items-center justify-between border-b border-border bg-surface px-6">
          <div className="relative w-80">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <input
              type="text"
              placeholder="Search loans, borrowers, segments..."
              className="h-9 w-full rounded-lg border border-border bg-muted pl-9 pr-4 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring"
            />
          </div>

          <div className="flex items-center gap-4">
            {/* Notification bell */}
            <button className="relative rounded-lg p-2 text-muted-foreground hover:bg-muted hover:text-foreground transition-colors">
              <Bell className="h-5 w-5" />
              <span className="absolute -top-0.5 -right-0.5 flex h-5 w-5 items-center justify-center rounded-full bg-danger text-[10px] font-bold text-white">
                3
              </span>
            </button>

            {/* User avatar */}
            <div className="flex h-9 w-9 items-center justify-center rounded-full bg-primary text-sm font-semibold text-primary-foreground">
              RK
            </div>
          </div>
        </header>

        {/* Page content */}
        <main className="flex-1 overflow-auto bg-surface-raised p-6">
          {children}
        </main>
      </div>
    </div>
  );
}
