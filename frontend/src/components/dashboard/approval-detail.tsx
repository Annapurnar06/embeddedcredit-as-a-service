"use client";

import { useState } from "react";
import type { ApprovalRequest } from "@/lib/mock-data";
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  X,
  Check,
  XCircle,
  Clock,
  User,
  FileText,
} from "lucide-react";

interface ApprovalDetailProps {
  approval: ApprovalRequest;
  onClose: () => void;
  onApprove: (id: string) => void;
  onReject: (id: string) => void;
}

const REASON_CODES = [
  "Approved - Within Policy",
  "Approved - Exception",
  "Rejected - Score Below Threshold",
  "Rejected - Data Insufficient",
  "Rejected - Policy Violation",
];

const STATUS_BADGE_VARIANT: Record<string, "warning" | "success" | "danger"> = {
  PENDING: "warning",
  APPROVED: "success",
  REJECTED: "danger",
};

function formatAmount(amount: number): string {
  return `₹${amount.toLocaleString("en-IN")}`;
}

function formatDateTime(dateStr: string): string {
  return new Date(dateStr).toLocaleDateString("en-IN", {
    day: "2-digit",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function ApprovalDetail({
  approval,
  onClose,
  onApprove,
  onReject,
}: ApprovalDetailProps) {
  const [reasonCode, setReasonCode] = useState(REASON_CODES[0]);
  const isPending = approval.status === "PENDING";

  return (
    <>
      {/* Backdrop overlay */}
      <div
        className="fixed inset-0 bg-black/30 z-40"
        onClick={onClose}
      />

      {/* Side panel */}
      <div className="fixed top-0 right-0 h-full w-[480px] bg-white shadow-xl z-50 flex flex-col overflow-hidden">
        {/* Panel header */}
        <div className="flex items-start justify-between border-b border-border px-6 py-5">
          <div className="space-y-2">
            <h2 className="text-lg font-semibold text-foreground">
              {approval.borrowerName}
            </h2>
            <div className="flex items-center gap-2">
              <Badge variant="outline" className="text-xs">
                {approval.segment}
              </Badge>
              <Badge variant={STATUS_BADGE_VARIANT[approval.status]}>
                {approval.status}
              </Badge>
            </div>
            <p className="text-sm text-muted-foreground">
              {approval.operation}
            </p>
          </div>
          <button
            onClick={onClose}
            className="rounded-lg p-2 text-muted-foreground hover:bg-muted hover:text-foreground transition-colors"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Panel body - scrollable */}
        <div className="flex-1 overflow-y-auto px-6 py-5 space-y-6">
          {/* Request Details */}
          <section>
            <div className="flex items-center gap-2 mb-3">
              <FileText className="h-4 w-4 text-muted-foreground" />
              <h3 className="text-sm font-semibold text-foreground uppercase tracking-wider">
                Request Details
              </h3>
            </div>
            <div className="rounded-lg border border-border bg-muted/30 p-4 space-y-3">
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Request ID</span>
                <span className="font-mono text-foreground">{approval.id}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Loan ID</span>
                <span className="font-mono text-foreground">{approval.loanId}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Operation</span>
                <span className="font-medium text-foreground">{approval.operation}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Amount</span>
                <span className="font-semibold text-foreground">
                  {formatAmount(approval.amount)}
                </span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Requested By</span>
                <span className="text-foreground">{approval.requestedBy}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Requested At</span>
                <span className="text-foreground">
                  {formatDateTime(approval.requestedAt)}
                </span>
              </div>
            </div>
          </section>

          {/* Borrower Context */}
          <section>
            <div className="flex items-center gap-2 mb-3">
              <User className="h-4 w-4 text-muted-foreground" />
              <h3 className="text-sm font-semibold text-foreground uppercase tracking-wider">
                Borrower Context
              </h3>
            </div>
            <div className="rounded-lg border border-border bg-muted/30 p-4 space-y-3">
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Segment</span>
                <Badge variant="outline" className="text-xs">
                  {approval.segment}
                </Badge>
              </div>
              <div className="text-sm">
                <span className="text-muted-foreground block mb-1">Risk Summary</span>
                <p className="text-foreground leading-relaxed">
                  {approval.riskSummary}
                </p>
              </div>
            </div>
          </section>

          {/* CAM Memo */}
          <section>
            <div className="flex items-center gap-2 mb-3">
              <FileText className="h-4 w-4 text-muted-foreground" />
              <h3 className="text-sm font-semibold text-foreground uppercase tracking-wider">
                CAM Memo
              </h3>
            </div>
            <div className="rounded-lg border border-border bg-muted/30 p-4">
              <p className="text-sm text-foreground leading-relaxed">
                Score 720/900. Low risk profile. 48 months cooperative tenure.
                92% pouring regularity. Recommended for approval within segment
                limits.
              </p>
            </div>
          </section>

          {/* Decision Section */}
          {isPending ? (
            <section>
              <div className="flex items-center gap-2 mb-3">
                <Clock className="h-4 w-4 text-muted-foreground" />
                <h3 className="text-sm font-semibold text-foreground uppercase tracking-wider">
                  Decision
                </h3>
              </div>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-foreground mb-1.5">
                    Reason Code
                  </label>
                  <select
                    value={reasonCode}
                    onChange={(e) => setReasonCode(e.target.value)}
                    className="h-9 w-full appearance-none rounded-lg border border-border bg-surface px-3 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
                  >
                    {REASON_CODES.map((code) => (
                      <option key={code} value={code}>
                        {code}
                      </option>
                    ))}
                  </select>
                </div>
                <div className="flex items-center gap-3">
                  <Button
                    variant="primary"
                    size="md"
                    className="flex-1 bg-success hover:bg-success/90 text-white"
                    onClick={() => onApprove(approval.id)}
                  >
                    <Check className="mr-2 h-4 w-4" />
                    Approve
                  </Button>
                  <Button
                    variant="danger"
                    size="md"
                    className="flex-1"
                    onClick={() => onReject(approval.id)}
                  >
                    <XCircle className="mr-2 h-4 w-4" />
                    Reject
                  </Button>
                </div>
              </div>
            </section>
          ) : (
            <section>
              <div className="flex items-center gap-2 mb-3">
                {approval.status === "APPROVED" ? (
                  <Check className="h-4 w-4 text-success" />
                ) : (
                  <XCircle className="h-4 w-4 text-danger" />
                )}
                <h3 className="text-sm font-semibold text-foreground uppercase tracking-wider">
                  Outcome
                </h3>
              </div>
              <div
                className={cn(
                  "rounded-lg border p-4 space-y-2",
                  approval.status === "APPROVED"
                    ? "border-success/30 bg-success-light"
                    : "border-danger/30 bg-danger-light"
                )}
              >
                <div className="flex items-center gap-2">
                  <Badge variant={STATUS_BADGE_VARIANT[approval.status]}>
                    {approval.status}
                  </Badge>
                </div>
                {approval.approvedBy && (
                  <p className="text-sm text-foreground">
                    <span className="text-muted-foreground">By:</span>{" "}
                    {approval.approvedBy}
                  </p>
                )}
                {approval.approvedAt && (
                  <p className="text-sm text-foreground">
                    <span className="text-muted-foreground">At:</span>{" "}
                    {formatDateTime(approval.approvedAt)}
                  </p>
                )}
                {approval.reason && (
                  <p className="text-sm text-foreground">
                    <span className="text-muted-foreground">Reason:</span>{" "}
                    {approval.reason}
                  </p>
                )}
              </div>
            </section>
          )}
        </div>
      </div>
    </>
  );
}
