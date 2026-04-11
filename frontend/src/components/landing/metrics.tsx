"use client";

import { Container } from "@/components/ui/container";
import { Section } from "@/components/ui/section";
import { AnimatedSection } from "@/components/ui/animated-section";
import { AnimatedCounter } from "@/components/ui/animated-counter";

const metrics = [
  { end: 60, suffix: "", label: "Lending Tools", sublabel: "Typed, auditable, policy-gated" },
  { end: 38, suffix: "", label: "Borrower Segments", sublabel: "Each with custom scoring & products" },
  { end: 256, suffix: "", label: "Tests Passing", sublabel: "Full coverage in 2.5 seconds" },
  { end: 17, suffix: "", label: "Policy Rules", sublabel: "7 structural + 10 behavioral" },
  { end: 90, suffix: "%", label: "Cost Reduction", sublabel: "\u20B9275 vs \u20B93,000 per origination" },
  { end: 15, suffix: " min", label: "Disbursement", sublabel: "WhatsApp to bank account" },
];

export function Metrics() {
  return (
    <Section background="dark">
      <Container>
        <AnimatedSection>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-8">
            {metrics.map((metric) => (
              <div key={metric.label} className="text-center">
                <div className="text-3xl lg:text-4xl font-bold text-white">
                  <AnimatedCounter
                    end={metric.end}
                    suffix={metric.suffix}
                    duration={1.5}
                  />
                </div>
                <div className="mt-2 text-sm font-medium text-slate-300">
                  {metric.label}
                </div>
                <div className="mt-1 text-xs text-slate-500">
                  {metric.sublabel}
                </div>
              </div>
            ))}
          </div>
        </AnimatedSection>
      </Container>
    </Section>
  );
}
