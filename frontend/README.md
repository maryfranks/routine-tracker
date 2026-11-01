# Frontend Architecture & Development

The frontend application is built using React and bundled with Vite, leveraging TanStack Router for file-based routing and shadcn/ui for component styling. It communicates with the Python FastAPI backend via asynchronous REST application programming interface (API) requests.

## Requirements

| Tool | Version | Purpose |
| --- | --- | --- |
| Node.js | 22.23.4 (`.nvmrc`, `engines.node`) | Runtime environment for the development server |
| Bun | 1.4.4 (`packageManager`, `engines.bun`) | Package management (`bun.lock` pins every package) |

Dependency versions pin strictly via `bun.lock`. Installing packages with Bun reproduces the project environment precisely, whereas installing with Node Package Manager (npm) re-resolves from version ranges in `package.json` and may introduce drift.

## Local Development

```sh
git clone <repository-url>
cd frontend

# If Node Version Manager (nvm) is installed, pick up .nvmrc automatically
nvm install && nvm use

# Install Bun (macOS / Linux)
curl -fsSL https://bun.sh/install | bash

bun install
bun run dev
```

Open the development server URL in the browser (typically `http://localhost:5173`).

Alternatively, npm installation (`npm install && npm run dev`) is supported, though it ignores `bun.lock` and may pull newer patch versions.

## Available Scripts

| Command | Description |
| --- | --- |
| `bun run dev` | Start the development server |
| `bun run build` | Generate production build |
| `bun run preview` | Serve the production build locally |
| `bun test` | Execute the test suite using Vitest |
| `bun run lint` | Run ESLint for code linting |
| `bun run format` | Format code with Prettier |

## Technology Stack

- Node.js 22
- TypeScript (TS) 5.8
- React 19
- TanStack Start 1.168 (routing and server functions)
- Vite 8
- Tailwind CSS 4
- shadcn/ui (New York style component library located in `src/components/ui/`)
- Vitest 4

## User Interface (UI) Components (shadcn/ui)

UI components are managed via shadcn/ui (`components.json`). To add new components:
```sh
bun x shadcn add <component-name>
```

## Routing Conventions

TanStack Start utilizes **file-based routing**. Every `.tsx` file within `src/routes/` defines a route. Avoid creating `src/pages/`, `src/routes/_app/index.tsx`, or `app/layout.tsx` (which belong to other framework conventions such as Next.js or Remix). The sole root layout is `src/routes/__root.tsx`.

### File-to-URL Mapping

| File | Uniform Resource Locator (URL) Path |
| --- | --- |
| `index.tsx` | `/` |
| `about.tsx` | `/about` |
| `users/index.tsx` | `/users` |
| `users/$id.tsx` | `/users/:id` (dynamic segment using bare `$`, without curly braces) |
| `posts/{-$category}.tsx` | `/posts/:category?` (optional segment) |
| `files/$.tsx` | `/files/*` (splat segment read via `_splat` parameter, never `*`) |
| `_layout.tsx` | Layout route rendering children via `<Outlet />` |
| `__root.tsx` | Application shell wrapping every page; preserves `<Outlet />` |

`routeTree.gen.ts` generates automatically and should not be edited manually.
