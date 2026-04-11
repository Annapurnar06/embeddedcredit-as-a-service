"use client";

import { useState, useMemo } from "react";
import Link from "next/link";
import { MOCK_LOANS } from "@/lib/mock-data";
import type { LoanStatus } from "@/lib/mock-data";
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import { ArrowUpDown } from "lucide-react";

type SortField =
  | "id"
  | "borrowerName"
  | "segment"
  | "amount"
  | "score"
  | "status"
  | "product"
  | "createdAt";
type SortDir = "asc" | "desc";

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

function formatDate(dateStr: string): string {
  return new Date(dateStr).toLocaleDateString("en-IN", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
}

function scoreColor(score: number): string {
  if (score > 700) return "text-success";
  if (score > 650) return "text-warning";
  return "text-danger";
}

const COLUMNS: { key: SortField; label: string; className?: string }[] = [
  { key: "id", label: "Loan ID", className: "w-28" },
  { key: "borrowerName", label: "Borrower" },
  { key: "segment", label: "Segment" },
  { key: "amount", label: "Amount", className: "text-right" },
  { key: "score", label: "Score", className: "text-center w-20" },
  { key: "status", label: "Status", className: "w-28" },
  { key: "product", label: "Product" },
  { key: "createdAt", label: "Created", className: "w-28" },
];

export default function LoansPage() {
  const [sortField, setSortField] = useState<SortField>("createdAt");
  const [sortDir, setSortDir] = useState<SortDir>("desc");

  const handleSort = (field: SortField) => {
    if (sortField === field) {
      setSortDir((prev) => (prev === "asc" ? "desc" : "asc"));
    } else {
      setSortField(field);
      setSortDir("asc");
    }
  };

  const sorted = useMemo(() => {
    const loans = [...MOCK_LOANS];
    loans.sort((a, b) => {
      const aVal = a[sortField];
      const bVal = b[sortField];

      if (typeof aVal === "number" && typeof bVal === "number") {
        return sortDir === "asc" ? aVal - bVal : bVal - aVal;
      }

      const aStr = String(aVal);
      const bStr = String(bVal);
      return sortDir === "asc"
        ? aStr.localeCompare(bStr)
        : bStr.localeCompare(aStr);
    });
    return loans;
  }, [sortField, sortDir]);

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div>
        <h1 className="text-2xl font-bold text-foreground">Loans</h1>
        <p className="text-sm text-muted-foreground mt-1">
          All loan applications ({MOCK_LOANS.length} total)
        </p>
      </div>

      {/* Table */}
      <div className="rounded-xl border border-border bg-surface overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-border bg-muted/50">
                {COLUMNS.map((col) => (
                  <th
                    key={col.key}
                    className={cn(
                      "px-4 py-3 text-left text-xs font-semibold text-muted-foreground uppercase tracking-wider cursor-pointer select-none hover:text-foreground transition-colors",
                      col.className
                    )}
                    onClick={() => handleSort(col.key)}
                  >
                    <span className="inline-flex items-center gap-1">
                      {col.label}
                      <ArrowUpDown
                        className={cn(
                          "h-3 w-3",
                          sortField === col.key
                            ? "text-primary"
                            : "text-muted-foreground/40"
                        )}
                      />
                    </span>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {sorted.map((loan) => (
                <tr
                  key={loan.id}
                  className="hover:bg-muted/30 transition-colors"
                >
                  <td className="px-4 py-3">
                    <Link
                      href={`/dashboard/loans/${loan.id}`}
                      className="font-mono text-xs text-primary hover:underline"
                    >
                      {loan.id}
                    </Link>
                  </td>
                  <td className="px-4 py-3">
                    <Link
                      href={`/dashboard/loans/${loan.id}`}
                      className="font-medium text-foreground hover:text-primary"
                    >
                      {loan.borrowerName}
                    </Link>
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
                    <span className={cn("font-semibold", scoreColor(loan.score))}>
                      {loan.score}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    <Badge variant={STATUS_BADGE_VARIANT[loan.status]}>
                      {loan.status}
                    </Badge>
                  </td>
                  <td className="px-4 py-3 text-muted-foreground">
                    {loan.product}
                  </td>
                  <td className="px-4 py-3 text-muted-foreground text-xs">
                    {formatDate(loan.createdAt)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
