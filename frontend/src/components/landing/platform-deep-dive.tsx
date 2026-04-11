"use client";

import { useState } from "react";
import { Container } from "@/components/ui/container";
import { Heading } from "@/components/ui/heading";
import { SectionLabel } from "@/components/ui/section-label";
import { Section } from "@/components/ui/section";
import { AnimatedSection } from "@/components/ui/animated-section";
import { TOOL_CATEGORIES, SEGMENT_CATEGORIES } from "@/lib/constants";
import { cn } from "@/lib/utils";
import { ChevronRight, Layers, Grid3X3 } from "lucide-react";

export function PlatformDeepDive() {
  const [activeCategory, setActiveCategory] = useState(0);
  const [activeSegmentGroup, setActiveSegmentGroup] = useState(
    Object.keys(SEGMENT_CATEGORIES)[0]
  );

  return (
    <Section id="platform" background="gray">
      <Container>
        <AnimatedSection className="text-center mb-16">
          <SectionLabel>Platform</SectionLabel>
          <Heading as="h2" size="3xl" className="mt-4">
            60 tools. 38 segments. One platform.
          </Heading>
          <p className="mt-4 text-lg text-muted-foreground max-w-2xl mx-auto">
            Every lending operation -- from identity verification to monitoring --
            is a typed, auditable, policy-gated tool callable by the AI agent.
          </p>
        </AnimatedSection>

        {/* Tool Stack */}
        <AnimatedSection className="mb-20">
          <div className="flex items-center gap-2 mb-6">
            <Layers className="h-5 w-5 text-primary" />
            <h3 className="text-xl font-semibold text-foreground">7-Layer Tool Stack</h3>
          </div>
          <div className="grid lg:grid-cols-[280px_1fr] gap-6">
            <div className="space-y-1">
              {TOOL_CATEGORIES.map((cat, i) => (
                <button
                  key={cat.name}
                  onClick={() => setActiveCategory(i)}
                  className={cn(
                    "w-full flex items-center justify-between px-4 py-3 rounded-lg text-sm font-medium transition-all cursor-pointer text-left",
                    activeCategory === i
                      ? "bg-white shadow-sm border border-border text-foreground"
                      : "text-muted-foreground hover:text-foreground hover:bg-white/50"
                  )}
                >
                  <span className="flex items-center gap-3">
                    <span
                      className="h-3 w-3 rounded-full"
                      style={{ backgroundColor: cat.color }}
                    />
                    {cat.name}
                  </span>
                  <span className="flex items-center gap-2">
                    <span className="text-xs text-muted-foreground">{cat.count} tools</span>
                    <ChevronRight className={cn(
                      "h-3.5 w-3.5 transition-transform",
                      activeCategory === i && "rotate-90"
                    )} />
                  </span>
                </button>
              ))}
            </div>
            <div className="bg-white rounded-xl border border-border p-6">
              <div className="flex items-center gap-2 mb-4">
                <span
                  className="h-3 w-3 rounded-full"
                  style={{ backgroundColor: TOOL_CATEGORIES[activeCategory].color }}
                />
                <h4 className="font-semibold text-foreground">
                  {TOOL_CATEGORIES[activeCategory].name}
                </h4>
                <span className="text-sm text-muted-foreground">
                  -- {TOOL_CATEGORIES[activeCategory].count} tools
                </span>
              </div>
              <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-2">
                {TOOL_CATEGORIES[activeCategory].tools.map((tool) => (
                  <div
                    key={tool}
                    className="flex items-center gap-2 px-3 py-2 rounded-lg bg-surface-raised text-sm text-foreground"
                  >
                    <span
                      className="h-1.5 w-1.5 rounded-full shrink-0"
                      style={{ backgroundColor: TOOL_CATEGORIES[activeCategory].color }}
                    />
                    {tool}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </AnimatedSection>

        {/* Segments */}
        <AnimatedSection id="segments">
          <div className="flex items-center gap-2 mb-6">
            <Grid3X3 className="h-5 w-5 text-primary" />
            <h3 className="text-xl font-semibold text-foreground">38 Borrower Segments</h3>
          </div>
          <div className="flex flex-wrap gap-2 mb-6">
            {Object.keys(SEGMENT_CATEGORIES).map((group) => (
              <button
                key={group}
                onClick={() => setActiveSegmentGroup(group)}
                className={cn(
                  "px-4 py-2 rounded-full text-sm font-medium transition-all cursor-pointer",
                  activeSegmentGroup === group
                    ? "bg-primary text-primary-foreground"
                    : "bg-white border border-border text-muted-foreground hover:text-foreground"
                )}
              >
                {group}
              </button>
            ))}
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3">
            {SEGMENT_CATEGORIES[activeSegmentGroup as keyof typeof SEGMENT_CATEGORIES].map((seg) => (
              <div
                key={seg.id}
                className="bg-white rounded-lg border border-border p-4 hover:shadow-md hover:border-primary/20 transition-all"
              >
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-lg">{seg.icon}</span>
                  <span className="font-medium text-foreground text-sm">{seg.name}</span>
                </div>
                <div className="space-y-1">
                  <div className="text-xs text-muted-foreground">
                    <span className="font-medium text-foreground">{seg.product}</span>
                  </div>
                  <div className="text-xs text-muted-foreground">
                    Ticket: {seg.ticket}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </AnimatedSection>
      </Container>
    </Section>
  );
}
