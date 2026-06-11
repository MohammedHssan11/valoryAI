import * as React from "react";
import { LogOut } from "lucide-react";
import { useAuth } from "@/auth/AuthProvider";
import { useNavigation } from "@/store/navigationStore";

export function TopNav() {
  const { currentTab } = useNavigation();
  const auth = useAuth();
  const initials = (auth.user?.display_name ?? "Investor")
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase())
    .join("") || "IN";

  return (
    <header className="fixed top-0 z-50 flex w-full items-center justify-between border-b border-white/10 bg-surface/68 px-4 py-4 shadow-[0_8px_30px_rgba(0,0,0,0.24)] backdrop-blur-xl md:px-10">
      <div className="flex items-center gap-2">
        <span className="material-symbols-outlined text-primary" style={{ fontVariationSettings: "'FILL' 1" }}>blur_on</span>
        <span className="font-headline-lg-mobile text-primary md:font-headline-lg">VALORAI</span>
      </div>
      
      <div className="flex items-center gap-4">
        <div className="hidden md:flex gap-6 font-label-caps text-on-surface-variant text-xs">
          {currentTab === 'broker' && <span className="text-primary-fixed-dim px-3 py-1 border border-primary-fixed-dim/30 rounded-full bg-primary/10">REASONING CONTEXT</span>}
          {currentTab === 'properties' && <span className="text-secondary-fixed">VALUATION ENGINE LIVE</span>}
        </div>
        
        <button
          type="button"
          aria-label="Sign out"
          title="Sign out"
          onClick={() => void auth.logout()}
          className="flex h-9 w-9 items-center justify-center rounded-full text-on-surface-variant transition-colors hover:bg-white/5 hover:text-primary-container"
        >
          <LogOut className="h-4 w-4" />
        </button>
        
        <div className="w-8 h-8 rounded-full bg-primary-container/20 border border-primary-fixed-dim flex items-center justify-center overflow-hidden relative" title={auth.user?.display_name ?? "Authenticated user"}>
          <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-primary-fixed-dim/40 via-transparent to-transparent animate-pulse" />
          <span className="font-label-caps text-primary text-[10px] relative z-10">{initials}</span>
        </div>
      </div>
    </header>
  );
}
