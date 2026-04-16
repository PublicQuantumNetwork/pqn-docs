# Running a Node

A full PQN node requires starting up to four processes. Start them in this order.

## 1. Start the Router

Using a config file:

```bash
uv run pqn start-router --config configs/config_messaging_example.toml
```

Or using CLI flags directly:

```bash
uv run pqn start-router --name router1 --host localhost --port 5555
```

The Router is required on the first machine in a node. Additional machines joining the same node do not need their own Router.

## 2. Start the Hardware Provider

Using a config file:

```bash
uv run pqn start-provider --config configs/config_messaging_example.toml
```

Or using CLI flags:

```bash
uv run pqn start-provider \
  --name provider1 \
  --router-name router1 \
  --instruments '{"dummy1": {"import": "pqnstack.pqn.drivers.dummies.DummyInstrument", "desc": "Test", "hw_address": "1234"}}'
```

## 3. Start the Node API

```bash
uv run fastapi run src/pqnstack/app/main.py
```

The API will be available at `http://127.0.0.1:8000`. Interactive API documentation is at `http://127.0.0.1:8000/docs`.

## 4. Start the Web Frontend (optional)

See the {doc}`../frontend/running` page for frontend setup instructions.

## Two-Node Setup

For two-node experiments (CHSH, QKD), each node runs its own full stack. Configure the `follower_node_address` in `config.toml` to point to the second node's API address.

The frontend also needs to be configured with the second node's address — see {doc}`../frontend/running`.
