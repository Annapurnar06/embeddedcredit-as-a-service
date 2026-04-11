"use client";

import { useState, useMemo, Fragment } from "react";
import { MOCK_LOANS } from "@/lib/mock-data";
import { cn } from "@/lib/utils";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  Activity,
  CheckCircle2,
  AlertTriangle,
  AlertOctagon,
  ChevronDown,
  ChevronRight,
} from "lucide-react";

type SignalHealth = "green" | "yellow" | "red";

function getSignalHealth(score: number): SignalHealth {
  if (score > 700) return "green";
  if (score >= 650) return "yellow";
  return "red";
}

function getIntervention(health: SignalHealth): string {
  if (health === "green") return "None";
  if (health === "yellow") return "Schedule Adjust";
  return "Escalate";
}

function formatAmount(amount: number): string {
  return `₹${amount.toLocaleString("en-IN")}`;
}

function formatDate(dateStr: string): string {
  return new Date(dateStr).toLocaleDateString("en-IN", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
}

const HEALTH_STYLES: Record<
  SignalHealth,
  { bg: string; ring: string; text: string }
> = {
  green: { bg: "bg-success", ring: "ring-success/20", text: "text-success" },
  yellow: { bg: "bg-warning", ring: "ring-warning/20", text: "text-warning" },
  red: { bg: "bg-danger", ring: "ring-danger/20", text: "text-danger" },
};

const INTERVENTION_BADGE_VARIANT: Record<
  string,
  "success" | "warning" | "danger"
> = {
  None: "success",
  "Schedule Adjust": "warning",
  Escalate: "danger",
};

function generateSignalHistory(
  loanId: string,
  score: number
): { date: string; signal: string; value: string; status: SignalHealth }[] {
  const base = score;
  return [
    {
      date: "2026-04-10",
      signal: "Income Signal",
      value: `Score ${base + 5}`,
      status: getSignalHealth(base + 5),
    },
    {
      date: "2026-04-03",
      signal: "Bank Balance Check",
      value: `₹${(12000 + Math.floor(Math.random() * 8000)).toLocaleString("en-IN")}`,
      status: getSignalHealth(base),
    },
    {
      date: "2026-03-27",
      signal: "Repayment Check",
      value: base > 680 ? "On-time" : "3 days late",
      status: base > 680 ? "green" : "yellow",
    },
    {
      date: "2026-03-20",
      signal: "Behavioral Score",
      value: `Score ${base - 10}`,
      status: getSignalHealth(base - 10),
    },
  ];
}

export default function MonitoringPage() {
  const [expandedLoan, setExpandedLoan] = useState<string | null>(null);

  const activeLoans = useMemo(
    () =>
      MOCK_LOANS.filter(
        (loan) => loan.status === "ACTIVE" || loan.status === "DISBURSED"
      ),
    []
  );

  const healthCounts = useMemo(() => {
    const counts = { green: 0, yellow: 0, red: 0 };
    activeLoans.forEach((loan) => {
      counts[getSignalHealth(loan.score)]++;
    });
    return counts;
  }, [activeLoans]);

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div>
        <div className="flex items-center gap-3 mb-1">
          <Activity className="h-7 w-7 text-primary" />
          <h1 className="text-2xl font-bold text-foreground">
            Portfolio Monitoring
          </h1>
        </div>
        <p className="text-sm text-muted-foreground">
          Active loan signal health and intervention tracking
        </p>
      </div>

      {/* Summary stats */}
      <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
        <Card padding="md">
          <p className="text-xs text-muted-foreground uppercase tracking-wider mb-1">
            Active Loans
          </p>
          <p className="text-2xl font-bold text-foreground">
            {activeLoans.length}
          </p>
        </Card>
        <Card padding="md">
          <div className="flex items-center gap-2 mb-1">
            <CheckCircle2 className="h-3.5 w-3.5 text-success" />
            <p className="text-xs text-muted-foreground uppercase tracking-wider">
              Healthy
            </p>
          </div>
          <p className="text-2xl font-bold text-success">
            {healthCounts.green}
          </p>
        </Card>
        <Card padding="md">
          <div className="flex items-center gap-2 mb-1">
            <AlertTriangle className="h-3.5 w-3.5 text-warning" />
            <p className="text-xs text-muted-foreground uppercase tracking-wider">
              Warning
            </p>
          </div>
          <p className="text-2xl font-bold text-warning">
            {healthCounts.yellow}
          </p>
        </Card>
        <Card padding="md">
          <div className="flex items-center gap-2 mb-1">
            <AlertOctagon className="h-3.5 w-3.5 text-danger" />
            <p className="text-xs text-muted-foreground uppercase tracking-wider">
              Critical
            </p>
          </div>
          <p className="text-2xl font-bold text-danger">{healthCounts.red}</p>
        </Card>
      </div>

      {/* Table */}
      <div className="rounded-xl border border-border bg-surface overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-border bg-muted/50">
                <th className="px-4 py-3 text-left text-xs font-semibold text-muted-foreground uppercase tracking-wider w-8" />
                <th className="px-4 py-3 text-left text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                  Loan ID
                </th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                  Borrower
                </th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                  Segment
                </th>
                <th className="px-4 py-3 text-right text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                  Amount
                </th>
                <th className="px-4 py-3 text-center text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                  Score
                </th>
                <th className="px-4 py-3 text-center text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                  Signal Health
                </th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                  Last Signal
                </th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                  Intervention
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {activeLoans.map((loan) => {
                const health = getSignalHealth(loan.score);
                const intervention = getIntervention(health);
                const isExpanded = expandedLoan === loan.id;
                const styles = HEALTH_STYLES[health];

                return (
                  <Fragment key={loan.id}>
                    <tr
                      className={cn(
                        "hover:bg-muted/30 transition-colors cursor-pointer",
                        isExpanded && "bg-muted/20"
                      )}
                      onClick={() =>
                        setExpandedLoan((prev) =>
                          prev === loan.id ? null : loan.id
                        )
                      }
                    >
                      <td className="px-4 py-3">
                        {isExpanded ? (
                          <ChevronDown className="h-4 w-4 text-muted-foreground" />
                        ) : (
                          <ChevronRight className="h-4 w-4 text-muted-foreground" />
                        )}
                      </td>
                      <td className="px-4 py-3 font-mono text-xs text-primary">
                        {loan.id}
                      </td>
                      <td className="px-4 py-3 font-medium text-foreground">
                        {loan.borrowerName}
                      </td>
                      <td className="px-4 py-3">
                        <Badge variant="outline" className="text-xs">
                          {loan.segment}
                        </Badge>
                      </td>
                      <td className="px-4 py-3 text-right font-medium text-foreground">
                        {formatAmount(loan.amount)}
                      </td>
                      <td className="px-4 py-3 text-center">
                        <span
                          className={cn("font-semibold", styles.text)}
                        >
                          {loan.score}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-center">
                        <span className="inline-flex items-center justify-center">
                          <span
                            className={cn(
                              "h-3 w-3 rounded-full ring-4",
                              styles.bg,
                              styles.ring
                            )}
                          />
                        </span>
                      </td>
                      <td className="px-4 py-3 text-xs text-muted-foreground">
                        {formatDate(loan.updatedAt)}
                      </td>
                      <td className="px-4 py-3">
                        <Badge variant={INTERVENTION_BADGE_VARIANT[intervention]}>
                          {intervention}
                        </Badge>
                      </td>
                    </tr>

                    {/* Expanded signal history */}
                    {isExpanded && (
                      <tr>
                        <td colSpan={9} className="px-4 py-4 bg-muted/10">
                          <div className="ml-8">
                            <h4 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-3">
                              Signal History
                            </h4>
                            <div className="grid grid-cols-1 gap-2 sm:grid-cols-2 lg:grid-cols-4">
                              {generateSignalHistory(
                                loan.id,
                                loan.score
                              ).map((signal, i) => {
                                const sh = HEALTH_STYLES[signal.status];
                                return (
                                  <Card
                                    key={i}
                                    padding="sm"
                                    className="bg-surface"
                                  >
                                    <div className="flex items-center gap-2 mb-1.5">
                                      <span
                                        className={cn(
                                          "h-2 w-2 rounded-full",
                                          sh.bg
                                        )}
                                      />
                                      <span className="text-xs font-medium text-foreground">
                                        {signal.signal}
                                      </span>
                                    </div>
                                    <p className="text-sm font-semibold text-foreground">
                                      {signal.value}
                                    </p>
                                    <p className="text-[10px] text-muted-foreground mt-1">
                                      {signal.date}
                                    </p>
                                  </Card>
                                );
                              })}
                            </div>
                          </div>
                        </td>
                      </tr>
                    )}
                  </Fragment>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}


