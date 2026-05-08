# PQN

The Public Quantum Network: a federation of physical sites (**Nodes**) that expose real quantum experiments to the public through a web interface.

This file is the canonical glossary for terms used across `pqn-docs`, `pqn-node`, `pqn-gui`, and `pqn-hardware`. When the same concept has multiple candidate names, the bolded entry is the one to use; aliases are listed as `_Avoid_`.

## Language

**Node**:
A PQN deployment at a single physical site — comprises a Node API, a Router, one or more Hardware Providers, instrument drivers, and the physical instruments themselves. The GUI is _not_ part of a Node.
_Avoid_: site, instance, station

**Node API**:
The FastAPI service inside a Node. The only Node component reachable from outside the local intranet; handles requests from the GUI and from peer Nodes. Sometimes informally called "the Node" when zoomed in (see Flagged ambiguities).
_Avoid_: backend, server

**Router**:
ZMQ message broker inside a Node. Routes messages between the Node API, Hardware Providers, and developer clients.

**Hardware Provider**:
Process inside a Node that hosts physical instruments and exposes them to the rest of the Node via ProxyInstruments.
_Avoid_: Instrument Provider (older name; still appears in some code paths)

**ProxyInstrument**:
Client-side handle for an instrument hosted by a Hardware Provider. Lets the Node API call the instrument without knowing where it physically runs.

**Instrument**:
Software abstraction for one piece of physical hardware — TimeTagger, Polarimeter, Rotator, etc. Concrete implementations are called drivers and live in `pqn-hardware`.
_Avoid_: device (reserved for the physical thing)

**Driver**:
A concrete Instrument implementation for a specific piece of hardware (e.g. Thorlabs rotator driver).

**Protocol**:
The quantum-measurement logic for a single experiment type — CHSH, QKD, Tomography, Visibility. Lives in `pqn-hardware`. Distinct from Experiment.

**Experiment**:
A user-facing activity in the GUI (CHSH Bell Test, Quantum Fortune, QKD, SSM, Tomography, Visibility). Implemented on top of one or more Protocols.

**GUI**:
`pqn-gui`, the Next.js public-facing web interface. Talks to a single Node API, typically over localhost. Optional — every Experiment can be run programmatically without it.
_Avoid_: frontend, web app, UI (when precision matters)

**PQN Network**:
A set of Nodes that can communicate with each other to run multi-Node Experiments (e.g. two-Node CHSH).

**PQN Clone**:
An institution-run instance of the PQN — i.e. an organisation that stands up its own Node(s) and optionally federates with others.

## Relationships

- A **PQN Network** is composed of one or more **Nodes**.
- A **Node** contains one **Node API**, one **Router**, and one or more **Hardware Providers**.
- A **Hardware Provider** hosts one or more **Instruments**; each Instrument is implemented by a **Driver**.
- The **Node API** reaches Instruments via **ProxyInstruments** routed through the **Router**.
- An **Experiment** in the **GUI** invokes one or more **Protocols** on the **Node API**.
- A **Protocol** orchestrates Instruments to perform a single quantum measurement task.

## Example dialogue

> **New contributor:** "When the user clicks 'Run CHSH' in the GUI, what happens?"
> **Maintainer:** "The **GUI** calls the **Node API**. The Node API kicks off the CHSH **Protocol**, which talks to the local **Hardware Provider** through **ProxyInstruments** to drive the **Instruments** — rotators, the TimeTagger, etc. For two-**Node** CHSH the Node API also coordinates with the peer **Node**'s Node API."
>
> **New contributor:** "And the GUI is part of the Node?"
> **Maintainer:** "No — the GUI is just a client. The **Node** is the backend stack at one site. You can run every **Experiment** without the GUI."

## Flagged ambiguities

- **"Node"** is polysemous by design:
  - At the **network** zoom level, "Node" means the whole site-level deployment.
  - When working **inside** a Node, "Node" is sometimes used as shorthand for the **Node API** (the brain of the Node).
  Resolution: prefer **"Node API"** in writing whenever you mean the FastAPI service. Reserve unqualified "Node" for the site-level meaning.
- **"Hardware"** has two unrelated meanings — the Python library `pqn-hardware` (drivers + Router + Provider + Protocols) and the physical devices themselves. In docs prose, write `pqn-hardware` (in code font) for the package and **Physical Device** / **Instrument** for the physical thing.
- **"Instrument Provider"** vs **"Hardware Provider"** — same concept, two names in code. Prefer **Hardware Provider** in docs.
