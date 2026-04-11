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
  FlaskConical,
  TestTube,
  Route,
  MessageSquare,
  Scale,
  CheckCircle2,
  TrendingUp,
} from "lucide-react";

const evalTypes = [
  {
    name: "Unit Evals",
    icon: TestTube,
    color: "bg-blue-600",
    description:
      "Per-tool correctness testing. Every tool invocation is validated against typed schemas and expected outputs.",
    examples: [
      "bureau_pull returns valid score",
      "aadhaar_verify matches format",
      "loan_calculate within bounds",
    ],
  },
  {
    name: "Trajectory Evals",
    icon: Route,
    color: "bg-violet-600",
    description:
      "Multi-tool chain ordering validation. Ensures the agent calls tools in the correct sequence for each workflow.",
    examples: [
      "KYC → Bureau → Score → Offer",
      "No disbursement before consent",
      "Verification before data access",
    ],
  },
  {
    name: "Conversation Evals",
    icon: MessageSquare,
    color: "bg-cyan-600",
    description:
      "End-to-end borrower journey testing. Full conversation simulations from greeting to loan disbursement.",
    examples: [
      "500+ test conversations/segment",
      "Multi-language dialogue flows",
      "Edge case scenario coverage",
    ],
  },
  {
    name: "Policy Evals",
    icon: Scale,
    color: "bg-amber-600",
    description:
      "Compliance rule hit rate testing. Every RBI provision and internal policy is continuously validated.",
    examples: [
      "Cooling-off period enforced",
      "Interest rate cap compliance",
      "Consent before data access",
    ],
  },
];

const evalMetrics = [
  { label: "Eval Pass Rate", value: "98.7%", color: "text-success" },
  { label: "Tool Accuracy", value: "99.2%", color: "text-primary" },
  { label: "Policy Compliance", value: "99.9%", color: "text-success" },
  { label: "Hallucination Rate", value: "0.3%", color: "text-success" },
  { label: "Mean Latency", value: "1.2s", color: "text-primary" },
  { label: "Confirmation Detection", value: "97.8%", color: "text-info" },
];

const segmentBreakdown = [
  { segment: "Dairy Farmer", unitPass: "99.1%", trajectoryPass: "98.4%", convPass: "97.9%", policyPass: "100%", overall: "98.8%" },
  { segment: "Kirana Shop", unitPass: "98.8%", trajectoryPass: "99.0%", convPass: "98.2%", policyPass: "100%", overall: "99.0%" },
  { segment: "Gig Worker", unitPass: "99.3%", trajectoryPass: "97.8%", convPass: "98.5%", policyPass: "99.9%", overall: "98.9%" },
  { segment: "Gold Loan", unitPass: "99.5%", trajectoryPass: "99.2%", convPass: "98.7%", policyPass: "100%", overall: "99.3%" },
  { segment: "EV Finance", unitPass: "98.6%", trajectoryPass: "98.1%", convPass: "97.4%", policyPass: "100%", overall: "98.5%" },
  { segment: "Solar Loan", unitPass: "99.0%", trajectoryPass: "98.6%", convPass: "98.0%", policyPass: "100%", overall: "98.9%" },
];

const regressionData = [
  { metric: "Eval Pass Rate", v1: 96.2, v2: 98.7 },
  { metric: "Tool Accuracy", v1: 97.8, v2: 99.2 },
  { metric: "Policy Compliance", v1: 99.5, v2: 99.9 },
  { metric: "Confirmation Detection", v1: 94.1, v2: 97.8 },
];

const containerVariants = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.1 } },
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.45, ease: "easeOut" as const } },
};

export function EvalFramework() {
  return (
    <Section id="eval-framework" background="gray">
      <Container>
        <AnimatedSection className="text-center mb-16">
          <SectionLabel>Evaluation Framework</SectionLabel>
          <Heading as="h2" size="3xl" className="mt-4">
            4-Layer Evaluation System
          </Heading>
          <p className="mt-4 text-lg text-muted-foreground max-w-2xl mx-auto">
            Every prompt change runs through 2,000+ automated tests across unit,
            trajectory, conversation, and policy evaluations before reaching production.
          </p>
        </AnimatedSection>

        {/* Eval Types */}
        <motion.div
          className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-16"
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-80px" }}
        >
          {evalTypes.map((evalType) => (
            <motion.div
              key={evalType.name}
              variants={itemVariants}
              className="bg-white rounded-xl border border-border p-6 h-full"
            >
              <div
                className={cn(
                  "h-11 w-11 rounded-xl flex items-center justify-center mb-4",
                  evalType.color
                )}
              >
                <evalType.icon className="h-5 w-5 text-white" />
              </div>
              <h3 className="font-semibold text-foreground text-sm mb-2">
                {evalType.name}
              </h3>
              <p className="text-xs text-muted-foreground leading-relaxed mb-4">
                {evalType.description}
              </p>
              <div className="space-y-1.5">
                {evalType.examples.map((ex) => (
                  <div
                    key={ex}
                    className="text-xs text-muted-foreground flex items-start gap-1.5"
                  >
                    <CheckCircle2 className="h-3 w-3 text-success mt-0.5 shrink-0" />
                    {ex}
                  </div>
                ))}
              </div>
            </motion.div>
          ))}
        </motion.div>

        {/* Eval Metrics Dashboard */}
        <AnimatedSection className="mb-16">
          <div className="flex items-center gap-2 mb-6">
            <FlaskConical className="h-5 w-5 text-primary" />
            <h3 className="text-lg font-semibold text-foreground">
              Live Eval Metrics
            </h3>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
            {evalMetrics.map((metric) => (
              <div
                key={metric.label}
                className="bg-white rounded-xl border border-border p-4 text-center"
              >
                <div className={cn("text-2xl font-bold", metric.color)}>
                  {metric.value}
                </div>
                <div className="text-xs text-muted-foreground mt-1">
                  {metric.label}
                </div>
              </div>
            ))}
          </div>
        </AnimatedSection>

        {/* Segment Breakdown */}
        <AnimatedSection className="mb-16">
          <div className="flex items-center gap-2 mb-6">
            <TrendingUp className="h-5 w-5 text-primary" />
            <h3 className="text-lg font-semibold text-foreground">
              Segment-Level Eval Scores
            </h3>
          </div>
          <div className="bg-white rounded-xl border border-border overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-border bg-surface-raised">
                    <th className="text-left px-4 py-3 font-semibold text-foreground">
                      Segment
                    </th>
                    <th className="text-center px-4 py-3 font-semibold text-foreground">
                      Unit
                    </th>
                    <th className="text-center px-4 py-3 font-semibold text-foreground">
                      Trajectory
                    </th>
                    <th className="text-center px-4 py-3 font-semibold text-foreground">
                      Conversation
                    </th>
                    <th className="text-center px-4 py-3 font-semibold text-foreground">
                      Policy
                    </th>
                    <th className="text-center px-4 py-3 font-semibold text-foreground">
                      Overall
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {segmentBreakdown.map((row, i) => (
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
                      <td className="px-4 py-3 text-center text-success font-medium">
                        {row.unitPass}
                      </td>
                      <td className="px-4 py-3 text-center text-success font-medium">
                        {row.trajectoryPass}
                      </td>
                      <td className="px-4 py-3 text-center text-success font-medium">
                        {row.convPass}
                      </td>
                      <td className="px-4 py-3 text-center text-success font-medium">
                        {row.policyPass}
                      </td>
                      <td className="px-4 py-3 text-center">
                        <Badge variant="success">{row.overall}</Badge>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </AnimatedSection>

        {/* Version Regression Tracking */}
        <AnimatedSection>
          <div className="flex items-center gap-2 mb-6">
            <TrendingUp className="h-5 w-5 text-primary" />
            <h3 className="text-lg font-semibold text-foreground">
              Version Regression Tracking
            </h3>
            <div className="flex items-center gap-3 ml-auto">
              <div className="flex items-center gap-1.5">
                <div className="h-3 w-3 rounded bg-blue-300" />
                <span className="text-xs text-muted-foreground">v1.2</span>
              </div>
              <div className="flex items-center gap-1.5">
                <div className="h-3 w-3 rounded bg-primary" />
                <span className="text-xs text-muted-foreground">v1.3 (current)</span>
              </div>
            </div>
          </div>
          <div className="bg-white rounded-xl border border-border p-6">
            <div className="space-y-4">
              {regressionData.map((row) => (
                <div key={row.metric}>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-foreground">
                      {row.metric}
                    </span>
                    <span className="text-xs text-success font-medium">
                      +{(row.v2 - row.v1).toFixed(1)}%
                    </span>
                  </div>
                  <div className="space-y-1.5">
                    <div className="flex items-center gap-3">
                      <span className="text-xs text-muted-foreground w-10">v1.2</span>
                      <div className="flex-1 h-5 bg-muted rounded-full overflow-hidden">
                        <motion.div
                          className="h-full bg-blue-300 rounded-full"
                          initial={{ width: 0 }}
                          whileInView={{ width: `${row.v1}%` }}
                          viewport={{ once: true }}
                          transition={{ duration: 0.8, ease: "easeOut" }}
                        />
                      </div>
                      <span className="text-xs font-medium text-muted-foreground w-12 text-right">
                        {row.v1}%
                      </span>
                    </div>
                    <div className="flex items-center gap-3">
                      <span className="text-xs text-muted-foreground w-10">v1.3</span>
                      <div className="flex-1 h-5 bg-muted rounded-full overflow-hidden">
                        <motion.div
                          className="h-full bg-primary rounded-full"
                          initial={{ width: 0 }}
                          whileInView={{ width: `${row.v2}%` }}
                          viewport={{ once: true }}
                          transition={{ duration: 0.8, ease: "easeOut", delay: 0.15 }}
                        />
                      </div>
                      <span className="text-xs font-medium text-foreground w-12 text-right">
                        {row.v2}%
                      </span>
                    </div>
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
