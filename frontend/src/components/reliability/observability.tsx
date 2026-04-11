"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";
import { Container } from "@/components/ui/container";
import { Heading } from "@/components/ui/heading";
import { SectionLabel } from "@/components/ui/section-label";
import { Section } from "@/components/ui/section";
import { Badge } from "@/components/ui/badge";
import { AnimatedSection } from "@/components/ui/animated-section";
import {
  Activity,
  ArrowRight,
  Clock,
  IndianRupee,
  Bell,
  TrendingDown,
  AlertTriangle,
} from "lucide-react";

const traceSteps = [
  { name: "Message In", latency: "2ms", color: "bg-blue-500" },
  { name: "Prompt Build", latency: "15ms", color: "bg-violet-500" },
  { name: "LLM Call", latency: "840ms", color: "bg-cyan-500" },
  { name: "Tool Calls", latency: "230ms", color: "bg-green-500" },
  { name: "Policy Eval", latency: "45ms", color: "bg-amber-500" },
  { name: "Response Out", latency: "8ms", color: "bg-rose-500" },
];

const totalTraceLatency = "1,140ms";

const costBreakdown = [
  {
    category: "LLM Token Cost",
    range: "₹8–15",
    unit: "per conversation",
    breakdown: "~2,100 tokens avg × ₹0.004–0.007/token",
    pct: 55,
    color: "bg-primary",
  },
  {
    category: "Tool API Cost",
    range: "₹2–5",
    unit: "per conversation",
    breakdown: "Bureau pull ₹2, KYC verify ₹1.5, Score compute ₹0.5",
    pct: 25,
    color: "bg-cyan-500",
  },
  {
    category: "Infrastructure",
    range: "₹1–3",
    unit: "per conversation",
    breakdown: "Compute, storage, tracing, and monitoring overhead",
    pct: 15,
    color: "bg-violet-500",
  },
  {
    category: "Guardrail Overhead",
    range: "₹0.5–2",
    unit: "per conversation",
    breakdown: "PII detection, policy eval, output validation",
    pct: 5,
    color: "bg-amber-500",
  },
];

const totalCost = "₹140–275 per fully processed loan";

const driftMetrics = [
  {
    name: "Score Distribution Shift",
    status: "normal",
    value: "0.02σ",
    threshold: "Alert at 0.5σ",
  },
  {
    name: "Approval Rate Drift",
    status: "normal",
    value: "−0.3%",
    threshold: "Alert at ±5%",
  },
  {
    name: "Tool Failure Rate",
    status: "normal",
    value: "0.1%",
    threshold: "Alert at 2%",
  },
  {
    name: "Avg Conversation Length",
    status: "warning",
    value: "+12%",
    threshold: "Alert at ±15%",
  },
];

const alertRules = [
  {
    name: "Hallucination Rate",
    condition: "> 1%",
    action: "Auto-pause segment + page oncall",
    severity: "critical",
  },
  {
    name: "Policy Violation",
    condition: "Any single violation",
    action: "Immediate kill switch + incident creation",
    severity: "critical",
  },
  {
    name: "Eval Score Drop",
    condition: "> 2% regression",
    action: "Auto-rollback to previous prompt version",
    severity: "high",
  },
  {
    name: "Latency P99",
    condition: "> 5 seconds",
    action: "Scale infra + alert engineering",
    severity: "medium",
  },
  {
    name: "Cost Per Conversation",
    condition: "> ₹20",
    action: "Review token usage + alert finance",
    severity: "medium",
  },
  {
    name: "Conversation Abandonment",
    condition: "> 40%",
    action: "Trigger prompt review + UX audit",
    severity: "low",
  },
];

const severityColors: Record<string, string> = {
  critical: "danger",
  high: "warning",
  medium: "info",
  low: "default",
};

export function Observability() {
  return (
    <Section id="observability" background="gray">
      <Container>
        <AnimatedSection className="text-center mb-16">
          <SectionLabel>Full Observability</SectionLabel>
          <Heading as="h2" size="3xl" className="mt-4">
            Every Agent Action, Traced & Costed
          </Heading>
          <p className="mt-4 text-lg text-muted-foreground max-w-2xl mx-auto">
            Complete visibility into every message, tool call, and decision.
            Real-time cost tracking, drift detection, and automated alerting.
          </p>
        </AnimatedSection>

        {/* Agent Trace Visualization */}
        <AnimatedSection className="mb-16">
          <div className="flex items-center gap-2 mb-6">
            <Activity className="h-5 w-5 text-primary" />
            <h3 className="text-lg font-semibold text-foreground">
              Agent Trace Visualization
            </h3>
            <Badge variant="outline" className="ml-2">
              Total: {totalTraceLatency}
            </Badge>
          </div>

          {/* Desktop horizontal trace */}
          <div className="hidden lg:block bg-white rounded-xl border border-border p-6">
            <div className="flex items-center justify-between">
              {traceSteps.map((step, i) => (
                <div key={step.name} className="flex items-center flex-1">
                  <div className="flex flex-col items-center flex-1">
                    <div
                      className={cn(
                        "h-12 w-12 rounded-xl flex items-center justify-center mb-2",
                        step.color
                      )}
                    >
                      <Clock className="h-5 w-5 text-white" />
                    </div>
                    <span className="text-xs font-medium text-foreground">
                      {step.name}
                    </span>
                    <span className="text-xs text-muted-foreground font-mono mt-0.5">
                      {step.latency}
                    </span>
                  </div>
                  {i < traceSteps.length - 1 && (
                    <ArrowRight className="h-4 w-4 text-muted-foreground/50 shrink-0 mx-1" />
                  )}
                </div>
              ))}
            </div>
            {/* Latency bar */}
            <div className="mt-6 flex h-3 rounded-full overflow-hidden">
              {traceSteps.map((step) => {
                const ms = parseInt(step.latency.replace(/[^\d]/g, ""));
                const pct = (ms / 1140) * 100;
                return (
                  <div
                    key={step.name}
                    className={cn("h-full", step.color)}
                    style={{ width: `${pct}%` }}
                    title={`${step.name}: ${step.latency}`}
                  />
                );
              })}
            </div>
            <div className="mt-2 flex justify-between text-xs text-muted-foreground">
              <span>0ms</span>
              <span>{totalTraceLatency}</span>
            </div>
          </div>

          {/* Mobile stacked trace */}
          <div className="lg:hidden space-y-2">
            {traceSteps.map((step) => (
              <div
                key={step.name}
                className="bg-white rounded-lg border border-border p-3 flex items-center justify-between"
              >
                <div className="flex items-center gap-3">
                  <div
                    className={cn(
                      "h-8 w-8 rounded-lg flex items-center justify-center",
                      step.color
                    )}
                  >
                    <Clock className="h-4 w-4 text-white" />
                  </div>
                  <span className="text-sm font-medium text-foreground">
                    {step.name}
                  </span>
                </div>
                <span className="text-sm font-mono text-muted-foreground">
                  {step.latency}
                </span>
              </div>
            ))}
          </div>
        </AnimatedSection>

        {/* Cost Tracking */}
        <AnimatedSection className="mb-16">
          <div className="flex items-center gap-2 mb-6">
            <IndianRupee className="h-5 w-5 text-primary" />
            <h3 className="text-lg font-semibold text-foreground">
              Cost Tracking
            </h3>
            <Badge variant="primary" className="ml-2">
              {totalCost}
            </Badge>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {costBreakdown.map((item) => (
              <div
                key={item.category}
                className="bg-white rounded-xl border border-border p-5"
              >
                <div className="flex items-center gap-2 mb-3">
                  <div className={cn("h-3 w-3 rounded-full", item.color)} />
                  <span className="text-xs font-medium text-foreground">
                    {item.category}
                  </span>
                </div>
                <div className="text-xl font-bold text-foreground">
                  {item.range}
                </div>
                <div className="text-xs text-muted-foreground mt-0.5">
                  {item.unit}
                </div>
                <div className="mt-3 h-2 bg-muted rounded-full overflow-hidden">
                  <motion.div
                    className={cn("h-full rounded-full", item.color)}
                    initial={{ width: 0 }}
                    whileInView={{ width: `${item.pct}%` }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.8, ease: "easeOut" }}
                  />
                </div>
                <div className="text-xs text-muted-foreground mt-2">
                  {item.breakdown}
                </div>
              </div>
            ))}
          </div>
        </AnimatedSection>

        {/* Drift Detection */}
        <AnimatedSection className="mb-16">
          <div className="flex items-center gap-2 mb-6">
            <TrendingDown className="h-5 w-5 text-primary" />
            <h3 className="text-lg font-semibold text-foreground">
              Drift Detection
            </h3>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {driftMetrics.map((metric) => (
              <div
                key={metric.name}
                className="bg-white rounded-xl border border-border p-5"
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs text-muted-foreground">
                    {metric.name}
                  </span>
                  <Badge
                    variant={
                      metric.status === "normal" ? "success" : "warning"
                    }
                  >
                    {metric.status}
                  </Badge>
                </div>
                <div className="text-2xl font-bold text-foreground">
                  {metric.value}
                </div>
                <div className="text-xs text-muted-foreground mt-1">
                  {metric.threshold}
                </div>
              </div>
            ))}
          </div>
        </AnimatedSection>

        {/* Alert Rules */}
        <AnimatedSection>
          <div className="flex items-center gap-2 mb-6">
            <Bell className="h-5 w-5 text-primary" />
            <h3 className="text-lg font-semibold text-foreground">
              Alert Rules & Thresholds
            </h3>
          </div>
          <div className="bg-white rounded-xl border border-border overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-border bg-surface-raised">
                    <th className="text-left px-4 py-3 font-semibold text-foreground">
                      Alert
                    </th>
                    <th className="text-left px-4 py-3 font-semibold text-foreground">
                      Condition
                    </th>
                    <th className="text-left px-4 py-3 font-semibold text-foreground">
                      Action
                    </th>
                    <th className="text-center px-4 py-3 font-semibold text-foreground">
                      Severity
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {alertRules.map((rule, i) => (
                    <tr
                      key={rule.name}
                      className={cn(
                        "border-b border-border last:border-0",
                        i % 2 === 1 && "bg-surface-raised/50"
                      )}
                    >
                      <td className="px-4 py-3 font-medium text-foreground flex items-center gap-2">
                        <AlertTriangle className="h-3.5 w-3.5 text-muted-foreground" />
                        {rule.name}
                      </td>
                      <td className="px-4 py-3 text-muted-foreground font-mono text-xs">
                        {rule.condition}
                      </td>
                      <td className="px-4 py-3 text-muted-foreground text-xs">
                        {rule.action}
                      </td>
                      <td className="px-4 py-3 text-center">
                        <Badge variant={severityColors[rule.severity] as "danger" | "warning" | "info" | "default"}>
                          {rule.severity}
                        </Badge>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </AnimatedSection>
      </Container>
    </Section>
  );
}
