# pqn-hardware

`pqn-hardware` is the Python library that talks to the individual pieces of hardware around a Node. It provides the software abstraction for an instrument, the concrete drivers behind real devices, and the ZMQ messaging fabric that carries instrument calls across a Node's intranet. It also ships a CLI, `pqn-hw`, that launches the Router and Instrument Provider processes a Node runs. `pqn-node` consumes it as a git-pinned dependency.

**Repository:** [github.com/PublicQuantumNetwork/pqn-hardware](https://github.com/PublicQuantumNetwork/pqn-hardware)

## The three layers

The library is organised into three layers, each documented on its own page:

- **Instruments & drivers** — the `Instrument` abstraction (a `typing.Protocol`), the typed sub-protocols for time taggers, rotators, and polarimeters, the concrete drivers that back real devices, and the `ProxyInstrument` that lets code drive a remote instrument as if it were local. See {doc}`instruments-and-drivers`.
- **Network transport** — the ZMQ star that carries instrument calls: the Router (broker), the Instrument Providers that host instruments, and the Client side that calls them. In practice this is a single-router network. See {doc}`network`.
- **The `pqn-hw` CLI** — the commands that stand up those processes during deployment: `start-router` and `start-provider`, and the TOML config that wires providers to a router. See {doc}`cli`.

## How `pqn-node` uses it

`pqn-node` pins `pqn-hardware` as a git dependency and consumes it two ways. In-process, the Node API drives instruments by calling **ProxyInstruments** — client-side handles whose method calls are marshalled across the Router to whichever Instrument Provider hosts the real device, so the Node API never needs to know which machine an instrument is plugged into. Out-of-process, a deployment uses the `pqn-hw` CLI to run the Router and Instrument Provider as long-lived processes. For the system-wide picture of how this fits with the Node API and the GUI, see {doc}`../overview/software-map`.

```{note}
This layer is **internal to a Node**. The Router, Instrument Providers, and the instruments behind them live on the Node's local network and are not reachable from outside it. Other Nodes never touch a peer's `pqn-hardware` resources directly — all cross-Node interaction goes through the **Node API**, the only externally reachable component of a Node.
```

## Where to go next

- {doc}`../overview/software-map` — how `pqn-hardware`, `pqn-node`, and `pqn-gui` fit together, with request walkthroughs.
- {doc}`../pqn-node/index` — the Node API service that consumes this library.
- {doc}`../physical-devices/index` — build and wiring guides for the physical devices the drivers control.

```{toctree}
:maxdepth: 2

instruments-and-drivers
network
cli
```
