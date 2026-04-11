"use client";

import { useState, useMemo } from "react";
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import {
  Search,
  ChevronDown,
  ChevronUp,
  MessageSquare,
  Wrench,
  ShieldCheck,
  Cpu,
  Clock,
  Filter,
} from "lucide-react";

interface TraceStep {
  name: string;
  duration: string;
  detail?: string;
}

interface Conversation {
  id: string;
  segment: string;
  borrower: string;
  outcome: "Approved" | "Referred" | "Rejected";
  toolCount: number;
  latency: string;
  timestamp: string;
  trace: TraceStep[];
}

const CONVERSATIONS: Conversation[] = [
  {
    id: "CONV-9847",
    segment: "Dairy Farmer",
    borrower: "R***a K***r",
    outcome: "Approved",
    toolCount: 5,
    latency: "2.1s",
    timestamp: "2026-04-11 14:22",
    trace: [
      { name: "Message Received", duration: "—", detail: "Loan application for ₹1,50,000" },
      { name: "Prompt Build", duration: "45ms", detail: "dairy_farmer v1.3 + context injection" },
      { name: "LLM Call", duration: "820ms", detail: "GPT-4o — 1,247 tokens in / 389 tokens out" },
      { name: "Tool: aadhaar_ekyc", duration: "340ms", detail: "Identity verified ✓" },
      { name: "Tool: bank_account_aa", duration: "280ms", detail: "6-month statement fetched" },
      { name: "Tool: cooperative_data", duration: "190ms", detail: "Pouring records retrieved" },
      { name: "Tool: bureau_check", duration: "150ms", detail: "Score: 712" },
      { name: "Tool: compute_score", duration: "45ms", detail: "EmbeddedCredit score: 78/100" },
      { name: "Policy Check", duration: "28ms", detail: "All policies passed" },
      { name: "Response Generated", duration: "2.1s total", detail: "Loan approved — ₹1,50,000 @ 14.5% p.a." },
    ],
  },
  {
    id: "CONV-9846",
    segment: "Kirana Shop",
    borrower: "S***h P***l",
    outcome: "Approved",
    toolCount: 4,
    latency: "1.8s",
    timestamp: "2026-04-11 13:55",
    trace: [
      { name: "Message Received", duration: "—", detail: "Working capital loan ₹75,000" },
      { name: "Prompt Build", duration: "38ms", detail: "kirana_shop v1.2 + context injection" },
      { name: "LLM Call", duration: "790ms", detail: "GPT-4o — 1,102 tokens in / 312 tokens out" },
      { name: "Tool: pan_verify", duration: "220ms", detail: "PAN verified ✓" },
      { name: "Tool: gst_fetch", duration: "310ms", detail: "12-month GST returns fetched" },
      { name: "Tool: bank_account_aa", duration: "260ms", detail: "Transaction analysis complete" },
      { name: "Tool: compute_score", duration: "42ms", detail: "EmbeddedCredit score: 82/100" },
      { name: "Policy Check", duration: "25ms", detail: "All policies passed" },
      { name: "Response Generated", duration: "1.8s total", detail: "Loan approved — ₹75,000 @ 16% p.a." },
    ],
  },
  {
    id: "CONV-9845",
    segment: "Gig Worker",
    borrower: "A***d R***n",
    outcome: "Referred",
    toolCount: 4,
    latency: "2.4s",
    timestamp: "2026-04-11 12:30",
    trace: [
      { name: "Message Received", duration: "—", detail: "Personal loan ₹50,000" },
      { name: "Prompt Build", duration: "52ms", detail: "gig_worker v2.1 (staging) + context injection" },
      { name: "LLM Call", duration: "950ms", detail: "GPT-4o — 1,380 tokens in / 425 tokens out" },
      { name: "Tool: platform_data", duration: "480ms", detail: "Multi-platform income fetched (Swiggy, Uber)" },
      { name: "Tool: bank_account_aa", duration: "290ms", detail: "Irregular deposits flagged" },
      { name: "Tool: bureau_check", duration: "180ms", detail: "Score: 628 (below threshold)" },
      { name: "Tool: compute_score", duration: "48ms", detail: "EmbeddedCredit score: 52/100" },
      { name: "Policy Check", duration: "32ms", detail: "HUMAN_REVIEW triggered — score below 60" },
      { name: "Response Generated", duration: "2.4s total", detail: "Referred to human review" },
    ],
  },
  {
    id: "CONV-9844",
    segment: "Gold Loan",
    borrower: "M***a D***i",
    outcome: "Approved",
    toolCount: 3,
    latency: "1.2s",
    timestamp: "2026-04-11 11:45",
    trace: [
      { name: "Message Received", duration: "—", detail: "Gold loan ₹2,00,000" },
      { name: "Prompt Build", duration: "35ms", detail: "gold_loan v1.4 + context injection" },
      { name: "LLM Call", duration: "680ms", detail: "GPT-4o — 890 tokens in / 278 tokens out" },
      { name: "Tool: aadhaar_ekyc", duration: "310ms", detail: "Identity verified ✓" },
      { name: "Tool: gold_valuation", duration: "120ms", detail: "22K, 45g — ₹2,47,500 market value" },
      { name: "Tool: compute_score", duration: "38ms", detail: "EmbeddedCredit score: 91/100" },
      { name: "Policy Check", duration: "22ms", detail: "All policies passed (LTV 80.8%)" },
      { name: "Response Generated", duration: "1.2s total", detail: "Loan approved — ₹2,00,000 @ 12% p.a." },
    ],
  },
  {
    id: "CONV-9843",
    segment: "Street Vendor",
    borrower: "P***a B***i",
    outcome: "Approved",
    toolCount: 4,
    latency: "1.9s",
    timestamp: "2026-04-11 10:20",
    trace: [
      { name: "Message Received", duration: "—", detail: "Micro loan ₹25,000" },
      { name: "Prompt Build", duration: "40ms", detail: "street_vendor v1.1 + context injection" },
      { name: "LLM Call", duration: "810ms", detail: "GPT-4o — 1,050 tokens in / 320 tokens out" },
      { name: "Tool: aadhaar_ekyc", duration: "330ms", detail: "Identity verified ✓" },
      { name: "Tool: upi_activity", duration: "250ms", detail: "Daily UPI collections analyzed" },
      { name: "Tool: location_verify", duration: "180ms", detail: "Vendor location confirmed" },
      { name: "Tool: compute_score", duration: "40ms", detail: "EmbeddedCredit score: 71/100" },
      { name: "Policy Check", duration: "26ms", detail: "All policies passed" },
      { name: "Response Generated", duration: "1.9s total", detail: "Loan approved — ₹25,000 @ 18% p.a." },
    ],
  },
  {
    id: "CONV-9842",
    segment: "Truck Operator",
    borrower: "V***h S***a",
    outcome: "Rejected",
    toolCount: 3,
    latency: "1.5s",
    timestamp: "2026-04-11 09:10",
    trace: [
      { name: "Message Received", duration: "—", detail: "Vehicle repair loan ₹3,00,000" },
      { name: "Prompt Build", duration: "42ms", detail: "truck_operator v2.0 (staging) + context injection" },
      { name: "LLM Call", duration: "780ms", detail: "GPT-4o — 1,180 tokens in / 350 tokens out" },
      { name: "Tool: aadhaar_ekyc", duration: "320ms", detail: "Identity verified ✓" },
      { name: "Tool: vehicle_rc_check", duration: "210ms", detail: "RC expired — compliance flag" },
      { name: "Tool: bureau_check", duration: "160ms", detail: "Score: 540 (high risk)" },
      { name: "Policy Check", duration: "30ms", detail: "AUTO_REJECT — bureau < 550 + compliance flag" },
      { name: "Response Generated", duration: "1.5s total", detail: "Rejected — does not meet eligibility criteria" },
    ],
  },
  {
    id: "CONV-9841",
    segment: "SHG Member",
    borrower: "L***a N***r",
    outcome: "Approved",
    toolCount: 4,
    latency: "1.7s",
    timestamp: "2026-04-10 22:45",
    trace: [
      { name: "Message Received", duration: "—", detail: "Group loan ₹40,000" },
      { name: "Prompt Build", duration: "36ms", detail: "shg_member v1.2 + context injection" },
      { name: "LLM Call", duration: "750ms", detail: "GPT-4o — 980 tokens in / 290 tokens out" },
      { name: "Tool: shg_verify", duration: "280ms", detail: "SHG membership confirmed — 3 yrs" },
      { name: "Tool: group_repayment", duration: "200ms", detail: "Group repayment rate: 98%" },
      { name: "Tool: bank_account_aa", duration: "240ms", detail: "Regular savings pattern" },
      { name: "Tool: compute_score", duration: "38ms", detail: "EmbeddedCredit score: 85/100" },
      { name: "Policy Check", duration: "24ms", detail: "All policies passed" },
      { name: "Response Generated", duration: "1.7s total", detail: "Loan approved — ₹40,000 @ 15% p.a." },
    ],
  },
  {
    id: "CONV-9840",
    segment: "Cotton Farmer",
    borrower: "B***a T***e",
    outcome: "Approved",
    toolCount: 5,
    latency: "2.3s",
    timestamp: "2026-04-10 20:15",
    trace: [
      { name: "Message Received", duration: "—", detail: "Crop loan ₹1,00,000" },
      { name: "Prompt Build", duration: "44ms", detail: "cotton_farmer v1.3 + context injection" },
      { name: "LLM Call", duration: "840ms", detail: "GPT-4o — 1,200 tokens in / 380 tokens out" },
      { name: "Tool: aadhaar_ekyc", duration: "330ms", detail: "Identity verified ✓" },
      { name: "Tool: land_records", duration: "420ms", detail: "2.5 acres verified via state API" },
      { name: "Tool: mandi_prices", duration: "180ms", detail: "Current cotton prices fetched" },
      { name: "Tool: weather_data", duration: "150ms", detail: "Favorable forecast next season" },
      { name: "Tool: compute_score", duration: "42ms", detail: "EmbeddedCredit score: 76/100" },
      { name: "Policy Check", duration: "28ms", detail: "All policies passed" },
      { name: "Response Generated", duration: "2.3s total", detail: "Loan approved — ₹1,00,000 @ 13.5% p.a." },
    ],
  },
  {
    id: "CONV-9839",
    segment: "Cab Driver",
    borrower: "R***j M***a",
    outcome: "Referred",
    toolCount: 3,
    latency: "1.6s",
    timestamp: "2026-04-10 18:30",
    trace: [
      { name: "Message Received", duration: "—", detail: "Personal loan ₹60,000" },
      { name: "Prompt Build", duration: "39ms", detail: "cab_driver v1.1 + context injection" },
      { name: "LLM Call", duration: "770ms", detail: "GPT-4o — 1,050 tokens in / 310 tokens out" },
      { name: "Tool: platform_data", duration: "350ms", detail: "Ola/Uber trip data fetched" },
      { name: "Tool: bank_account_aa", duration: "270ms", detail: "Mixed deposit patterns" },
      { name: "Tool: compute_score", duration: "40ms", detail: "EmbeddedCredit score: 58/100" },
      { name: "Policy Check", duration: "30ms", detail: "HUMAN_REVIEW — borderline score" },
      { name: "Response Generated", duration: "1.6s total", detail: "Referred to human review" },
    ],
  },
  {
    id: "CONV-9838",
    segment: "Medical Shop",
    borrower: "D***h G***a",
    outcome: "Approved",
    toolCount: 4,
    latency: "1.4s",
    timestamp: "2026-04-10 16:00",
    trace: [
      { name: "Message Received", duration: "—", detail: "Inventory financing ₹1,20,000" },
      { name: "Prompt Build", duration: "37ms", detail: "medical_shop v1.0 + context injection" },
      { name: "LLM Call", duration: "710ms", detail: "GPT-4o — 1,020 tokens in / 298 tokens out" },
      { name: "Tool: drug_license_verify", duration: "200ms", detail: "License valid until 2028" },
      { name: "Tool: gst_fetch", duration: "290ms", detail: "Consistent GST filings" },
      { name: "Tool: bank_account_aa", duration: "250ms", detail: "Healthy cash flow" },
      { name: "Tool: compute_score", duration: "40ms", detail: "EmbeddedCredit score: 88/100" },
      { name: "Policy Check", duration: "24ms", detail: "All policies passed" },
      { name: "Response Generated", duration: "1.4s total", detail: "Loan approved — ₹1,20,000 @ 15.5% p.a." },
    ],
  },
];

const SEGMENTS = ["All", "Dairy Farmer", "Kirana Shop", "Gig Worker", "Street Vendor", "Gold Loan", "Truck Operator", "SHG Member", "Cotton Farmer", "Cab Driver", "Medical Shop"];
const OUTCOMES = ["All", "Approved", "Referred", "Rejected"];

const outcomeVariant: Record<string, "success" | "warning" | "danger"> = {
  Approved: "success",
  Referred: "warning",
  Rejected: "danger",
};

const traceStepIcon: Record<string, typeof MessageSquare> = {
  "Message Received": MessageSquare,
  "Prompt Build": Cpu,
  "LLM Call": Cpu,
  "Policy Check": ShieldCheck,
  "Response Generated": MessageSquare,
};

export function AgentTraces() {
  const [search, setSearch] = useState("");
  const [segmentFilter, setSegmentFilter] = useState("All");
  const [outcomeFilter, setOutcomeFilter] = useState("All");
  const [expandedId, setExpandedId] = useState<string | null>(null);

  const filtered = useMemo(() => {
    return CONVERSATIONS.filter((c) => {
      if (segmentFilter !== "All" && c.segment !== segmentFilter) return false;
      if (outcomeFilter !== "All" && c.outcome !== outcomeFilter) return false;
      if (search) {
        const q = search.toLowerCase();
        return c.id.toLowerCase().includes(q) || c.segment.toLowerCase().includes(q) || c.borrower.toLowerCase().includes(q);
      }
      return true;
    });
  }, [search, segmentFilter, outcomeFilter]);

  return (
    <div className="space-y-6">
      {/* Filters */}
      <div className="flex flex-wrap items-center gap-3">
        <div className="relative w-64">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <input
            type="text"
            placeholder="Search conversations..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="h-9 w-full rounded-lg border border-border bg-muted pl-9 pr-4 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring"
          />
        </div>
        <div className="flex items-center gap-2">
          <Filter className="h-4 w-4 text-muted-foreground" />
          <select
            value={segmentFilter}
            onChange={(e) => setSegmentFilter(e.target.value)}
            className="h-9 rounded-lg border border-border bg-muted px-3 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
          >
            {SEGMENTS.map((s) => (
              <option key={s} value={s}>{s}</option>
            ))}
          </select>
          <select
            value={outcomeFilter}
            onChange={(e) => setOutcomeFilter(e.target.value)}
            className="h-9 rounded-lg border border-border bg-muted px-3 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
          >
            {OUTCOMES.map((o) => (
              <option key={o} value={o}>{o}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Conversations List */}
      <Card padding="none">
        <div className="px-6 py-4 border-b border-border">
          <h3 className="text-sm font-semibold text-foreground">Recent Conversations ({filtered.length})</h3>
        </div>
        <div className="divide-y divide-border">
          {filtered.map((conv) => (
            <div key={conv.id}>
              <button
                onClick={() => setExpandedId(expandedId === conv.id ? null : conv.id)}
                className="flex w-full items-center gap-4 px-6 py-3 text-left hover:bg-muted/30 transition-colors"
              >
                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-2">
                    <code className="text-xs font-mono font-semibold text-foreground">{conv.id}</code>
                    <Badge variant={outcomeVariant[conv.outcome]}>{conv.outcome}</Badge>
                  </div>
                  <div className="flex items-center gap-3 mt-1 text-xs text-muted-foreground">
                    <span>{conv.segment}</span>
                    <span>·</span>
                    <span>{conv.borrower}</span>
                    <span>·</span>
                    <span>{conv.toolCount} tools</span>
                    <span>·</span>
                    <span>{conv.latency}</span>
                  </div>
                </div>
                <span className="text-xs text-muted-foreground whitespace-nowrap">{conv.timestamp}</span>
                {expandedId === conv.id ? (
                  <ChevronUp className="h-4 w-4 text-muted-foreground shrink-0" />
                ) : (
                  <ChevronDown className="h-4 w-4 text-muted-foreground shrink-0" />
                )}
              </button>
              {expandedId === conv.id && (
                <div className="px-6 pb-4">
                  <div className="rounded-lg border border-border bg-muted/30 p-4">
                    <p className="text-xs font-semibold text-muted-foreground mb-3">Execution Trace</p>
                    <div className="space-y-1">
                      {conv.trace.map((step, i) => {
                        const isToolCall = step.name.startsWith("Tool:");
                        const StepIcon = isToolCall
                          ? Wrench
                          : traceStepIcon[step.name] ?? Clock;
                        return (
                          <div key={i} className="flex items-start gap-3 py-1.5">
                            <div className="flex h-5 w-5 shrink-0 items-center justify-center rounded bg-muted">
                              <StepIcon className={cn("h-3 w-3", isToolCall ? "text-info" : "text-muted-foreground")} />
                            </div>
                            <div className="min-w-0 flex-1">
                              <div className="flex items-center justify-between">
                                <span className={cn(
                                  "text-xs font-medium",
                                  isToolCall ? "text-info" : "text-foreground"
                                )}>
                                  {step.name}
                                </span>
                                <span className="text-xs tabular-nums text-muted-foreground">{step.duration}</span>
                              </div>
                              {step.detail && (
                                <p className="text-xs text-muted-foreground mt-0.5">{step.detail}</p>
                              )}
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
