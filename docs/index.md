---
myst:
  html_meta:
    "description lang=en": "Documentation for the Public Quantum Network (PQN)."
---

# Public Quantum Network

Welcome to the documentation for the **Public Quantum Network (PQN)**. The PQN lets the general public run real quantum experiments from a web browser. Each PQN site runs a small backend that drives real optical hardware, and a web interface presents the experiments as a series of interactive games.

The codebase is split across three packages:

- **[pqn-node](https://github.com/PublicQuantumNetwork/pqn-node)**: the backend service that runs at each site.
- **[pqn-gui](https://github.com/PublicQuantumNetwork/pqn-gui)**: the public-facing web interface.
- **[pqn-hardware](https://github.com/PublicQuantumNetwork/pqn-hardware)**: instrument drivers, messaging, and quantum protocols.

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
