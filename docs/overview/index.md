# Overview

```{toctree}
:hidden:

software-map
```

## What is the PQN?

The Public Quantum Network (PQN) is a federation of physical sites — called **Nodes** — that expose real quantum experiments to the general public through a lightweight web interface. A visitor with no background in quantum mechanics can walk up to a Node, click through an experiment in the browser, and watch real photons being measured in real time.

Each Node is a self-contained backend stack running on a small intranet. Nodes can talk to each other over the public internet to run multi-Node experiments such as the CHSH Bell test. The web interface (the GUI) is an optional client — every Experiment can also be run programmatically.

For the canonical glossary of terms used throughout the docs (Node, Node API, Hardware Provider, Protocol, Experiment, …), see {doc}`software-map` and the project's `CONTEXT.md`.

## Supported Experiments

| Experiment | Description |
|---|---|
| **CHSH Bell Test** | Verifies quantum entanglement by testing Bell inequalities between two Nodes |
| **Quantum Key Distribution (QKD)** | Generates a shared secret key between two parties using quantum mechanics |
| **Quantum Fortune** | Generates random numbers using quantum randomness |
| **Secret Message Sharing (SSM)** | Sends a secret message encoded with a quantum-generated key |
| **Tomography** | Characterises quantum states via state tomography |
| **Visibility** | Measures the visibility of quantum interference fringes |

## How the software fits together

The system is split across three packages plus a set of physical devices:

- **`pqn-node`** — the FastAPI service that runs at each Node. The Node API; the brain of the Node.
- **`pqn-gui`** — the Next.js web interface. Talks to a single Node API, typically over localhost.
- **`pqn-hardware`** — the Python library used by `pqn-node` to drive instruments, route ZMQ messages, and execute quantum protocols.
- **Physical devices** — the polarimeters, time taggers, rotators, and lasers that physically perform the measurements.

For the full mental model — diagrams of the network, a single Node, and the request flow through the system — see the {doc}`software-map`.

## Hardware requirements

Running a Node currently requires real quantum-optics hardware: a TimeTagger, polarisation rotators, and a polarimeter. Dummy drivers exist for software-only development, but full Experiment functionality requires physical instruments.

See {doc}`../physical-devices/index` for build guides for the physical components.

## Acknowledgements

The Public Quantum Network is supported in part by:

- NSF Quantum Leap Challenge Institute HQAN under Award No. 2016136
- Illinois Computes
- DOE Grant No. 712869, "Advanced Quantum Networks for Science Discovery"

For questions, contact the PQN team at [publicquantumnetwork@gmail.com](mailto:publicquantumnetwork@gmail.com).
