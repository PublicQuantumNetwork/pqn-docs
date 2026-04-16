# Architecture

A PQN node is composed of four main components. All components except the Node API reside in an internal intranet with no external network access.

```
                        ┌─────────────────────────────────┐
                        │           PQN Node               │
                        │                                  │
  Web UI / Other Nodes ─┤──► Node API (FastAPI)            │
                        │         │                        │
                        │         ▼                        │
                        │      Router (ZMQ)                │
                        │         │                        │
                        │         ▼                        │
                        │  Hardware Provider               │
                        │         │                        │
                        │         ▼                        │
                        │   Quantum Hardware               │
                        └─────────────────────────────────┘
```

## Node API

**File**: `src/pqnstack/app/main.py`

A FastAPI application that is the only component with external network access. It handles:
- Communication with the web frontend (`pqn-gui`)
- Node-to-node communication (e.g., for two-node CHSH experiments)
- Exposing experiment endpoints

Interactive API docs are available at `http://127.0.0.1:8000/docs` when the server is running.

## Router

**File**: `src/pqnstack/network/router.py`

Routes messages between Hardware Providers, PQN developers, and Node APIs using ZMQ sockets. Required on the first computer in a node; optional for additional computers joining the same node.

## Hardware Provider

**File**: `src/pqnstack/network/instrument_provider.py`

Hosts quantum hardware resources and makes them available to other components via ProxyInstruments. Each instrument is loaded from a driver class specified in the config file.

## Drivers

**Directory**: `src/pqnstack/pqn/drivers/`

Hardware drivers abstract physical devices:

| Driver | Description |
|---|---|
| `TimeTagger` | Photon detection timing |
| `Polarimeter` | Photon polarization measurement |
| `Rotator` / `RotaryEncoder` | Polarization basis rotation (half-wave plates) |
| `QKD Driver` | Quantum key distribution hardware |
| `CHSH Driver` | Bell test measurement |
| `DummyInstrument` | Software-only testing without physical hardware |

## Protocols

**Directory**: `src/pqnstack/pqn/protocols/`

Experiment protocols implement the quantum measurement logic:

| Protocol | File | Description |
|---|---|---|
| CHSH | `chsh.py` | Bell inequality test |
| QKD | `qkd.py` | Quantum key distribution |
| Tomography | `tomography.py` | Quantum state tomography |
| Visibility | `visibility.py` | Interference visibility measurement |
| Measurement | `measurement.py` | Base measurement functionality |

## CLI

The `pqn` CLI (implemented with [Typer](https://typer.tiangolo.com/)) provides commands to start each component. See {doc}`running` for usage.
