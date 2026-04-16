# Running the Frontend

## Prerequisites

Ensure the PQN Node API is running before starting the frontend. See {doc}`../backend/running`.

## Development Mode

```bash
npm run dev
```

Opens at [http://localhost:3000](http://localhost:3000). Includes hot reload for code changes.

## Production Mode

```bash
npm run build
npm run start
```

Production mode is faster than development mode and recommended for public deployments.

## Two-Node Operation

For two-node experiments (CHSH, QKD), run two frontend instances and two backend stacks simultaneously:

```
Node A:
  - pqn-stack API on port 8000
  - pqn-gui on port 3000 → NEXT_PUBLIC_API_ADDRESS=127.0.0.1:8000

Node B:
  - pqn-stack API on port 9000
  - pqn-gui on port 3001 → NEXT_PUBLIC_API_ADDRESS=127.0.0.1:9000
```

Set `NEXT_PUBLIC_FOLLOWER_NODE_ADDRESS` on each node to point to the other node's API.
