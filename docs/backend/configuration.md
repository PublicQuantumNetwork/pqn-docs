# Configuration

The backend uses TOML configuration files. Two separate config files are needed: one for the Node API and one for the Router and Hardware Provider.

## Node API Configuration (`config.toml`)

Copy the example config and rename it:

```bash
cp configs/config_app_example.toml config.toml
```

> **Important**: The file **must** be named `config.toml` and placed at the root of the repository.

Edit `config.toml` with your actual settings:

```toml
node_name = "example_node"

# Router configuration
router_name = "router1"
router_address = "xx.xx.xx.xx"  # Replace with actual IP address
router_port = 5555

# Rotary encoder serial address
rotary_encoder_address = "/dev/tty.usbmodem1101"

# Timetagger configuration (provider_name, instrument_name)
timetagger = ["provider", "tagger"]

# Bell state (default: Phi_plus = 0)
bell_state = 0

# CHSH experiment settings
[chsh_settings]
hwp = ["provider", "instrument_hwp"]
request_hwp = ["provider", "instrument_hwp"]
expectation_signs = [-1, 1, 1, 1]  # HV + VH basis

[chsh_settings.measurement_config]
integration_time_s = 5
binwidth = 500
channel1 = 1
channel2 = 2
dark_count = 0

# QKD experiment settings
[qkd_settings]
hwp = ["provider", "instrument_hwp"]
request_hwp = ["provider", "instrument_hwp"]
bitstring_length = 4
discriminating_threshold = 10

[qkd_settings.measurement_config]
integration_time_s = 5
binwidth = 500
channel1 = 1
channel2 = 2
dark_count = 0

# Daily CHSH report (optional, for automated Slack reporting)
[daily_report]
slack_webhook_url = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
api_url = "http://localhost:8000"
timetagger_address = "127.0.0.1:8000"
follower_node_address = "192.168.1.100:9000"
basis = [0, 22.5]
```

## Router and Hardware Provider Configuration

For the first computer in a PQN node, both a Router and Hardware Provider are needed. Additional computers in the same node only need a Hardware Provider.

Copy and edit the messaging config:

```bash
cp configs/config_messaging_example.toml my_messaging.toml
```

Example `config_messaging_example.toml`:

```toml
[router]
name = "pqnstack-router"
host = "localhost"
port = 5556

[provider]
name = "pqnstack-provider"
router_name = "pqnstack-router"
host = "localhost"
port = 5556
beat_period = 2000

[[provider.instruments]]
name = "dummy1"
import = "pqnstack.pqn.drivers.dummies.DummyInstrument"
desc = "Dummy instrument for testing"
hw_address = "1234"

[[provider.instruments]]
name = "dummy2"
import = "pqnstack.pqn.drivers.dummies.DummyInstrument"
desc = "Dummy instrument for testing"
hw_address = "1234"
```

Each `[[provider.instruments]]` entry specifies a hardware driver to load. Replace the dummy drivers with real hardware drivers for production use (see {doc}`architecture`).
