export const RESERVED_TOP_LEVEL_PATH_SEGMENTS = [
  "api",
  "assets",
  "build",
  "chunks",
  "dist",
  "favicon.ico",
  "fonts",
  "health",
  "icons",
  "images",
  "img",
  "manifest.json",
  "media",
  "public",
  "robots.txt",
  "static",
  "uploads",
  "v1",
  "vendor",
] as const;

export type ReservedTopLevelPathSegment = (typeof RESERVED_TOP_LEVEL_PATH_SEGMENTS)[number];

export const APP_ROUTES = {
  login: "/login",
  nexus: "/nexus",
  broker: "/broker",
  valuation: "/valuation",
  pulse: "/pulse",
  properties: "/properties",
  vault: "/vault",
} as const;

export type AppRoute = (typeof APP_ROUTES)[keyof typeof APP_ROUTES];

export const DEFAULT_AUTHENTICATED_ROUTE = APP_ROUTES.nexus;
export const APP_ROUTE_PATHS = Object.values(APP_ROUTES);

export function routeToReactPath(route: AppRoute): string {
  return route.replace(/^\/+/, "");
}

export function topLevelPathSegment(path: string): string {
  const normalized = path.trim().replace(/^\/+/, "");
  return normalized.split(/[/?#]/, 1)[0]?.toLowerCase() ?? "";
}

export function isReservedTopLevelPath(path: string): boolean {
  const segment = topLevelPathSegment(path);
  return RESERVED_TOP_LEVEL_PATH_SEGMENTS.includes(segment as ReservedTopLevelPathSegment);
}

export function findReservedRouteCollisions(routes: readonly string[] = APP_ROUTE_PATHS): string[] {
  return routes.filter(isReservedTopLevelPath);
}

export function assertNoReservedRouteCollisions(routes: readonly string[] = APP_ROUTE_PATHS): void {
  const collisions = findReservedRouteCollisions(routes);

  if (collisions.length > 0) {
    throw new Error(
      `SPA routes cannot use production static, API, or server-reserved path segments: ${collisions.join(", ")}`,
    );
  }
}
