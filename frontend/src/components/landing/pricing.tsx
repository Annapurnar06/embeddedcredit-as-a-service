"use client";

import { Container } from "@/components/ui/container";
import { Heading } from "@/components/ui/heading";
import { SectionLabel } from "@/components/ui/section-label";
import { Section } from "@/components/ui/section";
import { AnimatedSection } from "@/components/ui/animated-section";
import { Button } from "@/components/ui/button";
import { PRICING_TIERS } from "@/lib/constants";
import { Check } from "lucide-react";
import { cn } from "@/lib/utils";

export function Pricing() {
  return (
    <Section id="pricing">
      <Container size="lg">
        <AnimatedSection className="text-center mb-16">
          <SectionLabel>Pricing</SectionLabel>
          <Heading as="h2" size="3xl" className="mt-4">
            Choose your scale
          </Heading>
          <p className="mt-4 text-lg text-muted-foreground max-w-2xl mx-auto">
            Start with a handful of segments and scale to the full platform.
            Every plan includes RBI compliance, audit trails, and WhatsApp channel.
          </p>
        </AnimatedSection>

        <div className="grid md:grid-cols-3 gap-6">
          {PRICING_TIERS.map((tier, i) => (
            <AnimatedSection key={tier.name} delay={i * 0.1}>
              <div
                className={cn(
                  "rounded-2xl border p-8 h-full flex flex-col",
                  tier.highlighted
                    ? "border-primary bg-white shadow-lg shadow-primary/10 relative"
                    : "border-border bg-white"
                )}
              >
                {tier.highlighted && (
                  <div className="absolute -top-3 left-1/2 -translate-x-1/2">
                    <span className="px-3 py-1 bg-primary text-primary-foreground text-xs font-semibold rounded-full">
                      Most Popular
                    </span>
                  </div>
                )}
                <div>
                  <h3 className="text-xl font-semibold text-foreground">{tier.name}</h3>
                  <p className="mt-1 text-sm text-muted-foreground">{tier.description}</p>
                </div>
                <div className="mt-6">
                  <span className="text-3xl font-bold text-foreground">{tier.price}</span>
                </div>
                <ul className="mt-6 space-y-3 flex-1">
                  {tier.features.map((feature) => (
                    <li key={feature} className="flex items-start gap-2 text-sm text-muted-foreground">
                      <Check className="h-4 w-4 text-success shrink-0 mt-0.5" />
                      {feature}
                    </li>
                  ))}
                </ul>
                <div className="mt-8">
                  <Button
                    variant={tier.highlighted ? "primary" : "outline"}
                    className="w-full"
                    size="lg"
                  >
                    {tier.cta}
                  </Button>
                </div>
              </div>
            </AnimatedSection>
          ))}
        </div>
      </Container>
    </Section>
  );
}
