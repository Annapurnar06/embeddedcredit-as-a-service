import type { Document } from "@/lib/mock-data";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import {
  FileText,
  CheckCircle2,
  Clock,
  XCircle,
  Upload,
} from "lucide-react";

interface LoanDocumentsProps {
  documents: Document[];
}

const STATUS_CONFIG: Record<
  string,
  { variant: "success" | "warning" | "danger"; icon: typeof CheckCircle2 }
> = {
  VERIFIED: { variant: "success", icon: CheckCircle2 },
  PENDING: { variant: "warning", icon: Clock },
  REJECTED: { variant: "danger", icon: XCircle },
};

function formatDate(dateStr: string): string {
  return new Date(dateStr).toLocaleDateString("en-IN", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
}

export function LoanDocuments({ documents }: LoanDocumentsProps) {
  return (
    <div className="space-y-4">
      {/* Upload placeholder */}
      <div className="flex justify-end">
        <Button variant="outline" size="sm" className="gap-2">
          <Upload className="h-4 w-4" />
          Upload Document
        </Button>
      </div>

      {/* Document Grid */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {documents.map((doc) => {
          const statusCfg = STATUS_CONFIG[doc.status] ?? STATUS_CONFIG.PENDING;
          const StatusIcon = statusCfg.icon;

          return (
            <Card key={doc.id} padding="md" hover>
              <div className="flex items-start gap-3">
                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-muted">
                  <FileText className="h-5 w-5 text-muted-foreground" />
                </div>
                <div className="min-w-0 flex-1">
                  <p className="text-sm font-medium text-foreground truncate">
                    {doc.name}
                  </p>
                  <div className="mt-1 flex items-center gap-2">
                    <Badge variant="outline" className="text-[10px]">
                      {doc.type}
                    </Badge>
                  </div>
                </div>
              </div>

              <div className="mt-4 flex items-center justify-between">
                <Badge variant={statusCfg.variant} className="gap-1">
                  <StatusIcon className="h-3 w-3" />
                  {doc.status}
                </Badge>
                <span className="text-xs text-muted-foreground">
                  {formatDate(doc.uploadedAt)}
                </span>
              </div>
            </Card>
          );
        })}

        {documents.length === 0 && (
          <div className="col-span-full py-12 text-center text-sm text-muted-foreground">
            No documents uploaded yet.
          </div>
        )}
      </div>
    </div>
  );
}
