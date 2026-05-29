# Overview

```{toctree}
:hidden:

software-map
```

## What is the PQN?

The Public Quantum Network (PQN) lets the general public run real quantum experiments from a web browser. A visitor with no background in quantum mechanics can walk up to a PQN station, click through an experiment, and watch real photons being measured in real time.

A PQN site (a Node) bundles three things: a backend service that runs the experiments, a web interface that presents them as a series of interactive games, and a library that drives the physical hardware. The web interface is how the public actually meets the PQN. Each game is a guided walkthrough that wraps a quantum experiment, with the experiment itself acting as the game's backend.

Two Nodes can also talk to each other so they can run experiments that need both sides, such as the CHSH Bell test. The classical communication between Nodes runs over a VPN that connects all the participating sites, and the quantum communication runs through an optical fibre between the two labs. Nothing in the PQN is exposed to the public internet.

## How the software fits together

The PQN is built from three packages:

- **`pqn-node`**: the backend service that runs at each Node. Handles requests from the web interface and from peer Nodes, and orchestrates each experiment.
- **`pqn-gui`**: the web interface. A Next.js app whose pages are organised as games, each one wrapping a quantum experiment.
- **`pqn-hardware`**: the library that drives the physical devices, routes messages between processes, and runs the quantum protocols. The polarimeters, time taggers, rotators, and lasers it controls are part of this layer.

For diagrams of how these fit together, see the {doc}`software-map`.

## Hardware

A PQN Node currently runs on real quantum-optics hardware. Detailed requirements and setup notes are still being written, we will get back to them. For the parts that are already documented, see {doc}`../physical-devices/index`.

## Acknowledgements

The Public Quantum Network is supported in part by:

- NSF Quantum Leap Challenge Institute HQAN under Award No. 2016136
- Illinois Computes
- DOE Grant No. 712869, "Advanced Quantum Networks for Science Discovery"

For questions, contact the PQN team at [publicquantumnetwork@gmail.com](mailto:publicquantumnetwork@gmail.com).
