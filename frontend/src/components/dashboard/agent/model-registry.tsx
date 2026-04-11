"use client";

import { useState } from "react";
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import {
  Cpu,
  RotateCcw,
  ArrowRight,
  Zap,
  Users,
} from "lucide-react";

const MODELS = [
  { segmentGroup: "High-Complexity", model: "GPT-4o", provider: "OpenAI", version: "2024-08-06", cost: "₹4.20", status: "Active" },
  { segmentGroup: "High-Complexity", model: "GPT-4o (canary)", provider: "OpenAI", version: "2024-11-20", cost: "₹4.50", status: "Canary" },
  { segmentGroup: "Standard", model: "GPT-4o-mini", provider: "OpenAI", version: "2024-07-18", cost: "₹0.85", status: "Active" },
  { segmentGroup: "Standard", model: "GPT-4o-mini (canary)", provider: "OpenAI", version: "2025-01-31", cost: "₹0.90", status: "Canary" },
  { segmentGroup: "Low-Complexity", model: "GPT-4o-mini", provider: "OpenAI", version: "2024-07-18", cost: "₹0.85", status: "Active" },
  { segmentGroup: "Gold Loan", model: "GPT-4o", provider: "OpenAI", version: "2024-08-06", cost: "₹4.20", status: "Active" },
  { segmentGroup: "Fallback", model: "GPT-4o-mini", provider: "OpenAI", version: "2024-07-18", cost: "₹0.85", status: "Standby" },
];

const CANARY_MODELS = [
  {
    model: "GPT-4o (2024-11-20)",
    segmentGroup: "High-Complexity",
    traffic: 10,
    evalDelta: "+0.3%",
    deltaPositive: true,
    rollbackThreshold: "-2.0%",
    runsCompleted: 847,
    runsTotal: 1000,
  },
  {
    model: "GPT-4o-mini (2025-01-31)",
    segmentGroup: "Standard",
    traffic: 5,
    evalDelta: "-0.1%",
    deltaPositive: false,
    rollbackThreshold: "-2.0%",
    runsCompleted: 412,
    runsTotal: 1000,
  },
];

const FALLBACK_CHAIN = [
  { name: "GPT-4o", role: "Primary", health: "healthy", description: "Main model for complex segments" },
  { name: "GPT-4o-mini", role: "Fallback 1", health: "healthy", description: "Cost-efficient fallback for standard segments" },
  { name: "Rule-based Engine", role: "Fallback 2", health: "healthy", description: "Deterministic scoring without LLM" },
  { name: "Human Queue", role: "Fallback 3", health: "healthy", description: "Manual review by lending team" },
];

const statusVariant: Record<string, "success" | "warning" | "default" | "info"> = {
  Active: "success",
  Canary: "warning",
  Standby: "default",
};

const healthColor: Record<string, string> = {
  healthy: "bg-success",
  degraded: "bg-warning",
  down: "bg-danger",
};

export function ModelRegistry() {
  const [showRollbackConfirm, setShowRollbackConfirm] = useState<string | null>(null);

  return (
    <div className="space-y-6">
      {/* Model Table */}
      <Card padding="none">
        <div className="px-6 py-4 border-b border-border flex items-center gap-2">
          <Cpu className="h-4 w-4 text-primary" />
          <h3 className="text-sm font-semibold text-foreground">Model Registry</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-border bg-muted/50">
                <th className="px-6 py-3 text-left font-medium text-muted-foreground">Segment Group</th>
                <th className="px-4 py-3 text-left font-medium text-muted-foreground">Model</th>
                <th className="px-4 py-3 text-left font-medium text-muted-foreground">Provider</th>
                <th className="px-4 py-3 text-left font-medium text-muted-foreground">Version</th>
                <th className="px-4 py-3 text-right font-medium text-muted-foreground">Token Cost/Conv</th>
                <th className="px-4 py-3 text-center font-medium text-muted-foreground">Status</th>
              </tr>
            </thead>
            <tbody>
              {MODELS.map((m, i) => (
                <tr key={i} className="border-b border-border last:border-0 hover:bg-muted/30 transition-colors">
                  <td className="px-6 py-3 font-medium text-foreground">{m.segmentGroup}</td>
                  <td className="px-4 py-3 text-foreground">{m.model}</td>
                  <td className="px-4 py-3 text-muted-foreground">{m.provider}</td>
                  <td className="px-4 py-3">
                    <code className="text-xs bg-muted px-1.5 py-0.5 rounded font-mono">{m.version}</code>
                  </td>
                  <td className="px-4 py-3 text-right tabular-nums">{m.cost}</td>
                  <td className="px-4 py-3 text-center">
                    <Badge variant={statusVariant[m.status] ?? "default"}>{m.status}</Badge>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      {/* Canary Deployments */}
      <Card>
        <div className="flex items-center gap-2 mb-4">
          <Zap className="h-4 w-4 text-warning" />
          <h3 className="text-sm font-semibold text-foreground">Canary Deployments</h3>
        </div>
        <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
          {CANARY_MODELS.map((canary) => (
            <div key={canary.model} className="rounded-lg border border-border p-4 space-y-3">
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-sm font-medium text-foreground">{canary.model}</p>
                  <p className="text-xs text-muted-foreground">{canary.segmentGroup}</p>
                </div>
                <Badge variant="warning">{canary.traffic}% traffic</Badge>
              </div>
              <div className="grid grid-cols-3 gap-3 text-center">
                <div>
                  <p className={cn(
                    "text-sm font-bold",
                    canary.deltaPositive ? "text-success" : "text-danger"
                  )}>
                    {canary.evalDelta}
                  </p>
                  <p className="text-xs text-muted-foreground">Eval Delta</p>
                </div>
                <div>
                  <p className="text-sm font-bold text-foreground">{canary.rollbackThreshold}</p>
                  <p className="text-xs text-muted-foreground">Rollback At</p>
                </div>
                <div>
                  <p className="text-sm font-bold text-foreground">{canary.runsCompleted}/{canary.runsTotal}</p>
                  <p className="text-xs text-muted-foreground">Runs</p>
                </div>
              </div>
              {/* Progress bar */}
              <div className="w-full bg-muted rounded-full h-1.5">
                <div
                  className="bg-warning h-1.5 rounded-full transition-all"
                  style={{ width: `${(canary.runsCompleted / canary.runsTotal) * 100}%` }}
                />
              </div>
              <div className="flex items-center justify-between">
                <p className="text-xs text-muted-foreground">
                  {Math.round((canary.runsCompleted / canary.runsTotal) * 100)}% complete
                </p>
                {showRollbackConfirm === canary.model ? (
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-danger">Confirm rollback?</span>
                    <Button variant="danger" size="sm" onClick={() => setShowRollbackConfirm(null)}>
                      Yes, Rollback
                    </Button>
                    <Button variant="ghost" size="sm" onClick={() => setShowRollbackConfirm(null)}>
                      Cancel
                    </Button>
                  </div>
                ) : (
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setShowRollbackConfirm(canary.model)}
                  >
                    <RotateCcw className="h-3 w-3 mr-1" />
                    Rollback
                  </Button>
                )}
              </div>
            </div>
          ))}
        </div>
      </Card>

      {/* Fallback Chain */}
      <Card>
        <div className="flex items-center gap-2 mb-4">
          <Users className="h-4 w-4 text-primary" />
          <h3 className="text-sm font-semibold text-foreground">Fallback Chain</h3>
        </div>
        <div className="flex flex-col gap-2 lg:flex-row lg:items-center">
          {FALLBACK_CHAIN.map((node, i) => (
            <div key={node.name} className="flex items-center gap-2">
              <div className="flex-1 rounded-lg border border-border p-3 min-w-[180px]">
                <div className="flex items-center gap-2 mb-1">
                  <div className={cn("h-2.5 w-2.5 rounded-full", healthColor[node.health])} />
                  <span className="text-sm font-medium text-foreground">{node.name}</span>
                </div>
                <p className="text-xs text-muted-foreground">{node.role}</p>
                <p className="text-xs text-muted-foreground mt-1">{node.description}</p>
              </div>
              {i < FALLBACK_CHAIN.length - 1 && (
                <ArrowRight className="h-4 w-4 text-muted-foreground shrink-0 hidden lg:block" />
              )}
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
