# pqn-hardware

`pqn-hardware` is the Python library that everything below the Node API runs on. It provides the instrument abstractions, ZMQ-based messaging fabric, concrete drivers, and quantum protocol implementations that `pqn-node` consumes. It also ships a CLI (`pqn-hw`) used to launch the Router and Hardware Provider processes during deployment.

**Repository:** [github.com/PublicQuantumNetwork/pqn-hardware](https://github.com/PublicQuantumNetwork/pqn-hardware)

What lives in here:

- **Instrument base classes and ProxyInstrument plumbing**: the common abstractions over physical hardware.
- **Drivers**: concrete instruments such as Thorlabs rotators, TimeTagger, polarimeter, and QKD hardware, plus dummy drivers for software-only development.
- **Network layer**: Router (ZMQ broker) and Hardware Provider, plus the client side used by `pqn-node`.
- **Protocols**: quantum-measurement logic for CHSH, QKD, Tomography, Visibility.
- **`pqn-hw` CLI**: `start-router`, `start-provider`.

`pqn-hardware` was split out from `pqn-node` (originally `pqn-stack`) so hardware-driver work and Node-service work can evolve independently. `pqn-node` pins it as a git dependency.

> _Placeholder._ Detailed pages on the driver model, ProxyInstrument lifecycle, Router/Provider topology, Protocol authoring, and the `pqn-hw` CLI will be added here. Until then, see the [README](https://github.com/PublicQuantumNetwork/pqn-hardware) and the {doc}`../overview/software-map` for context.
