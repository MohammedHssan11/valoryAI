import { Link2, ShieldCheck } from "lucide-react";
import { GlassPanel } from "@/components/ui/glass";
import type { CopilotCitationPackage } from "@/types/copilot";

interface CitationViewerProps {
  citations: CopilotCitationPackage | null;
}

function CitationGroup({ label, values }: { label: string; values: string[] }) {
  return (
    <div className="grid gap-2">
      <div className="flex items-center justify-between gap-3">
        <span className="font-label-caps text-[10px] text-outline">{label}</span>
        <span className="font-data-tabular text-[10px] text-on-surface-variant">{values.length}</span>
      </div>
      {values.length ? (
        <div className="flex flex-wrap gap-2">
          {values.map((value) => (
            <span key={value} className="rounded-md border border-primary-fixed-dim/15 bg-primary-fixed-dim/5 px-2.5 py-1.5 font-data-tabular text-[10px] text-primary-fixed-dim">
              {value}
            </span>
          ))}
        </div>
      ) : (
        <p className="text-xs text-on-surface-variant">None returned.</p>
      )}
    </div>
  );
}

export function CitationViewer({ citations }: CitationViewerProps) {
  if (!citations) {
    return (
      <GlassPanel className="p-4">
        <p className="font-label-caps text-xs text-primary-fixed-dim">Citations</p>
        <p className="mt-2 text-sm text-on-surface-variant">No citation package returned.</p>
      </GlassPanel>
    );
  }

  return (
    <GlassPanel className="grid gap-4 p-4">
      <div className="flex items-center justify-between gap-3 border-b border-white/5 pb-3">
        <div>
          <p className="font-label-caps text-xs text-primary-fixed-dim">Citations</p>
          <p className="mt-1 text-xs text-on-surface-variant">Source identifiers preserved by the Composer.</p>
        </div>
        <Link2 className="h-4 w-4 text-primary-fixed-dim" />
      </div>

      <CitationGroup label="Valuation IDs" values={citations.valuation_ids} />
      <CitationGroup label="Tool Event IDs" values={citations.tool_event_ids} />
      <CitationGroup label="Comparable IDs" values={citations.comparable_ids} />

      {citations.unavailable_optional_citation_types.length ? (
        <div className="flex items-start gap-2 rounded-lg border border-secondary-fixed/20 bg-secondary-fixed/5 p-3">
          <ShieldCheck className="mt-0.5 h-4 w-4 text-secondary-fixed" />
          <p className="text-xs leading-5 text-on-surface-variant">
            Optional unavailable: {citations.unavailable_optional_citation_types.join(", ")}
          </p>
        </div>
      ) : null}
    </GlassPanel>
  );
}
