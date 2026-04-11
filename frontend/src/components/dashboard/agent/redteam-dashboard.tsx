"use client";

import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import {
  ShieldAlert,
  ShieldCheck,
  UserX,
  KeyRound,
  Bug,
  Lock,
} from "lucide-react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const ATTACK_CATEGORIES = [
  { name: "Prompt Injection", count: 12, icon: Bug, color: "text-danger" },
  { name: "Social Engineering", count: 8, icon: UserX, color: "text-warning" },
  { name: "PII Extraction", count: 15, icon: KeyRound, color: "text-danger" },
  { name: "Authority Escalation", count: 7, icon: ShieldAlert, color: "text-warning" },
  { name: "Jailbreak", count: 5, icon: Lock, color: "text-info" },
];

const RECENT_ATTACKS = [
  { id: 1, timestamp: "2026-04-11 14:32", category: "PII Extraction", summary: "Attempted to extract Aadhaar number via conversational context window overflow...", rule: "PII_GUARD_001", outcome: "BLOCKED" },
  { id: 2, timestamp: "2026-04-11 13:18", category: "Prompt Injection", summary: "Injected system prompt override via borrower name field with base64 encoding...", rule: "INJECT_DETECT_003", outcome: "BLOCKED" },
  { id: 3, timestamp: "2026-04-11 11:45", category: "Social Engineering", summary: "Impersonated loan officer requesting internal scoring parameters disclosure...", rule: "ROLE_VERIFY_002", outcome: "BLOCKED" },
  { id: 4, timestamp: "2026-04-11 10:22", category: "Jailbreak", summary: "Multi-turn jailbreak attempt using roleplay scenario to bypass lending policy...", rule: "JAILBREAK_DETECT_001", outcome: "BLOCKED" },
  { id: 5, timestamp: "2026-04-10 22:15", category: "Authority Escalation", summary: "Attempted to invoke admin-level tool calls through crafted conversation flow...", rule: "AUTH_GUARD_001", outcome: "BLOCKED" },
  { id: 6, timestamp: "2026-04-10 19:40", category: "PII Extraction", summary: "Used indirect questioning to attempt reconstruction of borrower bank details...", rule: "PII_GUARD_002", outcome: "BLOCKED" },
  { id: 7, timestamp: "2026-04-10 16:55", category: "Prompt Injection", summary: "Embedded instruction override in loan purpose description field using markdown...", rule: "INJECT_DETECT_001", outcome: "BLOCKED" },
  { id: 8, timestamp: "2026-04-10 14:30", category: "Social Engineering", summary: "Simulated urgency scenario claiming regulatory deadline to bypass verification...", rule: "SOCIAL_DETECT_003", outcome: "BLOCKED" },
];

const RULE_EFFECTIVENESS = [
  { rule: "PII_GUARD_001", triggers: 15, label: "PII Guard" },
  { rule: "INJECT_DETECT_003", triggers: 12, label: "Injection Detect" },
  { rule: "SOCIAL_DETECT_003", triggers: 8, label: "Social Engineering" },
  { rule: "AUTH_GUARD_001", triggers: 7, label: "Auth Guard" },
  { rule: "JAILBREAK_DETECT_001", triggers: 5, label: "Jailbreak Detect" },
];

const categoryVariant: Record<string, "danger" | "warning" | "info" | "primary"> = {
  "Prompt Injection": "danger",
  "Social Engineering": "warning",
  "PII Extraction": "danger",
  "Authority Escalation": "warning",
  "Jailbreak": "info",
};

export function RedTeamDashboard() {
  const totalAttacks = ATTACK_CATEGORIES.reduce((sum, c) => sum + c.count, 0);

  return (
    <div className="space-y-6">
      {/* Summary Stats */}
      <div className="grid grid-cols-3 gap-4">
        <Card padding="sm" className="text-center">
          <p className="text-2xl font-bold text-foreground">{totalAttacks}</p>
          <p className="text-xs text-muted-foreground">Total Attacks</p>
        </Card>
        <Card padding="sm" className="text-center">
          <p className="text-2xl font-bold text-success">0</p>
          <p className="text-xs text-muted-foreground">Successful</p>
        </Card>
        <Card padding="sm" className="text-center">
          <p className="text-2xl font-bold text-success">100%</p>
          <p className="text-xs text-muted-foreground">Block Rate</p>
        </Card>
      </div>

      {/* Attack Category Cards */}
      <div className="grid grid-cols-2 gap-4 lg:grid-cols-5">
        {ATTACK_CATEGORIES.map((cat) => {
          const Icon = cat.icon;
          return (
            <Card key={cat.name} padding="sm">
              <div className="flex items-center gap-2 mb-2">
                <Icon className={cn("h-4 w-4", cat.color)} />
                <span className="text-xs font-medium text-foreground">{cat.name}</span>
              </div>
              <div className="flex items-baseline gap-1">
                <span className="text-xl font-bold text-foreground">{cat.count}</span>
                <span className="text-xs text-muted-foreground">blocked</span>
              </div>
            </Card>
          );
        })}
      </div>

      {/* Recent Attacks Log */}
      <Card padding="none">
        <div className="px-6 py-4 border-b border-border flex items-center gap-2">
          <ShieldCheck className="h-4 w-4 text-success" />
          <h3 className="text-sm font-semibold text-foreground">Recent Attacks Log</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-border bg-muted/50">
                <th className="px-6 py-3 text-left font-medium text-muted-foreground">Timestamp</th>
                <th className="px-4 py-3 text-left font-medium text-muted-foreground">Category</th>
                <th className="px-4 py-3 text-left font-medium text-muted-foreground">Attack Summary</th>
                <th className="px-4 py-3 text-left font-medium text-muted-foreground">Rule</th>
                <th className="px-4 py-3 text-center font-medium text-muted-foreground">Outcome</th>
              </tr>
            </thead>
            <tbody>
              {RECENT_ATTACKS.map((attack) => (
                <tr key={attack.id} className="border-b border-border last:border-0 hover:bg-muted/30 transition-colors">
                  <td className="px-6 py-3 text-xs tabular-nums text-muted-foreground whitespace-nowrap">{attack.timestamp}</td>
                  <td className="px-4 py-3">
                    <Badge variant={categoryVariant[attack.category] ?? "default"}>{attack.category}</Badge>
                  </td>
                  <td className="px-4 py-3 text-xs text-foreground max-w-xs truncate">{attack.summary}</td>
                  <td className="px-4 py-3">
                    <code className="text-xs bg-muted px-1.5 py-0.5 rounded font-mono">{attack.rule}</code>
                  </td>
                  <td className="px-4 py-3 text-center">
                    <Badge variant="success">BLOCKED</Badge>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      {/* Behavioral Rule Effectiveness */}
      <Card>
        <h3 className="text-sm font-semibold text-foreground mb-4">Rule Effectiveness — Trigger Count</h3>
        <div className="h-56">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={RULE_EFFECTIVENESS} layout="vertical" margin={{ left: 20 }}>
              <XAxis
                type="number"
                tick={{ fontSize: 11, fill: "var(--color-muted-foreground)" }}
                tickLine={false}
                axisLine={{ stroke: "var(--color-border)" }}
              />
              <YAxis
                type="category"
                dataKey="label"
                tick={{ fontSize: 11, fill: "var(--color-muted-foreground)" }}
                tickLine={false}
                axisLine={{ stroke: "var(--color-border)" }}
                width={120}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: "var(--color-surface)",
                  border: "1px solid var(--color-border)",
                  borderRadius: "8px",
                  fontSize: "12px",
                }}
                formatter={(value) => [value, "Triggers"]}
              />
              <Bar dataKey="triggers" fill="var(--color-primary)" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </Card>
    </div>
  );
}
