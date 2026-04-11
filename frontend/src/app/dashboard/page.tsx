"use client";

import { useState, useMemo } from "react";
import Link from "next/link";
import { MOCK_LOANS } from "@/lib/mock-data";
import type { LoanApplication, LoanStatus } from "@/lib/mock-data";
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import {
  IndianRupee,
  Clock,
  TrendingUp,
  Landmark,
  ChevronDown,
} from "lucide-react";

const KANBAN_COLUMNS: LoanStatus[] = [
  "UNVERIFIED",
  "VERIFIED",
  "CONFIRMED",
  "DISBURSED",
  "ACTIVE",
];

const STATUS_COLORS: Record<LoanStatus, string> = {
  UNVERIFIED: "bg-muted text-muted-foreground",
  VERIFIED: "bg-info-light text-info",
  CONFIRMED: "bg-warning-light text-warning",
  DISBURSED: "bg-primary-light text-primary",
  ACTIVE: "bg-success-light text-success",
};

function segmentBadgeVariant(
  segment: string
): "default" | "primary" | "success" | "warning" | "danger" | "info" | "outline" {
  const map: Record<string, "primary" | "success" | "warning" | "danger" | "info"> = {
    "Dairy Farmer": "success",
    "Kirana Shop": "primary",
    "Gig Worker": "info",
    "Gold Loan": "warning",
    "Street Vendor": "danger",
    "Cab Driver": "info",
    "Truck Operator": "warning",
    "SHG Member": "success",
    "Cotton Farmer": "success",
    "Medical Shop": "primary",
  };
  return map[segment] ?? "default";
}

function formatAmount(amount: number): string {
  return `₹${amount.toLocaleString("en-IN")}`;
}

function relativeTime(dateStr: string): string {
  const diff = Date.now() - new Date(dateStr).getTime();
  const hours = Math.floor(diff / 3600000);
  if (hours < 1) return "Just now";
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  return `${days}d ago`;
}

function scoreColor(score: number): string {
  if (score > 700) return "text-success";
  if (score > 650) return "text-warning";
  return "text-danger";
}

export default function PipelinePage() {
  const [segmentFilter, setSegmentFilter] = useState("all");
  const [statusFilter, setStatusFilter] = useState("all");

  const segments = useMemo(
    () => Array.from(new Set(MOCK_LOANS.map((l) => l.segment))).sort(),
    []
  );

  const filtered = useMemo(() => {
    return MOCK_LOANS.filter((loan) => {
      if (segmentFilter !== "all" && loan.segment !== segmentFilter) return false;
      if (statusFilter !== "all" && loan.status !== statusFilter) return false;
      return true;
    });
  }, [segmentFilter, statusFilter]);

  // Summary stats
  const totalPipeline = filtered.reduce((sum, l) => sum + l.amount, 0);
  const avgProcessing =
    filtered.length > 0
      ? Math.round(
          filtered.reduce((sum, l) => sum + l.processingTime, 0) / filtered.length
        )
      : 0;
  const approvalRate =
    filtered.length > 0
      ? Math.round(
          (filtered.filter((l) => l.score > 650).length / filtered.length) * 100
        )
      : 0;
  const activeLoans = filtered.filter((l) => l.status === "ACTIVE").length;

  const columnLoans = useMemo(() => {
    const grouped: Record<LoanStatus, LoanApplication[]> = {
      UNVERIFIED: [],
      VERIFIED: [],
      CONFIRMED: [],
      DISBURSED: [],
      ACTIVE: [],
    };
    filtered.forEach((loan) => grouped[loan.status].push(loan));
    return grouped;
  }, [filtered]);

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div>
        <h1 className="text-2xl font-bold text-foreground">Pipeline</h1>
        <p className="text-sm text-muted-foreground mt-1">
          Track loan applications across all stages
        </p>
      </div>

      {/* Summary stats */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Card padding="md" className="flex items-center gap-4">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary-light">
            <IndianRupee className="h-5 w-5 text-primary" />
          </div>
          <div>
            <p className="text-sm text-muted-foreground">Total Pipeline</p>
            <p className="text-xl font-bold text-foreground">
              {formatAmount(totalPipeline)}
            </p>
          </div>
        </Card>

        <Card padding="md" className="flex items-center gap-4">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-info-light">
            <Clock className="h-5 w-5 text-info" />
          </div>
          <div>
            <p className="text-sm text-muted-foreground">Avg Processing</p>
            <p className="text-xl font-bold text-foreground">
              {avgProcessing} min
            </p>
          </div>
        </Card>

        <Card padding="md" className="flex items-center gap-4">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-success-light">
            <TrendingUp className="h-5 w-5 text-success" />
          </div>
          <div>
            <p className="text-sm text-muted-foreground">Approval Rate</p>
            <p className="text-xl font-bold text-foreground">
              {approvalRate}%
            </p>
          </div>
        </Card>

        <Card padding="md" className="flex items-center gap-4">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-warning-light">
            <Landmark className="h-5 w-5 text-warning" />
          </div>
          <div>
            <p className="text-sm text-muted-foreground">Active Loans</p>
            <p className="text-xl font-bold text-foreground">{activeLoans}</p>
          </div>
        </Card>
      </div>

      {/* Filters */}
      <Card padding="sm" className="flex flex-wrap items-center gap-3">
        <div className="relative">
          <select
            value={segmentFilter}
            onChange={(e) => setSegmentFilter(e.target.value)}
            className="h-9 appearance-none rounded-lg border border-border bg-surface pl-3 pr-8 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
          >
            <option value="all">All Segments</option>
            {segments.map((s) => (
              <option key={s} value={s}>
                {s}
              </option>
            ))}
          </select>
          <ChevronDown className="pointer-events-none absolute right-2 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
        </div>

        <div className="relative">
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="h-9 appearance-none rounded-lg border border-border bg-surface pl-3 pr-8 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
          >
            <option value="all">All Statuses</option>
            {KANBAN_COLUMNS.map((s) => (
              <option key={s} value={s}>
                {s}
              </option>
            ))}
          </select>
          <ChevronDown className="pointer-events-none absolute right-2 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
        </div>

        <div className="relative">
          <input
            type="text"
            placeholder="Date range"
            readOnly
            className="h-9 w-36 rounded-lg border border-border bg-surface px-3 text-sm text-muted-foreground cursor-not-allowed"
          />
        </div>

        <div className="relative">
          <input
            type="text"
            placeholder="Amount range"
            readOnly
            className="h-9 w-36 rounded-lg border border-border bg-surface px-3 text-sm text-muted-foreground cursor-not-allowed"
          />
        </div>
      </Card>

      {/* Kanban board */}
      <div className="flex gap-4 overflow-x-auto pb-4">
        {KANBAN_COLUMNS.map((status) => {
          const loans = columnLoans[status];
          return (
            <div
              key={status}
              className="flex min-w-[280px] flex-1 flex-col rounded-xl border border-border bg-surface"
            >
              {/* Column header */}
              <div className="flex items-center justify-between border-b border-border px-4 py-3">
                <div className="flex items-center gap-2">
                  <span
                    className={cn(
                      "inline-flex items-center rounded-md px-2 py-0.5 text-xs font-semibold",
                      STATUS_COLORS[status]
                    )}
                  >
                    {status}
                  </span>
                </div>
                <span className="flex h-6 w-6 items-center justify-center rounded-full bg-muted text-xs font-medium text-muted-foreground">
                  {loans.length}
                </span>
              </div>

              {/* Cards */}
              <div className="flex flex-col gap-3 p-3 overflow-y-auto max-h-[calc(100vh-380px)]">
                {loans.map((loan) => (
                  <Link
                    key={loan.id}
                    href={`/dashboard/loans/${loan.id}`}
                    className="block"
                  >
                    <div className="rounded-lg border border-border bg-surface p-3 transition-all hover:shadow-md hover:border-primary/20">
                      <div className="flex items-start justify-between mb-2">
                        <p className="text-sm font-medium text-foreground">
                          {loan.borrowerName}
                        </p>
                        <Badge variant={segmentBadgeVariant(loan.segment)} className="text-[10px]">
                          {loan.segment}
                        </Badge>
                      </div>

                      <p className="text-lg font-semibold text-foreground mb-2">
                        {formatAmount(loan.amount)}
                      </p>

                      <div className="flex items-center justify-between text-xs">
                        <span className={cn("font-medium", scoreColor(loan.score))}>
                          Score: {loan.score}
                        </span>
                        <span className="text-muted-foreground">
                          {loan.processingTime} min
                        </span>
                      </div>

                      <div className="mt-2 flex items-center justify-between text-xs text-muted-foreground">
                        <span>{loan.id}</span>
                        <span>{relativeTime(loan.createdAt)}</span>
                      </div>
                    </div>
                  </Link>
                ))}

                {loans.length === 0 && (
                  <p className="py-8 text-center text-sm text-muted-foreground">
                    No applications
                  </p>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
