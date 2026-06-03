export type NavTab = "nexus" | "broker" | "pulse" | "assets" | "vault";

export interface NavTabDefinition {
  id: NavTab;
  path: string;
  icon: string;
  label: string;
}

export const NAV_TABS: NavTabDefinition[] = [
  { id: "nexus", path: "/nexus", icon: "analytics", label: "Nexus" },
  { id: "broker", path: "/broker", icon: "explore", label: "Broker" },
  { id: "pulse", path: "/pulse", icon: "map", label: "Pulse" },
  { id: "assets", path: "/assets", icon: "real_estate_agent", label: "Assets" },
  { id: "vault", path: "/vault", icon: "account_balance_wallet", label: "Vault" },
];

export function tabFromPath(pathname: string): NavTab {
  return NAV_TABS.find((tab) => pathname.startsWith(tab.path))?.id ?? "nexus";
}

