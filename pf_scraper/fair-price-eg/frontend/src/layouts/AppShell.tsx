import * as React from "react";
import { AnimatePresence } from "framer-motion";
import { Outlet, useLocation } from "react-router-dom";
import { BottomNav } from "@/components/layout/BottomNav";
import { TopNav } from "@/components/layout/TopNav";
import { tabFromPath } from "@/navigation/tabs";
import { useNavigationStore } from "@/store/navigationStore";
import { ScreenTransition } from "./ScreenTransition";

export function AppShell() {
  const location = useLocation();
  const setTab = useNavigationStore((state) => state.setTab);

  React.useEffect(() => {
    setTab(tabFromPath(location.pathname));
  }, [location.pathname, setTab]);

  return (
    <div className="relative flex min-h-screen flex-col overflow-x-hidden bg-background font-body-md text-on-background selection:bg-primary-container selection:text-on-primary-container">
      <TopNav />
      <BottomNav />
      <main className="relative z-10 flex w-full flex-1">
        <AnimatePresence mode="wait">
          <ScreenTransition key={location.pathname}>
            <Outlet />
          </ScreenTransition>
        </AnimatePresence>
      </main>
    </div>
  );
}

