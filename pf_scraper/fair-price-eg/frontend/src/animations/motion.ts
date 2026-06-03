import type { Variants } from "framer-motion";

export const premiumEase = [0.22, 1, 0.36, 1] as const;
export const measuredTransition = { duration: 0.58, ease: premiumEase } as const;

export const screenTransition: Variants = {
  initial: { opacity: 0, scale: 0.99, filter: "blur(6px)" },
  animate: { opacity: 1, scale: 1, filter: "blur(0px)" },
  exit: { opacity: 0, scale: 1.006, filter: "blur(6px)" },
};

export const stagedReveal: Variants = {
  hidden: { opacity: 1 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.07,
      delayChildren: 0.04,
    },
  },
};

export const revealItem: Variants = {
  hidden: { opacity: 0, y: 10, filter: "blur(4px)" },
  show: {
    opacity: 1,
    y: 0,
    filter: "blur(0px)",
    transition: measuredTransition,
  },
};

export const valuationReveal: Variants = {
  hidden: { opacity: 0, y: 14, scale: 0.99, filter: "blur(8px)" },
  show: {
    opacity: 1,
    y: 0,
    scale: 1,
    filter: "blur(0px)",
    transition: { duration: 0.68, ease: premiumEase },
  },
};

export const confidenceFillTransition = { duration: 0.72, ease: premiumEase } as const;
