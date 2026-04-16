# Installation

## Prerequisites

- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- Quantum hardware components (TimeTagger, rotators, etc.) — see {doc}`../overview/index`

## Install uv

If you don't have `uv` installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Clone and Install

```bash
git clone https://github.com/PublicQuantumNetwork/pqn-stack.git
cd pqn-stack
```

Install dependencies including the FastAPI web server:

```bash
uv sync --extra webapp
```

This installs all required packages into an isolated virtual environment managed by `uv`.

## Verify Installation

Check that the `pqn` CLI is available:

```bash
uv run pqn --help
```

You should see a list of available commands.
