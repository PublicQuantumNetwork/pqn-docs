# Contributing

Thank you for your interest in contributing to the Public Quantum Network!

## Repositories

| Repository | Description |
|---|---|
| [pqn-stack](https://github.com/PublicQuantumNetwork/pqn-stack) | Python backend stack |
| [pqn-gui](https://github.com/PublicQuantumNetwork/pqn-gui) | Next.js frontend |
| [pqn-docs](https://github.com/PublicQuantumNetwork/pqn-docs) | This documentation site |

## Contributing to the Docs

The documentation site is built with [Sphinx](https://www.sphinx-doc.org/) and [MyST Markdown](https://myst-parser.readthedocs.io/).

### Setup

```bash
git clone https://github.com/PublicQuantumNetwork/pqn-docs.git
cd pqn-docs
uv sync
```

### Build Locally

```bash
cd docs
uv run make html
```

Open `docs/build/html/index.html` in your browser to preview the result.

### Adding Pages

1. Create a new `.md` file in the appropriate subdirectory under `docs/`
2. Add it to the `toctree` directive in the corresponding `index.md`
3. Build and verify locally before opening a pull request

### Writing Style

- Use plain, accessible language — remember that many readers are members of the general public interacting with quantum experiments for the first time
- Keep technical jargon to a minimum or define it when first used
- Use tables for configuration references and command comparisons

## Contributing to the Backend or Frontend

Please refer to the `CONTRIBUTING.md` file in each repository:
- [pqn-stack/CONTRIBUTING.md](https://github.com/PublicQuantumNetwork/pqn-stack/blob/master/CONTRIBUTING.md)

## Contact

For questions, reach the PQN team at [publicquantumnetwork@gmail.com](mailto:publicquantumnetwork@gmail.com).
