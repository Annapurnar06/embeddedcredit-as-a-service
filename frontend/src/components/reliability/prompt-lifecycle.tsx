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
  FileCode2,
  GitBranch,
  FlaskConical,
  Eye,
  Shuffle,
  CheckCircle2,
  Clock,
  BarChart3,
} from "lucide-react";

const promptRegistryData = [
  {
    segment: "Dairy Farmer",
    version: "v3.2.1",
    lastUpdated: "2025-04-08",
    evalScore: "98.8%",
    status: "active",
    tokens: "2,140",
  },
  {
    segment: "Kirana Shop",
    version: "v3.1.0",
    lastUpdated: "2025-04-06",
    evalScore: "99.0%",
    status: "active",
    tokens: "1,980",
  },
  {
    segment: "Gig Worker",
    version: "v2.8.3",
    lastUpdated: "2025-04-09",
    evalScore: "98.9%",
    status: "active",
    tokens: "2,310",
  },
  {
    segment: "Gold Loan",
    version: "v3.0.0",
    lastUpdated: "2025-04-10",
    evalScore: "99.3%",
    status: "active",
    tokens: "1,870",
  },
  {
    segment: "EV Finance",
    version: "v2.9.1-rc.2",
    lastUpdated: "2025-04-11",
    evalScore: "97.6%",
    status: "staging",
    tokens: "2,450",
  },
  {
    segment: "SHG Member",
    version: "v2.7.0",
    lastUpdated: "2025-04-05",
    evalScore: "98.5%",
    status: "active",
    tokens: "2,080",
  },
];

const observabilityMetrics = [
  {
    label: "Avg Token Usage",
    value: "2,138",
    unit: "tokens/conv",
    icon: BarChart3,
    color: "text-primary",
  },
  {
    label: "Completion Quality",
    value: "94.2",
    unit: "% coherence",
    icon: CheckCircle2,
    color: "text-success",
  },
  {
    label: "Refusal Rate",
    value: "2.1",
    unit: "% legitimate",
    icon: Eye,
    color: "text-warning",
  },
  {
    label: "Avg Latency",
    value: "1.2",
    unit: "seconds",
    icon: Clock,
    color: "text-info",
  },
];

const abTestVariants = [
  {
    name: "Variant A (Control)",
    description: "Standard prompt with structured output format",
    traffic: "50%",
    conversionRate: "34.2%",
    satisfaction: "4.3/5",
    active: true,
  },
  {
    name: "Variant B (Challenger)",
    description: "Empathetic opening + simplified language for rural segments",
    traffic: "50%",
    conversionRate: "38.7%",
    satisfaction: "4.6/5",
    active: true,
  },
];

export function PromptLifecycle() {
  return (
    <Section id="prompt-lifecycle" background="gray">
      <Container>
        <AnimatedSection className="text-center mb-16">
          <SectionLabel>Prompt Engineering</SectionLabel>
          <Heading as="h2" size="3xl" className="mt-4">
            Version-Controlled Prompt Lifecycle
          </Heading>
          <p className="mt-4 text-lg text-muted-foreground max-w-2xl mx-auto">
            38 segment-specific prompts, each versioned, A/B tested, and
            continuously optimized with full observability on every metric.
          </p>
        </AnimatedSection>

        {/* Version-Controlled Prompts Concept */}
        <AnimatedSection className="mb-16">
          <div className="flex items-center gap-2 mb-6">
            <GitBranch className="h-5 w-5 text-primary" />
            <h3 className="text-lg font-semibold text-foreground">
              38 Segment Prompt Registry
            </h3>
            <Badge variant="primary" className="ml-2">
              Git-Versioned
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
                      Version
                    </th>
                    <th className="text-left px-4 py-3 font-semibold text-foreground">
                      Last Updated
                    </th>
                    <th className="text-center px-4 py-3 font-semibold text-foreground">
                      Tokens
                    </th>
                    <th className="text-center px-4 py-3 font-semibold text-foreground">
                      Eval Score
                    </th>
                    <th className="text-center px-4 py-3 font-semibold text-foreground">
                      Status
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {promptRegistryData.map((row, i) => (
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
                        {row.version}
                      </td>
                      <td className="px-4 py-3 text-xs text-muted-foreground">
                        {row.lastUpdated}
                      </td>
                      <td className="px-4 py-3 text-center text-xs text-muted-foreground">
                        {row.tokens}
                      </td>
                      <td className="px-4 py-3 text-center">
                        <span className="text-success font-medium text-xs">
                          {row.evalScore}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-center">
                        <Badge
                          variant={
                            row.status === "active" ? "success" : "warning"
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

        {/* A/B Testing */}
        <AnimatedSection className="mb-16">
          <div className="flex items-center gap-2 mb-6">
            <Shuffle className="h-5 w-5 text-primary" />
            <h3 className="text-lg font-semibold text-foreground">
              A/B Testing Framework
            </h3>
          </div>
          <div className="grid md:grid-cols-2 gap-4">
            {abTestVariants.map((variant) => (
              <motion.div
                key={variant.name}
                initial={{ opacity: 0, y: 16 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.45 }}
                className="bg-white rounded-xl border border-border p-6"
              >
                <div className="flex items-center gap-2 mb-3">
                  <FlaskConical className="h-4 w-4 text-primary" />
                  <h4 className="font-semibold text-foreground text-sm">
                    {variant.name}
                  </h4>
                  <Badge variant="primary">{variant.traffic} traffic</Badge>
                </div>
                <p className="text-xs text-muted-foreground mb-4">
                  {variant.description}
                </p>
                <div className="grid grid-cols-2 gap-3">
                  <div className="bg-surface-raised rounded-lg p-3">
                    <div className="text-lg font-bold text-foreground">
                      {variant.conversionRate}
                    </div>
                    <div className="text-xs text-muted-foreground">
                      Conversion Rate
                    </div>
                  </div>
                  <div className="bg-surface-raised rounded-lg p-3">
                    <div className="text-lg font-bold text-foreground">
                      {variant.satisfaction}
                    </div>
                    <div className="text-xs text-muted-foreground">
                      Satisfaction Score
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </AnimatedSection>

        {/* Prompt Observability */}
        <AnimatedSection>
          <div className="flex items-center gap-2 mb-6">
            <FileCode2 className="h-5 w-5 text-primary" />
            <h3 className="text-lg font-semibold text-foreground">
              Prompt Observability Metrics
            </h3>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {observabilityMetrics.map((metric) => (
              <div
                key={metric.label}
                className="bg-white rounded-xl border border-border p-5"
              >
                <div className="flex items-center gap-2 mb-3">
                  <metric.icon className={cn("h-4 w-4", metric.color)} />
                  <span className="text-xs text-muted-foreground">
                    {metric.label}
                  </span>
                </div>
                <div className="text-2xl font-bold text-foreground">
                  {metric.value}
                </div>
                <div className="text-xs text-muted-foreground mt-1">
                  {metric.unit}
                </div>
              </div>
            ))}
          </div>
        </AnimatedSection>
      </Container>
    </Section>
  );
}
