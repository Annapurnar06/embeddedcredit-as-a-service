"use client";

import { Container } from "@/components/ui/container";
import { Heading } from "@/components/ui/heading";
import { SectionLabel } from "@/components/ui/section-label";
import { Section } from "@/components/ui/section";
import { AnimatedSection } from "@/components/ui/animated-section";
import { AlertTriangle, DollarSign, Shield } from "lucide-react";

const problems = [
  {
    icon: AlertTriangle,
    title: "Data Poverty",
    stat: "80%",
    statLabel: "rejection rate",
    description:
      "300 million Indians have no formal credit history. Bureau scores designed for salaried employees structurally exclude those whose creditworthiness is legible only through alternative data.",
    color: "text-danger",
    bg: "bg-danger-light",
  },
  {
    icon: DollarSign,
    title: "The Cost Problem",
    stat: "\u20B93,000",
    statLabel: "per origination",
    description:
      "Field visits, manual data entry, compliance paperwork. At 15% interest on a \u20B950,000 loan, origination cost alone consumes 40-60% of first year revenue. Small-ticket lending is broken.",
    color: "text-warning",
    bg: "bg-warning-light",
  },
  {
    icon: Shield,
    title: "Compliance Burden",
    stat: "17+",
    statLabel: "regulatory rules",
    description:
      "KFS delivery, cooling-off periods, CERSAI filing, PII masking, digital lending guidelines. Each new RBI regulation adds another manual process to an already strained workflow.",
    color: "text-primary",
    bg: "bg-primary-light",
  },
];

export function Problem() {
  return (
    <Section id="problem" background="gray">
      <Container>
        <AnimatedSection className="text-center mb-16">
          <SectionLabel>The Problem</SectionLabel>
          <Heading as="h2" size="3xl" className="mt-4">
            Why India&apos;s underserved can&apos;t get credit
          </Heading>
          <p className="mt-4 text-lg text-muted-foreground max-w-2xl mx-auto">
            Traditional lending infrastructure was designed for salaried employees
            with bureau scores above 700. It structurally excludes the people who
            need credit most.
          </p>
        </AnimatedSection>

        <div className="grid md:grid-cols-3 gap-8">
          {problems.map((problem, i) => (
            <AnimatedSection key={problem.title} delay={i * 0.1}>
              <div className="bg-white rounded-xl border border-border p-8 h-full">
                <div className={`inline-flex items-center justify-center h-12 w-12 rounded-xl ${problem.bg}`}>
                  <problem.icon className={`h-6 w-6 ${problem.color}`} />
                </div>
                <h3 className="mt-5 text-xl font-semibold text-foreground">
                  {problem.title}
                </h3>
                <div className="mt-3">
                  <span className={`text-3xl font-bold ${problem.color}`}>
                    {problem.stat}
                  </span>
                  <span className="ml-2 text-sm text-muted-foreground">
                    {problem.statLabel}
                  </span>
                </div>
                <p className="mt-4 text-sm text-muted-foreground leading-relaxed">
                  {problem.description}
                </p>
              </div>
            </AnimatedSection>
          ))}
        </div>
      </Container>
    </Section>
  );
}
