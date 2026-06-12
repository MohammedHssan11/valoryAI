import * as React from "react";
import { useNavigate } from "react-router-dom";
import { NAV_TABS } from "@/navigation/tabs";
import { useNavigation } from "@/store/navigationStore";
import { cn } from "@/lib/utils";

export function BottomNav() {
  const { currentTab, setTab } = useNavigation();
  const navigate = useNavigate();

  const selectTab = (tab: (typeof NAV_TABS)[number]) => {
    setTab(tab.id);
    navigate(tab.path);
  };

  return (
    <>
      {/* Mobile nav */}
      <nav className="fixed bottom-0 left-0 z-50 flex w-full items-center justify-around rounded-t-xl border-t border-white/5 bg-surface-container-lowest/86 px-6 pb-[calc(1rem+env(safe-area-inset-bottom))] pt-4 shadow-[0_-10px_34px_rgba(0,0,0,0.36)] backdrop-blur-2xl md:hidden">
        {NAV_TABS.map((tab) => {
          const isActive = currentTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => selectTab(tab)}
              aria-label={tab.label}
              aria-current={isActive ? "page" : undefined}
              className={cn(
                "flex flex-col items-center justify-center p-3 transition-all",
                isActive
                  ? "bg-primary/10 text-primary-fixed-dim rounded-full shadow-[0_0_12px_rgba(0,219,231,0.18)] scale-105 duration-500 ease-out"
                  : "text-outline hover:text-primary-fixed"
              )}
            >
              <span 
                className="material-symbols-outlined text-[24px]"
                style={{ fontVariationSettings: isActive ? "'FILL' 1" : "'FILL' 0" }}
              >
                {tab.icon}
              </span>
            </button>
          );
        })}
      </nav>

      {/* Desktop side nav (partial, shown on larger screens) */}
      <aside className="fixed inset-y-0 left-0 z-[40] hidden w-72 flex-col rounded-r-xl border-r border-primary/15 bg-surface-dim/94 p-6 pt-32 shadow-2xl shadow-primary/5 backdrop-blur-3xl md:flex">
        <div className="flex flex-col gap-2">
           {NAV_TABS.map((tab) => {
            const isActive = currentTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => selectTab(tab)}
                aria-current={isActive ? "page" : undefined}
                className={cn(
                  "flex items-center gap-4 p-3 rounded-lg transition-all duration-300 text-left",
                  isActive
                    ? "bg-secondary-container/30 text-secondary-fixed border-l-4 border-secondary-fixed pl-4"
                    : "text-on-surface-variant hover:bg-white/5 hover:pl-4 hover:text-primary-fixed"
                )}
              >
                <span className="material-symbols-outlined" style={{ fontVariationSettings: isActive ? "'FILL' 1" : "'FILL' 0" }}>
                  {tab.icon}
                </span>
                <span className="font-body-md whitespace-nowrap uppercase text-sm font-medium">{tab.label}</span>
              </button>
            );
          })}
        </div>
      </aside>
    </>
  );
}
