# Experiment Protocols

Protocols are implemented in `src/pqnstack/pqn/protocols/` and exposed via the Node API.

## CHSH Bell Test

**File**: `src/pqnstack/pqn/protocols/chsh.py`

Tests Bell inequalities to verify quantum entanglement between two nodes. Each node measures photon polarization in two bases; the correlations between results either satisfy or violate the classical Bell bound (S ≤ 2).

A violation (S > 2) confirms quantum entanglement. The PQN uses the CHSH form of the Bell inequality.

**Configuration** (`chsh_settings` in `config.toml`):
- `hwp`: Half-wave plate instrument for local basis rotation
- `request_hwp`: Half-wave plate on the follower node
- `expectation_signs`: Sign pattern for the correlation matrix (depends on the Bell state prepared)
- `measurement_config.integration_time_s`: How long to collect photon counts per measurement

## Quantum Key Distribution (QKD)

**File**: `src/pqnstack/pqn/protocols/qkd.py`

Implements the BB84-like protocol to generate a shared secret key between two parties using quantum mechanics. Eavesdropping disturbs the quantum states and is detectable.

**Configuration** (`qkd_settings` in `config.toml`):
- `bitstring_length`: Number of key bits to generate
- `discriminating_threshold`: Minimum coincidence count to classify a measurement as valid

## Quantum Fortune

Generates random bits using quantum measurement outcomes. Because quantum measurement results are fundamentally random, the output is certified random by the laws of physics.

## Secret Message Sharing (SSM)

Combines QKD key generation with classical encryption to allow two users to exchange a quantum-secured secret message through the web interface.

## Tomography

**File**: `src/pqnstack/pqn/protocols/tomography.py`

Performs quantum state tomography by measuring in multiple bases to reconstruct the density matrix of the quantum state being produced.

## Visibility

**File**: `src/pqnstack/pqn/protocols/visibility.py`

Measures the visibility of quantum interference — a key metric for assessing the quality of the quantum source and optical alignment.

## API Reference

All protocols are accessible via the Node API. With the server running, visit `http://127.0.0.1:8000/docs` for the full interactive OpenAPI documentation.
