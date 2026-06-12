import * as React from "react";
import { cn } from "@/lib/utils";
import { motion, type HTMLMotionProps } from "framer-motion";

export interface ButtonProps extends HTMLMotionProps<"button"> {
  variant?: "holo" | "ghost" | "solid";
  size?: "sm" | "default" | "lg";
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "solid", size = "default", ...props }, ref) => {
    const variants = {
      holo: "btn-holo border border-primary text-primary-fixed-dim",
      ghost: "bg-surface/50 hover:bg-surface border border-white/5 hover:border-primary/30 text-on-surface",
      solid: "bg-primary hover:bg-primary-fixed text-on-primary shadow-[0_0_12px_rgba(0,219,231,0.14)] hover:shadow-[0_0_18px_rgba(0,219,231,0.22)]",
    };

    const sizes = {
      sm: "px-4 py-2 text-xs",
      default: "px-6 py-3",
      lg: "px-8 py-4 text-lg",
    };

    return (
      <motion.button
        ref={ref}
        whileTap={{ scale: 0.98 }}
        className={cn(
          "inline-flex items-center justify-center rounded-lg font-label-caps transition-colors duration-300 gap-2",
          variants[variant],
          sizes[size],
          className
        )}
        {...props}
      />
    );
  }
);
Button.displayName = "Button";

export { Button };
