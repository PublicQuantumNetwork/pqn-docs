# Installation

## Prerequisites

- Node.js 18 or higher and npm ([installation guide](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm))
- A running PQN Node API (see {doc}`../backend/running`)

## Clone and Install

Clone the repository **outside** the `pqn-stack` directory:

```bash
git clone https://github.com/PublicQuantumNetwork/pqn-gui.git
cd pqn-gui
npm install
```

## Environment Configuration

Create a `.env.local` file at the root of the project:

```bash
NEXT_PUBLIC_API_ADDRESS=127.0.0.1:8000
NEXT_PUBLIC_TIMETAGGER_ADDRESS=127.0.0.1:8000
NEXT_PUBLIC_FOLLOWER_NODE_ADDRESS=127.0.0.1:9000
NEXT_PUBLIC_SURVEY_FORM_URL=https://surveys.illinois.edu/sec/1160990162
```

| Variable | Description |
|---|---|
| `NEXT_PUBLIC_API_ADDRESS` | Address of the local PQN Node API |
| `NEXT_PUBLIC_TIMETAGGER_ADDRESS` | Address of the node with the TimeTagger device |
| `NEXT_PUBLIC_FOLLOWER_NODE_ADDRESS` | Address of the second node (for two-node experiments) |
| `NEXT_PUBLIC_SURVEY_FORM_URL` | URL of the post-experiment survey (optional) |

Replace addresses with your actual Node API endpoints if they differ from the defaults.
