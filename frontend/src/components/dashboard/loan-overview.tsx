"use client";

import { useMemo } from "react";
import type { LoanApplication } from "@/lib/mock-data";
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import {
  CheckCircle2,
  Clock,
  Phone,
  Globe,
  User,
  CreditCard,
  Landmark,
  ShieldCheck,
} from "lucide-react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

interface LoanOverviewProps {
  loan: LoanApplication;
}

const IDENTITY_ITEMS = [
  { label: "Aadhaar eKYC", tool: "aadhaar_ekyc" },
  { label: "PAN Verification", tool: "pan_verify" },
  { label: "Bank Account (AA)", tool: "bank_account_aa" },
];

const SCORE_FEATURES: Record<string, { name: string; weight: number }[]> = {
  dairy_farmer: [
    { name: "Pouring Regularity", weight: 25 },
    { name: "Bank Stability", weight: 20 },
    { name: "Bureau Score", weight: 15 },
    { name: "Cooperative Tenure", weight: 15 },
    { name: "Seasonal Resilience", weight: 10 },
    { name: "Asset Ownership", weight: 10 },
    { name: "Digital Footprint", weight: 5 },
  ],
  kirana_shop: [
    { name: "GST Consistency", weight: 25 },
    { name: "Bank Txn Volume", weight: 20 },
    { name: "Bureau Score", weight: 15 },
    { name: "Shop Tenure", weight: 15 },
    { name: "Inventory Turnover", weight: 10 },
    { name: "UPI Activity", weight: 10 },
    { name: "Locality Score", weight: 5 },
  ],
  gig_worker: [
    { name: "Earnings Stability", weight: 25 },
    { name: "Platform Rating", weight: 20 },
    { name: "Bureau Score", weight: 15 },
    { name: "Trip Frequency", weight: 15 },
    { name: "Payout Regularity", weight: 10 },
    { name: "Digital Presence", weight: 10 },
    { name: "Location Consistency", weight: 5 },
  ],
  gold_loan: [
    { name: "Gold Purity", weight: 25 },
    { name: "LTV Ratio", weight: 20 },
    { name: "Bureau Score", weight: 15 },
    { name: "Repayment History", weight: 15 },
    { name: "Pledged Value", weight: 10 },
    { name: "Customer Tenure", weight: 10 },
    { name: "Documentation", weight: 5 },
  ],
};

const DEFAULT_FEATURES = [
  { name: "Income Stability", weight: 25 },
  { name: "Bank Stability", weight: 20 },
  { name: "Bureau Score", weight: 15 },
  { name: "Business Tenure", weight: 15 },
  { name: "Asset Ownership", weight: 10 },
  { name: "Digital Footprint", weight: 10 },
  { name: "Locality Score", weight: 5 },
];

function maskPhone(phone: string): string {
  if (phone.length < 6) return phone;
  return phone.slice(0, phone.length - 4).replace(/\d/g, "•") + phone.slice(-4);
}

export function LoanOverview({ loan }: LoanOverviewProps) {
  const toolMap = useMemo(() => {
    const map = new Map<string, string>();
    loan.toolCalls.forEach((tc) => map.set(tc.tool, tc.status));
    return map;
  }, [loan.toolCalls]);

  const dataSources = useMemo(() => {
    return Array.from(new Set(loan.toolCalls.map((tc) => tc.tool)));
  }, [loan.toolCalls]);

  const scoreFeatures = SCORE_FEATURES[loan.segmentId] ?? DEFAULT_FEATURES;

  return (
    <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
      {/* Borrower Profile */}
      <Card padding="md">
        <h3 className="mb-4 text-sm font-semibold uppercase tracking-wider text-muted-foreground">
          Borrower Profile
        </h3>
        <div className="space-y-3">
          <div className="flex items-center gap-3">
            <User className="h-4 w-4 text-muted-foreground" />
            <span className="text-sm text-muted-foreground">Name</span>
            <span className="ml-auto text-sm font-medium text-foreground">
              {loan.borrowerName}
            </span>
          </div>
          <div className="flex items-center gap-3">
            <Phone className="h-4 w-4 text-muted-foreground" />
            <span className="text-sm text-muted-foreground">Phone</span>
            <span className="ml-auto font-mono text-sm text-foreground">
              {maskPhone(loan.phone)}
            </span>
          </div>
          <div className="flex items-center gap-3">
            <Globe className="h-4 w-4 text-muted-foreground" />
            <span className="text-sm text-muted-foreground">Language</span>
            <span className="ml-auto text-sm font-medium text-foreground uppercase">
              {loan.language}
            </span>
          </div>
          <div className="flex items-center gap-3">
            <Landmark className="h-4 w-4 text-muted-foreground" />
            <span className="text-sm text-muted-foreground">Segment</span>
            <Badge variant="outline" className="ml-auto">
              {loan.segment}
            </Badge>
          </div>
          <div className="flex items-center gap-3">
            <CreditCard className="h-4 w-4 text-muted-foreground" />
            <span className="text-sm text-muted-foreground">Product</span>
            <span className="ml-auto text-sm font-medium text-foreground">
              {loan.product}
            </span>
          </div>
        </div>
      </Card>

      {/* Identity Verification */}
      <Card padding="md">
        <h3 className="mb-4 text-sm font-semibold uppercase tracking-wider text-muted-foreground">
          Identity Verification
        </h3>
        <div className="space-y-3">
          {IDENTITY_ITEMS.map((item) => {
            const status = toolMap.get(item.tool);
            const verified = status === "SUCCESS";
            return (
              <div
                key={item.tool}
                className="flex items-center justify-between rounded-lg border border-border px-4 py-3"
              >
                <div className="flex items-center gap-3">
                  <ShieldCheck
                    className={cn(
                      "h-4 w-4",
                      verified ? "text-success" : "text-warning"
                    )}
                  />
                  <span className="text-sm font-medium text-foreground">
                    {item.label}
                  </span>
                </div>
                {verified ? (
                  <div className="flex items-center gap-1.5">
                    <CheckCircle2 className="h-4 w-4 text-success" />
                    <span className="text-xs font-medium text-success">
                      Verified
                    </span>
                  </div>
                ) : (
                  <div className="flex items-center gap-1.5">
                    <Clock className="h-4 w-4 text-warning" />
                    <span className="text-xs font-medium text-warning">
                      Pending
                    </span>
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* Data Sources */}
        <h3 className="mb-3 mt-6 text-sm font-semibold uppercase tracking-wider text-muted-foreground">
          Data Sources Collected
        </h3>
        <div className="flex flex-wrap gap-2">
          {dataSources.map((source) => (
            <Badge key={source} variant="default" className="font-mono text-xs">
              {source}
            </Badge>
          ))}
        </div>
      </Card>

      {/* Score Breakdown */}
      <Card padding="md" className="lg:col-span-1">
        <h3 className="mb-4 text-sm font-semibold uppercase tracking-wider text-muted-foreground">
          Score Breakdown
        </h3>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={scoreFeatures}
              layout="vertical"
              margin={{ top: 0, right: 20, left: 0, bottom: 0 }}
            >
              <XAxis
                type="number"
                domain={[0, 30]}
                tickFormatter={(v: number) => `${v}%`}
                tick={{ fontSize: 11, fill: "var(--color-muted-foreground)" }}
              />
              <YAxis
                type="category"
                dataKey="name"
                width={130}
                tick={{ fontSize: 11, fill: "var(--color-foreground)" }}
              />
              <Tooltip
                formatter={(value) => [`${value}%`, "Weight"]}
                contentStyle={{
                  backgroundColor: "var(--color-surface)",
                  border: "1px solid var(--color-border)",
                  borderRadius: "8px",
                  fontSize: "12px",
                }}
              />
              <Bar
                dataKey="weight"
                fill="var(--color-primary)"
                radius={[0, 4, 4, 0]}
                barSize={18}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </Card>

      {/* Product Terms */}
      <Card padding="md">
        <h3 className="mb-4 text-sm font-semibold uppercase tracking-wider text-muted-foreground">
          Product Terms
        </h3>
        <div className="space-y-3">
          <div className="flex items-center justify-between border-b border-border pb-2">
            <span className="text-sm text-muted-foreground">Product Type</span>
            <span className="text-sm font-medium text-foreground">
              {loan.product}
            </span>
          </div>
          <div className="flex items-center justify-between border-b border-border pb-2">
            <span className="text-sm text-muted-foreground">Amount</span>
            <span className="text-sm font-medium text-foreground">
              ₹{loan.amount.toLocaleString("en-IN")}
            </span>
          </div>
          <div className="flex items-center justify-between border-b border-border pb-2">
            <span className="text-sm text-muted-foreground">Tenure</span>
            <span className="text-sm font-medium text-foreground">
              {loan.schedule.length} months
            </span>
          </div>
          <div className="flex items-center justify-between border-b border-border pb-2">
            <span className="text-sm text-muted-foreground">
              Insurance Required
            </span>
            <Badge variant="info" className="text-xs">
              Yes
            </Badge>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm text-muted-foreground">Schedule Type</span>
            <span className="text-sm font-medium text-foreground">
              Seasonal Dynamic
            </span>
          </div>
        </div>
      </Card>
    </div>
  );
}
