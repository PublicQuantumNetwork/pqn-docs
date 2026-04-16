# Configuration

## Environment Variables

All frontend configuration is done through environment variables in a `.env.local` file at the project root. See {doc}`installation` for the full variable reference.

## Multi-Node Setup

The PQN is designed for two-node quantum experiments. To run two frontend instances simultaneously (one per node):

1. Start the first instance on the default port:
   ```bash
   npm run dev
   # Available at http://localhost:3000
   ```

2. Start the second instance on port 3001:
   ```bash
   PORT=3001 npm run dev
   # Available at http://localhost:3001
   ```

Each frontend instance should point to its corresponding Node API via `NEXT_PUBLIC_API_ADDRESS`. Use separate `.env.local` files (e.g., `.env.locala` and `.env.localb`) and load them manually, or configure the addresses at startup.

> **Note**: The PQN currently supports exactly two nodes. Three or more nodes are not yet supported.
