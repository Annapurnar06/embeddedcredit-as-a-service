import { useMemo } from "react";
import type { PolicyResult } from "@/lib/mock-data";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { CheckCircle2, XCircle, ShieldCheck } from "lucide-react";

interface LoanPolicyProps {
  policyResults: PolicyResult[];
}

export function LoanPolicy({ policyResults }: LoanPolicyProps) {
  const { structural, behavioral, totalPassed } = useMemo(() => {
    const s = policyResults.filter((p) => p.type === "STRUCTURAL");
    const b = policyResults.filter((p) => p.type === "BEHAVIORAL");
    const passed = policyResults.filter((p) => p.passed).length;
    return { structural: s, behavioral: b, totalPassed: passed };
  }, [policyResults]);

  return (
    <div className="space-y-6">
      {/* Summary */}
      <Card padding="md">
        <div className="flex items-center gap-4">
          <ShieldCheck className="h-6 w-6 text-primary" />
          <div className="flex items-center gap-6">
            <div>
              <p className="text-2xl font-bold text-foreground">
                {totalPassed}/{policyResults.length}
              </p>
              <p className="text-xs text-muted-foreground">Rules Passed</p>
            </div>
            <div className="h-8 w-px bg-border" />
            <div>
              <p className="text-lg font-semibold text-foreground">
                {structural.length}
              </p>
              <p className="text-xs text-muted-foreground">Structural</p>
            </div>
            <div className="h-8 w-px bg-border" />
            <div>
              <p className="text-lg font-semibold text-foreground">
                {behavioral.length}
              </p>
              <p className="text-xs text-muted-foreground">Behavioral</p>
            </div>
          </div>
        </div>
      </Card>

      {/* Policy Table */}
      <Card padding="none">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-border bg-muted/50">
                <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  Status
                </th>
                <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  Rule
                </th>
                <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  Type
                </th>
                <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  Detail
                </th>
              </tr>
            </thead>
            <tbody>
              {/* Structural Section */}
              <tr>
                <td
                  colSpan={4}
                  className="bg-muted/30 px-4 py-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground"
                >
                  Structural Rules ({structural.length})
                </td>
              </tr>
              {structural.map((rule) => (
                <tr
                  key={rule.rule}
                  className="border-b border-border transition-colors hover:bg-muted/20"
                >
                  <td className="px-4 py-3">
                    {rule.passed ? (
                      <CheckCircle2 className="h-4 w-4 text-success" />
                    ) : (
                      <XCircle className="h-4 w-4 text-danger" />
                    )}
                  </td>
                  <td className="px-4 py-3 font-medium text-foreground">
                    {rule.rule}
                  </td>
                  <td className="px-4 py-3">
                    <Badge variant="info" className="text-[10px]">
                      STRUCTURAL
                    </Badge>
                  </td>
                  <td className="px-4 py-3 text-muted-foreground">
                    {rule.detail}
                  </td>
                </tr>
              ))}

              {/* Behavioral Section */}
              <tr>
                <td
                  colSpan={4}
                  className="bg-muted/30 px-4 py-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground"
                >
                  Behavioral Rules ({behavioral.length})
                </td>
              </tr>
              {behavioral.map((rule) => (
                <tr
                  key={rule.rule}
                  className="border-b border-border transition-colors hover:bg-muted/20"
                >
                  <td className="px-4 py-3">
                    {rule.passed ? (
                      <CheckCircle2 className="h-4 w-4 text-success" />
                    ) : (
                      <XCircle className="h-4 w-4 text-danger" />
                    )}
                  </td>
                  <td className="px-4 py-3 font-medium text-foreground">
                    {rule.rule}
                  </td>
                  <td className="px-4 py-3">
                    <Badge variant="warning" className="text-[10px]">
                      BEHAVIORAL
                    </Badge>
                  </td>
                  <td className="px-4 py-3 text-muted-foreground">
                    {rule.detail}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
