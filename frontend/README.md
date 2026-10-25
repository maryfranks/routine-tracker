# Routine Tracker

A minimalist routine manager: views with a fixed cadence (daily / weekly / monthly),
tasks that reset cleanly at the end of each period with no rollover, and a history
log of past periods.

## Requirements

| Tool | Version | Why |
| --- | --- | --- |
| Node.js | 22.23.4 (`.nvmrc`, `engines.node`) | runtime for the dev server |
| Bun | 1.4.4 (`packageManager`, `engines.bun`) | reads `bun.lock`, which pins every package |

The exact dependency versions live in `bun.lock`. Installing with Bun reproduces
this project precisely; installing with npm re-resolves from the `^` ranges in
`package.json` and can drift to newer versions.

## Local development

```sh
git clone <this-repository-url>
cd <repository-name>

# if nvm is installed, this picks up .nvmrc automatically
nvm install && nvm use

# install Bun (macOS / Linux)
curl -fsSL https://bun.sh/install | bash

bun install
bun run dev
```

Open the URL the dev server prints (usually `http://localhost:8080`).

Prefer npm? `npm install && npm run dev` also works, but it ignores `bun.lock`
and may pull newer patch versions of the packages.

## Scripts

| Command | What it does |
| --- | --- |
| `bun run dev` | start the dev server |
| `bun run build` | production build |
| `bun run preview` | serve the production build |
| `bun test` | run the test suite |
| `bun run lint` | ESLint |
| `bun run format` | Prettier |

## Built with

- Node.js 22
- TypeScript 5.8
- React 19
- TanStack Start 1.168 (routing + server functions)
- Vite 8
- Tailwind CSS 4
- Vitest 4

## Notes

- No backend or database: all data is stored in the browser's `localStorage`.
- Demo data and a simulated clock can be toggled from the flask icon in the header.
