"use client";

import { useState } from "react";
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import {
  ShieldCheck,
  Power,
  AlertTriangle,
  UserCheck,
  Bot,
  Eye,
  CircleDot,
  Info,
} from "lucide-react";

const AUTONOMY_LEVELS = [
  {
    id: "FULL_HUMAN",
    label: "Full Human",
    icon: UserCheck,
    description: "All loan decisions made by human reviewers. Agent assists with data collection only.",
    automated: ["Data collection", "Document verification", "Score computation"],
    manual: ["Loan decisioning", "Terms setting", "Disbursement approval", "Borrower communication"],
  },
  {
    id: "HUMAN_WRITE",
    label: "Human Write",
    icon: Eye,
    description: "Agent makes recommendations but humans approve all write operations (approvals, rejections, disbursements).",
    automated: ["Data collection", "Score computation", "Risk assessment", "Recommendation generation", "Borrower communication"],
    manual: ["Loan approval/rejection", "Terms modification", "Disbursement trigger"],
  },
  {
    id: "HUMAN_EXCEPTIONS",
    label: "Human Exceptions",
    icon: Bot,
    description: "Agent handles standard cases autonomously. Human review only for edge cases and exceptions.",
    automated: ["Data collection", "Score computation", "Standard approvals", "Standard rejections", "Terms setting", "Borrower communication"],
    manual: ["Edge case review (score 55-65)", "High-value loans (>₹5L)", "Policy override requests"],
  },
  {
    id: "FULL_AUTO",
    label: "Full Auto",
    icon: Bot,
    description: "Agent operates fully autonomously within policy bounds. Human notification only.",
    automated: ["All loan operations", "Decisioning", "Terms setting", "Disbursement", "Borrower communication"],
    manual: ["Policy violations (auto-escalated)", "System alerts"],
  },
];

const FALLBACK_LAYERS = [
  { name: "LLM Fallback Chain", description: "GPT-4o → GPT-4o-mini → Rule Engine", health: "healthy" },
  { name: "Human Review Queue", description: "Average response time: 12 min", health: "healthy" },
  { name: "Emergency Escalation", description: "PagerDuty → Ops Lead → CTO", health: "healthy" },
];

const healthConfig: Record<string, { color: string; label: string }> = {
  healthy: { color: "bg-success", label: "Healthy" },
  degraded: { color: "bg-warning", label: "Degraded" },
  down: { color: "bg-danger", label: "Down" },
};

export function AutonomyControls() {
  const [currentLevel, setCurrentLevel] = useState("HUMAN_WRITE");
  const [agentEnabled, setAgentEnabled] = useState(true);
  const [showKillConfirm, setShowKillConfirm] = useState(false);

  const currentIndex = AUTONOMY_LEVELS.findIndex((l) => l.id === currentLevel);

  return (
    <div className="space-y-6">
      {/* Autonomy Level Selector */}
      <Card>
        <div className="flex items-center gap-2 mb-4">
          <ShieldCheck className="h-4 w-4 text-primary" />
          <h3 className="text-sm font-semibold text-foreground">Autonomy Level</h3>
        </div>

        {/* Visual Slider */}
        <div className="mb-6">
          <div className="relative">
            {/* Track */}
            <div className="h-2 rounded-full bg-muted">
              <div
                className="h-2 rounded-full bg-primary transition-all duration-300"
                style={{ width: `${(currentIndex / (AUTONOMY_LEVELS.length - 1)) * 100}%` }}
              />
            </div>
            {/* Dots */}
            <div className="absolute inset-0 flex items-center justify-between">
              {AUTONOMY_LEVELS.map((level, i) => (
                <button
                  key={level.id}
                  onClick={() => setCurrentLevel(level.id)}
                  className={cn(
                    "h-5 w-5 rounded-full border-2 transition-all duration-200 cursor-pointer",
                    i <= currentIndex
                      ? "border-primary bg-primary"
                      : "border-border bg-surface"
                  )}
                  title={level.label}
                />
              ))}
            </div>
          </div>
          {/* Labels */}
          <div className="flex items-start justify-between mt-3">
            {AUTONOMY_LEVELS.map((level) => (
              <div
                key={level.id}
                className={cn(
                  "text-center max-w-[120px]",
                  level.id === currentLevel ? "text-primary" : "text-muted-foreground"
                )}
              >
                <p className={cn(
                  "text-xs font-medium",
                  level.id === currentLevel && "font-bold"
                )}>
                  {level.label}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Level Detail Cards */}
        <div className="grid grid-cols-1 gap-4 lg:grid-cols-2 xl:grid-cols-4">
          {AUTONOMY_LEVELS.map((level) => {
            const isActive = level.id === currentLevel;
            const Icon = level.icon;
            return (
              <button
                key={level.id}
                onClick={() => setCurrentLevel(level.id)}
                className={cn(
                  "rounded-lg border p-4 text-left transition-all cursor-pointer",
                  isActive
                    ? "border-primary bg-primary/5 ring-1 ring-primary"
                    : "border-border hover:border-primary/30"
                )}
              >
                <div className="flex items-center gap-2 mb-2">
                  <Icon className={cn("h-4 w-4", isActive ? "text-primary" : "text-muted-foreground")} />
                  <span className={cn("text-sm font-medium", isActive ? "text-primary" : "text-foreground")}>
                    {level.label}
                  </span>
                  {isActive && <Badge variant="primary">Current</Badge>}
                </div>
                <p className="text-xs text-muted-foreground mb-3">{level.description}</p>
                <div className="space-y-1.5">
                  <p className="text-xs font-semibold text-success">Automated:</p>
                  <div className="flex flex-wrap gap-1">
                    {level.automated.map((item) => (
                      <span key={item} className="text-[10px] bg-success/10 text-success px-1.5 py-0.5 rounded">
                        {item}
                      </span>
                    ))}
                  </div>
                  <p className="text-xs font-semibold text-warning mt-2">Manual:</p>
                  <div className="flex flex-wrap gap-1">
                    {level.manual.map((item) => (
                      <span key={item} className="text-[10px] bg-warning/10 text-warning px-1.5 py-0.5 rounded">
                        {item}
                      </span>
                    ))}
                  </div>
                </div>
              </button>
            );
          })}
        </div>
      </Card>

      {/* Kill Switch */}
      <Card className={cn(
        agentEnabled ? "border-success/30" : "border-danger/30"
      )}>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className={cn(
              "flex h-10 w-10 items-center justify-center rounded-full",
              agentEnabled ? "bg-success/10" : "bg-danger/10"
            )}>
              <Power className={cn("h-5 w-5", agentEnabled ? "text-success" : "text-danger")} />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <p className="text-sm font-semibold text-foreground">
                  Agent Status
                </p>
                <Badge variant={agentEnabled ? "success" : "danger"}>
                  {agentEnabled ? "Active" : "Disabled"}
                </Badge>
              </div>
              <p className="text-xs text-muted-foreground mt-0.5">
                {agentEnabled
                  ? "Agent is processing loan applications normally."
                  : "Agent is disabled. All new conversations are routed to human queue."}
              </p>
            </div>
          </div>
          <div>
            {agentEnabled ? (
              showKillConfirm ? (
                <div className="flex items-center gap-2">
                  <span className="text-xs text-danger font-medium">Disable agent?</span>
                  <Button
                    variant="danger"
                    size="sm"
                    onClick={() => {
                      setAgentEnabled(false);
                      setShowKillConfirm(false);
                    }}
                  >
                    Yes, Disable
                  </Button>
                  <Button variant="ghost" size="sm" onClick={() => setShowKillConfirm(false)}>
                    Cancel
                  </Button>
                </div>
              ) : (
                <Button variant="danger" size="sm" onClick={() => setShowKillConfirm(true)}>
                  <Power className="h-3 w-3 mr-1" />
                  Disable Agent
                </Button>
              )
            ) : (
              <Button
                variant="primary"
                size="sm"
                onClick={() => setAgentEnabled(true)}
              >
                <Power className="h-3 w-3 mr-1" />
                Enable Agent
              </Button>
            )}
          </div>
        </div>
        {!agentEnabled && (
          <div className="mt-4 rounded-lg bg-danger/5 border border-danger/20 p-3 flex items-start gap-2">
            <AlertTriangle className="h-4 w-4 text-danger shrink-0 mt-0.5" />
            <p className="text-xs text-danger">
              Agent is disabled. All incoming loan conversations are being routed to the human review queue. Re-enable when ready.
            </p>
          </div>
        )}
      </Card>

      {/* Fallback Status */}
      <Card>
        <div className="flex items-center gap-2 mb-4">
          <CircleDot className="h-4 w-4 text-primary" />
          <h3 className="text-sm font-semibold text-foreground">Fallback Layers</h3>
        </div>
        <div className="space-y-3">
          {FALLBACK_LAYERS.map((layer) => {
            const hc = healthConfig[layer.health];
            return (
              <div key={layer.name} className="flex items-center justify-between rounded-lg border border-border p-3">
                <div className="flex items-center gap-3">
                  <div className={cn("h-2.5 w-2.5 rounded-full", hc.color)} />
                  <div>
                    <p className="text-sm font-medium text-foreground">{layer.name}</p>
                    <p className="text-xs text-muted-foreground">{layer.description}</p>
                  </div>
                </div>
                <Badge variant="success">{hc.label}</Badge>
              </div>
            );
          })}
        </div>
      </Card>

      {/* Configuration Note */}
      <div className="flex items-start gap-2 rounded-lg bg-info/5 border border-info/20 p-4">
        <Info className="h-4 w-4 text-info shrink-0 mt-0.5" />
        <p className="text-xs text-info">
          Changes take effect immediately. All active conversations will complete under current rules.
        </p>
      </div>
    </div>
  );
}
