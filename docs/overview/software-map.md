# Software Map

This page is the top-level mental map of the Public Quantum Network: how the whole system fits together, how a single Node is structured, where each package lives, and how a real request flows through everything.

```{note}
For a glossary of the terms used here (Node, Node API, Instrument Provider, ProxyInstrument, Protocol, Experiment, GUI), see `CONTEXT.md` at the repository root.

Deeper, package-specific details live under {doc}`../pqn-node/index`, {doc}`../pqn-gui/index`, and {doc}`../pqn-hardware/index`. Operator-focused setup lives under {doc}`../deployment/index`.
```

## 1. The PQN Network

At the network level the PQN is a small group of optical labs scattered across a few institutions. Each lab is a **Node**: it can run quantum experiments end to end on its own, and any pair of Nodes that have been physically connected can team up on experiments that need two sites at once, like the CHSH Bell test.

Connecting two Nodes takes two channels. Classically, like normal computers, every Node sits on a shared VPN that links all the participating sites. Quantumly, the two labs are physically joined by an optical fibre that lets them exchange entangled photons. The fibre carries the quantum state of the experiment; the VPN carries the classical bookkeeping the two Nodes need to agree on what they measured.

A visitor meets a Node through its **GUI**, a small web app that runs alongside the Node API. The GUI is the part of the PQN that the public actually sees.

```{mermaid}
flowchart LR
    GUIA[GUI]:::client
    GUIB[GUI]:::client
    subgraph NodeA["Node A"]
        APIA[Node API]
        InstrA[(Optical<br/>hardware)]
    end
    subgraph NodeB["Node B"]
        APIB[Node API]
        InstrB[(Optical<br/>hardware)]
    end
    GUIA -.HTTP.-> APIA
    GUIB -.HTTP.-> APIB
    APIA <==>|"classical (VPN)"| APIB
    InstrA <==>|"quantum (optical fibre)"| InstrB

    classDef client fill:#fff3e0,stroke:#b36b1f;
```

Inside a Node, the Node API is the only component that ever talks to anything outside the Node. Everything else (Router, Instrument Providers, drivers, instruments) lives on the Node's local network and is reachable only through the Node API. Nothing in the PQN is exposed to the public internet.

## 2. A single Node

Zoom into one Node. It contains four logical layers:

```{mermaid}
flowchart TB
    GUI[GUI / browser]:::ext
    Peer[Peer Node API]:::ext

    subgraph Node["Node (site intranet)"]
        API[Node API<br/><i>pqn-node</i>]
        Router[Router<br/><i>pqn-hardware</i>]
        Provider1[Instrument Provider<br/><i>pqn-hardware</i>]
        Provider2[Instrument Provider<br/><i>pqn-hardware</i>]
        Driver1[Driver]
        Driver2[Driver]
        Driver3[Driver]
        Instr1[(Physical<br/>Instrument)]
        Instr2[(Physical<br/>Instrument)]
        Instr3[(Physical<br/>Instrument)]
    end

    GUI -.HTTP / WebSocket.-> API
    Peer -.HTTP.-> API
    API -- ZMQ --> Router
    Router -- ZMQ --> Provider1
    Router -- ZMQ --> Provider2
    Provider1 --> Driver1
    Provider1 --> Driver2
    Provider2 --> Driver3
    Driver1 --> Instr1
    Driver2 --> Instr2
    Driver3 --> Instr3

    classDef ext fill:#eee,stroke:#888,stroke-dasharray: 4 2;
```

- **Node API** (in `pqn-node`): FastAPI service. The only component reachable from outside. Handles GUI requests and peer-Node coordination. Owns the orchestration logic for each Experiment.
- **Router** (in `pqn-hardware`): ZMQ message broker. All in-Node messaging passes through it.
- **Instrument Provider** (in `pqn-hardware`): process that hosts physical instruments. A Node can run more than one Provider; for example, one machine per optics table or per piece of expensive hardware.
- **Driver** (in `pqn-hardware`): concrete instrument implementation. Talks to one piece of physical hardware (Thorlabs rotator, TimeTagger, etc.).

The Node API never talks to a Driver directly. It calls a **ProxyInstrument**, a client-side handle whose method calls are serialised onto the Router and dispatched to whichever Instrument Provider hosts the real instrument. This means the Node API code does not need to know which machine an instrument is plugged into.

## 3. The three packages

The same picture, redrawn around the package boundary instead of the runtime topology:

```{mermaid}
flowchart LR
    GUI["pqn-gui<br/><sub>Next.js · TypeScript</sub><br/>public web UI"]:::ts
    Node["pqn-node<br/><sub>FastAPI · Python</sub><br/>Node API service"]:::py
    HW["pqn-hardware<br/><sub>library · Python</sub><br/>drivers, Router, Provider"]:::py

    GUI -- HTTP / WebSocket --> Node
    Node -- imports --> HW
    Node -- launches --> RouterProc["Router process<br/><i>pqn-hw start-router</i>"]
    Node -- launches --> ProviderProc["Instrument Provider process<br/><i>pqn-hw start-provider</i>"]
    RouterProc -. provided by .- HW
    ProviderProc -. provided by .- HW

    classDef py fill:#e6f0ff,stroke:#3b6cb3;
    classDef ts fill:#fff3e0,stroke:#b36b1f;
```

- **`pqn-node`** is the only package that actually runs the Node API service. It depends on `pqn-hardware` as a git-pinned library and orchestrates everything: HTTP routing, peer-Node coordination, Protocol logic, Experiment lifecycle, WebSocket streaming.
- **`pqn-gui`** is a Next.js application. It has no Python; it knows the Node API only through its HTTP/WebSocket surface.
- **`pqn-hardware`** is a Python library *and* a CLI (`pqn-hw`). The library is consumed in-process by `pqn-node` for ProxyInstrument calls. The CLI runs the Router and Instrument Provider as separate long-lived processes, started during deployment.

The split between `pqn-node` and `pqn-hardware` exists so that hardware-driver work (which moves at the pace of new instruments and ZMQ infrastructure changes) can evolve independently of the FastAPI service (which moves at the pace of new Experiments and UI features).

## 4. Walkthrough: a single-Node experiment

What happens when a visitor clicks **Run** on the Quantum Fortune page in the GUI:

```{mermaid}
sequenceDiagram
    actor User
    participant GUI as GUI<br/>(pqn-gui)
    participant API as Node API<br/>(pqn-node)
    participant Proto as Protocol<br/>(pqn-node)
    participant Router as Router<br/>(pqn-hardware)
    participant Provider as Instrument Provider<br/>(pqn-hardware)
    participant Instr as Physical Instrument

    User->>GUI: click "Run"
    GUI->>API: POST /experiments/quantum-fortune
    API->>Proto: invoke Protocol
    Proto->>Router: ProxyInstrument call
    Router->>Provider: routed ZMQ message
    Provider->>Instr: driver call
    Instr-->>Provider: measurement
    Provider-->>Router: result
    Router-->>Proto: result
    Proto-->>API: result
    API-->>GUI: WebSocket update
    GUI-->>User: render result
```

Two things to notice:

1. **ProxyInstruments hide the network.** From the Protocol's point of view, calling an instrument looks like a local method call, but the call is actually marshalled across ZMQ to wherever the Hardware Provider is running.
2. **Results stream back over WebSocket.** Long-running experiments emit progress updates as they go, so the GUI can render live counts and partial results rather than waiting for a single response at the end.

## 5. Walkthrough: a two-Node CHSH experiment

The CHSH Bell test is the canonical multi-Node Experiment. Two Nodes (call them Alice and Bob) each measure one half of an entangled pair on independently chosen polarisation bases, and the Node API on the initiating side aggregates the results.

```{mermaid}
sequenceDiagram
    actor User
    participant GUI as GUI<br/>(at Alice)
    participant Alice as Node API<br/>Alice
    participant Bob as Node API<br/>Bob
    participant InstrA as Alice's<br/>instruments
    participant InstrB as Bob's<br/>instruments

    User->>GUI: click "Run CHSH"
    GUI->>Alice: POST /experiments/chsh<br/>(peer = Bob)
    Alice->>Bob: announce run, exchange config
    par measurement on each side
        Alice->>InstrA: rotate, measure
        InstrA-->>Alice: counts
    and
        Bob->>InstrB: rotate, measure
        InstrB-->>Bob: counts
    end
    Bob-->>Alice: counts for Bob's bases
    Alice->>Alice: compute CHSH inequality value
    Alice-->>GUI: WebSocket result
    GUI-->>User: render Bell-violation plot
```

Key points:

- The **GUI only talks to one Node API** (Alice's). The peer-Node coordination is entirely between Node APIs over HTTP. The GUI never connects to Bob.
- Each Node drives its own instruments through its own Router and Instrument Providers; neither side touches the other side's hardware.
- The initiating Node (Alice) is responsible for aggregating the joint statistics and computing the Bell inequality value.

## Where to go next

- {doc}`../deployment/index`: how to actually stand up a Node and join a network.
- {doc}`../pqn-node/index`, {doc}`../pqn-gui/index`, {doc}`../pqn-hardware/index`: package-specific internals.
- {doc}`../physical-devices/index`: build guides for the physical instruments referenced throughout this page.
