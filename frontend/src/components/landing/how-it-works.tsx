"use client";

import { Container } from "@/components/ui/container";
import { Heading } from "@/components/ui/heading";
import { SectionLabel } from "@/components/ui/section-label";
import { Section } from "@/components/ui/section";
import { AnimatedSection } from "@/components/ui/animated-section";
import { HOW_IT_WORKS_STEPS } from "@/lib/constants";
import { MessageSquare, Search, Brain, Zap } from "lucide-react";

const icons = [MessageSquare, Search, Brain, Zap];

export function HowItWorks() {
  return (
    <Section id="how-it-works">
      <Container>
        <AnimatedSection className="text-center mb-16">
          <SectionLabel>How It Works</SectionLabel>
          <Heading as="h2" size="3xl" className="mt-4">
            WhatsApp to disbursement in 15 minutes
          </Heading>
          <p className="mt-4 text-lg text-muted-foreground max-w-2xl mx-auto">
            A single AI agent orchestrates the entire lending workflow -- from
            borrower greeting to fund transfer -- through policy-gated tools.
          </p>
        </AnimatedSection>

        <div className="grid md:grid-cols-4 gap-6">
          {HOW_IT_WORKS_STEPS.map((step, i) => {
            const Icon = icons[i];
            return (
              <AnimatedSection key={step.step} delay={i * 0.12}>
                <div className="relative text-center">
                  {i < 3 && (
                    <div className="hidden md:block absolute top-8 left-[calc(50%+32px)] w-[calc(100%-64px)] h-px bg-border" />
                  )}
                  <div className="relative inline-flex items-center justify-center h-16 w-16 rounded-2xl bg-primary-light mb-4">
                    <Icon className="h-7 w-7 text-primary" />
                    <span className="absolute -top-2 -right-2 h-6 w-6 rounded-full bg-primary text-white text-xs font-bold flex items-center justify-center">
                      {step.step}
                    </span>
                  </div>
                  <h3 className="text-lg font-semibold text-foreground">
                    {step.title}
                  </h3>
                  <p className="mt-2 text-sm text-muted-foreground leading-relaxed">
                    {step.description}
                  </p>
                  <p className="mt-2 text-xs text-primary font-medium">
                    {step.detail}
                  </p>
                </div>
              </AnimatedSection>
            );
          })}
        </div>
      </Container>
    </Section>
  );
}
