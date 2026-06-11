import { Navigate, Route, Routes } from "react-router-dom";
import { AppProviders } from "@/app/AppProviders";
import { AppShell } from "@/layouts/AppShell";
import { AuthScreen } from "@/features/auth/AuthScreen";
import { ProtectedRoute } from "@/features/auth/ProtectedRoute";
import { BrokerScreen } from "@/features/broker/BrokerScreen";
import { NexusScreen } from "@/features/nexus/NexusScreen";
import { PropertiesScreen } from "@/features/properties/PropertiesScreen";
import { PulseScreen } from "@/features/pulse/PulseScreen";
import { ValuationScreen } from "@/features/valuation/ValuationScreen";
import { VaultScreen } from "@/features/vault/VaultScreen";
import { APP_ROUTES, DEFAULT_AUTHENTICATED_ROUTE, routeToReactPath } from "@/navigation/routes";

function AppRoutes() {
  return (
    <Routes>
      <Route path={routeToReactPath(APP_ROUTES.login)} element={<AuthScreen />} />
      <Route element={<ProtectedRoute />}>
        <Route element={<AppShell />}>
          <Route index element={<Navigate to={DEFAULT_AUTHENTICATED_ROUTE} replace />} />
          <Route path={routeToReactPath(APP_ROUTES.nexus)} element={<NexusScreen />} />
          <Route path={routeToReactPath(APP_ROUTES.broker)} element={<BrokerScreen />} />
          <Route path={routeToReactPath(APP_ROUTES.valuation)} element={<ValuationScreen />} />
          <Route path={routeToReactPath(APP_ROUTES.pulse)} element={<PulseScreen />} />
          <Route path={routeToReactPath(APP_ROUTES.properties)} element={<PropertiesScreen />} />
          <Route path={routeToReactPath(APP_ROUTES.vault)} element={<VaultScreen />} />
          <Route path="*" element={<Navigate to={DEFAULT_AUTHENTICATED_ROUTE} replace />} />
        </Route>
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
