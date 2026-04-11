"use client";

import { useMemo } from "react";
import { MOCK_LOANS } from "@/lib/mock-data";
import { Card } from "@/components/ui/card";
import {
  BarChart3,
  TrendingUp,
  PieChart as PieChartIcon,
  DollarSign,
  FileText,
  CheckCircle2,
  Target,
} from "lucide-react";
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import type { PieLabelRenderProps } from "recharts";

function formatAmount(amount: number): string {
  if (amount >= 10_000_000) return `₹${(amount / 10_000_000).toFixed(1)}Cr`;
  if (amount >= 100_000) return `₹${(amount / 100_000).toFixed(1)}L`;
  if (amount >= 1_000) return `₹${(amount / 1_000).toFixed(0)}K`;
  return `₹${amount}`;
}

const CHART_COLORS = {
  primary: "#2563eb",
  violet: "#7c3aed",
  success: "#16a34a",
  warning: "#d97706",
  danger: "#dc2626",
  info: "#0891b2",
  slate: "#475569",
  rose: "#e11d48",
};

const PIE_COLORS = [
  CHART_COLORS.primary,
  CHART_COLORS.violet,
  CHART_COLORS.success,
  CHART_COLORS.warning,
  CHART_COLORS.info,
  CHART_COLORS.danger,
];

export default function AnalyticsPage() {
  // Summary metrics
  const metrics = useMemo(() => {
    const totalOriginations = MOCK_LOANS.length;
    const totalValue = MOCK_LOANS.reduce((sum, l) => sum + l.amount, 0);
    const approvedCount = MOCK_LOANS.filter(
      (l) =>
        l.status === "CONFIRMED" ||
        l.status === "DISBURSED" ||
        l.status === "ACTIVE"
    ).length;
    const approvalRate = Math.round((approvedCount / totalOriginations) * 100);
    const avgScore = Math.round(
      MOCK_LOANS.reduce((sum, l) => sum + l.score, 0) / totalOriginations
    );

    return { totalOriginations, totalValue, approvalRate, avgScore };
  }, []);

  // Chart 1: Segment Distribution (top 8)
  const segmentDistribution = useMemo(() => {
    const counts: Record<string, number> = {};
    MOCK_LOANS.forEach((l) => {
      counts[l.segment] = (counts[l.segment] || 0) + 1;
    });
    return Object.entries(counts)
      .map(([segment, count]) => ({ segment, count }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 8);
  }, []);

  // Chart 2: Origination Trend (mock 12 months)
  const originationTrend = useMemo(() => {
    const months = [
      "May",
      "Jun",
      "Jul",
      "Aug",
      "Sep",
      "Oct",
      "Nov",
      "Dec",
      "Jan",
      "Feb",
      "Mar",
      "Apr",
    ];
    const baseCount = 18;
    return months.map((month, i) => ({
      month,
      originations: baseCount + Math.floor(i * 2.5 + Math.sin(i) * 3),
      value:
        (baseCount + Math.floor(i * 2.5 + Math.sin(i) * 3)) *
        (150000 + i * 10000),
    }));
  }, []);

  // Chart 3: Product Mix (top 6)
  const productMix = useMemo(() => {
    const counts: Record<string, number> = {};
    MOCK_LOANS.forEach((l) => {
      counts[l.product] = (counts[l.product] || 0) + 1;
    });
    return Object.entries(counts)
      .map(([product, count]) => ({ product, count }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 6);
  }, []);

  // Chart 4: Approval/Rejection by Segment
  const approvalBySegment = useMemo(() => {
    const data: Record<
      string,
      { segment: string; approved: number; referred: number; rejected: number }
    > = {};
    MOCK_LOANS.forEach((l) => {
      if (!data[l.segment]) {
        data[l.segment] = {
          segment: l.segment,
          approved: 0,
          referred: 0,
          rejected: 0,
        };
      }
      if (
        l.status === "CONFIRMED" ||
        l.status === "DISBURSED" ||
        l.status === "ACTIVE"
      ) {
        data[l.segment].approved++;
      } else if (l.status === "VERIFIED") {
        data[l.segment].referred++;
      } else {
        data[l.segment].rejected++;
      }
    });
    return Object.values(data)
      .sort(
        (a, b) =>
          b.approved + b.referred + b.rejected -
          (a.approved + a.referred + a.rejected)
      )
      .slice(0, 8);
  }, []);

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div>
        <div className="flex items-center gap-3 mb-1">
          <BarChart3 className="h-7 w-7 text-primary" />
          <h1 className="text-2xl font-bold text-foreground">
            Portfolio Analytics
          </h1>
        </div>
        <p className="text-sm text-muted-foreground">
          Origination volume, approval rates, and portfolio health
        </p>
      </div>

      {/* Summary metric cards */}
      <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
        <Card padding="md">
          <div className="flex items-center gap-2 mb-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/10">
              <FileText className="h-4 w-4 text-primary" />
            </div>
          </div>
          <p className="text-xs text-muted-foreground uppercase tracking-wider mb-1">
            Total Originations
          </p>
          <p className="text-2xl font-bold text-foreground">
            {metrics.totalOriginations}
          </p>
        </Card>
        <Card padding="md">
          <div className="flex items-center gap-2 mb-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-success/10">
              <DollarSign className="h-4 w-4 text-success" />
            </div>
          </div>
          <p className="text-xs text-muted-foreground uppercase tracking-wider mb-1">
            Total Value
          </p>
          <p className="text-2xl font-bold text-foreground">
            {formatAmount(metrics.totalValue)}
          </p>
        </Card>
        <Card padding="md">
          <div className="flex items-center gap-2 mb-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-info/10">
              <CheckCircle2 className="h-4 w-4 text-info" />
            </div>
          </div>
          <p className="text-xs text-muted-foreground uppercase tracking-wider mb-1">
            Approval Rate
          </p>
          <p className="text-2xl font-bold text-foreground">
            {metrics.approvalRate}%
          </p>
        </Card>
        <Card padding="md">
          <div className="flex items-center gap-2 mb-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-violet-500/10">
              <Target className="h-4 w-4 text-violet-500" />
            </div>
          </div>
          <p className="text-xs text-muted-foreground uppercase tracking-wider mb-1">
            Avg Score
          </p>
          <p className="text-2xl font-bold text-foreground">
            {metrics.avgScore}
          </p>
        </Card>
      </div>

      {/* Charts grid */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Chart 1: Segment Distribution */}
        <Card padding="md">
          <div className="flex items-center gap-2 mb-4">
            <BarChart3 className="h-4 w-4 text-muted-foreground" />
            <h3 className="text-sm font-semibold text-foreground uppercase tracking-wider">
              Segment Distribution
            </h3>
          </div>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={segmentDistribution}
                margin={{ top: 4, right: 12, left: 4, bottom: 40 }}
              >
                <XAxis
                  dataKey="segment"
                  tick={{ fontSize: 10 }}
                  angle={-35}
                  textAnchor="end"
                  interval={0}
                />
                <YAxis tick={{ fontSize: 11 }} allowDecimals={false} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "var(--color-surface)",
                    border: "1px solid var(--color-border)",
                    borderRadius: "8px",
                    fontSize: "12px",
                  }}
                />
                <Bar dataKey="count" radius={[4, 4, 0, 0]}>
                  {segmentDistribution.map((_, index) => (
                    <Cell
                      key={`seg-${index}`}
                      fill={PIE_COLORS[index % PIE_COLORS.length]}
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>

        {/* Chart 2: Origination Trend */}
        <Card padding="md">
          <div className="flex items-center gap-2 mb-4">
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
            <h3 className="text-sm font-semibold text-foreground uppercase tracking-wider">
              Origination Trend
            </h3>
          </div>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart
                data={originationTrend}
                margin={{ top: 4, right: 12, left: 4, bottom: 4 }}
              >
                <XAxis dataKey="month" tick={{ fontSize: 11 }} />
                <YAxis tick={{ fontSize: 11 }} allowDecimals={false} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "var(--color-surface)",
                    border: "1px solid var(--color-border)",
                    borderRadius: "8px",
                    fontSize: "12px",
                  }}
                />
                <Legend wrapperStyle={{ fontSize: "12px" }} />
                <Line
                  type="monotone"
                  dataKey="originations"
                  stroke={CHART_COLORS.primary}
                  strokeWidth={2}
                  dot={{ r: 4 }}
                  activeDot={{ r: 6 }}
                  name="Originations"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </Card>

        {/* Chart 3: Product Mix */}
        <Card padding="md">
          <div className="flex items-center gap-2 mb-4">
            <PieChartIcon className="h-4 w-4 text-muted-foreground" />
            <h3 className="text-sm font-semibold text-foreground uppercase tracking-wider">
              Product Mix
            </h3>
          </div>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={productMix}
                  dataKey="count"
                  nameKey="product"
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  innerRadius={50}
                  paddingAngle={2}
                  label={({ percent, ...rest }: PieLabelRenderProps) => {
                    const name = String((rest as Record<string, unknown>).product ?? "");
                    const pct = Number(percent ?? 0);
                    return `${name.length > 15 ? name.slice(0, 15) + "…" : name} ${(pct * 100).toFixed(0)}%`;
                  }}
                  labelLine={{ strokeWidth: 1 }}
                >
                  {productMix.map((_, index) => (
                    <Cell
                      key={`pie-${index}`}
                      fill={PIE_COLORS[index % PIE_COLORS.length]}
                    />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{
                    backgroundColor: "var(--color-surface)",
                    border: "1px solid var(--color-border)",
                    borderRadius: "8px",
                    fontSize: "12px",
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </Card>

        {/* Chart 4: Approval/Rejection by Segment */}
        <Card padding="md">
          <div className="flex items-center gap-2 mb-4">
            <CheckCircle2 className="h-4 w-4 text-muted-foreground" />
            <h3 className="text-sm font-semibold text-foreground uppercase tracking-wider">
              Approval / Rejection by Segment
            </h3>
          </div>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={approvalBySegment}
                margin={{ top: 4, right: 12, left: 4, bottom: 40 }}
              >
                <XAxis
                  dataKey="segment"
                  tick={{ fontSize: 10 }}
                  angle={-35}
                  textAnchor="end"
                  interval={0}
                />
                <YAxis tick={{ fontSize: 11 }} allowDecimals={false} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "var(--color-surface)",
                    border: "1px solid var(--color-border)",
                    borderRadius: "8px",
                    fontSize: "12px",
                  }}
                />
                <Legend wrapperStyle={{ fontSize: "12px" }} />
                <Bar
                  dataKey="approved"
                  stackId="a"
                  fill={CHART_COLORS.success}
                  radius={[0, 0, 0, 0]}
                  name="Approved"
                />
                <Bar
                  dataKey="referred"
                  stackId="a"
                  fill={CHART_COLORS.warning}
                  radius={[0, 0, 0, 0]}
                  name="Referred"
                />
                <Bar
                  dataKey="rejected"
                  stackId="a"
                  fill={CHART_COLORS.danger}
                  radius={[4, 4, 0, 0]}
                  name="Rejected"
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>
    </div>
  );
}
