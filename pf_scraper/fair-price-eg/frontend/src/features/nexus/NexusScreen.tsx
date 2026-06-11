import * as React from "react";
import { AiOrb } from "@/components/intelligence/AiOrb";
import { GlassCard } from "@/components/ui/glass";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import { APP_ROUTES } from "@/navigation/routes";

export function NexusScreen() {
  const [orbState, setOrbState] = React.useState<"idle" | "thinking" | "analyzing" | "responding">("idle");
  const navigate = useNavigate();
  const openValuation = React.useCallback(() => navigate(APP_ROUTES.valuation), [navigate]);

  React.useEffect(() => {
    const t1 = setTimeout(() => setOrbState("thinking"), 1000);
    const t2 = setTimeout(() => setOrbState("idle"), 4000);
    return () => { clearTimeout(t1); clearTimeout(t2); };
  }, []);

  return (
    <div className="flex flex-col items-center justify-center relative w-full h-full min-h-[80vh]">
      <div className="absolute inset-0 z-0 flex items-center justify-center pointer-events-none opacity-20">
        <div className="w-[800px] h-[800px] bg-primary-fixed/10 rounded-full blur-[120px]" />
      </div>

      <div className="relative z-20 flex flex-col items-center text-center mt-12 md:mt-0">
        <motion.div 
           initial={{ scale: 0.9, opacity: 0, filter: "blur(15px)", y: 20 }}
           animate={{ scale: 1, opacity: 1, filter: "blur(0px)", y: 0 }}
           transition={{ duration: 1.5, ease: [0.22, 1, 0.36, 1] }} 
           className="mb-10 relative"
        >
          <div className="absolute inset-0 bg-primary-fixed-dim/5 blur-[50px] animate-pulse rounded-full" />
          <AiOrb size="lg" state={orbState} />
        </motion.div>
        
        <motion.h1 
          initial={{ opacity: 0, y: 20, filter: "blur(10px)" }} 
          animate={{ opacity: 1, y: 0, filter: "blur(0px)" }} 
          transition={{ delay: 0.3, duration: 1.2, ease: [0.22, 1, 0.36, 1] }}
          className="font-display-lg text-display-lg text-on-surface mb-4 drop-shadow-sm"
        >
          Good Morning, <span className="text-primary-fixed drop-shadow-[0_4px_18px_rgba(0,219,231,0.18)]">Investor</span>.
        </motion.h1>
        
        <motion.div 
          initial={{ opacity: 0, filter: "blur(4px)", scale: 0.95 }} 
          animate={{ opacity: 1, filter: "blur(0px)", scale: 1 }} 
          transition={{ delay: 0.6, duration: 1, ease: [0.22, 1, 0.36, 1] }}
          className="bg-surface/30 backdrop-blur-md px-6 py-2 rounded-full border border-white/5 inline-flex items-center gap-2 mx-auto shadow-[0_8px_30px_rgba(0,0,0,0.5)]"
        >
          <span className="w-1.5 h-1.5 rounded-full bg-primary-fixed-dim animate-pulse" />
          <p className="font-body-md text-on-surface-variant leading-relaxed text-sm">
            Valuation engine connected. Market intelligence services are ready for backend data contracts.
          </p>
        </motion.div>
      </div>

      <motion.div 
        initial={{ opacity: 0, y: 30, filter: "blur(8px)" }} 
        animate={{ opacity: 1, y: 0, filter: "blur(0px)" }} 
        transition={{ delay: 0.6, duration: 1.2, ease: [0.22, 1, 0.36, 1] }}
        className="w-full max-w-5xl mt-16 z-20 grid grid-cols-1 md:grid-cols-3 gap-6 px-4"
      >
        <GlassCard className="p-6 relative overflow-hidden group">
          <div className="absolute top-0 right-0 p-4 opacity-20 group-hover:opacity-100 transition-opacity">
            <span className="material-symbols-outlined text-primary">water_drop</span>
          </div>
          <h3 className="font-label-caps text-on-surface-variant mb-4">Connected Intelligence</h3>
          
          <div className="flex flex-col gap-3">
            <div className="flex justify-between items-center">
              <span className="font-body-md text-on-surface">Fair-price API</span>
              <span className="font-data-tabular text-tertiary-fixed-dim">LIVE</span>
            </div>
            <div className="w-full bg-surface-container h-1 rounded-full overflow-hidden">
              <div className="bg-tertiary-fixed h-full w-full shadow-[0_0_6px_rgba(111,251,190,0.28)]" />
            </div>
            
            <div className="flex justify-between items-center mt-2">
              <span className="font-body-md text-on-surface">Explainability trace</span>
              <span className="font-data-tabular text-primary-fixed-dim">LIVE</span>
            </div>
            <div className="w-full bg-surface-container h-1 rounded-full overflow-hidden">
              <div className="bg-primary-fixed-dim h-full w-full shadow-[0_0_6px_rgba(0,219,231,0.28)]" />
            </div>
          </div>
        </GlassCard>

        <GlassCard className="p-6 relative overflow-hidden md:col-span-2 group flex flex-col justify-between border-l border-t border-tertiary-fixed-dim/30">
          <div className="absolute top-0 right-0 w-32 h-32 bg-tertiary-fixed/5 rounded-full blur-2xl -mr-10 -mt-10" />
          <div>
            <h3 className="font-label-caps text-on-surface-variant mb-2">Production Focus</h3>
            <p className="font-headline-lg-mobile text-on-surface mb-1">Trustworthy valuation workflow</p>
            <p className="font-body-md text-outline">Comparable retrieval, confidence scoring, and deterministic explanations are now the primary product surface.</p>
          </div>
          <div className="mt-6 flex justify-end">
            <Button type="button" variant="holo" size="sm" className="hidden md:flex" onClick={openValuation}>
              OPEN VALUATION <span className="material-symbols-outlined text-sm">radar</span>
            </Button>
            <Button type="button" variant="solid" size="sm" className="md:hidden" onClick={openValuation}>
              OPEN VALUATION
            </Button>
          </div>
        </GlassCard>
      </motion.div>
    </div>
  );
}
