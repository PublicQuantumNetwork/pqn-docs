---
myst:
  html_meta:
    "description lang=en": "Documentation for the Public Quantum Network (PQN)."
---

# Public Quantum Network

Welcome to the documentation for the **Public Quantum Network (PQN)** — a federation of physical sites that lets the general public run real quantum experiments through a web interface.

The codebase is split across three packages:

- **[pqn-node](https://github.com/PublicQuantumNetwork/pqn-node)** — the FastAPI service that runs at each site
- **[pqn-gui](https://github.com/PublicQuantumNetwork/pqn-gui)** — the public-facing web interface
- **[pqn-hardware](https://github.com/PublicQuantumNetwork/pqn-hardware)** — instrument drivers, ZMQ messaging, and quantum protocols

> **Early Development**: This project is in early stages. APIs, installation procedures, and distribution methods are subject to change.

```{toctree}
:maxdepth: 2
:hidden:

overview/index
deployment/index
pqn-node/index
pqn-gui/index
pqn-hardware/index
physical-devices/index
contributing/index
```
