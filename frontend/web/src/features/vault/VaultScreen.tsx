import * as React from "react";
import { GlassCard, GlassPanel } from "@/components/ui/glass";
import { motion } from "framer-motion";

export function VaultScreen() {
  return (
    <motion.div 
      initial="hidden"
      animate="show"
      variants={{
        hidden: { opacity: 0 },
        show: {
          opacity: 1,
          transition: { staggerChildren: 0.2 }
        }
      }}
      className="w-full max-w-6xl mx-auto flex flex-col gap-8 p-4 pt-8"
    >
      <motion.div 
        variants={{
          hidden: { opacity: 0, y: 10, filter: "blur(4px)" },
          show: { opacity: 1, y: 0, filter: "blur(0px)", transition: { duration: 0.8, ease: [0.22, 1, 0.36, 1] } }
        }}
        className="text-left space-y-2 mb-4"
      >
        <h1 className="font-headline-lg-mobile md:font-headline-lg text-primary drop-shadow-sm">Intelligence Matrix</h1>
        <p className="font-body-md text-on-surface-variant max-w-2xl">Your persistent cognitive context. Analyzing risk appetite across <strong className="text-on-surface">14,021</strong> global data points.</p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <motion.div 
          variants={{
            hidden: { opacity: 0, scale: 0.98, filter: "blur(4px)" },
            show: { opacity: 1, scale: 1, filter: "blur(0px)", transition: { duration: 0.8, ease: [0.22, 1, 0.36, 1] } }
          }}
          className="lg:col-span-8 flex flex-col h-full"
        >
            <GlassCard className="p-6 min-h-[300px] flex flex-col h-full">
                <div className="flex justify-between items-start mb-6">
                    <div>
                        <h3 className="font-body-md text-on-surface font-semibold mb-1">Neural Property Linking</h3>
                        <p className="font-label-caps text-outline">Real-time intent mapping</p>
                    </div>
                    <div className="flex items-center gap-2 bg-primary/10 px-3 py-1.5 rounded-full border border-primary/20">
                        <div className="w-2 h-2 rounded-full bg-tertiary-fixed-dim animate-[pulse_2s_infinite]" />
                        <span className="font-label-caps text-[10px] text-tertiary-fixed-dim">SYNCED</span>
                    </div>
                </div>
                
                <div className="mt-auto grid grid-cols-3 gap-4 border-t border-white/5 pt-6">
                    <div className="bg-surface/30 p-3 rounded-lg border border-white/5 hover:bg-surface/50 transition-colors">
                        <span className="font-label-caps text-[10px] text-outline block mb-1">VIEWED ASSETS</span>
                        <span className="font-data-tabular text-primary-fixed text-lg drop-shadow-[0_0_6px_rgba(0,219,231,0.18)]">1,402</span>
                    </div>
                    <div className="bg-surface/30 p-3 rounded-lg border border-white/5 hover:bg-surface/50 transition-colors">
                        <span className="font-label-caps text-[10px] text-outline block mb-1">PATTERN MATCH</span>
                        <span className="font-data-tabular text-tertiary-fixed text-lg drop-shadow-[0_0_6px_rgba(78,222,163,0.18)]">94.2%</span>
                    </div>
                    <div className="bg-surface/30 p-3 rounded-lg border border-white/5 hover:bg-surface/50 transition-colors">
                        <span className="font-label-caps text-[10px] text-outline block mb-1">RISK DEVIATION</span>
                        <span className="font-data-tabular text-error text-lg">+1.4%</span>
                    </div>
                </div>
            </GlassCard>
        </motion.div>

        <motion.div 
          variants={{
            hidden: { opacity: 0, scale: 0.98, filter: "blur(4px)" },
            show: { opacity: 1, scale: 1, filter: "blur(0px)", transition: { duration: 0.8, ease: [0.22, 1, 0.36, 1] } }
          }}
          className="lg:col-span-4"
        >
            <GlassCard className="p-6 flex flex-col items-center justify-center text-center h-full">
                <div className="w-24 h-24 rounded-full bg-surface-container flex items-center justify-center mb-6 relative">
                    <div className="absolute inset-2 rounded-full border border-primary/40 animate-[spin_20s_linear_infinite]" />
                    <span className="material-symbols-outlined text-3xl text-primary drop-shadow-[0_0_10px_rgba(0,219,231,0.22)]">psychology</span>
                </div>
                <h3 className="font-body-md text-on-surface font-semibold mb-2">Aggressive Growth</h3>
                <p className="font-data-tabular text-outline-variant mb-6 text-sm">Active Strategy Directive</p>
                <button className="w-full bg-primary/10 border border-primary/30 text-primary-fixed-dim hover:bg-primary/20 transition-all py-3 rounded-lg font-label-caps text-xs hover:border-primary/50">
                    RECALIBRATE INTENT
                </button>
            </GlassCard>
        </motion.div>

        <motion.div 
          variants={{
            hidden: { opacity: 0, y: 10, filter: "blur(4px)" },
            show: { opacity: 1, y: 0, filter: "blur(0px)", transition: { duration: 0.8, ease: [0.22, 1, 0.36, 1] } }
          }}
          className="lg:col-span-6"
        >
            <GlassPanel className="p-6 h-full">
                <h3 className="font-label-caps text-primary mb-6 flex items-center gap-2">
                    <span className="material-symbols-outlined text-[16px]">saved_search</span>
                    Persisted Queries
                </h3>
                <div className="space-y-3">
                    <div className="flex items-center justify-between p-3 rounded-lg bg-surface/30 border border-white/5 hover:bg-surface/50 transition-colors cursor-pointer group">
                        <div className="flex items-center gap-3">
                            <div className="w-2 h-2 rounded-full bg-tertiary-fixed shadow-[0_0_6px_rgba(111,251,190,0.22)]" />
                            <div>
                                <p className="font-body-md text-on-surface text-sm">New Cairo Commercial Tier 1</p>
                                <p className="font-data-tabular text-[10px] text-outline flex items-center gap-1"><span className="material-symbols-outlined text-[12px] opacity-70">schedule</span> Last run 2h ago</p>
                            </div>
                        </div>
                        <span className="font-label-caps text-primary-fixed-dim text-xs opacity-50 group-hover:opacity-100 transition-opacity">RUN</span>
                    </div>
                    <div className="flex items-center justify-between p-3 rounded-lg bg-surface/30 border border-white/5 hover:bg-surface/50 transition-colors cursor-pointer group">
                        <div className="flex items-center gap-3">
                            <div className="w-2 h-2 rounded-full bg-secondary-fixed shadow-[0_0_6px_rgba(225,224,255,0.22)]" />
                            <div>
                                <p className="font-body-md text-on-surface text-sm">Zayed Luxury Residential</p>
                                <p className="font-data-tabular text-[10px] text-outline flex items-center gap-1"><span className="material-symbols-outlined text-[12px] opacity-70">schedule</span> Last run 1d ago</p>
                            </div>
                        </div>
                         <span className="font-label-caps text-primary-fixed-dim text-xs opacity-50 group-hover:opacity-100 transition-opacity">RUN</span>
                    </div>
                </div>
            </GlassPanel>
        </motion.div>

        <motion.div 
          variants={{
            hidden: { opacity: 0, y: 10, filter: "blur(4px)" },
            show: { opacity: 1, y: 0, filter: "blur(0px)", transition: { duration: 0.8, ease: [0.22, 1, 0.36, 1] } }
          }}
          className="lg:col-span-6"
        >
            <GlassPanel className="p-6 flex flex-col justify-between h-full">
                <div>
                     <h3 className="font-label-caps text-secondary mb-6 flex items-center gap-2">
                        <span className="material-symbols-outlined text-[16px]">picture_as_pdf</span>
                        Executive Valuation Reports
                    </h3>
                    <p className="font-body-md text-sm text-on-surface-variant mb-6">Generated reports are persisted securely. Ready for distribution.</p>
                </div>
               
                <div className="flex flex-col gap-3">
                    <div className="glass-card flex items-center justify-between p-4 rounded-lg bg-primary/5 cursor-pointer hover:bg-primary/10 transition-colors border border-primary/10 hover:border-primary/30">
                        <div className="flex items-center gap-3">
                             <span className="material-symbols-outlined text-primary-fixed-dim opacity-70">description</span>
                             <div>
                                <p className="font-data-tabular text-on-surface text-sm">Hexa Tower Penthouse</p>
                                <p className="font-label-caps text-outline text-[10px] mt-1">OCT 24, 2024</p>
                             </div>
                        </div>
                        <span className="material-symbols-outlined text-outline">download</span>
                    </div>
                </div>
            </GlassPanel>
        </motion.div>
      </div>
    </motion.div>
  );
}
