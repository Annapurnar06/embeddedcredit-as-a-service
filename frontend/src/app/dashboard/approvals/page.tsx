"use client";

import { useState, useMemo } from "react";
import { MOCK_APPROVALS } from "@/lib/mock-data";
import type { ApprovalRequest, ApprovalStatus } from "@/lib/mock-data";
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import { ApprovalDetail } from "@/components/dashboard/approval-detail";
import { AuditTrail } from "@/components/dashboard/audit-trail";
import { Clock, CheckCircle, XCircle, ListFilter } from "lucide-react";

type FilterTab = "ALL" | ApprovalStatus;

const STATUS_BADGE_VARIANT: Record<ApprovalStatus, "warning" | "success" | "danger"> = {
  PENDING: "warning",
  APPROVED: "success",
  REJECTED: "danger",
};

function formatAmount(amount: number): string {
  return `₹${amount.toLocaleString("en-IN")}`;
}

function formatDate(dateStr: string): string {
  return new Date(dateStr).toLocaleDateString("en-IN", {
    day: "2-digit",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function truncate(text: string, maxLen: number): string {
  return text.length > maxLen ? text.slice(0, maxLen) + "…" : text;
}

export default function ApprovalsPage() {
  const [approvals, setApprovals] = useState<ApprovalRequest[]>(MOCK_APPROVALS);
  const [activeTab, setActiveTab] = useState<FilterTab>("ALL");
  const [selectedApproval, setSelectedApproval] = useState<ApprovalRequest | null>(null);

  const counts = useMemo(() => {
    const c = { ALL: approvals.length, PENDING: 0, APPROVED: 0, REJECTED: 0 };
    approvals.forEach((a) => c[a.status]++);
    return c;
  }, [approvals]);

  const filtered = useMemo(() => {
    if (activeTab === "ALL") return approvals;
    return approvals.filter((a) => a.status === activeTab);
  }, [approvals, activeTab]);

  const handleApprove = (id: string) => {
    setApprovals((prev) =>
      prev.map((a) =>
        a.id === id
          ? {
              ...a,
              status: "APPROVED" as ApprovalStatus,
              approvedBy: "Rajesh Kumar (Credit Head)",
              approvedAt: new Date().toISOString(),
              reason: "Approved - Within Policy",
            }
          : a
      )
    );
    setSelectedApproval(null);
  };

  const handleReject = (id: string) => {
    setApprovals((prev) =>
      prev.map((a) =>
        a.id === id
          ? {
              ...a,
              status: "REJECTED" as ApprovalStatus,
              approvedBy: "Rajesh Kumar (Credit Head)",
              approvedAt: new Date().toISOString(),
              reason: "Rejected - Score Below Threshold",
            }
          : a
      )
    );
    setSelectedApproval(null);
  };

  const tabs: { key: FilterTab; label: string; icon: React.ElementType }[] = [
    { key: "ALL", label: "All", icon: ListFilter },
    { key: "PENDING", label: "Pending", icon: Clock },
    { key: "APPROVED", label: "Approved", icon: CheckCircle },
    { key: "REJECTED", label: "Rejected", icon: XCircle },
  ];

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div>
        <h1 className="text-2xl font-bold text-foreground">Approval Queue</h1>
        <p className="text-sm text-muted-foreground mt-1">
          Review pending maker-checker requests for WRITE operations
        </p>
      </div>

      {/* Filter tabs */}
      <div className="flex items-center gap-1 rounded-lg border border-border bg-surface p-1">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.key;
          return (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key)}
              className={cn(
                "inline-flex items-center gap-2 rounded-md px-4 py-2 text-sm font-medium transition-colors",
                isActive
                  ? "bg-primary text-primary-foreground shadow-sm"
                  : "text-muted-foreground hover:bg-muted hover:text-foreground"
              )}
            >
              <Icon className="h-4 w-4" />
              {tab.label}
              <span
                className={cn(
                  "ml-1 inline-flex h-5 min-w-[20px] items-center justify-center rounded-full px-1.5 text-xs font-semibold",
                  isActive
                    ? "bg-white/20 text-primary-foreground"
                    : "bg-muted text-muted-foreground"
                )}
              >
                {counts[tab.key]}
              </span>
            </button>
          );
        })}
      </div>

      {/* Table */}
      <div className="rounded-xl border border-border bg-surface overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-border bg-muted/50">
                <th className="px-4 py-3 text-left text-xs font-semibold text-muted-foreground uppercase tracking-wider w-28">
                  Request ID
                </th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                  Borrower
                </th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                  Segment
                </th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                  Operation
                </th>
                <th className="px-4 py-3 text-right text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                  Amount
                </th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                  Risk Summary
                </th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-muted-foreground uppercase tracking-wider w-36">
                  Requested At
                </th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-muted-foreground uppercase tracking-wider w-28">
                  Status
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {filtered.map((approval) => (
                <tr
                  key={approval.id}
                  onClick={() => setSelectedApproval(approval)}
                  className="hover:bg-muted/30 transition-colors cursor-pointer"
                >
                  <td className="px-4 py-3">
                    <span className="font-mono text-xs text-primary">
                      {approval.id}
                    </span>
                  </td>
                  <td className="px-4 py-3 font-medium text-foreground">
                    {approval.borrowerName}
                  </td>
                  <td className="px-4 py-3">
                    <Badge variant="outline" className="text-xs">
                      {approval.segment}
                    </Badge>
                  </td>
                  <td className="px-4 py-3 text-foreground">
                    {approval.operation}
                  </td>
                  <td className="px-4 py-3 text-right font-medium text-foreground">
                    {formatAmount(approval.amount)}
                  </td>
                  <td className="px-4 py-3 text-muted-foreground text-xs max-w-[200px]">
                    {truncate(approval.riskSummary, 50)}
                  </td>
                  <td className="px-4 py-3 text-muted-foreground text-xs">
                    {formatDate(approval.requestedAt)}
                  </td>
                  <td className="px-4 py-3">
                    <Badge variant={STATUS_BADGE_VARIANT[approval.status]}>
                      {approval.status}
                    </Badge>
                  </td>
                </tr>
              ))}
              {filtered.length === 0 && (
                <tr>
                  <td
                    colSpan={8}
                    className="px-4 py-12 text-center text-sm text-muted-foreground"
                  >
                    No approval requests match the current filter.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Audit Trail */}
      <AuditTrail approvals={approvals} />

      {/* Side Panel */}
      {selectedApproval && (
        <ApprovalDetail
          approval={selectedApproval}
          onClose={() => setSelectedApproval(null)}
          onApprove={handleApprove}
          onReject={handleReject}
        />
      )}
    </div>
  );
}
