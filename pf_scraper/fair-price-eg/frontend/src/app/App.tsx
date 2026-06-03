import { Navigate, Route, Routes } from "react-router-dom";
import { AppProviders } from "@/app/AppProviders";
import { AppShell } from "@/layouts/AppShell";
import { AssetsScreen } from "@/features/assets/AssetsScreen";
import { BrokerScreen } from "@/features/broker/BrokerScreen";
import { NexusScreen } from "@/features/nexus/NexusScreen";
import { PulseScreen } from "@/features/pulse/PulseScreen";
import { ValuationScreen } from "@/features/valuation/ValuationScreen";
import { VaultScreen } from "@/features/vault/VaultScreen";

function AppRoutes() {
  return (
    <Routes>
      <Route element={<AppShell />}>
        <Route index element={<Navigate to="/nexus" replace />} />
        <Route path="nexus" element={<NexusScreen />} />
        <Route path="broker" element={<BrokerScreen />} />
        <Route path="valuation" element={<ValuationScreen />} />
        <Route path="pulse" element={<PulseScreen />} />
        <Route path="assets" element={<AssetsScreen />} />
        <Route path="vault" element={<VaultScreen />} />
        <Route path="*" element={<Navigate to="/nexus" replace />} />
      </Route>
    </Routes>
  );
}

export default function App() {
  return (
    <AppProviders>
      <AppRoutes />
    </AppProviders>
  );
}
