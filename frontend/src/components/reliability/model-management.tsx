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
  Database,
  Cpu,
  ArrowRight,
  GitBranch,
  FlaskConical,
  RotateCcw,
  Bot,
  User,
  Server,
  Zap,
  CheckCircle2,
} from "lucide-react";

const modelRegistry = [
  {
    segment: "Dairy Farmer",
    model: "GPT-4o-mini",
    version: "2025-03-26",
    status: "production",
    throughput: "42 conv/min",
    costPer: "₹9.2",
  },
  {
    segment: "Kirana Shop",
    model: "GPT-4o-mini",
    version: "2025-03-26",
    status: "production",
    throughput: "45 conv/min",
    costPer: "₹8.8",
  },
  {
    segment: "Gig Worker",
    model: "GPT-4o",
    version: "2025-04-01",
    status: "production",
    throughput: "28 conv/min",
    costPer: "₹14.5",
  },
  {
    segment: "Gold Loan",
    model: "GPT-4o-mini",
    version: "2025-03-26",
    status: "production",
    throughput: "40 conv/min",
    costPer: "₹8.1",
  },
  {
    segment: "EV Finance",
    model: "GPT-4o",
    version: "2025-04-01",
    status: "canary",
    throughput: "25 conv/min",
    costPer: "₹15.2",
  },
  {
    segment: "Solar Loan",
    model: "GPT-4o-mini",
    version: "2025-03-26",
    status: "production",
    throughput: "38 conv/min",
    costPer: "₹9.5",
  },
];

const canarySteps = [
  {
    name: "5% Traffic",
    description: "Route 5% of segment traffic to new model version",
    icon: GitBranch,
    color: "bg-blue-600",
  },
  {
    name: "Parallel Evals",
    description: "Run eval suite on both old and new model outputs in real-time",
    icon: FlaskConical,
    color: "bg-violet-600",
  },
  {
    name: "Score Compare",
    description: "Compare pass rates, latency, cost, and hallucination metrics",
    icon: Cpu,
    color: "bg-cyan-600",
  },
  {
    name: "Auto-Rollback",
    description: "If regression detected, instantly revert to previous version",
    icon: RotateCcw,
    color: "bg-amber-600",
  },
];

const fallbackChain = [
  {
    name: "Primary Model",
    model: "GPT-4o / GPT-4o-mini",
    description: "Segment-specific primary model with full capability",
    icon: Zap,
    color: "bg-primary",
    status: "active",
  },
  {
    name: "Fallback Model",
    model: "GPT-3.5-turbo",
    description: "Lower-cost model for degraded but functional service",
    icon: Server,
    color: "bg-warning",
    status: "standby",
  },
  {
    name: "Rule-Based",
    model: "Deterministic Engine",
    description: "Pre-coded decision trees handle standard flows without LLM",
    icon: Bot,
    color: "bg-info",
    status: "standby",
  },
  {
    name: "Human Queue",
    model: "Human Agent",
    description: "Route to human with full context if all models unavailable",
    icon: User,
    color: "bg-success",
    status: "standby",
  },
];

const fineTuningPipeline = [
  {
    step: "Data Collection",
    description: "High-quality production conversations labeled by human reviewers",
    metrics: "10K+ conversations/month per segment",
  },
  {
    step: "Data Curation",
    description: "Filter for quality, remove PII, balance segment representation",
    metrics: "3-stage review pipeline, 98% label agreement",
  },
  {
    step: "Fine-Tune Training",
    description: "LoRA fine-tuning on segment-specific data with eval checkpoints",
    metrics: "2-4 hour training cycles, daily iteration capability",
  },
  {
    step: "Eval Gate",
    description: "Must pass full eval suite with no regression before deployment",
    metrics: "500+ test cases, 98%+ pass rate required",
  },
  {
    step: "Canary Deploy",
    description: "5% traffic rollout with real-time monitoring and comparison",
    metrics: "24-48 hour soak period before full rollout",
  },
];

export function ModelManagement() {
  return (
    <Section id="model-management" background="gray">
      <Container>
        <AnimatedSection className="text-center mb-16">
          <SectionLabel>Model Operations</SectionLabel>
          <Heading as="h2" size="3xl" className="mt-4">
            Model Registry & Deployment
          </Heading>
          <p className="mt-4 text-lg text-muted-foreground max-w-2xl mx-auto">
            Every segment runs on a specific model version with canary deploys,
            automatic rollback, and a multi-layer fallback chain. Zero downtime, always.
          </p>
        </AnimatedSection>

        {/* Model Registry */}
        <AnimatedSection className="mb-16">
          <div className="flex items-center gap-2 mb-6">
            <Database className="h-5 w-5 text-primary" />
            <h3 className="text-lg font-semibold text-foreground">
              Model Registry
            </h3>
            <Badge variant="primary" className="ml-2">
              Per-Segment Assignment
            </Badge>
          </div>
          <div className="bg-white rounded-xl border border-border overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-border bg-surface-raised">
                    <th className="text-left px-4 py-3 font-semibold text-foreground">
                      Segment
                    </th>
                    <th className="text-left px-4 py-3 font-semibold text-foreground">
                      Model
                    </th>
                    <th className="text-left px-4 py-3 font-semibold text-foreground">
                      Version
                    </th>
                    <th className="text-center px-4 py-3 font-semibold text-foreground">
                      Throughput
                    </th>
                    <th className="text-center px-4 py-3 font-semibold text-foreground">
                      Cost/Conv
                    </th>
                    <th className="text-center px-4 py-3 font-semibold text-foreground">
                      Status
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {modelRegistry.map((row, i) => (
                    <tr
                      key={row.segment}
                      className={cn(
                        "border-b border-border last:border-0",
                        i % 2 === 1 && "bg-surface-raised/50"
                      )}
                    >
                      <td className="px-4 py-3 font-medium text-foreground">
                        {row.segment}
                      </td>
                      <td className="px-4 py-3 font-mono text-xs text-muted-foreground">
                        {row.model}
                      </td>
                      <td className="px-4 py-3 text-xs text-muted-foreground">
                        {row.version}
                      </td>
                      <td className="px-4 py-3 text-center text-xs text-muted-foreground">
                        {row.throughput}
                      </td>
                      <td className="px-4 py-3 text-center text-xs font-medium text-foreground">
                        {row.costPer}
                      </td>
                      <td className="px-4 py-3 text-center">
                        <Badge
                          variant={
                            row.status === "production" ? "success" : "warning"
                          }
                        >
                          {row.status}
                        </Badge>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </AnimatedSection>

        {/* Canary Deployment */}
        <AnimatedSection className="mb-16">
          <div className="flex items-center gap-2 mb-6">
            <GitBranch className="h-5 w-5 text-primary" />
            <h3 className="text-lg font-semibold text-foreground">
              Canary Deployment Pipeline
            </h3>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {canarySteps.map((step, i) => (
              <div key={step.name} className="relative">
                {i < canarySteps.length - 1 && (
                  <div className="hidden lg:block absolute top-1/2 -right-2 z-10">
                    <ArrowRight className="h-4 w-4 text-muted-foreground" />
                  </div>
                )}
                <motion.div
                  initial={{ opacity: 0, y: 16 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.45, delay: i * 0.1 }}
                  className="bg-white rounded-xl border border-border p-5 h-full"
                >
                  <div
                    className={cn(
                      "h-10 w-10 rounded-lg flex items-center justify-center mb-3",
                      step.color
                    )}
                  >
                    <step.icon className="h-5 w-5 text-white" />
                  </div>
                  <h4 className="font-semibold text-foreground text-sm mb-1">
                    {step.name}
                  </h4>
                  <p className="text-xs text-muted-foreground leading-relaxed">
                    {step.description}
                  </p>
                </motion.div>
              </div>
            ))}
          </div>
        </AnimatedSection>

        {/* Fallback Chain */}
        <AnimatedSection className="mb-16">
          <div className="flex items-center gap-2 mb-6">
            <RotateCcw className="h-5 w-5 text-primary" />
            <h3 className="text-lg font-semibold text-foreground">
              Multi-Layer Fallback Chain
            </h3>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {fallbackChain.map((step, i) => (
              <div key={step.name} className="relative">
                {i < fallbackChain.length - 1 && (
                  <div className="hidden lg:block absolute top-1/2 -right-2 z-10">
                    <ArrowRight className="h-4 w-4 text-muted-foreground" />
                  </div>
                )}
                <div className="bg-white rounded-xl border border-border p-5 h-full">
                  <div className="flex items-center justify-between mb-3">
                    <div
                      className={cn(
                        "h-10 w-10 rounded-lg flex items-center justify-center",
                        step.color
                      )}
                    >
                      <step.icon className="h-5 w-5 text-white" />
                    </div>
                    <Badge
                      variant={
                        step.status === "active" ? "success" : "default"
                      }
                    >
                      {step.status}
                    </Badge>
                  </div>
                  <h4 className="font-semibold text-foreground text-sm">
                    {step.name}
                  </h4>
                  <div className="text-xs font-mono text-primary mt-1">
                    {step.model}
                  </div>
                  <p className="text-xs text-muted-foreground mt-2 leading-relaxed">
                    {step.description}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </AnimatedSection>

        {/* Fine-Tuning Pipeline */}
        <AnimatedSection>
          <div className="flex items-center gap-2 mb-6">
            <Cpu className="h-5 w-5 text-primary" />
            <h3 className="text-lg font-semibold text-foreground">
              Fine-Tuning Pipeline
            </h3>
          </div>
          <div className="bg-white rounded-xl border border-border p-6">
            <div className="space-y-4">
              {fineTuningPipeline.map((step, i) => (
                <motion.div
                  key={step.step}
                  initial={{ opacity: 0, x: -16 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.4, delay: i * 0.08 }}
                  className="flex items-start gap-4"
                >
                  <div className="flex flex-col items-center">
                    <div className="h-8 w-8 rounded-full bg-primary flex items-center justify-center text-white text-xs font-bold shrink-0">
                      {i + 1}
                    </div>
                    {i < fineTuningPipeline.length - 1 && (
                      <div className="w-0.5 h-8 bg-border mt-1" />
                    )}
                  </div>
                  <div className="pb-4">
                    <h4 className="font-semibold text-foreground text-sm">
                      {step.step}
                    </h4>
                    <p className="text-xs text-muted-foreground mt-1">
                      {step.description}
                    </p>
                    <div className="flex items-center gap-1.5 mt-2 text-xs text-primary">
                      <CheckCircle2 className="h-3 w-3" />
                      {step.metrics}
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </AnimatedSection>
      </Container>
    </Section>
  );
}
