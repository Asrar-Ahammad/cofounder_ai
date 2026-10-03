"use client";

import { useState } from "react";

export interface PendingApproval {
  id: string;
  action: string;
  payload: Record<string, unknown>;
  riskLevel: "low" | "medium" | "high" | "block";
  requestedBy: string;
}

interface ApprovalsInboxProps {
  initialApprovals?: PendingApproval[];
  onResolve?: (id: string, status: "approved" | "rejected") => Promise<void> | void;
}

export function ApprovalsInbox({
  initialApprovals = [],
  onResolve,
}: ApprovalsInboxProps) {
  const [approvals, setApprovals] = useState<PendingApproval[]>(initialApprovals);

  const handleResolve = async (id: string, status: "approved" | "rejected") => {
    try {
      if (onResolve) {
        await onResolve(id, status);
      }
      setApprovals((prev) => prev.filter((item) => item.id !== id));
    } catch (err) {
      console.error(`Failed to resolve approval ${id}:`, err);
    }
  };

  const getRiskBadge = (risk: PendingApproval["riskLevel"]) => {
    switch (risk) {
      case "low":
        return "bg-emerald-500/10 text-emerald-400 border-emerald-500/20";
      case "medium":
        return "bg-amber-500/10 text-amber-400 border-amber-500/20";
      case "high":
        return "bg-rose-500/10 text-rose-400 border-rose-500/20";
      case "block":
        return "bg-red-500/20 text-red-300 border-red-500/40";
    }
  };

  return (
    <div className="bg-[#18181b] border border-[#27272a] rounded-xl p-6 shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-lg font-semibold text-zinc-100">Approvals Inbox</h2>
          <p className="text-sm text-zinc-400">
            Human-in-the-loop review queue for gated agent tool executions
          </p>
        </div>
        <span className="px-2.5 py-1 text-xs font-medium rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20">
          {approvals.length} Pending
        </span>
      </div>

      {approvals.length === 0 ? (
        <div className="py-8 text-center text-sm text-zinc-500 border border-dashed border-zinc-800 rounded-lg">
          No pending actions. All agent operations are running smoothly.
        </div>
      ) : (
        <div className="space-y-4">
          {approvals.map((req) => (
            <div
              key={req.id}
              className="p-4 rounded-lg bg-[#09090b] border border-zinc-800 flex flex-col gap-3"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="font-mono text-sm font-medium text-zinc-200">
                    {req.action}
                  </span>
                  <span
                    className={`text-xs px-2 py-0.5 rounded-full border uppercase tracking-wider font-semibold ${getRiskBadge(
                      req.riskLevel
                    )}`}
                  >
                    {req.riskLevel}
                  </span>
                </div>
                <span className="text-xs text-zinc-500">From: {req.requestedBy}</span>
              </div>

              <div className="bg-zinc-950 p-3 rounded text-xs font-mono text-zinc-300 overflow-x-auto border border-zinc-800/80">
                <pre>{JSON.stringify(req.payload, null, 2)}</pre>
              </div>

              <div className="flex justify-end gap-2 pt-1">
                <button
                  type="button"
                  onClick={() => handleResolve(req.id, "rejected")}
                  className="px-3 py-1.5 text-xs font-medium rounded-md bg-zinc-800 hover:bg-zinc-700 text-zinc-300 transition-colors"
                >
                  Reject
                </button>
                <button
                  type="button"
                  onClick={() => handleResolve(req.id, "approved")}
                  className="px-3 py-1.5 text-xs font-medium rounded-md bg-blue-600 hover:bg-blue-500 text-white transition-colors"
                >
                  Approve Execution
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
