"use client";

import { useState } from "react";
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import {
  CheckCircle2,
  XCircle,
  AlertTriangle,
  ChevronDown,
  ChevronUp,
  Activity,
  FileCheck,
  MessageSquare,
  ShieldCheck,
} from "lucide-react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const EVAL_TYPES = [
  { name: "Unit", passed: 342, total: 345, icon: FileCheck },
  { name: "Trajectory", passed: 89, total: 90, icon: Activity },
  { name: "Conversation", passed: 156, total: 158, icon: MessageSquare },
  { name: "Policy", passed: 170, total: 170, icon: ShieldCheck },
];

const SEGMENT_BREAKDOWN = [
  { segment: "Dairy Farmer", accuracy: 99.2, compliance: 100, hallucination: 0.1, latency: "1.1s", status: "Pass" },
  { segment: "Kirana Shop", accuracy: 98.8, compliance: 100, hallucination: 0.3, latency: "1.3s", status: "Pass" },
  { segment: "Gig Worker", accuracy: 97.5, compliance: 99.8, hallucination: 0.5, latency: "1.4s", status: "Warning" },
  { segment: "Street Vendor", accuracy: 98.1, compliance: 100, hallucination: 0.2, latency: "1.2s", status: "Pass" },
  { segment: "Gold Loan", accuracy: 99.5, compliance: 100, hallucination: 0.0, latency: "0.9s", status: "Pass" },
  { segment: "Truck Operator", accuracy: 96.8, compliance: 99.5, hallucination: 0.8, latency: "1.6s", status: "Warning" },
  { segment: "SHG Member", accuracy: 99.0, compliance: 100, hallucination: 0.1, latency: "1.1s", status: "Pass" },
  { segment: "Cotton Farmer", accuracy: 98.4, compliance: 100, hallucination: 0.2, latency: "1.2s", status: "Pass" },
];

const EVAL_HISTORY = [
  { run: "834", score: 96.2 },
  { run: "835", score: 97.1 },
  { run: "836", score: 96.8 },
  { run: "837", score: 97.5 },
  { run: "838", score: 97.2 },
  { run: "839", score: 98.0 },
  { run: "840", score: 97.8 },
  { run: "841", score: 98.1 },
  { run: "842", score: 97.9 },
  { run: "843", score: 98.3 },
  { run: "844", score: 98.0 },
  { run: "845", score: 98.5 },
  { run: "846", score: 98.4 },
  { run: "847", score: 98.7 },
];

const FAILED_EVALS = [
  {
    id: "EVAL-847-U-203",
    type: "Unit",
    segment: "Gig Worker",
    description: "Tool chain order validation for multi-platform income aggregation",
    expected: "fetch_platform_data → aggregate_income → normalize_frequency → score",
    actual: "fetch_platform_data → normalize_frequency → aggregate_income → score",
    severity: "Medium",
  },
  {
    id: "EVAL-847-C-089",
    type: "Conversation",
    segment: "Truck Operator",
    description: "Fallback language switch when borrower responds in Hindi mid-conversation",
    expected: "Detect language change → switch prompt template → continue in Hindi",
    actual: "Continued in English for 2 turns before switching",
    severity: "Low",
  },
];

const statusConfig: Record<string, { color: string; icon: typeof CheckCircle2 }> = {
  Pass: { color: "text-success", icon: CheckCircle2 },
  Warning: { color: "text-warning", icon: AlertTriangle },
  Fail: { color: "text-danger", icon: XCircle },
};

export function EvalDashboard() {
  const [expandedFail, setExpandedFail] = useState<string | null>(null);

  return (
    <div className="space-y-6">
      {/* Latest Run Banner */}
      <Card className="border-success/30 bg-success/5">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-success/10">
              <CheckCircle2 className="h-5 w-5 text-success" />
            </div>
            <div>
              <p className="text-sm font-medium text-foreground">Latest Eval Run</p>
              <p className="text-xs text-muted-foreground">Run #847 — Apr 11, 2026</p>
            </div>
          </div>
          <div className="text-right">
            <p className="text-2xl font-bold text-success">98.7%</p>
            <p className="text-xs text-muted-foreground">pass rate</p>
          </div>
        </div>
      </Card>

      {/* Eval Type Cards */}
      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        {EVAL_TYPES.map((evalType) => {
          const pct = ((evalType.passed / evalType.total) * 100).toFixed(1);
          const isPerfect = evalType.passed === evalType.total;
          const Icon = evalType.icon;
          return (
            <Card key={evalType.name} padding="sm">
              <div className="flex items-start justify-between">
                <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/10">
                  <Icon className="h-4 w-4 text-primary" />
                </div>
                <Badge variant={isPerfect ? "success" : "warning"}>
                  {pct}%
                </Badge>
              </div>
              <p className="mt-3 text-sm font-medium text-foreground">{evalType.name}</p>
              <p className="text-xs text-muted-foreground">
                {evalType.passed}/{evalType.total} passed
              </p>
            </Card>
          );
        })}
      </div>

      {/* Segment Breakdown Table */}
      <Card padding="none">
        <div className="px-6 py-4 border-b border-border">
          <h3 className="text-sm font-semibold text-foreground">Segment Breakdown</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-border bg-muted/50">
                <th className="px-6 py-3 text-left font-medium text-muted-foreground">Segment</th>
                <th className="px-4 py-3 text-right font-medium text-muted-foreground">Accuracy</th>
                <th className="px-4 py-3 text-right font-medium text-muted-foreground">Compliance</th>
                <th className="px-4 py-3 text-right font-medium text-muted-foreground">Hallucination Rate</th>
                <th className="px-4 py-3 text-right font-medium text-muted-foreground">Avg Latency</th>
                <th className="px-4 py-3 text-center font-medium text-muted-foreground">Status</th>
              </tr>
            </thead>
            <tbody>
              {SEGMENT_BREAKDOWN.map((row) => {
                const sc = statusConfig[row.status];
                const StatusIcon = sc.icon;
                return (
                  <tr key={row.segment} className="border-b border-border last:border-0 hover:bg-muted/30 transition-colors">
                    <td className="px-6 py-3 font-medium text-foreground">{row.segment}</td>
                    <td className="px-4 py-3 text-right tabular-nums">{row.accuracy}%</td>
                    <td className="px-4 py-3 text-right tabular-nums">{row.compliance}%</td>
                    <td className="px-4 py-3 text-right tabular-nums">{row.hallucination}%</td>
                    <td className="px-4 py-3 text-right tabular-nums">{row.latency}</td>
                    <td className="px-4 py-3">
                      <div className="flex items-center justify-center gap-1.5">
                        <StatusIcon className={cn("h-4 w-4", sc.color)} />
                        <span className={cn("text-xs font-medium", sc.color)}>{row.status}</span>
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </Card>

      {/* Eval History Chart */}
      <Card>
        <h3 className="text-sm font-semibold text-foreground mb-4">Eval Score History</h3>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={EVAL_HISTORY}>
              <XAxis
                dataKey="run"
                tick={{ fontSize: 11, fill: "var(--color-muted-foreground)" }}
                tickLine={false}
                axisLine={{ stroke: "var(--color-border)" }}
                tickFormatter={(v) => `#${v}`}
              />
              <YAxis
                domain={[95, 100]}
                tick={{ fontSize: 11, fill: "var(--color-muted-foreground)" }}
                tickLine={false}
                axisLine={{ stroke: "var(--color-border)" }}
                tickFormatter={(v) => `${v}%`}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: "var(--color-surface)",
                  border: "1px solid var(--color-border)",
                  borderRadius: "8px",
                  fontSize: "12px",
                }}
                formatter={(value) => [`${value}%`, "Score"]}
                labelFormatter={(label) => `Run #${label}`}
              />
              <Line
                type="monotone"
                dataKey="score"
                stroke="var(--color-primary)"
                strokeWidth={2}
                dot={{ r: 3, fill: "var(--color-primary)" }}
                activeDot={{ r: 5, fill: "var(--color-primary)" }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </Card>

      {/* Failed Eval Drill-Down */}
      <Card padding="none">
        <div className="px-6 py-4 border-b border-border">
          <h3 className="text-sm font-semibold text-foreground">Failed Evals ({FAILED_EVALS.length})</h3>
        </div>
        <div className="divide-y divide-border">
          {FAILED_EVALS.map((fail) => (
            <div key={fail.id}>
              <button
                onClick={() => setExpandedFail(expandedFail === fail.id ? null : fail.id)}
                className="flex w-full items-center justify-between px-6 py-3 text-left hover:bg-muted/30 transition-colors"
              >
                <div className="flex items-center gap-3">
                  <XCircle className="h-4 w-4 text-danger shrink-0" />
                  <div>
                    <p className="text-sm font-medium text-foreground">{fail.id}</p>
                    <p className="text-xs text-muted-foreground">{fail.description}</p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <Badge variant={fail.type === "Unit" ? "primary" : "info"}>{fail.type}</Badge>
                  <Badge variant={fail.severity === "Medium" ? "warning" : "default"}>{fail.severity}</Badge>
                  {expandedFail === fail.id ? (
                    <ChevronUp className="h-4 w-4 text-muted-foreground" />
                  ) : (
                    <ChevronDown className="h-4 w-4 text-muted-foreground" />
                  )}
                </div>
              </button>
              {expandedFail === fail.id && (
                <div className="px-6 pb-4 space-y-3">
                  <div className="grid grid-cols-1 gap-3 lg:grid-cols-2">
                    <div className="rounded-lg bg-success/5 border border-success/20 p-3">
                      <p className="text-xs font-semibold text-success mb-1">Expected Tool Chain</p>
                      <p className="text-xs text-foreground font-mono">{fail.expected}</p>
                    </div>
                    <div className="rounded-lg bg-danger/5 border border-danger/20 p-3">
                      <p className="text-xs font-semibold text-danger mb-1">Actual Tool Chain</p>
                      <p className="text-xs text-foreground font-mono">{fail.actual}</p>
                    </div>
                  </div>
                  <p className="text-xs text-muted-foreground">
                    Segment: <span className="font-medium text-foreground">{fail.segment}</span>
                  </p>
                </div>
              )}
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
