const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...options?.headers },
    ...options,
  });
  if (!res.ok) {
    throw new Error(`API ${res.status}: ${await res.text()}`);
  }
  return res.json();
}

// -- Loans ------------------------------------------------------------------

export interface LoanSummary {
  id: string;
  borrower_id: string;
  segment: string;
  status: string;
  amount: string | null;
  created_at: string;
}

export interface LoanDetail extends LoanSummary {
  lender_id: string;
  interest_rate: string | null;
  tenure_months: number | null;
  score: number | null;
  score_grade: string | null;
  decision: string | null;
}

export function listLoans(params?: { lender_id?: string; status?: string; limit?: number }) {
  const qs = new URLSearchParams();
  if (params?.lender_id) qs.set("lender_id", params.lender_id);
  if (params?.status) qs.set("status", params.status);
  if (params?.limit) qs.set("limit", String(params.limit));
  return request<{ count: number; loans: LoanSummary[] }>(`/api/loans/?${qs}`);
}

export function getLoan(loanId: string) {
  return request<LoanDetail>(`/api/loans/${loanId}`);
}

// -- Sessions ----------------------------------------------------------------

export interface SessionCreate {
  lender_id: string;
  channel: string;
  channel_user_id: string;
  segment?: string;
  language?: string;
}

export function createSession(payload: SessionCreate) {
  return request<{ id: string; state: string }>("/api/sessions/", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function getSession(sessionId: string) {
  return request<{ id: string; state: string }>(`/api/sessions/${sessionId}`);
}

// -- Chat --------------------------------------------------------------------

export interface ChatRequest {
  channel?: string;
  channel_user_id: string;
  lender_id?: string;
  content: string;
  segment?: string;
  language?: string;
}

export interface ChatResponse {
  session_id: string;
  state: string;
  response: string;
  tools_called: string[];
  channel: string;
}

export function sendMessage(payload: ChatRequest) {
  return request<ChatResponse>("/api/chat/message", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

// -- Audit -------------------------------------------------------------------

export interface ToolExecution {
  id: string;
  tool_name: string;
  tool_category: string;
  result_status: string;
  latency_ms: number;
  session_state_before: string;
  session_state_after: string;
  created_at: string;
}

export interface AuditTimelineEntry {
  type: "audit_log" | "tool_execution";
  event: string;
  actor: string;
  timestamp: string;
}

export function getAuditLogs(sessionId: string) {
  return request<{ session_id: string; count: number; logs: unknown[] }>(
    `/api/audit/logs/${sessionId}`
  );
}

export function getToolExecutions(sessionId: string) {
  return request<{ session_id: string; count: number; executions: ToolExecution[] }>(
    `/api/audit/tools/${sessionId}`
  );
}

export function getLoanAuditTrail(loanId: string) {
  return request<{
    loan_application_id: string;
    audit_logs: number;
    tool_executions: number;
    timeline: AuditTimelineEntry[];
  }>(`/api/audit/loan/${loanId}`);
}

// -- Health ------------------------------------------------------------------

export function healthCheck() {
  return request<{ status: string }>("/api/health");
}
