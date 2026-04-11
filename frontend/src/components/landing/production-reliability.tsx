"use client";

import Link from "next/link";
import { Container } from "@/components/ui/container";
import { Heading } from "@/components/ui/heading";
import { SectionLabel } from "@/components/ui/section-label";
import { Section } from "@/components/ui/section";
import { AnimatedSection } from "@/components/ui/animated-section";
import { COMPLIANCE_GUARANTEES } from "@/lib/constants";
import { Button } from "@/components/ui/button";
import {
  ShieldCheck,
  FlaskConical,
  Users,
  Scale,
  ArrowRight,
  CheckCircle2,
  Lock,
  AlertTriangle,
  Eye,
} from "lucide-react";

const guardrailLayers = [
  {
    name: "Input Guards",
    description: "PII detection, injection detection, language identification",
    icon: Lock,
    color: "bg-blue-600",
    examples: ["Blocks Aadhaar/PAN in free text", "Detects prompt injection attempts", "Identifies borrower language"],
  },
  {
    name: "Structural Policy",
    description: "7 pre-tool deterministic rules",
    icon: ShieldCheck,
    color: "bg-violet-600",
    examples: ["Session state check", "Confirmation required", "Authority (maker-checker)", "Circuit breaker"],
  },
  {
    name: "Execution Pipeline",
    description: "7-step tool execution with audit trail",
    icon: Eye,
    color: "bg-cyan-600",
    examples: ["State check → Confirm → Auth → Breaker → Execute → Trace → Emit"],
  },
  {
    name: "Output Guards",
    description: "10 post-response behavioral rules",
    icon: AlertTriangle,
    color: "bg-amber-600",
    examples: ["No false promises", "PII masking verified", "Amount bounds check", "Language appropriateness"],
  },
];

export function ProductionReliability() {
  return (
    <Section id="reliability" background="gray">
      <Container>
        <AnimatedSection className="text-center mb-16">
          <SectionLabel>Production Reliability</SectionLabel>
          <Heading as="h2" size="3xl" className="mt-4">
            AI you can trust with lending decisions
          </Heading>
          <p className="mt-4 text-lg text-muted-foreground max-w-2xl mx-auto">
            Not a chatbot bolted onto legacy systems. A production-grade AI with
            guardrails, evals, red-teaming, and human-in-the-loop controls at every layer.
          </p>
        </AnimatedSection>

        {/* Guardrail Stack */}
        <AnimatedSection className="mb-16">
          <h3 className="text-lg font-semibold text-foreground mb-6 flex items-center gap-2">
            <ShieldCheck className="h-5 w-5 text-primary" />
            4-Layer Guardrail Stack
          </h3>
          <div className="grid md:grid-cols-4 gap-4">
            {guardrailLayers.map((layer, i) => (
              <div key={layer.name} className="relative">
                {i < 3 && (
                  <div className="hidden md:block absolute top-1/2 -right-2 z-10">
                    <ArrowRight className="h-4 w-4 text-muted-foreground" />
                  </div>
                )}
                <div className="bg-white rounded-xl border border-border p-5 h-full">
                  <div className={`inline-flex items-center justify-center h-10 w-10 rounded-lg ${layer.color} mb-3`}>
                    <layer.icon className="h-5 w-5 text-white" />
                  </div>
                  <h4 className="font-semibold text-foreground text-sm">{layer.name}</h4>
                  <p className="text-xs text-muted-foreground mt-1">{layer.description}</p>
                  <div className="mt-3 space-y-1">
                    {layer.examples.map((ex) => (
                      <div key={ex} className="text-xs text-muted-foreground flex items-start gap-1.5">
                        <CheckCircle2 className="h-3 w-3 text-success mt-0.5 shrink-0" />
                        {ex}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </AnimatedSection>

        {/* Eval + Red-Team + Human-in-the-Loop */}
        <div className="grid md:grid-cols-2 gap-8 mb-16">
          <AnimatedSection>
            <div className="bg-white rounded-xl border border-border p-6 h-full">
              <div className="flex items-center gap-2 mb-4">
                <FlaskConical className="h-5 w-5 text-primary" />
                <h3 className="font-semibold text-foreground">Eval + Red-Team</h3>
              </div>
              <p className="text-sm text-muted-foreground mb-4">
                Every prompt change runs through 500+ test conversations, adversarial
                attacks, and regression checks before touching production.
              </p>
              <div className="grid grid-cols-2 gap-3">
                {[
                  { label: "Eval Pass Rate", value: "98.7%" },
                  { label: "Attack Block Rate", value: "100%" },
                  { label: "Hallucination Rate", value: "0.3%" },
                  { label: "Policy Compliance", value: "99.9%" },
                ].map((metric) => (
                  <div key={metric.label} className="bg-surface-raised rounded-lg p-3">
                    <div className="text-xl font-bold text-foreground">{metric.value}</div>
                    <div className="text-xs text-muted-foreground">{metric.label}</div>
                  </div>
                ))}
              </div>
            </div>
          </AnimatedSection>

          <AnimatedSection delay={0.1}>
            <div className="bg-white rounded-xl border border-border p-6 h-full">
              <div className="flex items-center gap-2 mb-4">
                <Users className="h-5 w-5 text-primary" />
                <h3 className="font-semibold text-foreground">Human-in-the-Loop</h3>
              </div>
              <p className="text-sm text-muted-foreground mb-4">
                You control the dial. Configure the autonomy level per lender --
                from full human review to fully automated with exception handling.
              </p>
              <div className="space-y-3">
                {[
                  { level: "Full Human", desc: "Human approves every decision", pct: 25 },
                  { level: "Human WRITE", desc: "Auto-READ, human approves disbursements", pct: 50 },
                  { level: "Human Exceptions", desc: "Auto except low-confidence scores", pct: 75 },
                  { level: "Full Auto", desc: "AI handles end-to-end, humans monitor", pct: 100 },
                ].map((item) => (
                  <div key={item.level} className="flex items-center gap-3">
                    <div className="w-20 h-2 bg-muted rounded-full overflow-hidden shrink-0">
                      <div
                        className="h-full bg-primary rounded-full"
                        style={{ width: `${item.pct}%` }}
                      />
                    </div>
                    <div>
                      <span className="text-sm font-medium text-foreground">{item.level}</span>
                      <span className="text-xs text-muted-foreground ml-2">{item.desc}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </AnimatedSection>
        </div>

        {/* Compliance Grid */}
        <AnimatedSection>
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-foreground flex items-center gap-2">
              <Scale className="h-5 w-5 text-primary" />
              Structural Compliance
            </h3>
            <span className="text-sm text-muted-foreground">
              12 RBI provisions. Built in, not bolted on.
            </span>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {COMPLIANCE_GUARANTEES.map((item) => (
              <div
                key={item.rule}
                className="bg-white rounded-lg border border-border p-4 flex items-start gap-3"
              >
                <CheckCircle2 className="h-5 w-5 text-success shrink-0 mt-0.5" />
                <div>
                  <div className="text-sm font-medium text-foreground">{item.rule}</div>
                  <div className="text-xs text-muted-foreground mt-0.5">{item.provision}</div>
                  <div className="text-xs text-muted-foreground mt-1">{item.description}</div>
                </div>
              </div>
            ))}
          </div>
          <div className="mt-8 text-center">
            <Link href="/platform/reliability">
              <Button variant="outline">
                Deep-Dive: Agent Lifecycle & Reliability
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </Link>
          </div>
        </AnimatedSection>
      </Container>
    </Section>
  );
}
