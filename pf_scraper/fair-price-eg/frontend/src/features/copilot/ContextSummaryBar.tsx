import { Building2, GitBranch, Landmark, LineChart, MemoryStick, Scale } from "lucide-react";
import { GlassPanel } from "@/components/ui/glass";
import type { CopilotHumanContext } from "@/types/copilot";

interface ContextSummaryBarProps {
  context: CopilotHumanContext | null;
}

export function ContextSummaryBar({ context }: ContextSummaryBarProps) {
  const items = [
    { label: "Property", value: context?.activeProperty ?? "No active property", icon: Building2 },
    { label: "Scenario", value: context?.activeScenario ?? "Base valuation", icon: GitBranch },
    { label: "Valuation", value: context?.latestValuation ?? "No valuation", icon: Landmark },
    { label: "Negotiation", value: context?.latestNegotiation ?? "No negotiation", icon: Scale },
    { label: "Investment", value: context?.latestInvestment ?? "No investment", icon: LineChart },
    { label: "Memory", value: context?.memoryStatus ?? "Pending", icon: MemoryStick },
  ];

  return (
    <GlassPanel className="grid gap-3 p-4">
      <div className="grid gap-2 sm:grid-cols-2">
        {items.map(({ label, value, icon: Icon }) => (
          <div key={label} className="min-w-0 rounded-lg border border-white/10 bg-surface/20 p-3">
            <div className="mb-2 flex items-center gap-2">
              <Icon className="h-3.5 w-3.5 text-primary-fixed-dim" />
              <span className="font-label-caps text-[10px] text-outline">{label}</span>
            </div>
            <p className="truncate text-xs text-on-surface-variant" title={value}>
              {value}
            </p>
          </div>
        ))}
      </div>

      {context?.relevantHistory.length ? (
        <div className="flex flex-wrap gap-2 border-t border-white/5 pt-3">
          {context.relevantHistory.map((item) => (
            <span key={item} className="rounded-md border border-white/10 bg-surface/20 px-2.5 py-1.5 font-data-tabular text-[10px] text-on-surface-variant">
              {item}
            </span>
          ))}
        </div>
      ) : null}
    </GlassPanel>
  );
}
