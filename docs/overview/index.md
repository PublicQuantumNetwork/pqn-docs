# Overview

## What is the PQN?

The Public Quantum Network (PQN) is a distributed quantum network system that enables the general public to interact with real quantum hardware through a lightweight web interface. Visitors can run quantum experiments — including entanglement verification, quantum key distribution, and quantum random number generation — without any prior knowledge of quantum mechanics.

The network is built around a **node-based architecture**: each PQN node consists of a backend software stack (`pqn-stack`) managing hardware and protocols, and a frontend web interface (`pqn-gui`) for public interaction.

## Supported Experiments

| Experiment | Description |
|---|---|
| **CHSH Bell Test** | Verifies quantum entanglement by testing Bell inequalities between two nodes |
| **Quantum Key Distribution (QKD)** | Generates a shared secret key between two parties using quantum mechanics |
| **Quantum Fortune** | Generates random numbers using quantum randomness |
| **Secret Message Sharing (SSM)** | Sends a secret message encoded with quantum-generated keys |
| **Tomography** | Characterizes quantum states via state tomography |
| **Visibility** | Measures the visibility of quantum interference fringes |

## Architecture

The PQN uses a two-repo architecture:

- **[pqn-stack](https://github.com/PublicQuantumNetwork/pqn-stack)**: Python backend that manages quantum hardware, protocols, and node-to-node communication via a FastAPI server.
- **[pqn-gui](https://github.com/PublicQuantumNetwork/pqn-gui)**: Next.js frontend providing the public-facing web interface.

See the {doc}`../backend/architecture` and {doc}`../frontend/architecture` pages for details.

## Hardware Requirements

Running the full PQN stack currently requires physical quantum hardware components:

- **TimeTagger**: Photon detection timing device
- **Rotators / Rotary Encoders**: Polarization basis rotation control (e.g., half-wave plates)
- **Polarimeter**: Photon polarization measurement

Dummy instrument drivers are available for software-only testing, but full experiment functionality requires real hardware.

## Acknowledgements

The Public Quantum Network is supported in part by:

- NSF Quantum Leap Challenge Institute HQAN under Award No. 2016136
- Illinois Computes
- DOE Grant No. 712869, "Advanced Quantum Networks for Science Discovery"

For questions, contact the PQN team at [publicquantumnetwork@gmail.com](mailto:publicquantumnetwork@gmail.com).
