"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";
import { Container } from "@/components/ui/container";
import { Heading } from "@/components/ui/heading";
import { SectionLabel } from "@/components/ui/section-label";
import { Section } from "@/components/ui/section";
import {
  Pencil,
  Hammer,
  FlaskConical,
  Swords,
  Rocket,
  Activity,
  TrendingUp,
  ArrowRight,
} from "lucide-react";

const pipelineSteps = [
  {
    name: "Design",
    icon: Pencil,
    color: "bg-violet-600",
    description:
      "Segment-specific prompt architecture. Define tools, policies, and borrower personas for each of 38 segments.",
  },
  {
    name: "Build",
    icon: Hammer,
    color: "bg-blue-600",
    description:
      "Version-controlled prompt authoring with typed tool schemas, policy rules, and conversation templates.",
  },
  {
    name: "Evaluate",
    icon: FlaskConical,
    color: "bg-cyan-600",
    description:
      "500+ automated test conversations per segment. Unit, trajectory, conversation, and policy evals.",
  },
  {
    name: "Red-Team",
    icon: Swords,
    color: "bg-orange-600",
    description:
      "Adversarial attack simulation: prompt injection, social engineering, PII extraction, jailbreak attempts.",
  },
  {
    name: "Deploy",
    icon: Rocket,
    color: "bg-green-600",
    description:
      "Canary rollout at 5% traffic with parallel eval scoring. Auto-rollback on regression detection.",
  },
  {
    name: "Monitor",
    icon: Activity,
    color: "bg-amber-600",
    description:
      "Real-time trace observability, cost tracking, drift detection, and alert rules on every metric.",
  },
  {
    name: "Improve",
    icon: TrendingUp,
    color: "bg-rose-600",
    description:
      "Continuous fine-tuning from production data. A/B test prompt variants. Close the feedback loop.",
  },
];

const containerVariants = {
  hidden: {},
  visible: {
    transition: {
      staggerChildren: 0.1,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 24 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5, ease: "easeOut" as const } },
};

export function AgentPipeline() {
  return (
    <Section id="agent-pipeline" background="white">
      <Container>
        <div className="text-center mb-16">
          <SectionLabel>Development Lifecycle</SectionLabel>
          <Heading as="h2" size="3xl" className="mt-4">
            Agent Development Pipeline
          </Heading>
          <p className="mt-4 text-lg text-muted-foreground max-w-2xl mx-auto">
            Every AI agent goes through a rigorous 7-stage lifecycle before it
            touches a single borrower. No shortcuts.
          </p>
        </div>

        {/* Horizontal flow - desktop */}
        <motion.div
          className="hidden lg:flex items-start justify-between gap-2"
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-80px" }}
        >
          {pipelineSteps.map((step, i) => (
            <motion.div
              key={step.name}
              variants={itemVariants}
              className="flex items-start flex-1"
            >
              <div className="flex flex-col items-center text-center flex-1">
                <div
                  className={cn(
                    "h-14 w-14 rounded-2xl flex items-center justify-center mb-4",
                    step.color
                  )}
                >
                  <step.icon className="h-6 w-6 text-white" />
                </div>
                <h3 className="font-semibold text-foreground text-sm mb-2">
                  {step.name}
                </h3>
                <p className="text-xs text-muted-foreground leading-relaxed max-w-[160px]">
                  {step.description}
                </p>
              </div>
              {i < pipelineSteps.length - 1 && (
                <div className="pt-5 px-1 shrink-0">
                  <ArrowRight className="h-4 w-4 text-muted-foreground/50" />
                </div>
              )}
            </motion.div>
          ))}
        </motion.div>

        {/* Stacked flow - mobile / tablet */}
        <motion.div
          className="lg:hidden grid sm:grid-cols-2 gap-4"
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-80px" }}
        >
          {pipelineSteps.map((step) => (
            <motion.div
              key={step.name}
              variants={itemVariants}
              className="bg-surface rounded-xl border border-border p-5 flex items-start gap-4"
            >
              <div
                className={cn(
                  "h-11 w-11 rounded-xl flex items-center justify-center shrink-0",
                  step.color
                )}
              >
                <step.icon className="h-5 w-5 text-white" />
              </div>
              <div>
                <h3 className="font-semibold text-foreground text-sm">
                  {step.name}
                </h3>
                <p className="text-xs text-muted-foreground mt-1 leading-relaxed">
                  {step.description}
                </p>
              </div>
            </motion.div>
          ))}
        </motion.div>
      </Container>
    </Section>
  );
}
