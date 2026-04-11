import { Navbar } from "@/components/layout/navbar";
import { Footer } from "@/components/layout/footer";
import { Hero } from "@/components/landing/hero";
import { Problem } from "@/components/landing/problem";
import { HowItWorks } from "@/components/landing/how-it-works";
import { PlatformDeepDive } from "@/components/landing/platform-deep-dive";
import { BorrowerJourneys } from "@/components/landing/borrower-journeys";
import { ProductionReliability } from "@/components/landing/production-reliability";
import { Metrics } from "@/components/landing/metrics";
import { Pricing } from "@/components/landing/pricing";
import { FinalCTA } from "@/components/landing/final-cta";

export default function Home() {
  return (
    <>
      <Navbar />
      <main>
        <Hero />
        <Problem />
        <HowItWorks />
        <PlatformDeepDive />
        <BorrowerJourneys />
        <ProductionReliability />
        <Metrics />
        <Pricing />
        <FinalCTA />
      </main>
      <Footer />
    </>
  );
}
