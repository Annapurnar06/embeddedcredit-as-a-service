"use client";

import { useMemo } from "react";
import type { EMIEntry } from "@/lib/mock-data";
import { cn } from "@/lib/utils";
import { Card } from "@/components/ui/card";
import { Calendar } from "lucide-react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

interface LoanScheduleProps {
  schedule: EMIEntry[];
  segment: string;
}

const SEASON_STYLES: Record<string, { bg: string; text: string; label: string }> = {
  flush: {
    bg: "bg-green-50",
    text: "text-green-700",
    label: "Flush",
  },
  lean: {
    bg: "bg-amber-50",
    text: "text-amber-700",
    label: "Lean",
  },
  normal: {
    bg: "",
    text: "text-muted-foreground",
    label: "Normal",
  },
};

const SEASON_CHART_COLORS: Record<string, string> = {
  flush: "#22c55e",
  lean: "#f59e0b",
  normal: "var(--color-primary)",
};

const DAIRY_SEGMENTS = ["dairy_farmer", "cotton_farmer"];

function formatAmount(amount: number): string {
  return `₹${amount.toLocaleString("en-IN")}`;
}

export function LoanSchedule({ schedule, segment }: LoanScheduleProps) {
  const isDairySeasonal = DAIRY_SEGMENTS.includes(segment);

  const totals = useMemo(() => {
    return schedule.reduce(
      (acc, entry) => ({
        principal: acc.principal + entry.principal,
        interest: acc.interest + entry.interest,
        total: acc.total + entry.total,
      }),
      { principal: 0, interest: 0, total: 0 }
    );
  }, [schedule]);

  const chartData = useMemo(() => {
    return schedule.map((entry) => ({
      month: `M${entry.month}`,
      total: entry.total,
      principal: entry.principal,
      interest: entry.interest,
      season: entry.season,
      fill: SEASON_CHART_COLORS[entry.season],
    }));
  }, [schedule]);

  return (
    <div className="space-y-6">
      {/* EMI Chart */}
      <Card padding="md">
        <div className="mb-4 flex items-center justify-between">
          <h3 className="text-sm font-semibold uppercase tracking-wider text-muted-foreground">
            EMI Schedule Chart
          </h3>
          {isDairySeasonal && (
            <div className="flex items-center gap-3 text-xs">
              <div className="flex items-center gap-1.5">
                <span className="inline-block h-3 w-3 rounded-sm bg-green-500" />
                <span className="text-muted-foreground">Flush Season</span>
              </div>
              <div className="flex items-center gap-1.5">
                <span className="inline-block h-3 w-3 rounded-sm bg-amber-500" />
                <span className="text-muted-foreground">Lean Season</span>
              </div>
              <div className="flex items-center gap-1.5">
                <span className="inline-block h-3 w-3 rounded-sm bg-primary" />
                <span className="text-muted-foreground">Normal</span>
              </div>
            </div>
          )}
        </div>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={chartData}
              margin={{ top: 5, right: 10, left: 10, bottom: 0 }}
            >
              <XAxis
                dataKey="month"
                tick={{ fontSize: 11, fill: "var(--color-muted-foreground)" }}
              />
              <YAxis
                tickFormatter={(v: number) =>
                  `₹${(v / 1000).toFixed(0)}k`
                }
                tick={{ fontSize: 11, fill: "var(--color-muted-foreground)" }}
              />
              <Tooltip
                formatter={(value, name) => [
                  formatAmount(Number(value)),
                  String(name).charAt(0).toUpperCase() + String(name).slice(1),
                ]}
                contentStyle={{
                  backgroundColor: "var(--color-surface)",
                  border: "1px solid var(--color-border)",
                  borderRadius: "8px",
                  fontSize: "12px",
                }}
              />
              <Bar dataKey="total" radius={[4, 4, 0, 0]} barSize={24}>
                {chartData.map((entry, index) => (
                  <rect key={index} fill={entry.fill} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </Card>

      {/* EMI Table */}
      <Card padding="none">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-border bg-muted/50">
                <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  Month
                </th>
                <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  Date
                </th>
                <th className="px-4 py-3 text-right text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  Principal
                </th>
                <th className="px-4 py-3 text-right text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  Interest
                </th>
                <th className="px-4 py-3 text-right text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  Total EMI
                </th>
                <th className="px-4 py-3 text-center text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  Season
                </th>
              </tr>
            </thead>
            <tbody>
              {schedule.map((entry) => {
                const seasonCfg = SEASON_STYLES[entry.season];
                return (
                  <tr
                    key={entry.month}
                    className={cn(
                      "border-b border-border transition-colors hover:bg-muted/20",
                      seasonCfg.bg
                    )}
                  >
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-2">
                        <Calendar className="h-3.5 w-3.5 text-muted-foreground" />
                        <span className="font-mono text-xs font-medium text-foreground">
                          #{entry.month}
                        </span>
                      </div>
                    </td>
                    <td className="px-4 py-3 font-mono text-xs text-muted-foreground">
                      {entry.date}
                    </td>
                    <td className="px-4 py-3 text-right font-mono text-xs text-foreground">
                      {formatAmount(entry.principal)}
                    </td>
                    <td className="px-4 py-3 text-right font-mono text-xs text-muted-foreground">
                      {formatAmount(entry.interest)}
                    </td>
                    <td className="px-4 py-3 text-right font-mono text-xs font-medium text-foreground">
                      {formatAmount(entry.total)}
                    </td>
                    <td className="px-4 py-3 text-center">
                      <span
                        className={cn(
                          "inline-flex items-center rounded-full px-2 py-0.5 text-[10px] font-semibold",
                          entry.season === "flush" &&
                            "bg-green-100 text-green-700",
                          entry.season === "lean" &&
                            "bg-amber-100 text-amber-700",
                          entry.season === "normal" &&
                            "bg-slate-100 text-slate-600"
                        )}
                      >
                        {seasonCfg.label}
                        {isDairySeasonal && entry.season !== "normal" && (
                          <span className="ml-1">
                            {entry.season === "flush" ? "↑" : "↓"}
                          </span>
                        )}
                      </span>
                    </td>
                  </tr>
                );
              })}

              {/* Summary row */}
              <tr className="border-t-2 border-border bg-muted/50 font-semibold">
                <td className="px-4 py-3 text-xs uppercase tracking-wider text-muted-foreground" colSpan={2}>
                  Total
                </td>
                <td className="px-4 py-3 text-right font-mono text-xs text-foreground">
                  {formatAmount(totals.principal)}
                </td>
                <td className="px-4 py-3 text-right font-mono text-xs text-muted-foreground">
                  {formatAmount(totals.interest)}
                </td>
                <td className="px-4 py-3 text-right font-mono text-xs font-bold text-foreground">
                  {formatAmount(totals.total)}
                </td>
                <td className="px-4 py-3" />
              </tr>
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
