import * as React from "react";
import { GlassCard, GlassPanel } from "@/components/ui/glass";
import { motion, AnimatePresence } from "framer-motion";

export function PulseScreen() {
  const [step, setStep] = React.useState(0);

  React.useEffect(() => {
    const t1 = setTimeout(() => setStep(1), 300);
    const t2 = setTimeout(() => setStep(2), 700);
    const t3 = setTimeout(() => setStep(3), 1100);
    return () => { clearTimeout(t1); clearTimeout(t2); clearTimeout(t3); };
  }, []);

  return (
    <div className="relative w-full h-full flex flex-col md:flex-row gap-6 px-4 py-6 md:p-8 flex-1 min-h-[80vh]">
      {/* Map Background (Simulated via overlay) */}
      <div className="absolute inset-0 z-[-1] overflow-hidden rounded-3xl mx-4 md:mx-8 mb-4 border border-white/5">
        <div className="absolute inset-0 bg-[#08090a] opacity-90 z-10" />
        <motion.img 
          initial={{ opacity: 0, scale: 1.05, filter: "blur(20px)" }}
          animate={{ opacity: 0.5, scale: 1, filter: "blur(0px)" }}
          transition={{ duration: 2.5, ease: [0.22, 1, 0.36, 1] }}
          src="https://lh3.googleusercontent.com/aida-public/AB6AXuC6wLMXLJCpqXt38fLbr9CwVxaeEchCREJKKhKvGmcLtHvmfXI8-hSbNaanSJKLyAMEalVQAnjWtXZ0DfPzjQtKFgr_mfAhBsVo3qvtbqAIxkaimOXOsOn9gbEolnCzXeD0PDE_K-0wv0i4k2RwTaxjuPvGIPEksSo1AHs8eOdAXsizFrCSV0IYoQWHRd-CYvP9HAbotNFrSJkgIfD69PeyTtOTmP8ZZ1AzDkJRY_civw0HQ-bH8dF6NAbiDq_m1jdYo_kLqS7F_MYK"
          className="w-full h-full object-cover mix-blend-screen mix-blend-luminosity"
          alt="Map Background"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-background via-background/40 to-transparent z-10 pointer-events-none" />
        
        <AnimatePresence>
          {step >= 1 && (
            <motion.div 
                initial={{ opacity: 0, scale: 0 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 1.5, type: "spring", bounce: 0.2 }}
                className="absolute top-[40%] left-[30%] z-20"
            >
                <div className="w-48 h-48 rounded-full bg-tertiary-fixed-dim/10 blur-[30px] animate-[pulse_3s_ease-in-out_infinite] absolute -ml-24 -mt-24 pointer-events-none" />
                <motion.div 
                  className="absolute inset-0 rounded-full border border-tertiary-fixed-dim/30"
                  animate={{ scale: [1, 2.5], opacity: [0.8, 0] }}
                  transition={{ repeat: Infinity, duration: 2.5, ease: "easeOut" }}
                />
                <div className="absolute inset-x-0 bottom-0 top-0 m-auto w-3 h-3 rounded-full bg-tertiary-fixed-dim shadow-[0_0_10px_rgba(78,222,163,0.32)]" />
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      <AnimatePresence>
        {step >= 2 && (
          <motion.div 
            initial={{ opacity: 0, x: -20, filter: "blur(8px)" }}
            animate={{ opacity: 1, x: 0, filter: "blur(0px)" }}
            transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
            className="w-full md:w-[380px]"
          >
            <GlassCard floating className="w-full h-fit p-6 flex flex-col gap-6 self-start pointer-events-auto">
              <div className="flex items-center justify-between border-b border-white/10 pb-4">
                <h2 className="font-label-caps text-primary-fixed-dim flex items-center gap-2">
                  <span className="material-symbols-outlined text-[18px]">radar</span>
                  Zone Analysis
                </h2>
                <div className="flex gap-2">
                  <button className="w-8 h-8 rounded-full border border-primary/20 flex items-center justify-center text-primary-fixed-dim hover:bg-primary/10">
                    <span className="material-symbols-outlined text-[16px]">filter_list</span>
                  </button>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <GlassPanel className="p-4 flex flex-col gap-2 relative overflow-hidden group border-white/5 shadow-[0_4px_15px_rgba(0,0,0,0.5)]">
                  <div className="absolute left-0 top-0 w-1 h-full bg-primary-fixed-dim opacity-50 transition-opacity" />
                  <span className="font-label-caps text-[10px] text-on-surface-variant">Liquidity Index</span>
                  <span className="font-headline-lg-mobile text-primary drop-shadow-[0_0_8px_rgba(0,219,231,0.18)]">94.2</span>
                  <div className="flex items-center gap-1 text-tertiary-fixed-dim font-data-tabular justify-start text-xs">
                    <span className="material-symbols-outlined text-[14px]">trending_up</span> +2.4%
                  </div>
                </GlassPanel>
                <GlassPanel className="p-4 flex flex-col gap-2 relative overflow-hidden group border-white/5 shadow-[0_4px_15px_rgba(0,0,0,0.5)]">
                  <div className="absolute left-0 top-0 w-1 h-full bg-tertiary-fixed-dim opacity-50 transition-opacity" />
                  <span className="font-label-caps text-[10px] text-on-surface-variant">Yield Var</span>
                  <span className="font-headline-lg-mobile text-on-surface">12.8%</span>
                  <div className="flex items-center gap-1 text-tertiary-fixed-dim font-data-tabular justify-start text-xs">
                    <span className="material-symbols-outlined text-[14px]">trending_up</span> +0.8%
                  </div>
                </GlassPanel>
              </div>

              <div className="flex flex-col gap-3">
                <h3 className="font-label-caps text-[10px] text-on-surface-variant">Intensity Spectrum</h3>
                <div className="h-1.5 w-full rounded-full bg-gradient-to-r from-surface-variant via-primary-fixed-dim/50 to-primary-fixed" />
                <div className="flex justify-between font-data-tabular text-[10px] text-on-surface-variant">
                  <span>Low Signal</span>
                  <span>Peak Action</span>
                </div>
              </div>

              <div className="flex flex-col gap-4 mt-2">
                <h3 className="font-label-caps text-[10px] text-on-surface-variant flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-error animate-[pulse_2s_infinite]" /> Live Anomalies
                </h3>
                <div className="flex flex-col gap-3">
                  <div className="bg-surface/30 p-3 rounded-lg border-l-2 border-l-tertiary-fixed flex flex-col gap-1 cursor-pointer hover:bg-surface/50 transition-colors shadow-sm">
                    <div className="flex justify-between items-center">
                      <span className="font-label-caps text-[10px] text-tertiary-fixed-dim drop-shadow-[0_0_6px_rgba(78,222,163,0.18)]">BUY SIGNAL</span>
                      <span className="font-data-tabular text-[10px] text-on-surface-variant">1m ago</span>
                    </div>
                    <p className="font-body-md text-sm text-on-surface">Massive capital inflow detected in District 5.</p>
                  </div>
                </div>
              </div>
            </GlassCard>
          </motion.div>
        )}
      </AnimatePresence>
      
      <AnimatePresence>
        {step >= 3 && (
          <motion.div 
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
            className="flex-1 flex flex-col justify-end items-end pointer-events-none pb-10 pr-4 z-10"
          >
            <div className="glass-panel pointer-events-auto rounded-full p-1 flex shadow-lg border border-white/10 mt-auto backdrop-blur-xl bg-surface/30">
                <button className="px-6 py-2 rounded-full bg-primary/20 text-primary-fixed-dim font-label-caps text-[10px] transition-colors hover:bg-primary/30">VALUATION</button>
                <button className="px-6 py-2 rounded-full text-on-surface-variant hover:text-on-surface font-label-caps text-[10px] transition-colors">LIQUIDITY</button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
