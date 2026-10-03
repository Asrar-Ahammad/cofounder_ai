export interface VentureCardProps {
  name: string;
  stage: string;
  jurisdiction: string;
  northStarGoal: string;
  budgetCaps: {
    monthly: number;
    maxCac: number;
    outreach: number;
  };
}

export function VentureCard({
  name = "QuantumSaaS",
  stage = "Validation",
  jurisdiction = "India (DPDP / Companies Act)",
  northStarGoal = "First paying customer by Day 90 ($1,500 MRR)",
  budgetCaps = { monthly: 5000, maxCac: 120, outreach: 500 },
}: Partial<VentureCardProps>) {
  return (
    <div className="bg-[#18181b] border border-[#27272a] rounded-xl p-6 shadow-sm">
      <div className="flex items-start justify-between">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-xl font-bold text-zinc-100">{name}</h1>
            <span className="px-2.5 py-0.5 text-xs font-semibold rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20">
              {stage}
            </span>
          </div>
          <p className="text-xs text-zinc-500 mt-1">Jurisdiction: {jurisdiction}</p>
        </div>
      </div>

      <div className="mt-5 p-4 rounded-lg bg-[#09090b] border border-zinc-800">
        <span className="text-xs font-semibold text-zinc-400 uppercase tracking-wider">
          North-Star Milestone
        </span>
        <p className="text-sm font-medium text-zinc-200 mt-1">{northStarGoal}</p>
      </div>

      <div className="mt-5 grid grid-cols-3 gap-3">
        <div className="p-3 rounded-lg bg-[#09090b] border border-zinc-800/80">
          <span className="text-xs text-zinc-500">Monthly Budget Cap</span>
          <p className="text-base font-semibold text-zinc-200 mt-0.5">
            ${budgetCaps.monthly.toLocaleString()}
          </p>
        </div>
        <div className="p-3 rounded-lg bg-[#09090b] border border-zinc-800/80">
          <span className="text-xs text-zinc-500">Max CAC Ceiling</span>
          <p className="text-base font-semibold text-zinc-200 mt-0.5">
            ${budgetCaps.maxCac.toLocaleString()}
          </p>
        </div>
        <div className="p-3 rounded-lg bg-[#09090b] border border-zinc-800/80">
          <span className="text-xs text-zinc-500">Outreach Volume Cap</span>
          <p className="text-base font-semibold text-zinc-200 mt-0.5">
            {budgetCaps.outreach.toLocaleString()} / mo
          </p>
        </div>
      </div>
    </div>
  );
}
