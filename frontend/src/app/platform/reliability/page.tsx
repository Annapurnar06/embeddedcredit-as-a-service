import type { Metadata } from "next";
import { Navbar } from "@/components/layout/navbar";
import { Footer } from "@/components/layout/footer";
import { AgentPipeline } from "@/components/reliability/agent-pipeline";
import { EvalFramework } from "@/components/reliability/eval-framework";
import { RedTeaming } from "@/components/reliability/red-teaming";
import { PromptLifecycle } from "@/components/reliability/prompt-lifecycle";
import { GuardrailStack } from "@/components/reliability/guardrail-stack";
import { Observability } from "@/components/reliability/observability";
import { HumanControls } from "@/components/reliability/human-controls";
import { ModelManagement } from "@/components/reliability/model-management";

export const metadata: Metadata = {
  title: "Production Reliability | EmbeddedCredit",
  description:
    "Deep-dive into EmbeddedCredit's agent lifecycle, evaluation framework, red-teaming, guardrail stack, observability, and human-in-the-loop controls. Built for NBFC CTOs and risk heads who need to trust AI lending.",
};

export default function ReliabilityPage() {
  return (
    <>
      <Navbar />
      <main className="pt-16">
        <AgentPipeline />
        <EvalFramework />
        <RedTeaming />
        <PromptLifecycle />
        <GuardrailStack />
        <Observability />
        <HumanControls />
        <ModelManagement />
      </main>
      <Footer />
    </>
  );
}
