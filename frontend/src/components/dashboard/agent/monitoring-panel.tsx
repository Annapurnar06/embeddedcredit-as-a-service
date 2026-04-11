"use client";

import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import {
  MessageSquare,
  Clock,
  Wrench,
  ShieldAlert,
  CheckCircle2,
  AlertTriangle,
  XCircle,
  Bell,
} from "lucide-react";

const REALTIME_METRICS = [
  { label: "Conversations/hr", value: "42", icon: MessageSquare, trend: "+8%", trendUp: true },
  { label: "Avg Latency", value: "1.2s", icon: Clock, trend: "-12%", trendUp: true },
  { label: "Tool Success Rate", value: "99.1%", icon: Wrench, trend: "+0.2%", trendUp: true },
  { label: "Policy Violations", value: "0", icon: ShieldAlert, trend: "—", trendUp: true },
];

const ALERT_RULES = [
  { name: "High Latency", metric: "p95_latency", threshold: "> 3.0s", current: "1.8s", status: "OK" },
  { name: "Low Eval Score", metric: "eval_pass_rate", threshold: "< 95%", current: "98.7%", status: "OK" },
  { name: "Tool Failure Rate", metric: "tool_error_rate", threshold: "> 2%", current: "0.9%", status: "OK" },
  { name: "Policy Violations", metric: "policy_violation_count", threshold: "> 0/hr", current: "0/hr", status: "OK" },
  { name: "Token Cost Spike", metric: "avg_token_cost", threshold: "> ₹6.00/conv", current: "₹4.15/conv", status: "OK" },
  { name: "Hallucination Rate", metric: "hallucination_rate", threshold: "> 1%", current: "0.8%", status: "WARNING" },
];

const INCIDENTS = [
  {
    date: "2026-04-05",
    title: "Elevated latency — bank API timeout",
    description: "Bank Account AA API experienced 30s timeouts affecting 12 conversations. Fallback to cached data activated.",
    severity: "WARNING",
    resolution: "API provider resolved upstream timeout. Conversations completed via cached bank data.",
    duration: "45 min",
  },
  {
    date: "2026-03-28",
    title: "Canary model eval regression",
    description: "GPT-4o-mini canary (2025-01-15) showed -3.2% eval delta, triggering auto-rollback threshold.",
    severity: "WARNING",
    resolution: "Auto-rollback executed. Traffic reverted to stable GPT-4o-mini (2024-07-18).",
    duration: "12 min",
  },
  {
    date: "2026-03-15",
    title: "Prompt injection attempt spike",
    description: "Coordinated prompt injection attempts detected from single IP range. 23 attacks in 10 minutes.",
    severity: "CRITICAL",
    resolution: "All attacks blocked by INJECT_DETECT rules. IP range added to rate-limit blocklist.",
    duration: "28 min",
  },
  {
    date: "2026-02-20",
    title: "Scoring model drift — cotton farmer",
    description: "Eval accuracy for cotton_farmer segment dropped to 94.1% due to seasonal data pattern shift.",
    severity: "WARNING",
    resolution: "Prompt updated to v1.3 with seasonal variance context. Eval recovered to 98.4%.",
    duration: "2 hr",
  },
];

const statusIcon: Record<string, typeof CheckCircle2> = {
  OK: CheckCircle2,
  WARNING: AlertTriangle,
  CRITICAL: XCircle,
};

const statusColor: Record<string, string> = {
  OK: "text-success",
  WARNING: "text-warning",
  CRITICAL: "text-danger",
};

const severityVariant: Record<string, "success" | "warning" | "danger"> = {
  OK: "success",
  WARNING: "warning",
  CRITICAL: "danger",
};

export function MonitoringPanel() {
  return (
    <div className="space-y-6">
      {/* Real-time Metrics */}
      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        {REALTIME_METRICS.map((metric) => {
          const Icon = metric.icon;
          return (
            <Card key={metric.label} padding="sm">
              <div className="flex items-start justify-between">
                <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/10">
                  <Icon className="h-4 w-4 text-primary" />
                </div>
                {metric.trend !== "—" && (
                  <span className={cn(
                    "text-xs font-medium",
                    metric.trendUp ? "text-success" : "text-danger"
                  )}>
                    {metric.trend}
                  </span>
                )}
              </div>
              <p className="mt-3 text-2xl font-bold text-foreground">{metric.value}</p>
              <p className="text-xs text-muted-foreground">{metric.label}</p>
            </Card>
          );
        })}
      </div>

      {/* Alert Rules */}
      <Card padding="none">
        <div className="px-6 py-4 border-b border-border flex items-center gap-2">
          <Bell className="h-4 w-4 text-primary" />
          <h3 className="text-sm font-semibold text-foreground">Alert Rules</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-border bg-muted/50">
                <th className="px-6 py-3 text-left font-medium text-muted-foreground">Rule Name</th>
                <th className="px-4 py-3 text-left font-medium text-muted-foreground">Metric</th>
                <th className="px-4 py-3 text-left font-medium text-muted-foreground">Threshold</th>
                <th className="px-4 py-3 text-left font-medium text-muted-foreground">Current Value</th>
                <th className="px-4 py-3 text-center font-medium text-muted-foreground">Status</th>
              </tr>
            </thead>
            <tbody>
              {ALERT_RULES.map((rule) => {
                const StatusIcon = statusIcon[rule.status];
                return (
                  <tr key={rule.name} className="border-b border-border last:border-0 hover:bg-muted/30 transition-colors">
                    <td className="px-6 py-3 font-medium text-foreground">{rule.name}</td>
                    <td className="px-4 py-3">
                      <code className="text-xs bg-muted px-1.5 py-0.5 rounded font-mono">{rule.metric}</code>
                    </td>
                    <td className="px-4 py-3 text-muted-foreground tabular-nums">{rule.threshold}</td>
                    <td className="px-4 py-3 tabular-nums font-medium text-foreground">{rule.current}</td>
                    <td className="px-4 py-3">
                      <div className="flex items-center justify-center gap-1.5">
                        <StatusIcon className={cn("h-4 w-4", statusColor[rule.status])} />
                        <span className={cn("text-xs font-medium", statusColor[rule.status])}>{rule.status}</span>
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </Card>

      {/* Incident History */}
      <Card padding="none">
        <div className="px-6 py-4 border-b border-border">
          <h3 className="text-sm font-semibold text-foreground">Incident History</h3>
        </div>
        <div className="divide-y divide-border">
          {INCIDENTS.map((incident, i) => (
            <div key={i} className="px-6 py-4 space-y-2">
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-2">
                  <Badge variant={severityVariant[incident.severity]}>{incident.severity}</Badge>
                  <span className="text-sm font-medium text-foreground">{incident.title}</span>
                </div>
                <div className="flex items-center gap-3 text-xs text-muted-foreground shrink-0">
                  <span>{incident.date}</span>
                  <span>·</span>
                  <span>{incident.duration}</span>
                </div>
              </div>
              <p className="text-xs text-muted-foreground">{incident.description}</p>
              <div className="flex items-start gap-1.5">
                <CheckCircle2 className="h-3.5 w-3.5 text-success shrink-0 mt-0.5" />
                <p className="text-xs text-success">{incident.resolution}</p>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
