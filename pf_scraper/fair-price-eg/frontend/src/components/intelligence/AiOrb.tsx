import * as React from "react";
import { AnimatePresence, motion } from "framer-motion";
import { premiumEase } from "@/animations/motion";
import { cn } from "@/lib/utils";

export type OrbState = "idle" | "thinking" | "analyzing" | "responding";

interface AiOrbProps {
  className?: string;
  size?: "sm" | "md" | "lg" | "xl";
  state?: OrbState;
}

export function AiOrb({ className, size = "md", state = "idle", ...props }: AiOrbProps) {
  const sizeClasses = {
    sm: "w-8 h-8",
    md: "w-16 h-16",
    lg: "w-32 h-32",
    xl: "w-64 h-64",
  };

  const coreStyles = {
    idle: "bg-surface-tint shadow-[0_2px_8px_rgba(0,219,231,0.12)]",
    thinking: "bg-gradient-to-br from-tertiary-fixed-dim/55 to-primary-fixed-dim/25 shadow-[0_2px_12px_rgba(111,251,190,0.16)]",
    analyzing: "bg-gradient-to-br from-secondary-fixed/45 to-primary-fixed/25 shadow-[0_2px_14px_rgba(225,224,255,0.16)]",
    responding: "bg-gradient-to-br from-primary-fixed/65 to-primary-container/55 shadow-[0_4px_22px_rgba(0,219,231,0.22)]",
  } satisfies Record<OrbState, string>;

  const glowStyles = {
    idle: "bg-primary-fixed-dim/5 blur-[18px]",
    thinking: "bg-tertiary-fixed-dim/10 blur-[26px]",
    analyzing: "bg-secondary-fixed/10 blur-[22px]",
    responding: "bg-primary-fixed/12 blur-[34px]",
  } satisfies Record<OrbState, string>;

  return (
    <motion.div
      layout
      variants={{
        idle: { scale: 1 },
        thinking: { scale: [1, 1.015, 1] },
        analyzing: { scale: [1, 0.985, 1] },
        responding: { scale: [1, 1.02, 1] },
      }}
      animate={state}
      transition={{ 
        scale: { repeat: Infinity, duration: state === "analyzing" ? 3.2 : 5.2, ease: "easeInOut" },
        layout: { duration: 1.2, ease: premiumEase }
      }}
      className={cn("relative flex items-center justify-center rounded-full", sizeClasses[size], className)}
      {...props}
    >
      <motion.div
        layout
        className={cn("absolute inset-0 rounded-full transition-all duration-1000", glowStyles[state])}
      />
      <div
        className={cn(
          "absolute h-3/4 w-3/4 rounded-full mix-blend-screen opacity-60 orb-pulse transition-all duration-1000",
          state === "idle" ? "bg-gradient-to-br from-primary-container/30 to-secondary-container/30 blur-md" : "bg-white/5 blur-lg",
        )}
      />
      <motion.div layout className={cn("relative h-1/2 w-1/2 rounded-full transition-all duration-1000", coreStyles[state])} />
      <motion.div
        animate={{ rotate: state === "analyzing" ? 360 : 180 }}
        transition={{ duration: state === "analyzing" ? 34 : 68, repeat: Infinity, ease: "linear" }}
        className={cn(
          "absolute inset-0 rounded-full border transition-colors duration-1000",
          state === "thinking"
            ? "border-tertiary-fixed-dim/10"
            : state === "analyzing"
              ? "border-secondary-fixed/10"
              : "border-primary-fixed-dim/5",
        )}
      />
      <motion.div
        animate={{ rotate: state === "analyzing" ? -360 : -180 }}
        transition={{ duration: state === "analyzing" ? 44 : 88, repeat: Infinity, ease: "linear" }}
        className={cn(
          "absolute -inset-2 rounded-full border border-dashed transition-colors duration-1000",
          state === "thinking"
            ? "border-tertiary-fixed/10"
            : state === "analyzing"
              ? "border-secondary-fixed/10"
              : "border-secondary-fixed/5",
        )}
      />
      <AnimatePresence>
        {state === "thinking" && (
          <motion.div
            initial={{ opacity: 0, scale: 0.7 }}
            animate={{ opacity: [0, 0.35, 0], scale: [0.7, 1.08, 0.7] }}
            exit={{ opacity: 0 }}
            transition={{ repeat: Infinity, duration: 4, ease: "easeInOut" }}
            className="absolute inset-0 rounded-full border border-tertiary-fixed-dim/20 mix-blend-screen"
          />
        )}
      </AnimatePresence>
    </motion.div>
  );
}
