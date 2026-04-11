"use client";

import { useState, useMemo } from "react";
import type { ToolCall } from "@/lib/mock-data";
import { cn } from "@/lib/utils";
import { Card } from "@/components/ui/card";
import { Activity, Clock, Zap, CheckCircle2, XCircle, Timer } from "lucide-react";

interface ActivityFeedProps {
  toolCalls: ToolCall[];
}

type CategoryFilter = "All" | "Identity" | "Data" | "Scoring" | "Product" | "Execution";

const CATEGORY_FILTERS: CategoryFilter[] = [
  "All",
  "Identity",
  "Data",
  "Scoring",
  "Product",
  "Execution",
];

const CATEGORY_COLORS: Record<string, string> = {
  Identity: "bg-blue-100 text-blue-700",
  Data: "bg-violet-100 text-violet-700",
  Scoring: "bg-cyan-100 text-cyan-700",
  Product: "bg-green-100 text-green-700",
  Execution: "bg-amber-100 text-amber-700",
  Servicing: "bg-red-100 text-red-700",
  Monitoring: "bg-slate-100 text-slate-700",
};

const STATUS_CONFIG: Record<
  string,
  { color: string; icon: typeof CheckCircle2; label: string }
> = {
  SUCCESS: { color: "text-success", icon: CheckCircle2, label: "SUCCESS" },
  FAILED: { color: "text-danger", icon: XCircle, label: "FAILED" },
  PENDING: { color: "text-warning", icon: Timer, label: "PENDING" },
};

function formatTime(timestamp: string): string {
  const date = new Date(timestamp);
  return date.toLocaleTimeString("en-IN", {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  });
}

function truncate(str: string, len: number): string {
  return str.length > len ? str.slice(0, len) + "…" : str;
}

export function ActivityFeed({ toolCalls }: ActivityFeedProps) {
  const [filter, setFilter] = useState<CategoryFilter>("All");

  const sorted = useMemo(() => {
    const calls = [...toolCalls].sort(
      (a, b) =>
        new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
    );
    if (filter === "All") return calls;
    return calls.filter((tc) => tc.category === filter);
  }, [toolCalls, filter]);

  const stats = useMemo(() => {
    const total = toolCalls.length;
    const avgLatency =
      total > 0
        ? Math.round(
            toolCalls.reduce((sum, tc) => sum + tc.latencyMs, 0) / total
          )
        : 0;
    const successRate =
      total > 0
        ? Math.round(
            (toolCalls.filter((tc) => tc.status === "SUCCESS").length / total) *
              100
          )
        : 0;
    return { total, avgLatency, successRate };
  }, [toolCalls]);

  return (
    <div className="space-y-4">
      {/* Filter Pills */}
      <Card padding="sm">
        <div className="flex flex-wrap items-center gap-2">
          <Activity className="h-4 w-4 text-muted-foreground" />
          {CATEGORY_FILTERS.map((cat) => (
            <button
              key={cat}
              onClick={() => setFilter(cat)}
              className={cn(
                "rounded-full px-3 py-1 text-xs font-medium transition-all",
                filter === cat
                  ? "bg-primary text-primary-foreground shadow-sm"
                  : "bg-muted text-muted-foreground hover:bg-muted/80 hover:text-foreground"
              )}
            >
              {cat}
            </button>
          ))}
        </div>
      </Card>

      {/* Feed */}
      <Card padding="none">
        <div className="divide-y divide-border">
          {sorted.map((tc) => {
            const statusCfg = STATUS_CONFIG[tc.status] ?? STATUS_CONFIG.PENDING;
            const StatusIcon = statusCfg.icon;

            return (
              <div
                key={tc.id}
                className="flex items-center gap-4 px-4 py-3 transition-colors hover:bg-muted/30"
              >
                {/* Timestamp */}
                <span className="shrink-0 font-mono text-xs text-muted-foreground">
                  {formatTime(tc.timestamp)}
                </span>

                {/* Tool Name */}
                <span className="shrink-0 w-36 font-mono text-xs font-medium text-foreground">
                  {tc.tool}
                </span>

                {/* Category Badge */}
                <span
                  className={cn(
                    "inline-flex shrink-0 items-center rounded-full px-2 py-0.5 text-[10px] font-semibold",
                    CATEGORY_COLORS[tc.category] ?? "bg-slate-100 text-slate-700"
                  )}
                >
                  {tc.category}
                </span>

                {/* Status */}
                <div className="flex shrink-0 items-center gap-1">
                  <StatusIcon className={cn("h-3.5 w-3.5", statusCfg.color)} />
                  <span
                    className={cn(
                      "text-[10px] font-semibold",
                      statusCfg.color
                    )}
                  >
                    {statusCfg.label}
                  </span>
                </div>

                {/* Latency */}
                <div className="flex shrink-0 items-center gap-1">
                  <Zap className="h-3 w-3 text-muted-foreground" />
                  <span className="font-mono text-xs text-muted-foreground">
                    {tc.latencyMs}ms
                  </span>
                </div>

                {/* I/O Preview */}
                <div className="min-w-0 flex-1 truncate">
                  <span className="font-mono text-xs text-muted-foreground">
                    {truncate(tc.input, 60)}
                  </span>
                </div>
              </div>
            );
          })}

          {sorted.length === 0 && (
            <div className="py-12 text-center text-sm text-muted-foreground">
              No tool calls match the selected filter.
            </div>
          )}
        </div>
      </Card>

      {/* Stats Footer */}
      <Card padding="sm">
        <div className="flex items-center justify-between text-sm">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-1.5">
              <Activity className="h-4 w-4 text-primary" />
              <span className="font-medium text-foreground">
                {stats.total}
              </span>
              <span className="text-muted-foreground">tools executed</span>
            </div>
            <div className="flex items-center gap-1.5">
              <Clock className="h-4 w-4 text-info" />
              <span className="text-muted-foreground">avg latency</span>
              <span className="font-mono font-medium text-foreground">
                {stats.avgLatency}ms
              </span>
            </div>
          </div>
          <div className="flex items-center gap-1.5">
            <CheckCircle2 className="h-4 w-4 text-success" />
            <span className="font-medium text-foreground">
              {stats.successRate}%
            </span>
            <span className="text-muted-foreground">success</span>
          </div>
        </div>
      </Card>
    </div>
  );
}
