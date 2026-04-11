"use client";

import { use, useState } from "react";
import Link from "next/link";
import { MOCK_LOANS } from "@/lib/mock-data";
import type { LoanStatus } from "@/lib/mock-data";
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ArrowLeft } from "lucide-react";
import { LoanOverview } from "@/components/dashboard/loan-overview";
import { ActivityFeed } from "@/components/dashboard/activity-feed";
import { LoanDocuments } from "@/components/dashboard/loan-documents";
import { LoanPolicy } from "@/components/dashboard/loan-policy";
import { LoanSchedule } from "@/components/dashboard/loan-schedule";

type Tab = "overview" | "activity" | "documents" | "policy" | "schedule";

const TABS: { key: Tab; label: string }[] = [
  { key: "overview", label: "Overview" },
  { key: "activity", label: "Activity Feed" },
  { key: "documents", label: "Documents" },
  { key: "policy", label: "Policy" },
  { key: "schedule", label: "Schedule" },
];

const STATUS_BADGE_VARIANT: Record<
  LoanStatus,
  "default" | "info" | "warning" | "primary" | "success"
> = {
  UNVERIFIED: "default",
  VERIFIED: "info",
  CONFIRMED: "warning",
  DISBURSED: "primary",
  ACTIVE: "success",
};

function formatAmount(amount: number): string {
  return `₹${amount.toLocaleString("en-IN")}`;
}

function scoreColor(score: number): string {
  if (score > 700) return "text-success";
  if (score > 650) return "text-warning";
  return "text-danger";
}

export default function LoanDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = use(params);
  const [activeTab, setActiveTab] = useState<Tab>("overview");

  const loan = MOCK_LOANS.find((l) => l.id === id);

  if (!loan) {
    return (
      <div className="flex flex-col items-center justify-center py-24">
        <p className="text-lg font-medium text-muted-foreground">
          Loan not found
        </p>
        <Link href="/dashboard/loans" className="mt-4">
          <Button variant="outline" size="sm">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Loans
          </Button>
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Back button */}
      <Link href="/dashboard/loans">
        <Button variant="ghost" size="sm" className="gap-2">
          <ArrowLeft className="h-4 w-4" />
          Back to Loans
        </Button>
      </Link>

      {/* Header */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div className="space-y-2">
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-bold text-foreground">
              {loan.borrowerName}
            </h1>
            <Badge variant="outline">{loan.segment}</Badge>
            <Badge variant={STATUS_BADGE_VARIANT[loan.status]}>
              {loan.status}
            </Badge>
          </div>
          <p className="font-mono text-sm text-muted-foreground">{loan.id}</p>
        </div>

        <div className="flex items-center gap-6">
          <div className="text-right">
            <p className="text-sm text-muted-foreground">Amount</p>
            <p className="text-xl font-bold text-foreground">
              {formatAmount(loan.amount)}
            </p>
          </div>
          <div className="text-right">
            <p className="text-sm text-muted-foreground">Score</p>
            <p
              className={cn(
                "text-xl font-bold",
                scoreColor(loan.score)
              )}
            >
              {loan.score}
            </p>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 rounded-lg border border-border bg-muted/50 p-1">
        {TABS.map((tab) => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key)}
            className={cn(
              "rounded-md px-4 py-2 text-sm font-medium transition-all",
              activeTab === tab.key
                ? "bg-surface text-foreground shadow-sm"
                : "text-muted-foreground hover:text-foreground"
            )}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab content */}
      <div>
        {activeTab === "overview" && <LoanOverview loan={loan} />}
        {activeTab === "activity" && (
          <ActivityFeed toolCalls={loan.toolCalls} />
        )}
        {activeTab === "documents" && (
          <LoanDocuments documents={loan.documents} />
        )}
        {activeTab === "policy" && (
          <LoanPolicy policyResults={loan.policyResults} />
        )}
        {activeTab === "schedule" && (
          <LoanSchedule schedule={loan.schedule} segment={loan.segmentId} />
        )}
      </div>
    </div>
  );
}
