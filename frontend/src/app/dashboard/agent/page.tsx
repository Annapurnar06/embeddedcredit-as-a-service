"use client";

import { useState } from "react";
import { cn } from "@/lib/utils";
import {
  FlaskConical,
  ShieldAlert,
  FileText,
  Route,
  Cpu,
  Activity,
  SlidersHorizontal,
} from "lucide-react";
import { EvalDashboard } from "@/components/dashboard/agent/eval-dashboard";
import { RedTeamDashboard } from "@/components/dashboard/agent/redteam-dashboard";
import { PromptRegistry } from "@/components/dashboard/agent/prompt-registry";
import { AgentTraces } from "@/components/dashboard/agent/agent-traces";
import { ModelRegistry } from "@/components/dashboard/agent/model-registry";
import { MonitoringPanel } from "@/components/dashboard/agent/monitoring-panel";
import { AutonomyControls } from "@/components/dashboard/agent/autonomy-controls";

const TABS = [
  { id: "evals", label: "Evals", icon: FlaskConical },
  { id: "redteam", label: "Red-Team", icon: ShieldAlert },
  { id: "prompts", label: "Prompts", icon: FileText },
  { id: "traces", label: "Traces", icon: Route },
  { id: "models", label: "Models", icon: Cpu },
  { id: "monitoring", label: "Monitoring", icon: Activity },
  { id: "controls", label: "Controls", icon: SlidersHorizontal },
] as const;

type TabId = (typeof TABS)[number]["id"];

const TAB_COMPONENTS: Record<TabId, React.FC> = {
  evals: EvalDashboard,
  redteam: RedTeamDashboard,
  prompts: PromptRegistry,
  traces: AgentTraces,
  models: ModelRegistry,
  monitoring: MonitoringPanel,
  controls: AutonomyControls,
};

export default function AgentLifeyclePage() {
  const [activeTab, setActiveTab] = useState<TabId>("evals");

  const ActiveComponent = TAB_COMPONENTS[activeTab];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-foreground">
          Agent Lifecycle Console
        </h1>
        <p className="text-sm text-muted-foreground mt-1">
          Production reliability controls for your AI lending agent
        </p>
      </div>

      {/* Tab Navigation */}
      <div className="border-b border-border">
        <nav className="flex gap-1 -mb-px overflow-x-auto">
          {TABS.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={cn(
                  "flex items-center gap-2 px-4 py-2.5 text-sm font-medium border-b-2 transition-colors whitespace-nowrap cursor-pointer",
                  isActive
                    ? "border-primary text-primary"
                    : "border-transparent text-muted-foreground hover:text-foreground hover:border-border"
                )}
              >
                <Icon className="h-4 w-4" />
                {tab.label}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Tab Content */}
      <ActiveComponent />
    </div>
  );
}
