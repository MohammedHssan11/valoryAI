import { existsSync, readdirSync, statSync } from "node:fs";
import { resolve } from "node:path";
import {
  APP_ROUTE_PATHS,
  assertNoReservedRouteCollisions,
  topLevelPathSegment,
} from "./routes";

const frontendRoot = process.cwd();

const FORESEEABLE_STATIC_DIRECTORIES = [
  "assets",
  "build",
  "chunks",
  "fonts",
  "icons",
  "images",
  "img",
  "media",
  "public",
  "static",
  "uploads",
  "vendor",
] as const;

function listImmediateDirectories(directory: string): string[] {
  if (!existsSync(directory)) return [];

  return readdirSync(directory, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name.toLowerCase());
}

function existingProductionDirectories(): string[] {
  const directories = new Set<string>(FORESEEABLE_STATIC_DIRECTORIES);

  for (const outputRoot of ["dist", "build"]) {
    for (const directory of listImmediateDirectories(resolve(frontendRoot, outputRoot))) {
      directories.add(directory);
    }
  }

  for (const directory of listImmediateDirectories(resolve(frontendRoot, "public"))) {
    directories.add(directory);
  }

  for (const directory of FORESEEABLE_STATIC_DIRECTORIES) {
    const candidate = resolve(frontendRoot, directory);
    if (existsSync(candidate) && statSync(candidate).isDirectory()) {
      directories.add(directory);
    }
  }

  return Array.from(directories).sort();
}

describe("SPA route policy", () => {
  it("keeps app routes away from reserved production path segments", () => {
    expect(() => assertNoReservedRouteCollisions()).not.toThrow();
  });

  it("keeps app routes away from existing and foreseeable production directories", () => {
    const productionDirectories = new Set(existingProductionDirectories());
    const collisions = APP_ROUTE_PATHS.filter((route) => productionDirectories.has(topLevelPathSegment(route)));

    expect(collisions).toEqual([]);
  });

  it("fails closed for known static directory route names", () => {
    expect(() => assertNoReservedRouteCollisions([...APP_ROUTE_PATHS, "/assets"])).toThrow("/assets");
    expect(() => assertNoReservedRouteCollisions([...APP_ROUTE_PATHS, "/static"])).toThrow("/static");
    expect(() => assertNoReservedRouteCollisions([...APP_ROUTE_PATHS, "/images"])).toThrow("/images");
  });
});
