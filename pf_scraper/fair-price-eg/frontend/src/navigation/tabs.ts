import { APP_ROUTES, type AppRoute } from "@/navigation/routes";

export type NavTab = "nexus" | "broker" | "pulse" | "properties" | "vault";

export interface NavTabDefinition {
  id: NavTab;
  path: AppRoute;
  icon: string;
  label: string;
}

export const NAV_TABS: NavTabDefinition[] = [
  { id: "nexus", path: APP_ROUTES.nexus, icon: "analytics", label: "Nexus" },
  { id: "broker", path: APP_ROUTES.broker, icon: "explore", label: "Broker" },
  { id: "pulse", path: APP_ROUTES.pulse, icon: "map", label: "Pulse" },
  { id: "properties", path: APP_ROUTES.properties, icon: "real_estate_agent", label: "Properties" },
  { id: "vault", path: APP_ROUTES.vault, icon: "account_balance_wallet", label: "Vault" },
];

export function tabFromPath(pathname: string): NavTab {
  return NAV_TABS.find((tab) => pathname.startsWith(tab.path))?.id ?? "nexus";
}
