import { existsSync, readdirSync, statSync } from "node:fs";
import { resolve } from "node:path";
import { fileURLToPath } from "node:url";
import {
  APP_ROUTE_PATHS,
  RESERVED_TOP_LEVEL_PATH_SEGMENTS,
  topLevelPathSegment,
} from "../src/navigation/routes";

interface PhysicalDirectoryRisk {
  directory: string;
  existsToday: boolean;
  couldExistLater: boolean;
}

interface CollisionRisk {
  route: string;
  directory: string;
  risk: "current" | "future";
}

const frontendRoot = fileURLToPath(new URL("../", import.meta.url));

const STANDARD_PRODUCTION_DIRECTORIES = [
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

function directoryExists(directory: string): boolean {
  return existsSync(directory) && statSync(directory).isDirectory();
}

function physicalDirectoryRisks(): PhysicalDirectoryRisk[] {
  const directories = new Map<string, PhysicalDirectoryRisk>();

  for (const directory of STANDARD_PRODUCTION_DIRECTORIES) {
    directories.set(directory, {
      directory,
      existsToday: false,
      couldExistLater: true,
    });
  }

  for (const rootName of ["dist", "build"]) {
    const outputRoot = resolve(frontendRoot, rootName);
    for (const directory of listImmediateDirectories(outputRoot)) {
      directories.set(directory, {
        directory,
        existsToday: true,
        couldExistLater: true,
      });
    }
  }

  const publicRoot = resolve(frontendRoot, "public");
  for (const directory of listImmediateDirectories(publicRoot)) {
    directories.set(directory, {
      directory,
      existsToday: true,
      couldExistLater: true,
    });
  }

  for (const directory of STANDARD_PRODUCTION_DIRECTORIES) {
    if (directoryExists(resolve(frontendRoot, directory))) {
      directories.set(directory, {
        directory,
        existsToday: true,
        couldExistLater: true,
      });
    }
  }

  return Array.from(directories.values()).sort((a, b) => a.directory.localeCompare(b.directory));
}

function collisionRisks(directories: PhysicalDirectoryRisk[]): CollisionRisk[] {
  const physicalDirectories = new Map(directories.map((directory) => [directory.directory, directory]));
  const reservedSegments = new Set<string>(RESERVED_TOP_LEVEL_PATH_SEGMENTS);
  const risks: CollisionRisk[] = [];

  for (const route of APP_ROUTE_PATHS) {
    const segment = topLevelPathSegment(route);
    const physicalDirectory = physicalDirectories.get(segment);

    if (physicalDirectory) {
      risks.push({
        route,
        directory: segment,
        risk: physicalDirectory.existsToday ? "current" : "future",
      });
      continue;
    }

    if (reservedSegments.has(segment)) {
      risks.push({
        route,
        directory: segment,
        risk: "future",
      });
    }
  }

  return risks;
}

const directories = physicalDirectoryRisks();
const collisions = collisionRisks(directories);

console.log("Routes");
console.table(APP_ROUTE_PATHS.map((route) => ({ route, topLevelSegment: topLevelPathSegment(route) })));

console.log("Physical directory risk inventory");
console.table(
  directories.map((directory) => ({
    directory: directory.directory,
    existsToday: directory.existsToday ? "yes" : "no",
    couldExistLater: directory.couldExistLater ? "yes" : "no",
  })),
);

console.log("Route collision risks");
console.table(collisions);

if (collisions.length > 0) {
  console.error("SPA route collision policy failed.");
  process.exitCode = 1;
} else {
  console.log("No SPA route collisions detected.");
}
