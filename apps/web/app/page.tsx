import { ApprovalsInbox } from "../components/approvals-inbox";
import { VentureCard } from "../components/venture-card";

export default function Home() {
  return (
    <main className="max-w-6xl mx-auto px-6 py-10 space-y-8">
      <header className="flex items-center justify-between border-b border-zinc-800 pb-6">
        <div>
          <span className="text-xs font-semibold uppercase tracking-wider text-blue-400">
            Cofunder Platform
          </span>
          <h1 className="text-2xl font-bold tracking-tight text-white mt-1">
            Founder Operating Console
          </h1>
        </div>
        <div className="flex items-center gap-2">
          <span className="inline-block w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse" />
          <span className="text-xs text-zinc-400 font-medium">Agent Swarm Active</span>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        <div className="lg:col-span-7 space-y-6">
          <VentureCard />
          <div className="bg-[#18181b] border border-[#27272a] rounded-xl p-6 shadow-sm">
            <h3 className="text-base font-semibold text-zinc-200 mb-3">Active Specialist Agents</h3>
            <div className="grid grid-cols-2 gap-3 text-xs">
              <div className="p-3 rounded-lg bg-zinc-950 border border-zinc-800/80">
                <span className="font-semibold text-zinc-300">Market Intelligence</span>
                <p className="text-zinc-500 mt-1">Listening to live trends & competitor moves</p>
              </div>
              <div className="p-3 rounded-lg bg-zinc-950 border border-zinc-800/80">
                <span className="font-semibold text-zinc-300">Validation & TAM</span>
                <p className="text-zinc-500 mt-1">TAM/SAM/SOM and timing score formulation</p>
              </div>
              <div className="p-3 rounded-lg bg-zinc-950 border border-zinc-800/80">
                <span className="font-semibold text-zinc-300">Financial Projections</span>
                <p className="text-zinc-500 mt-1">Enforcing budget caps & break-even models</p>
              </div>
              <div className="p-3 rounded-lg bg-zinc-950 border border-zinc-800/80">
                <span className="font-semibold text-zinc-300">Legal & Compliance</span>
                <p className="text-zinc-500 mt-1">Official gazette citation & consent gating</p>
              </div>
            </div>
          </div>
        </div>

        <div className="lg:col-span-5">
          <ApprovalsInbox />
        </div>
      </div>
    </main>
  );
}
