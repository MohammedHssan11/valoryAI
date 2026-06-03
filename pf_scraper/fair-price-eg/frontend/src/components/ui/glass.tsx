import * as React from "react";
import { cn } from "@/lib/utils";

const GlassCard = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & { floating?: boolean }
>(({ className, floating, ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      floating ? "glass-card-floating" : "glass-card",
      "rounded-lg",
      className
    )}
    {...props}
  />
));
GlassCard.displayName = "GlassCard";

const GlassPanel = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("glass-panel rounded-lg", className)}
    {...props}
  />
));
GlassPanel.displayName = "GlassPanel";

export { GlassCard, GlassPanel };
