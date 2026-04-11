"use client";

import { useState } from "react";
import { Container } from "@/components/ui/container";
import { Heading } from "@/components/ui/heading";
import { SectionLabel } from "@/components/ui/section-label";
import { Section } from "@/components/ui/section";
import { AnimatedSection } from "@/components/ui/animated-section";
import { BORROWER_JOURNEYS } from "@/lib/constants";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import { CheckCircle2, ArrowRight } from "lucide-react";

export function BorrowerJourneys() {
  const [activeJourney, setActiveJourney] = useState(0);
  const journey = BORROWER_JOURNEYS[activeJourney];

  return (
    <Section id="use-cases">
      <Container>
        <AnimatedSection className="text-center mb-12">
          <SectionLabel>Use Cases</SectionLabel>
          <Heading as="h2" size="3xl" className="mt-4">
            Real borrowers. Real journeys.
          </Heading>
          <p className="mt-4 text-lg text-muted-foreground max-w-2xl mx-auto">
            See how the AI agent originates loans for three different borrower
            segments -- each with segment-specific data, scoring, and products.
          </p>
        </AnimatedSection>

        <div className="flex flex-wrap justify-center gap-2 mb-10">
          {BORROWER_JOURNEYS.map((j, i) => (
            <button
              key={j.title}
              onClick={() => setActiveJourney(i)}
              className={cn(
                "px-5 py-2.5 rounded-lg text-sm font-medium transition-all cursor-pointer",
                activeJourney === i
                  ? "bg-primary text-primary-foreground shadow-sm"
                  : "bg-surface-raised border border-border text-muted-foreground hover:text-foreground"
              )}
            >
              {j.segment}
            </button>
          ))}
        </div>

        <AnimatedSection key={activeJourney}>
          <div className="bg-white rounded-2xl border border-border overflow-hidden">
            <div className="px-8 py-6 border-b border-border bg-surface-raised">
              <h3 className="text-xl font-semibold text-foreground">{journey.title}</h3>
              <div className="mt-2 flex items-center gap-3">
                <Badge variant="primary">{journey.segment}</Badge>
                <span className="text-sm text-muted-foreground">{journey.loan}</span>
              </div>
            </div>
            <div className="p-8">
              <div className="space-y-0">
                {journey.steps.map((step, i) => (
                  <div key={i} className="relative flex gap-4">
                    <div className="flex flex-col items-center">
                      <div className="h-8 w-8 rounded-full bg-primary-light flex items-center justify-center shrink-0">
                        <CheckCircle2 className="h-4 w-4 text-primary" />
                      </div>
                      {i < journey.steps.length - 1 && (
                        <div className="w-px h-full bg-border min-h-[24px]" />
                      )}
                    </div>
                    <div className="pb-6">
                      <div className="flex items-center gap-2">
                        <span className="text-xs font-mono px-2 py-0.5 rounded bg-surface-raised text-muted-foreground border border-border">
                          {step.tool}
                        </span>
                      </div>
                      <p className="mt-1 text-sm text-muted-foreground leading-relaxed">
                        {step.description}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
              <div className="mt-4 pt-4 border-t border-border flex items-center gap-2 text-sm text-primary font-medium">
                <ArrowRight className="h-4 w-4" />
                Total time: 15 minutes. Total cost: ~{"\u20B9"}200 per origination.
              </div>
            </div>
          </div>
        </AnimatedSection>
      </Container>
    </Section>
  );
}
