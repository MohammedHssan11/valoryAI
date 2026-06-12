import { motion } from "framer-motion";
import { Database, X } from "lucide-react";
import { GlassPanel } from "@/components/ui/glass";
import { CitationViewer } from "@/features/copilot/CitationViewer";
import type { CopilotFrontendPayload } from "@/types/copilot";

interface EvidenceDrawerProps {
  isOpen: boolean;
  payload: CopilotFrontendPayload | null;
  onClose: () => void;
}

function safeString(value: unknown): string {
  if (value === null || value === undefined || value === "") return "Unavailable";
  if (typeof value === "string" || typeof value === "number" || typeof value === "boolean") return String(value);
  return JSON.stringify(value);
}

function EvidenceList({ title, items }: { title: string; items: Array<Record<string, unknown>> }) {
  return (
    <GlassPanel className="grid gap-3 p-4">
      <div className="flex items-center justify-between gap-3 border-b border-white/5 pb-3">
        <p className="font-label-caps text-xs text-primary-fixed-dim">{title}</p>
        <span className="font-data-tabular text-[10px] text-outline">{items.length}</span>
      </div>
      {items.length ? (
        <div className="grid gap-2">
          {items.slice(0, 12).map((item, index) => {
            const primary =
              item.comparable && typeof item.comparable === "object"
                ? item.comparable
                : item.feature_driver && typeof item.feature_driver === "object"
                  ? item.feature_driver
                  : item;
            const record = primary as Record<string, unknown>;
            const label =
              record.comparable_id ??
              record.property_id ??
              record.feature ??
              record.name ??
              record.text ??
              `Evidence ${index + 1}`;
            return (
              <div key={`${title}-${index}`} className="rounded-lg border border-white/10 bg-surface/20 p-3">
                <p className="truncate font-data-tabular text-sm text-on-surface">{safeString(label)}</p>
                <div className="mt-2 flex flex-wrap gap-2">
                  {Object.entries(record)
                    .slice(0, 5)
                    .map(([key, value]) => (
                      <span key={key} className="rounded-md border border-white/10 bg-surface/20 px-2 py-1 font-data-tabular text-[10px] text-on-surface-variant">
                        {key}: {safeString(value)}
                      </span>
                    ))}
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <p className="text-sm text-on-surface-variant">No evidence rows returned.</p>
      )}
    </GlassPanel>
  );
}

export function EvidenceDrawer({ isOpen, payload, onClose }: EvidenceDrawerProps) {
  if (!isOpen) return null;

  const evidence = payload?.full_evidence;
  const comparables = Array.isArray(evidence?.comparables) ? evidence.comparables : [];
  const featureDrivers = Array.isArray(evidence?.feature_drivers) ? evidence.feature_drivers : [];
  const marketInsights = Array.isArray(evidence?.market_insights) ? evidence.market_insights : [];

  return (
    <div className="fixed inset-0 z-[70] flex justify-end bg-black/45">
      <motion.aside
        initial={{ x: 420, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        exit={{ x: 420, opacity: 0 }}
        className="grid h-full w-full max-w-2xl content-start gap-4 overflow-y-auto border-l border-white/10 bg-surface-container p-5 shadow-2xl"
      >
        <div className="flex items-start justify-between gap-4">
          <div>
            <p className="font-label-caps text-xs text-primary-fixed-dim">Evidence Package</p>
            <h3 className="mt-1 font-body-md text-on-surface">Traceable records</h3>
          </div>
          <button
            type="button"
            aria-label="Close evidence"
            title="Close"
            onClick={onClose}
            className="rounded-md border border-white/10 bg-surface/30 p-2 text-on-surface-variant hover:text-primary-fixed-dim"
          >
            <X className="h-4 w-4" />
          </button>
        </div>

        <GlassPanel className="flex items-start gap-3 p-4">
          <Database className="mt-0.5 h-4 w-4 text-primary-fixed-dim" />
          <div>
            <p className="font-label-caps text-[10px] text-outline">Composition</p>
            <p className="mt-1 text-sm text-on-surface-variant">{payload?.composition_status ?? "No payload"}</p>
          </div>
        </GlassPanel>

        <EvidenceList title="Comparable Evidence" items={comparables as Array<Record<string, unknown>>} />
        <EvidenceList title="Feature Drivers" items={featureDrivers as Array<Record<string, unknown>>} />
        <EvidenceList title="Market Evidence" items={marketInsights as Array<Record<string, unknown>>} />
        <CitationViewer citations={payload?.citations ?? null} />
      </motion.aside>
    </div>
  );
}
