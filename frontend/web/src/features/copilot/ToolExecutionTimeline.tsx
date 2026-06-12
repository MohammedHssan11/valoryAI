import { CheckCircle2, Circle, CircleAlert, Clock3 } from "lucide-react";
import { GlassPanel } from "@/components/ui/glass";
import { cn } from "@/lib/utils";
import type { CopilotFrontendPayload } from "@/types/copilot";

interface ToolExecutionTimelineProps {
  payload: CopilotFrontendPayload | null;
}

function toolLabel(value: string): string {
  return value.replaceAll("_", " ").replace("TOOL", "Tool");
}

export function ToolExecutionTimeline({ payload }: ToolExecutionTimelineProps) {
  const outputs = payload?.tool_outputs ?? [];
  const failures = payload?.failed_tools ?? [];

  return (
    <GlassPanel className="grid gap-4 p-4">
      <div className="flex items-center justify-between gap-3 border-b border-white/5 pb-3">
        <div>
          <p className="font-label-caps text-xs text-primary-fixed-dim">Tool Execution</p>
          <p className="mt-1 text-xs text-on-surface-variant">
            {outputs.length} used, {failures.length} failed
          </p>
        </div>
        <Clock3 className="h-4 w-4 text-primary-fixed-dim" />
      </div>

      {outputs.length === 0 && failures.length === 0 ? (
        <div className="flex items-start gap-3 rounded-lg border border-white/10 bg-surface/20 p-3">
          <Circle className="mt-0.5 h-4 w-4 text-outline" />
          <p className="text-sm text-on-surface-variant">No tool output was returned.</p>
        </div>
      ) : (
        <div className="grid gap-3">
          {outputs.map((output) => (
            <div key={`${output.planned_tool}-${output.ordering_metadata.order_index}`} className="grid grid-cols-[24px_1fr] gap-3">
              <CheckCircle2 className="mt-1 h-4 w-4 text-tertiary-fixed-dim" />
              <div className="min-w-0 rounded-lg border border-tertiary-fixed-dim/15 bg-tertiary-fixed-dim/5 p-3">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <p className="truncate font-data-tabular text-sm text-on-surface">{toolLabel(output.planned_tool)}</p>
                  <span className="rounded-md border border-white/10 px-2 py-1 font-data-tabular text-[10px] text-on-surface-variant">
                    {output.tool_name}
                  </span>
                </div>
                <p className="mt-2 text-xs text-on-surface-variant">
                  Results used from order {output.ordering_metadata.order_index + 1}
                  {output.ordering_metadata.parallel_group_index != null
                    ? `, group ${output.ordering_metadata.parallel_group_index + 1}`
                    : ""}
                </p>
              </div>
            </div>
          ))}

          {failures.map((failure) => (
            <div key={`${failure.planned_tool}-${failure.ordering_metadata.order_index}`} className="grid grid-cols-[24px_1fr] gap-3">
              <CircleAlert className="mt-1 h-4 w-4 text-error" />
              <div className={cn("min-w-0 rounded-lg border border-error/20 bg-error/5 p-3")}>
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <p className="truncate font-data-tabular text-sm text-on-surface">{toolLabel(String(failure.planned_tool))}</p>
                  <span className="rounded-md border border-white/10 px-2 py-1 font-data-tabular text-[10px] text-error">
                    {failure.error_type}
                  </span>
                </div>
                <p className="mt-2 text-xs text-on-surface-variant">{failure.failure_category ?? "TOOL_FAILURE"}</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </GlassPanel>
  );
}
