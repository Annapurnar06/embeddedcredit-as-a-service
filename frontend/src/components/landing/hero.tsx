"use client";

import { motion } from "framer-motion";
import { ArrowRight, Play } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Container } from "@/components/ui/container";

export function Hero() {
  return (
    <section className="relative pt-32 pb-20 lg:pt-40 lg:pb-32 overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-b from-primary-light/30 to-transparent" />
      <div className="absolute top-20 left-1/4 w-96 h-96 bg-primary/5 rounded-full blur-3xl" />
      <div className="absolute bottom-0 right-1/4 w-72 h-72 bg-accent/5 rounded-full blur-3xl" />

      <Container className="relative">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center max-w-4xl mx-auto"
        >
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.1 }}
            className="inline-flex items-center gap-2 px-4 py-1.5 bg-primary-light text-primary text-sm font-medium rounded-full mb-6"
          >
            <span className="relative flex h-2 w-2">
              <span className="absolute inline-flex h-full w-full rounded-full bg-primary opacity-75 animate-ping" />
              <span className="relative inline-flex h-2 w-2 rounded-full bg-primary" />
            </span>
            AI-Native Lending Infrastructure
          </motion.div>

          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight text-foreground leading-tight">
            Embedded Credit{" "}
            <span className="text-primary">as a Service</span>
          </h1>

          <p className="mt-6 text-lg lg:text-xl text-muted-foreground max-w-2xl mx-auto leading-relaxed">
            The AI lending operating system for India&apos;s{" "}
            <span className="font-semibold text-foreground">300 million underserved borrowers</span>.
            From WhatsApp conversation to disbursement in 15 minutes.
          </p>

          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-3"
          >
            <Button size="xl">
              Request Demo
              <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
            <Button variant="outline" size="xl">
              <Play className="mr-2 h-4 w-4" />
              See Platform
            </Button>
          </motion.div>

          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
            className="mt-12 flex flex-wrap items-center justify-center gap-x-8 gap-y-3 text-sm text-muted-foreground"
          >
            <span className="flex items-center gap-1.5">
              <span className="h-1.5 w-1.5 rounded-full bg-success" />
              80-90% cost reduction
            </span>
            <span className="flex items-center gap-1.5">
              <span className="h-1.5 w-1.5 rounded-full bg-success" />
              RBI compliant
            </span>
            <span className="flex items-center gap-1.5">
              <span className="h-1.5 w-1.5 rounded-full bg-success" />
              15-min disbursement
            </span>
            <span className="flex items-center gap-1.5">
              <span className="h-1.5 w-1.5 rounded-full bg-success" />
              WhatsApp-native
            </span>
          </motion.div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6, duration: 0.8 }}
          className="mt-16 mx-auto max-w-5xl"
        >
          <div className="relative rounded-2xl border border-border bg-white shadow-xl overflow-hidden">
            <div className="flex items-center gap-1.5 px-4 py-3 bg-surface-raised border-b border-border">
              <div className="h-3 w-3 rounded-full bg-danger/60" />
              <div className="h-3 w-3 rounded-full bg-warning/60" />
              <div className="h-3 w-3 rounded-full bg-success/60" />
              <span className="ml-3 text-xs text-muted-foreground font-mono">platform.embeddedcredit.in</span>
            </div>
            <div className="p-8 bg-gradient-to-br from-surface-raised to-white">
              <div className="grid grid-cols-7 gap-2 text-center text-xs">
                {["Identity", "Data", "Scoring", "Product", "Execution", "Servicing", "Monitoring"].map((layer, i) => (
                  <div key={layer} className="space-y-2">
                    <div className={`h-12 rounded-lg flex items-center justify-center text-white font-medium ${
                      ["bg-blue-600", "bg-violet-600", "bg-cyan-600", "bg-green-600", "bg-amber-600", "bg-red-600", "bg-slate-600"][i]
                    }`}>
                      {layer}
                    </div>
                    <div className="text-muted-foreground">
                      {[6, 24, 8, 5, 6, 6, 5][i]} tools
                    </div>
                  </div>
                ))}
              </div>
              <div className="mt-4 text-center">
                <div className="inline-flex items-center gap-3 px-4 py-2 bg-primary-light rounded-lg text-sm text-primary font-medium">
                  <span>38 Segments</span>
                  <span className="h-1 w-1 rounded-full bg-primary/40" />
                  <span>60 Tools</span>
                  <span className="h-1 w-1 rounded-full bg-primary/40" />
                  <span>17 Policy Rules</span>
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      </Container>
    </section>
  );
}
