import type { ApprovalRequest } from "@/lib/mock-data";
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";

interface AuditTrailProps {
  approvals: ApprovalRequest[];
}

interface AuditEvent {
  id: string;
  approvalId: string;
  borrowerName: string;
  action: "Submitted" | "Approved" | "Rejected";
  by: string;
  at: string;
  reason?: string;
}

const ACTION_COLORS: Record<string, string> = {
  Submitted: "bg-info",
  Approved: "bg-success",
  Rejected: "bg-danger",
};

const ACTION_BADGE_VARIANT: Record<string, "info" | "success" | "danger"> = {
  Submitted: "info",
  Approved: "success",
  Rejected: "danger",
};

function formatDateTime(dateStr: string): string {
  return new Date(dateStr).toLocaleDateString("en-IN", {
    day: "2-digit",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function buildAuditEvents(approvals: ApprovalRequest[]): AuditEvent[] {
  const events: AuditEvent[] = [];

  approvals.forEach((approval) => {
    // Every approval was submitted
    events.push({
      id: `${approval.id}-submitted`,
      approvalId: approval.id,
      borrowerName: approval.borrowerName,
      action: "Submitted",
      by: approval.requestedBy,
      at: approval.requestedAt,
    });

    // If approved or rejected, add the decision event
    if (approval.status === "APPROVED" && approval.approvedAt) {
      events.push({
        id: `${approval.id}-approved`,
        approvalId: approval.id,
        borrowerName: approval.borrowerName,
        action: "Approved",
        by: approval.approvedBy ?? "Unknown",
        at: approval.approvedAt,
        reason: approval.reason,
      });
    } else if (approval.status === "REJECTED" && approval.approvedAt) {
      events.push({
        id: `${approval.id}-rejected`,
        approvalId: approval.id,
        borrowerName: approval.borrowerName,
        action: "Rejected",
        by: approval.approvedBy ?? "Unknown",
        at: approval.approvedAt,
        reason: approval.reason,
      });
    }
  });

  // Sort chronologically (newest first)
  events.sort((a, b) => new Date(b.at).getTime() - new Date(a.at).getTime());

  return events;
}

export function AuditTrail({ approvals }: AuditTrailProps) {
  const events = buildAuditEvents(approvals);

  if (events.length === 0) return null;

  return (
    <div className="rounded-xl border border-border bg-surface p-6">
      <h2 className="text-lg font-semibold text-foreground mb-1">
        Audit Trail
      </h2>
      <p className="text-sm text-muted-foreground mb-6">
        Chronological record of all approval actions
      </p>

      <div className="relative">
        {/* Vertical line */}
        <div className="absolute left-[11px] top-2 bottom-2 w-0.5 bg-border" />

        <div className="space-y-6">
          {events.map((event) => (
            <div key={event.id} className="relative flex gap-4">
              {/* Dot */}
              <div
                className={cn(
                  "relative z-10 mt-1 h-6 w-6 shrink-0 rounded-full border-2 border-white flex items-center justify-center",
                  ACTION_COLORS[event.action]
                )}
              >
                <div className="h-2 w-2 rounded-full bg-white" />
              </div>

              {/* Content */}
              <div className="flex-1 pb-1">
                <div className="flex flex-wrap items-center gap-2">
                  <Badge variant={ACTION_BADGE_VARIANT[event.action]}>
                    {event.action}
                  </Badge>
                  <span className="text-sm font-medium text-foreground">
                    {event.approvalId}
                  </span>
                  <span className="text-sm text-muted-foreground">
                    — {event.borrowerName}
                  </span>
                </div>
                <div className="mt-1 flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-muted-foreground">
                  <span>{formatDateTime(event.at)}</span>
                  <span>by {event.by}</span>
                </div>
                {event.reason && (
                  <p className="mt-1 text-xs text-muted-foreground">
                    Reason: {event.reason}
                  </p>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
