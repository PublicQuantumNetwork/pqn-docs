# pqn-node

`pqn-node` is the FastAPI service that runs at each PQN site. It is the **Node API** — the only externally reachable component of a Node — and the orchestration brain for every Experiment. It depends on `pqn-hardware` as a git-pinned Python library for instrument access and Protocol logic.

**Repository:** [github.com/PublicQuantumNetwork/pqn-node](https://github.com/PublicQuantumNetwork/pqn-node)

Responsibilities:

- Expose HTTP and WebSocket endpoints to the GUI and to peer Nodes
- Coordinate multi-Node Experiments (e.g. two-Node CHSH)
- Drive instruments through ProxyInstruments backed by the Router
- Manage Experiment lifecycle: launch, progress streaming, cancellation

> _Placeholder._ Detailed pages on `pqn-node`'s internal architecture, request flow, configuration, and HTTP API will be added here. Until then, see the [README](https://github.com/PublicQuantumNetwork/pqn-node) and the {doc}`../overview/software-map` for context.
