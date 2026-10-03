# Web Application (`apps/web`)

**Purpose:** Next.js 15 (App Router) + React 19 + TypeScript + Tailwind CSS 4 frontend for Cofunder, featuring the **Inter** font family, the Approvals Inbox for human-in-the-loop review, and the Venture Dashboard.

## Files
- `app/layout.tsx` — Root layout configuring Next.js Inter font variable (`--font-inter`).
- `app/page.tsx` — Main operating console page.
- `app/globals.css` — Tailwind CSS 4 theme tokens.
- `components/approvals-inbox.tsx` — Human-in-the-loop review queue for gated tool executions.
- `components/venture-card.tsx` — Venture profile, milestones, and financial budget caps.

## Module Index
<!-- BEGIN GENERATED -->

### Files & Manifest

- *No python files found in module.*


<!-- END GENERATED -->

## Development
```bash
bun install
bun run dev
```

## Production Build
```bash
bun run build
```
