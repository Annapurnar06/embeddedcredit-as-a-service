"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";
import { Container } from "@/components/ui/container";
import { Heading } from "@/components/ui/heading";
import { SectionLabel } from "@/components/ui/section-label";
import { Section } from "@/components/ui/section";
import { Badge } from "@/components/ui/badge";
import { AnimatedSection } from "@/components/ui/animated-section";
import {
  Users,
  ShieldCheck,
  ArrowRight,
  CheckCircle2,
  AlertTriangle,
  Eye,
  UserCheck,
  Bot,
  ClipboardCheck,
} from "lucide-react";

const autonomyLevels = [
  {
    level: 0,
    name: "Full Human",
    description:
      "Human reviews and approves every AI decision. AI assists with data gathering and scoring only.",
    useCases: "Initial deployment, high-risk segments, regulatory requirement",
    color: "bg-red-500",
    aiRole: "Read-only assistant",
    humanRole: "All decisions",
  },
  {
    level: 1,
    name: "Human WRITE",
    description:
      "AI handles all READ operations autonomously. Human approves WRITE operations (disbursements, account changes).",
    useCases: "Standard NBFC operations, balanced efficiency and control",
    color: "bg-orange-500",
    aiRole: "Auto-READ, recommend WRITE",
    humanRole: "Approve disbursements",
  },
  {
    level: 2,
    name: "Human Exceptions",
    description:
      "AI operates fully autonomous except for low-confidence scores, edge cases, and amounts above threshold.",
    useCases: "Mature deployments with established trust, high-volume segments",
    color: "bg-blue-500",
    aiRole: "End-to-end with escalation",
    humanRole: "Exception review only",
  },
  {
    level: 3,
    name: "Full Auto",
    description:
      "AI handles the complete lending lifecycle end-to-end. Humans monitor dashboards and handle escalations.",
    useCases: "High-confidence segments with proven track record",
    color: "bg-green-500",
    aiRole: "Complete autonomy",
    humanRole: "Monitor & escalation",
  },
];

const makerCheckerGates = [
  {
    operation: "Loan Disbursement",
    maker: "AI Agent",
    checker: "Human Officer",
    threshold: "All amounts",
    sla: "< 15 minutes",
  },
  {
    operation: "Credit Limit Increase",
    maker: "AI Agent",
    checker: "Risk Manager",
    threshold: "> ₹50,000",
    sla: "< 30 minutes",
  },
  {
    operation: "KYC Override",
    maker: "Branch Officer",
    checker: "Compliance Head",
    threshold: "All overrides",
    sla: "< 1 hour",
  },
  {
    operation: "Interest Rate Change",
    maker: "AI Agent",
    checker: "Product Manager",
    threshold: "> 0.5% deviation",
    sla: "< 2 hours",
  },
  {
    operation: "Account Closure",
    maker: "AI Agent",
    checker: "Human Officer",
    threshold: "All closures",
    sla: "< 30 minutes",
  },
];

const escalationFlow = [
  {
    trigger: "Confidence < 60%",
    action: "Auto-escalate to human queue",
    icon: AlertTriangle,
    color: "bg-danger",
  },
  {
    trigger: "60% ≤ Confidence < 80%",
    action: "Flag for review, continue with caution",
    icon: Eye,
    color: "bg-warning",
  },
  {
    trigger: "80% ≤ Confidence < 95%",
    action: "Proceed with enhanced monitoring",
    icon: UserCheck,
    color: "bg-info",
  },
  {
    trigger: "Confidence ≥ 95%",
    action: "Full autonomous processing",
    icon: Bot,
    color: "bg-success",
  },
];

export function HumanControls() {
  const [activeLevel, setActiveLevel] = useState(1);

  return (
    <Section id="human-controls" background="white">
      <Container>
        <AnimatedSection className="text-center mb-16">
          <SectionLabel>Human-in-the-Loop</SectionLabel>
          <Heading as="h2" size="3xl" className="mt-4">
            You Control the Dial
          </Heading>
          <p className="mt-4 text-lg text-muted-foreground max-w-2xl mx-auto">
            Configure the autonomy level per lender, per segment. From full
            human review to fully automated — your risk appetite, your rules.
          </p>
        </AnimatedSection>

        {/* Autonomy Ladder */}
        <AnimatedSection className="mb-16">
          <div className="flex items-center gap-2 mb-6">
            <Users className="h-5 w-5 text-primary" />
            <h3 className="text-lg font-semibold text-foreground">
              Autonomy Ladder
            </h3>
          </div>

          {/* Interactive slider */}
          <div className="bg-white rounded-xl border border-border p-6 mb-6">
            <div className="flex items-center justify-between mb-6">
              {autonomyLevels.map((level) => (
                <button
                  key={level.level}
                  onClick={() => setActiveLevel(level.level)}
                  className={cn(
                    "flex flex-col items-center cursor-pointer transition-all",
                    activeLevel === level.level
                      ? "scale-110"
                      : "opacity-50 hover:opacity-75"
                  )}
                >
                  <div
                    className={cn(
                      "h-12 w-12 rounded-full flex items-center justify-center text-white font-bold text-sm mb-2 transition-all",
                      level.color,
                      activeLevel === level.level && "ring-4 ring-offset-2 ring-primary/30"
                    )}
                  >
                    L{level.level}
                  </div>
                  <span className="text-xs font-medium text-foreground hidden sm:block">
                    {level.name}
                  </span>
                </button>
              ))}
            </div>

            {/* Track */}
            <div className="relative h-2 bg-muted rounded-full mb-8">
              <motion.div
                className="absolute h-full bg-primary rounded-full"
                animate={{ width: `${(activeLevel / 3) * 100}%` }}
                transition={{ duration: 0.4, ease: "easeOut" }}
              />
            </div>

            {/* Active level detail */}
            <motion.div
              key={activeLevel}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
              className="bg-surface-raised rounded-xl p-6"
            >
              <div className="flex items-center gap-3 mb-3">
                <div
                  className={cn(
                    "h-10 w-10 rounded-lg flex items-center justify-center text-white font-bold text-sm",
                    autonomyLevels[activeLevel].color
                  )}
                >
                  L{activeLevel}
                </div>
                <div>
                  <h4 className="font-semibold text-foreground">
                    {autonomyLevels[activeLevel].name}
                  </h4>
                  <Badge variant="outline">Level {activeLevel}</Badge>
                </div>
              </div>
              <p className="text-sm text-muted-foreground mb-4">
                {autonomyLevels[activeLevel].description}
              </p>
              <div className="grid sm:grid-cols-3 gap-4">
                <div className="bg-white rounded-lg p-3 border border-border">
                  <div className="text-xs text-muted-foreground mb-1">
                    AI Role
                  </div>
                  <div className="text-sm font-medium text-foreground">
                    {autonomyLevels[activeLevel].aiRole}
                  </div>
                </div>
                <div className="bg-white rounded-lg p-3 border border-border">
                  <div className="text-xs text-muted-foreground mb-1">
                    Human Role
                  </div>
                  <div className="text-sm font-medium text-foreground">
                    {autonomyLevels[activeLevel].humanRole}
                  </div>
                </div>
                <div className="bg-white rounded-lg p-3 border border-border">
                  <div className="text-xs text-muted-foreground mb-1">
                    Use Cases
                  </div>
                  <div className="text-sm font-medium text-foreground">
                    {autonomyLevels[activeLevel].useCases}
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </AnimatedSection>

        {/* Maker-Checker Gates */}
        <AnimatedSection className="mb-16">
          <div className="flex items-center gap-2 mb-6">
            <ShieldCheck className="h-5 w-5 text-primary" />
            <h3 className="text-lg font-semibold text-foreground">
              Maker-Checker Gates on WRITE Operations
            </h3>
          </div>
          <div className="bg-white rounded-xl border border-border overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-border bg-surface-raised">
                    <th className="text-left px-4 py-3 font-semibold text-foreground">
                      Operation
                    </th>
                    <th className="text-left px-4 py-3 font-semibold text-foreground">
                      Maker
                    </th>
                    <th className="text-left px-4 py-3 font-semibold text-foreground">
                      Checker
                    </th>
                    <th className="text-left px-4 py-3 font-semibold text-foreground">
                      Threshold
                    </th>
                    <th className="text-center px-4 py-3 font-semibold text-foreground">
                      SLA
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {makerCheckerGates.map((gate, i) => (
                    <tr
                      key={gate.operation}
                      className={cn(
                        "border-b border-border last:border-0",
                        i % 2 === 1 && "bg-surface-raised/50"
                      )}
                    >
                      <td className="px-4 py-3 font-medium text-foreground">
                        {gate.operation}
                      </td>
                      <td className="px-4 py-3 text-muted-foreground">
                        {gate.maker}
                      </td>
                      <td className="px-4 py-3 text-muted-foreground">
                        {gate.checker}
                      </td>
                      <td className="px-4 py-3 text-xs font-mono text-muted-foreground">
                        {gate.threshold}
                      </td>
                      <td className="px-4 py-3 text-center">
                        <Badge variant="outline">{gate.sla}</Badge>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </AnimatedSection>

        {/* Confidence-Based Escalation */}
        <AnimatedSection className="mb-16">
          <div className="flex items-center gap-2 mb-6">
            <AlertTriangle className="h-5 w-5 text-primary" />
            <h3 className="text-lg font-semibold text-foreground">
              Confidence-Based Escalation Flow
            </h3>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {escalationFlow.map((step, i) => (
              <div key={step.trigger} className="relative">
                {i < escalationFlow.length - 1 && (
                  <div className="hidden lg:block absolute top-1/2 -right-2 z-10">
                    <ArrowRight className="h-4 w-4 text-muted-foreground" />
                  </div>
                )}
                <div className="bg-white rounded-xl border border-border p-5 h-full">
                  <div
                    className={cn(
                      "h-10 w-10 rounded-lg flex items-center justify-center mb-3",
                      step.color
                    )}
                  >
                    <step.icon className="h-5 w-5 text-white" />
                  </div>
                  <div className="text-sm font-semibold text-foreground mb-1">
                    {step.trigger}
                  </div>
                  <p className="text-xs text-muted-foreground">
                    {step.action}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </AnimatedSection>

        {/* Override Audit */}
        <AnimatedSection>
          <div className="flex items-center gap-2 mb-6">
            <ClipboardCheck className="h-5 w-5 text-primary" />
            <h3 className="text-lg font-semibold text-foreground">
              Override Audit Trail
            </h3>
          </div>
          <div className="bg-white rounded-xl border border-border p-6">
            <p className="text-sm text-muted-foreground mb-4">
              Every human override is immutably logged with full context for
              regulatory compliance and model improvement.
            </p>
            <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
              {[
                {
                  field: "Override ID",
                  example: "OVR-2025-04821",
                },
                {
                  field: "Officer Identity",
                  example: "Verified via SSO + role",
                },
                {
                  field: "AI Recommendation",
                  example: "Original score + rationale",
                },
                {
                  field: "Override Reason",
                  example: "Mandatory free-text + category",
                },
              ].map((item) => (
                <div
                  key={item.field}
                  className="bg-surface-raised rounded-lg p-4"
                >
                  <div className="text-xs text-muted-foreground mb-1">
                    {item.field}
                  </div>
                  <div className="text-sm font-medium text-foreground flex items-center gap-1.5">
                    <CheckCircle2 className="h-3.5 w-3.5 text-success shrink-0" />
                    {item.example}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </AnimatedSection>
      </Container>
    </Section>
  );
}
