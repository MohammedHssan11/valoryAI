# SPA Routing Policy

ValorAI uses React Router with `BrowserRouter`, Vite, Docker, and nginx. SPA routes must never reuse top-level URL segments that can be served as physical directories or server-owned endpoints in production.

## Allowed route names

Use product-domain route names:

| Route | Status |
| --- | --- |
| `/properties` | Allowed |
| `/market-intelligence` | Allowed |
| `/broker-center` | Allowed |
| `/user-settings` | Allowed |
| `/portfolio` | Allowed |

## Reserved route names

Do not create SPA routes whose first path segment is any of:

| Segment | Why |
| --- | --- |
| `/assets` | Vite build output commonly creates `dist/assets`. |
| `/static` | Common public/static deployment directory. |
| `/images` | Common public asset directory. |
| `/fonts` | Common public asset directory. |
| `/icons` | Common public asset directory. |
| `/media` | Common generated or uploaded asset directory. |
| `/uploads` | Common uploaded asset directory. |
| `/chunks` | Common bundler chunk directory. |
| `/build` | Common generated output directory. |
| `/vendor` | Common bundled third-party asset directory. |
| `/dist` | Build output name. |
| `/public` | Source directory name that can leak into deployments. |
| `/v1` | Backend API proxy prefix. |
| `/api` | Reserved for future API proxying. |
| `/health` | Backend/container health endpoints. |

Root files such as `/favicon.ico`, `/robots.txt`, and `/manifest.json` are also server-reserved and must not become SPA routes.

## Enforcement

- Route constants live in `frontend/src/navigation/routes.ts`.
- Navigation tabs must use `APP_ROUTES` from that file.
- `npm run test` runs the route policy test and the collision detector.
- `npm run check:routes` prints the route inventory, physical directory risk inventory, and collision table.

## Nginx policy

The SPA fallback must not use `$uri/` because that asks nginx to resolve physical directories before serving `index.html`. Static files are served only through explicit file locations. All other browser routes fall through directly to `/index.html`.
