import * as React from "react";
import { AnimatePresence, motion } from "framer-motion";
import { BotMessageSquare, PanelRightClose } from "lucide-react";
import { CopilotPanel } from "@/features/copilot/CopilotPanel";
import { usePropertyContextStore } from "@/store/propertyContextStore";

export function CopilotDrawer() {
  const [isOpen, setIsOpen] = React.useState(false);
  const activePropertyId = usePropertyContextStore((state) => state.activePropertyId);

  return (
    <>
      <button
        type="button"
        aria-label="Open Copilot"
        title="Copilot"
        onClick={() => setIsOpen(true)}
        className="fixed bottom-24 right-4 z-[55] flex h-12 w-12 items-center justify-center rounded-full border border-primary-fixed-dim/25 bg-surface-container/92 text-primary-fixed-dim shadow-2xl shadow-primary/10 backdrop-blur-2xl transition-transform hover:scale-105 md:bottom-6 md:right-6"
      >
        <BotMessageSquare className="h-5 w-5" />
        {typeof activePropertyId === "number" && (
          <span className="absolute -right-0.5 -top-0.5 h-3 w-3 rounded-full border border-surface-container bg-tertiary-fixed-dim" />
        )}
      </button>

      <AnimatePresence>
        {isOpen && (
          <div className="fixed inset-0 z-[65] flex justify-end bg-black/45">
            <motion.aside
              initial={{ x: 520, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              exit={{ x: 520, opacity: 0 }}
              transition={{ duration: 0.28, ease: [0.2, 0.8, 0.2, 1] }}
              className="grid h-full w-full max-w-[520px] grid-rows-[auto_1fr] gap-4 overflow-hidden border-l border-white/10 bg-surface-container p-4 shadow-2xl md:p-5"
            >
              <div className="flex items-start justify-between gap-4 border-b border-white/5 pb-4">
                <div>
                  <p className="font-label-caps text-xs text-primary-fixed-dim">ValorAI Copilot</p>
                  <h2 className="mt-1 font-body-md text-on-surface">Property intelligence layer</h2>
                </div>
                <button
                  type="button"
                  aria-label="Close Copilot"
                  title="Close"
                  onClick={() => setIsOpen(false)}
                  className="rounded-md border border-white/10 bg-surface/30 p-2 text-on-surface-variant hover:text-primary-fixed-dim"
                >
                  <PanelRightClose className="h-4 w-4" />
                </button>
              </div>

              <div className="min-h-0">
                <CopilotPanel />
              </div>
            </motion.aside>
          </div>
        )}
      </AnimatePresence>
    </>
  );
}
