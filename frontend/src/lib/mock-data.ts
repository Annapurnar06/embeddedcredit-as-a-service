export type LoanStatus = "UNVERIFIED" | "VERIFIED" | "CONFIRMED" | "DISBURSED" | "ACTIVE";
export type ApprovalStatus = "PENDING" | "APPROVED" | "REJECTED";

export interface LoanApplication {
  id: string;
  borrowerName: string;
  segment: string;
  segmentId: string;
  amount: number;
  score: number;
  status: LoanStatus;
  approvalStatus?: ApprovalStatus;
  product: string;
  createdAt: string;
  updatedAt: string;
  phone: string;
  language: string;
  processingTime: number;
  toolCalls: ToolCall[];
  documents: Document[];
  policyResults: PolicyResult[];
  schedule: EMIEntry[];
}

export interface ToolCall {
  id: string;
  timestamp: string;
  tool: string;
  category: string;
  status: "SUCCESS" | "FAILED" | "PENDING";
  latencyMs: number;
  input: string;
  output: string;
}

export interface Document {
  id: string;
  name: string;
  type: string;
  status: "VERIFIED" | "PENDING" | "REJECTED";
  uploadedAt: string;
}

export interface PolicyResult {
  rule: string;
  type: "STRUCTURAL" | "BEHAVIORAL";
  passed: boolean;
  detail: string;
}

export interface EMIEntry {
  month: number;
  date: string;
  principal: number;
  interest: number;
  total: number;
  season: "flush" | "lean" | "normal";
}

export interface ApprovalRequest {
  id: string;
  loanId: string;
  borrowerName: string;
  segment: string;
  operation: string;
  amount: number;
  riskSummary: string;
  requestedAt: string;
  requestedBy: string;
  status: ApprovalStatus;
  approvedBy?: string;
  approvedAt?: string;
  reason?: string;
}

const segments = [
  { id: "dairy_farmer", name: "Dairy Farmer", product: "Seasonal Dynamic EMI" },
  { id: "kirana_shop", name: "Kirana Shop", product: "Daily Micro Collection" },
  { id: "gig_worker", name: "Gig Worker", product: "Payout Linked" },
  { id: "gold_loan", name: "Gold Loan", product: "Gold Pledge" },
  { id: "street_vendor", name: "Street Vendor", product: "PM SVANidhi Plus" },
  { id: "cab_driver", name: "Cab Driver", product: "Vehicle Finance PV" },
  { id: "truck_operator", name: "Truck Operator", product: "Vehicle Finance CV" },
  { id: "shg_member", name: "SHG Member", product: "Group Linked" },
  { id: "cotton_farmer", name: "Cotton Farmer", product: "Harvest Linked" },
  { id: "medical_shop", name: "Medical Shop", product: "Inventory Finance" },
];

const firstNames = ["Ramesh", "Priya", "Ajay", "Sunita", "Vikram", "Meena", "Suresh", "Kavita", "Rajan", "Deepa", "Amit", "Geeta", "Rohit", "Savita", "Mohan", "Lakshmi", "Arun", "Neha", "Gopal", "Anita", "Dinesh", "Pooja", "Manoj", "Rekha", "Sanjay", "Kamla", "Vinod", "Usha", "Pramod", "Seema"];
const lastNames = ["Patel", "Sharma", "Yadav", "Singh", "Gupta", "Joshi", "Reddy", "Nair", "Deshmukh", "Pillai", "Mishra", "Chauhan", "Verma", "Kulkarni", "Iyer"];

function randomFrom<T>(arr: readonly T[]): T {
  return arr[Math.floor(Math.random() * arr.length)];
}

function generateToolCalls(segment: string): ToolCall[] {
  const tools = [
    { tool: "aadhaar_ekyc", category: "Identity", latency: 1200 },
    { tool: "pan_verify", category: "Identity", latency: 800 },
    { tool: "bank_account_aa", category: "Data", latency: 2100 },
    { tool: "credit_bureau", category: "Data", latency: 1500 },
    { tool: "segment_score", category: "Scoring", latency: 450 },
    { tool: "policy_check", category: "Scoring", latency: 200 },
    { tool: "product_design", category: "Product", latency: 350 },
    { tool: "kfs_delivery", category: "Execution", latency: 600 },
    { tool: "esign_request", category: "Execution", latency: 1800 },
    { tool: "disbursement", category: "Execution", latency: 3200 },
  ];

  const segmentTools: Record<string, { tool: string; category: string; latency: number }[]> = {
    dairy_farmer: [{ tool: "dairy_cooperative", category: "Data", latency: 1800 }],
    kirana_shop: [{ tool: "gst_returns", category: "Data", latency: 2200 }],
    gig_worker: [{ tool: "platform_earnings", category: "Data", latency: 1600 }],
    gold_loan: [{ tool: "gold_purity_check", category: "Data", latency: 900 }],
    cab_driver: [{ tool: "platform_earnings", category: "Data", latency: 1600 }],
    truck_operator: [{ tool: "fastag_data", category: "Data", latency: 1400 }],
  };

  const allTools = [...tools.slice(0, 4), ...(segmentTools[segment] || []), ...tools.slice(4)];
  const baseTime = new Date("2026-04-11T10:00:00Z");

  return allTools.map((t, i) => ({
    id: `tc-${i}`,
    timestamp: new Date(baseTime.getTime() + i * 5000).toISOString(),
    tool: t.tool,
    category: t.category,
    status: Math.random() > 0.05 ? "SUCCESS" as const : "FAILED" as const,
    latencyMs: t.latency + Math.floor(Math.random() * 500),
    input: `{ "borrower_id": "BRW-***", "segment": "${segment}" }`,
    output: `{ "status": "ok", "confidence": ${(0.85 + Math.random() * 0.15).toFixed(2)} }`,
  }));
}

function generatePolicyResults(): PolicyResult[] {
  return [
    { rule: "Session State Check", type: "STRUCTURAL", passed: true, detail: "Session in SCORING state -- tool category allowed" },
    { rule: "Confirmation Required", type: "STRUCTURAL", passed: true, detail: "Borrower consent recorded for data pull" },
    { rule: "Authority Check", type: "STRUCTURAL", passed: true, detail: "READ operation -- no maker-checker required" },
    { rule: "Circuit Breaker", type: "STRUCTURAL", passed: true, detail: "Circuit CLOSED -- tool healthy" },
    { rule: "KFS Delivery", type: "STRUCTURAL", passed: true, detail: "Key Facts Statement delivered before agreement" },
    { rule: "Cooling-Off Period", type: "STRUCTURAL", passed: true, detail: "3-day look-up period enforced" },
    { rule: "All-In-Cost Cap", type: "STRUCTURAL", passed: true, detail: "Total cost 18.5% within RBI ceiling 26%" },
    { rule: "PII Masking", type: "BEHAVIORAL", passed: true, detail: "All Aadhaar/PAN numbers masked in response" },
    { rule: "No False Promises", type: "BEHAVIORAL", passed: true, detail: "No guarantee/assured language detected" },
    { rule: "Language Appropriateness", type: "BEHAVIORAL", passed: true, detail: "Response in borrower's preferred language" },
    { rule: "Amount Bounds", type: "BEHAVIORAL", passed: true, detail: "Loan amount within segment range" },
    { rule: "Tenure Bounds", type: "BEHAVIORAL", passed: true, detail: "Tenure within segment limits" },
    { rule: "Interest Rate Disclosure", type: "BEHAVIORAL", passed: true, detail: "Rate disclosed on reducing balance basis" },
    { rule: "No Coercive Language", type: "BEHAVIORAL", passed: true, detail: "Recovery language within guidelines" },
    { rule: "Data Source Citation", type: "BEHAVIORAL", passed: true, detail: "All data sources cited in explanation" },
    { rule: "CERSAI Filing", type: "STRUCTURAL", passed: true, detail: "Security interest registration initiated" },
    { rule: "Digital Lending Compliance", type: "BEHAVIORAL", passed: true, detail: "DLG framework requirements met" },
  ];
}

function generateSchedule(amount: number, months: number): EMIEntry[] {
  const rate = 0.015;
  const entries: EMIEntry[] = [];
  let remaining = amount;

  for (let i = 1; i <= months; i++) {
    const month = ((new Date().getMonth() + i) % 12) + 1;
    const isFlush = month >= 10 || month <= 2;
    const isLean = month >= 4 && month <= 6;
    const season: "flush" | "lean" | "normal" = isFlush ? "flush" : isLean ? "lean" : "normal";
    const multiplier = isFlush ? 1.3 : isLean ? 0.7 : 1.0;

    const basePrincipal = amount / months;
    const principal = Math.round(basePrincipal * multiplier);
    const interest = Math.round(remaining * rate);
    remaining = Math.max(0, remaining - principal);

    entries.push({
      month: i,
      date: `2026-${String(month).padStart(2, "0")}-05`,
      principal,
      interest,
      total: principal + interest,
      season,
    });
  }
  return entries;
}

export function generateMockLoans(count: number = 30): LoanApplication[] {
  const statuses: LoanStatus[] = ["UNVERIFIED", "VERIFIED", "CONFIRMED", "DISBURSED", "ACTIVE"];

  return Array.from({ length: count }, (_, i) => {
    const seg = randomFrom(segments);
    const status = randomFrom(statuses);
    const amount = Math.round((50000 + Math.random() * 450000) / 1000) * 1000;
    const score = Math.floor(580 + Math.random() * 170);
    const firstName = randomFrom(firstNames);
    const lastName = randomFrom(lastNames);

    return {
      id: `LOAN-${String(i + 1).padStart(4, "0")}`,
      borrowerName: `${firstName} ${lastName}`,
      segment: seg.name,
      segmentId: seg.id,
      amount,
      score,
      status,
      product: seg.product,
      createdAt: new Date(Date.now() - Math.random() * 7 * 86400000).toISOString(),
      updatedAt: new Date(Date.now() - Math.random() * 86400000).toISOString(),
      phone: `+91 ${Math.floor(7000000000 + Math.random() * 2999999999)}`,
      language: randomFrom(["hi", "en", "gu", "mr"]),
      processingTime: Math.floor(8 + Math.random() * 12),
      toolCalls: generateToolCalls(seg.id),
      documents: [
        { id: "doc-1", name: "Aadhaar Card", type: "Identity", status: "VERIFIED", uploadedAt: new Date().toISOString() },
        { id: "doc-2", name: "PAN Card", type: "Identity", status: "VERIFIED", uploadedAt: new Date().toISOString() },
        { id: "doc-3", name: "Bank Statement", type: "Financial", status: score > 650 ? "VERIFIED" : "PENDING", uploadedAt: new Date().toISOString() },
      ],
      policyResults: generatePolicyResults(),
      schedule: generateSchedule(amount, 12),
    };
  });
}

export function generateApprovalRequests(): ApprovalRequest[] {
  const loans = generateMockLoans(8);
  return loans.map((loan, i) => ({
    id: `APR-${String(i + 1).padStart(4, "0")}`,
    loanId: loan.id,
    borrowerName: loan.borrowerName,
    segment: loan.segment,
    operation: randomFrom(["Disbursement", "eSign Request", "Moratorium Apply", "Schedule Adjust", "eNACH Setup"]),
    amount: loan.amount,
    riskSummary: `Score ${loan.score}/900. ${loan.score > 700 ? "Low risk" : loan.score > 650 ? "Medium risk" : "Elevated risk"}. ${loan.policyResults.filter(p => p.passed).length}/17 policy checks passed.`,
    requestedAt: loan.updatedAt,
    requestedBy: "AI Agent",
    status: i < 3 ? "PENDING" : i < 6 ? "APPROVED" : "REJECTED",
    approvedBy: i >= 3 ? "Rajesh Kumar (Credit Head)" : undefined,
    approvedAt: i >= 3 ? new Date().toISOString() : undefined,
    reason: i >= 6 ? "Score below threshold for auto-approval" : undefined,
  }));
}

export const MOCK_LOANS = generateMockLoans(30);
export const MOCK_APPROVALS = generateApprovalRequests();
