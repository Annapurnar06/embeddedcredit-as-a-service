"use client";

import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import {
  X,
  BarChart3,
  Package,
  Pause,
  Activity,
  TrendingUp,
} from "lucide-react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";

interface SegmentDetailProps {
  segmentId: string;
  segmentName: string;
  product: string;
  ticket: string;
  onClose: () => void;
}

interface ScoringWeight {
  feature: string;
  weight: number;
}

const SEGMENT_SCORING: Record<string, ScoringWeight[]> = {
  dairy_farmer: [
    { feature: "Pouring Regularity", weight: 25 },
    { feature: "Fat Content Consistency", weight: 15 },
    { feature: "Cooperative Tenure", weight: 20 },
    { feature: "Bank Balance Trend", weight: 15 },
    { feature: "Credit Bureau", weight: 10 },
    { feature: "Herd Size", weight: 15 },
  ],
  kirana_shop: [
    { feature: "GST Trend", weight: 30 },
    { feature: "Bank Regularity", weight: 25 },
    { feature: "UPI Inflow", weight: 15 },
    { feature: "Shop Vintage", weight: 10 },
    { feature: "Credit Bureau", weight: 10 },
    { feature: "Inventory Turnover", weight: 10 },
  ],
  gig_worker: [
    { feature: "Platform Earnings", weight: 30 },
    { feature: "Rating Score", weight: 15 },
    { feature: "Active Days", weight: 15 },
    { feature: "Bank Balance", weight: 15 },
    { feature: "Credit Bureau", weight: 10 },
    { feature: "Device Score", weight: 15 },
  ],
  gold_loan: [
    { feature: "Gold Purity", weight: 30 },
    { feature: "Gold Weight", weight: 25 },
    { feature: "Market Price", weight: 15 },
    { feature: "LTV Ratio", weight: 15 },
    { feature: "Credit Bureau", weight: 10 },
    { feature: "Repayment History", weight: 5 },
  ],
  cab_driver: [
    { feature: "Daily Trips", weight: 25 },
    { feature: "Platform Rating", weight: 15 },
    { feature: "Vehicle Age", weight: 10 },
    { feature: "Earnings Stability", weight: 20 },
    { feature: "Credit Bureau", weight: 10 },
    { feature: "Bank Balance", weight: 20 },
  ],
  street_vendor: [
    { feature: "UPI Collections", weight: 30 },
    { feature: "Location Stability", weight: 15 },
    { feature: "Market Vintage", weight: 15 },
    { feature: "Bank Deposit Pattern", weight: 20 },
    { feature: "Credit Bureau", weight: 10 },
    { feature: "Municipal License", weight: 10 },
  ],
};

function getGenericWeights(): ScoringWeight[] {
  return [
    { feature: "Primary Data Source", weight: 25 },
    { feature: "Bank Regularity", weight: 20 },
    { feature: "Income Stability", weight: 20 },
    { feature: "Credit Bureau", weight: 15 },
    { feature: "Vintage/Tenure", weight: 10 },
    { feature: "Behavioral Score", weight: 10 },
  ];
}

interface SegmentConfig {
  tenure: string;
  insurance: string;
  schedule: string;
  moratorium: { condition: string; duration: string }[];
  monitoring: { cadence: string; signals: string[]; triggers: string[] };
  graduation: {
    minMonths: number;
    onTimeRate: string;
    amountMultiplier: string;
  };
}

const SEGMENT_CONFIGS: Record<string, SegmentConfig> = {
  dairy_farmer: {
    tenure: "6-18 months",
    insurance: "Cattle mortality cover bundled",
    schedule: "Seasonal Dynamic EMI (flush/lean adjustment)",
    moratorium: [
      { condition: "Cattle disease outbreak in district", duration: "2 months" },
      { condition: "Temperature > 42°C for 7+ days", duration: "1 month" },
      { condition: "Flood alert in taluka", duration: "1 month" },
    ],
    monitoring: {
      cadence: "Weekly",
      signals: [
        "Dairy cooperative pouring data",
        "Bank account inflows",
        "Milk price index",
        "Weather data",
      ],
      triggers: [
        "Pouring regularity drops below 70%",
        "Bank balance below ₹5,000 for 7 days",
        "Fat content drops below 4%",
      ],
    },
    graduation: {
      minMonths: 12,
      onTimeRate: "90%",
      amountMultiplier: "1.5x",
    },
  },
  kirana_shop: {
    tenure: "6-24 months",
    insurance: "Shop fire/theft cover optional",
    schedule: "Daily Micro Collection (26 days/month)",
    moratorium: [
      { condition: "Festival shutdown > 5 days", duration: "15 days" },
      { condition: "Road construction blocking access", duration: "1 month" },
    ],
    monitoring: {
      cadence: "Daily",
      signals: [
        "UPI collection volume",
        "GST filing status",
        "Bank deposit pattern",
        "Device activity",
      ],
      triggers: [
        "Daily UPI volume drops 50% for 3 days",
        "GST filing missed",
        "No bank deposit for 5 days",
      ],
    },
    graduation: {
      minMonths: 6,
      onTimeRate: "85%",
      amountMultiplier: "2x",
    },
  },
  gig_worker: {
    tenure: "3-12 months",
    insurance: "Accident cover bundled",
    schedule: "Payout-Linked (15% auto-deducted)",
    moratorium: [
      { condition: "Hospitalization > 3 days", duration: "1 month" },
      { condition: "Vehicle breakdown (verified)", duration: "15 days" },
    ],
    monitoring: {
      cadence: "Per-payout",
      signals: [
        "Platform payout data",
        "Trip count",
        "Rating changes",
        "Active days per week",
      ],
      triggers: [
        "Earnings drop 40% week-on-week",
        "Rating drops below 4.0",
        "Active days < 3/week for 2 weeks",
      ],
    },
    graduation: {
      minMonths: 6,
      onTimeRate: "80%",
      amountMultiplier: "1.5x",
    },
  },
  gold_loan: {
    tenure: "3-12 months",
    insurance: "Gold safe custody included",
    schedule: "Bullet/EMI (interest monthly, principal at end)",
    moratorium: [
      { condition: "Gold price drops > 10% in 30 days", duration: "1 month" },
    ],
    monitoring: {
      cadence: "Daily",
      signals: [
        "Gold spot price",
        "LTV ratio",
        "Interest payment status",
        "Auction calendar",
      ],
      triggers: [
        "LTV exceeds 75%",
        "Interest overdue > 30 days",
        "Gold price below pledge threshold",
      ],
    },
    graduation: {
      minMonths: 6,
      onTimeRate: "95%",
      amountMultiplier: "1.3x",
    },
  },
  cab_driver: {
    tenure: "12-48 months",
    insurance: "Comprehensive vehicle cover bundled",
    schedule: "Vehicle Finance PV (daily/weekly EMI)",
    moratorium: [
      { condition: "Vehicle in accident (FIR filed)", duration: "1 month" },
      { condition: "City-wide lockdown > 7 days", duration: "1 month" },
    ],
    monitoring: {
      cadence: "Weekly",
      signals: [
        "Platform trip data",
        "Earnings trend",
        "Vehicle telematics",
        "Insurance status",
      ],
      triggers: [
        "Weekly trips drop below 30",
        "Earnings below ₹12,000/week",
        "Insurance lapsed",
      ],
    },
    graduation: {
      minMonths: 12,
      onTimeRate: "90%",
      amountMultiplier: "1.5x",
    },
  },
  street_vendor: {
    tenure: "6-12 months",
    insurance: "PM SVANidhi linked",
    schedule: "PM SVANidhi Plus (weekly collection)",
    moratorium: [
      { condition: "Municipal eviction notice", duration: "1 month" },
      { condition: "Monsoon disruption > 10 days", duration: "15 days" },
    ],
    monitoring: {
      cadence: "Weekly",
      signals: [
        "UPI collection data",
        "Location check-in",
        "Bank deposit pattern",
        "Municipal license status",
      ],
      triggers: [
        "UPI collections zero for 5 days",
        "No location check-in for 7 days",
        "Bank balance below ₹1,000",
      ],
    },
    graduation: {
      minMonths: 6,
      onTimeRate: "80%",
      amountMultiplier: "2x",
    },
  },
};

function getGenericConfig(product: string, _ticket: string): SegmentConfig {
  return {
    tenure: "6-24 months",
    insurance: "Optional credit-linked insurance",
    schedule: `${product} (standard schedule)`,
    moratorium: [
      { condition: "Natural calamity in district", duration: "1-2 months" },
      { condition: "Medical emergency (documented)", duration: "1 month" },
    ],
    monitoring: {
      cadence: "Monthly",
      signals: [
        "Bank account activity",
        "Credit bureau updates",
        "Primary income signals",
        "Behavioral indicators",
      ],
      triggers: [
        "Income drops 30% for 2 months",
        "EMI bounce 2 consecutive months",
        "Credit bureau score drops > 50 points",
      ],
    },
    graduation: {
      minMonths: 12,
      onTimeRate: "85%",
      amountMultiplier: "1.5x",
    },
  };
}

const BAR_COLORS = [
  "#2563eb",
  "#7c3aed",
  "#0891b2",
  "#16a34a",
  "#d97706",
  "#dc2626",
];

export function SegmentDetail({
  segmentId,
  segmentName,
  product,
  ticket,
  onClose,
}: SegmentDetailProps) {
  const weights = SEGMENT_SCORING[segmentId] ?? getGenericWeights();
  const config =
    SEGMENT_CONFIGS[segmentId] ?? getGenericConfig(product, ticket);

  return (
    <div className="mt-4 rounded-xl border border-primary/20 bg-surface p-6 space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <h3 className="text-lg font-semibold text-foreground">
            {segmentName} — Configuration
          </h3>
          <p className="text-sm text-muted-foreground mt-1">
            Segment-specific scoring, product design, and monitoring rules
          </p>
        </div>
        <button
          onClick={onClose}
          className="rounded-lg p-2 text-muted-foreground hover:bg-muted hover:text-foreground transition-colors"
        >
          <X className="h-5 w-5" />
        </button>
      </div>

      {/* Scoring Weights */}
      <section>
        <div className="flex items-center gap-2 mb-3">
          <BarChart3 className="h-4 w-4 text-primary" />
          <h4 className="text-sm font-semibold text-foreground uppercase tracking-wider">
            Scoring Weights
          </h4>
        </div>
        <Card padding="sm" className="bg-muted/30">
          <div className="h-56">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={weights}
                layout="vertical"
                margin={{ top: 4, right: 30, left: 10, bottom: 4 }}
              >
                <XAxis
                  type="number"
                  domain={[0, 35]}
                  tickFormatter={(v: number) => `${v}%`}
                  tick={{ fontSize: 11 }}
                />
                <YAxis
                  type="category"
                  dataKey="feature"
                  width={140}
                  tick={{ fontSize: 11 }}
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
                <Bar dataKey="weight" radius={[0, 4, 4, 0]}>
                  {weights.map((_, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={BAR_COLORS[index % BAR_COLORS.length]}
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </section>

      {/* Product Configuration */}
      <section>
        <div className="flex items-center gap-2 mb-3">
          <Package className="h-4 w-4 text-primary" />
          <h4 className="text-sm font-semibold text-foreground uppercase tracking-wider">
            Product Configuration
          </h4>
        </div>
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
          {[
            { label: "Product Type", value: product },
            { label: "Amount Range", value: `₹${ticket}` },
            { label: "Tenure", value: config.tenure },
            { label: "Insurance", value: config.insurance },
          ].map((item) => (
            <Card key={item.label} padding="sm" className="bg-muted/30">
              <p className="text-xs text-muted-foreground mb-1">{item.label}</p>
              <p className="text-sm font-medium text-foreground">
                {item.value}
              </p>
            </Card>
          ))}
        </div>
        <div className="mt-3">
          <Card padding="sm" className="bg-muted/30">
            <p className="text-xs text-muted-foreground mb-1">
              Schedule Template
            </p>
            <p className="text-sm font-medium text-foreground">
              {config.schedule}
            </p>
          </Card>
        </div>
      </section>

      {/* Moratorium Triggers */}
      <section>
        <div className="flex items-center gap-2 mb-3">
          <Pause className="h-4 w-4 text-warning" />
          <h4 className="text-sm font-semibold text-foreground uppercase tracking-wider">
            Moratorium Triggers
          </h4>
        </div>
        <div className="space-y-2">
          {config.moratorium.map((m, i) => (
            <Card key={i} padding="sm" className="bg-muted/30">
              <div className="flex items-center justify-between gap-4">
                <p className="text-sm text-foreground">{m.condition}</p>
                <Badge variant="warning" className="shrink-0">
                  → {m.duration}
                </Badge>
              </div>
            </Card>
          ))}
        </div>
      </section>

      {/* Monitoring */}
      <section>
        <div className="flex items-center gap-2 mb-3">
          <Activity className="h-4 w-4 text-info" />
          <h4 className="text-sm font-semibold text-foreground uppercase tracking-wider">
            Monitoring
          </h4>
        </div>
        <Card padding="sm" className="bg-muted/30 space-y-4">
          <div>
            <p className="text-xs text-muted-foreground mb-1">Cadence</p>
            <Badge variant="info">{config.monitoring.cadence}</Badge>
          </div>
          <div>
            <p className="text-xs text-muted-foreground mb-2">Signals</p>
            <div className="flex flex-wrap gap-1.5">
              {config.monitoring.signals.map((s) => (
                <Badge key={s} variant="outline">
                  {s}
                </Badge>
              ))}
            </div>
          </div>
          <div>
            <p className="text-xs text-muted-foreground mb-2">
              Trigger Conditions
            </p>
            <ul className="space-y-1.5">
              {config.monitoring.triggers.map((t) => (
                <li
                  key={t}
                  className="flex items-start gap-2 text-sm text-foreground"
                >
                  <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-danger" />
                  {t}
                </li>
              ))}
            </ul>
          </div>
        </Card>
      </section>

      {/* Graduation Criteria */}
      <section>
        <div className="flex items-center gap-2 mb-3">
          <TrendingUp className="h-4 w-4 text-success" />
          <h4 className="text-sm font-semibold text-foreground uppercase tracking-wider">
            Graduation Criteria
          </h4>
        </div>
        <div className="grid grid-cols-3 gap-3">
          <Card padding="sm" className="bg-muted/30 text-center">
            <p className="text-xs text-muted-foreground mb-1">Min Months</p>
            <p className="text-xl font-bold text-foreground">
              {config.graduation.minMonths}
            </p>
          </Card>
          <Card padding="sm" className="bg-muted/30 text-center">
            <p className="text-xs text-muted-foreground mb-1">On-Time Rate</p>
            <p className="text-xl font-bold text-success">
              {config.graduation.onTimeRate}
            </p>
          </Card>
          <Card padding="sm" className="bg-muted/30 text-center">
            <p className="text-xs text-muted-foreground mb-1">
              Amount Multiplier
            </p>
            <p className="text-xl font-bold text-primary">
              {config.graduation.amountMultiplier}
            </p>
          </Card>
        </div>
      </section>
    </div>
  );
}
