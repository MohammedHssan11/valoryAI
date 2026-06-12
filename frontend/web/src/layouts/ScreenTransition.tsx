import * as React from "react";
import { motion } from "framer-motion";
import { premiumEase, screenTransition } from "@/animations/motion";

export function ScreenTransition({ children, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <motion.div
      variants={screenTransition}
      initial="initial"
      animate="animate"
      exit="exit"
      transition={{ duration: 0.55, ease: premiumEase }}
      className="w-full flex-1 flex flex-col pt-24 pb-32 md:pl-72 max-w-[1600px] mx-auto overflow-x-hidden min-h-screen"
      {...props}
    >
      {children}
    </motion.div>
  );
}

