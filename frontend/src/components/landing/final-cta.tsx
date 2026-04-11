"use client";

import { Container } from "@/components/ui/container";
import { Section } from "@/components/ui/section";
import { AnimatedSection } from "@/components/ui/animated-section";
import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";

export function FinalCTA() {
  return (
    <Section background="primary" className="py-24">
      <Container size="md">
        <AnimatedSection className="text-center">
          <h2 className="text-3xl lg:text-5xl font-bold text-white leading-tight">
            Built for the 300 million.
          </h2>
          <p className="mt-6 text-lg text-blue-100 max-w-xl mx-auto leading-relaxed">
            An AI-native lending operating system that makes micro-loans
            economically viable. From WhatsApp to disbursement in 15 minutes.
          </p>
          <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-3">
            <Button
              size="xl"
              className="bg-white text-primary hover:bg-blue-50"
            >
              Request Demo
              <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
            <Button
              variant="outline"
              size="xl"
              className="border-white/30 text-white hover:bg-white/10"
            >
              See Platform
            </Button>
          </div>
        </AnimatedSection>
      </Container>
    </Section>
  );
}
