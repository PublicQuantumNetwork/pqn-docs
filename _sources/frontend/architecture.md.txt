# Architecture

The frontend is a [Next.js](https://nextjs.org/) 16 application using the App Router with React 19, TypeScript, and Material-UI.

## Directory Structure

```
src/app/
├── layout.tsx          # Root layout: MUI theme, navigation bar
├── page.tsx            # Home page: experiment selection
├── calls.tsx           # Centralized API client (fetch wrappers for the Node API)
├── contexts/           # React contexts
│   └── PageRedirectContext.tsx
├── hooks/              # Custom React hooks
│   └── useWebSocket.ts # WebSocket hook for real-time experiment updates
├── components/         # Shared UI components
│   ├── Whobit.tsx      # Animated character that guides users
│   ├── HeaderBar.tsx   # Top navigation bar
│   └── ...
├── chsh/               # CHSH Bell test experiment (pages 1–3)
├── qf/                 # Quantum Fortune (pages 1–2)
├── qkd/                # Quantum Key Distribution
├── ssm/                # Secret Message Sharing (pages 1–4)
├── survey/             # Post-experiment user feedback
└── about/              # Project information page
```

## Design Patterns

### Page Layout

Each experiment page follows a consistent two-column layout:
- **Left**: Whobit character with step-by-step instructions
- **Right**: Interactive content (buttons, results, visualizations)

### API Communication

All calls to the Node API are centralized in `calls.tsx`. This file exports typed functions for each endpoint, keeping API logic out of UI components.

### Real-Time Updates

Experiment results are streamed from the backend via WebSocket. The `useWebSocket` hook in `hooks/` manages the connection lifecycle and delivers updates to components.

### Multi-Page Experiments

Multi-step experiments (e.g., CHSH has 3 pages, SSM has 4 pages) use `PageRedirectContext` to track progress and navigate between steps while preserving experiment state.

## Key Technologies

| Technology | Version | Purpose |
|---|---|---|
| Next.js | 16 | React framework with App Router |
| React | 19 | UI rendering |
| TypeScript | — | Type safety |
| Material-UI | — | Component library and theming |
