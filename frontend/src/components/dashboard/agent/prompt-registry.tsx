"use client";

import { useState, useMemo } from "react";
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import {
  Search,
  FileText,
  GitCompare,
  ArrowUpCircle,
} from "lucide-react";

const PROMPTS = [
  { segment: "dairy_farmer", name: "Dairy Farmer", version: "v1.3", updated: "2026-04-10", score: 99.2, status: "Active" },
  { segment: "kirana_shop", name: "Kirana Shop", version: "v1.2", updated: "2026-04-09", score: 98.8, status: "Active" },
  { segment: "gig_worker", name: "Gig Worker", version: "v2.1", updated: "2026-04-11", score: 97.5, status: "Staging" },
  { segment: "street_vendor", name: "Street Vendor", version: "v1.1", updated: "2026-04-06", score: 98.1, status: "Active" },
  { segment: "gold_loan", name: "Gold Loan", version: "v1.4", updated: "2026-04-08", score: 99.5, status: "Active" },
  { segment: "truck_operator", name: "Truck Operator", version: "v2.0", updated: "2026-04-11", score: 96.8, status: "Staging" },
  { segment: "shg_member", name: "SHG Member", version: "v1.2", updated: "2026-04-05", score: 99.0, status: "Active" },
  { segment: "cotton_farmer", name: "Cotton Farmer", version: "v1.3", updated: "2026-04-07", score: 98.4, status: "Active" },
  { segment: "cab_driver", name: "Cab Driver", version: "v1.1", updated: "2026-04-04", score: 97.9, status: "Active" },
  { segment: "medical_shop", name: "Medical Shop", version: "v1.0", updated: "2026-04-02", score: 98.6, status: "Active" },
  { segment: "ev_driver", name: "EV Driver", version: "v0.9", updated: "2026-03-28", score: 95.2, status: "Deprecated" },
  { segment: "solar_installer", name: "Solar Installer", version: "v1.1", updated: "2026-04-03", score: 97.8, status: "Active" },
];

const statusVariant: Record<string, "success" | "warning" | "default"> = {
  Active: "success",
  Staging: "warning",
  Deprecated: "default",
};

const DIFF_OLD = `You are a lending agent for dairy farmers.
Evaluate loan eligibility based on:
- Pouring regularity (last 6 months)
- Cooperative membership tenure
- Bank account stability
- Bureau score (if available)

Respond in the borrower's preferred language.
Maximum loan amount: ₹2,00,000.`;

const DIFF_NEW = `You are a lending agent for dairy farmers.
Evaluate loan eligibility based on:
- Pouring regularity (last 6 months)
- Cooperative membership tenure
- Bank account stability
- Bureau score (if available)
- Seasonal income variance (new)

Respond in the borrower's preferred language.
Use simplified terms for first-time borrowers.
Maximum loan amount: ₹3,00,000.`;

export function PromptRegistry() {
  const [search, setSearch] = useState("");
  const [showDiff, setShowDiff] = useState(false);

  const filtered = useMemo(() => {
    if (!search) return PROMPTS;
    const q = search.toLowerCase();
    return PROMPTS.filter(
      (p) =>
        p.name.toLowerCase().includes(q) ||
        p.segment.toLowerCase().includes(q) ||
        p.status.toLowerCase().includes(q)
    );
  }, [search]);

  const oldLines = DIFF_OLD.split("\n");
  const newLines = DIFF_NEW.split("\n");

  return (
    <div className="space-y-6">
      {/* Search */}
      <div className="relative w-full max-w-sm">
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
        <input
          type="text"
          placeholder="Search prompts by segment, status..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="h-9 w-full rounded-lg border border-border bg-muted pl-9 pr-4 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring"
        />
      </div>

      {/* Prompt Table */}
      <Card padding="none">
        <div className="px-6 py-4 border-b border-border flex items-center gap-2">
          <FileText className="h-4 w-4 text-primary" />
          <h3 className="text-sm font-semibold text-foreground">Segment Prompts</h3>
          <span className="text-xs text-muted-foreground ml-auto">{filtered.length} prompts</span>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-border bg-muted/50">
                <th className="px-6 py-3 text-left font-medium text-muted-foreground">Segment Name</th>
                <th className="px-4 py-3 text-left font-medium text-muted-foreground">Version</th>
                <th className="px-4 py-3 text-left font-medium text-muted-foreground">Last Updated</th>
                <th className="px-4 py-3 text-right font-medium text-muted-foreground">Eval Score</th>
                <th className="px-4 py-3 text-center font-medium text-muted-foreground">Status</th>
                <th className="px-4 py-3 text-center font-medium text-muted-foreground">Actions</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((prompt) => (
                <tr key={prompt.segment} className="border-b border-border last:border-0 hover:bg-muted/30 transition-colors">
                  <td className="px-6 py-3 font-medium text-foreground">{prompt.name}</td>
                  <td className="px-4 py-3">
                    <code className="text-xs bg-muted px-1.5 py-0.5 rounded font-mono">{prompt.version}</code>
                  </td>
                  <td className="px-4 py-3 text-muted-foreground">{prompt.updated}</td>
                  <td className="px-4 py-3 text-right tabular-nums">
                    <span className={cn(
                      "font-medium",
                      prompt.score >= 98 ? "text-success" : prompt.score >= 97 ? "text-warning" : "text-danger"
                    )}>
                      {prompt.score}%
                    </span>
                  </td>
                  <td className="px-4 py-3 text-center">
                    <Badge variant={statusVariant[prompt.status] ?? "default"}>{prompt.status}</Badge>
                  </td>
                  <td className="px-4 py-3 text-center">
                    <Button
                      variant="outline"
                      size="sm"
                      disabled={prompt.status !== "Staging"}
                      className="text-xs"
                    >
                      <ArrowUpCircle className="h-3 w-3 mr-1" />
                      Promote
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      {/* Diff Viewer */}
      <Card padding="none">
        <div className="px-6 py-4 border-b border-border flex items-center justify-between">
          <div className="flex items-center gap-2">
            <GitCompare className="h-4 w-4 text-primary" />
            <h3 className="text-sm font-semibold text-foreground">Version Diff — dairy_farmer</h3>
          </div>
          <div className="flex items-center gap-2">
            <Badge variant="default">v1.2</Badge>
            <span className="text-xs text-muted-foreground">→</span>
            <Badge variant="primary">v1.3</Badge>
            <Button variant="ghost" size="sm" onClick={() => setShowDiff(!showDiff)}>
              {showDiff ? "Hide" : "Show"} Diff
            </Button>
          </div>
        </div>
        {showDiff && (
          <div className="grid grid-cols-1 lg:grid-cols-2 divide-y lg:divide-y-0 lg:divide-x divide-border">
            {/* Old Version */}
            <div className="p-4">
              <p className="text-xs font-semibold text-muted-foreground mb-2">v1.2 (Previous)</p>
              <div className="rounded-lg bg-muted/50 p-3 font-mono text-xs leading-relaxed">
                {oldLines.map((line, i) => {
                  const isRemoved = !newLines.includes(line) && line.trim() !== "";
                  return (
                    <div
                      key={i}
                      className={cn(
                        "px-1",
                        isRemoved && "bg-danger/10 text-danger"
                      )}
                    >
                      {line || "\u00A0"}
                    </div>
                  );
                })}
              </div>
            </div>
            {/* New Version */}
            <div className="p-4">
              <p className="text-xs font-semibold text-muted-foreground mb-2">v1.3 (Current)</p>
              <div className="rounded-lg bg-muted/50 p-3 font-mono text-xs leading-relaxed">
                {newLines.map((line, i) => {
                  const isAdded = !oldLines.includes(line) && line.trim() !== "";
                  return (
                    <div
                      key={i}
                      className={cn(
                        "px-1",
                        isAdded && "bg-success/10 text-success"
                      )}
                    >
                      {line || "\u00A0"}
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        )}
      </Card>
    </div>
  );
}
