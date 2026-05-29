# Instruments & drivers

A Node is surrounded by real equipment (rotators, time taggers, polarimeters), and
something has to turn "rotate this waveplate to 22.5°" into the actual bytes that make
the motor move. That's the job of this part of `pqn-hardware`: it gives every piece of
hardware a uniform shape in software, so the rest of the system can drive it without
knowing the messy details of any particular device.

Two ideas sit at the centre of that, and it helps to keep them apart from the start.

The first is the **Instrument**, the *software abstraction* for a piece of hardware.
It's a small contract that says what any instrument looks like: it has a name, it can be
started and closed, and it exposes some values you can read or write and some actions
you can call. The rest of the system only ever talks to this abstraction.

The second is the **Driver**, a *concrete implementation* of that contract for one
specific piece of hardware, like a Thorlabs rotator or a Swabian time tagger. The same
kind of instrument can have several Drivers: a rotator is still a rotator whether it
speaks the Thorlabs APT protocol, a plain serial protocol, or the ELLx protocol, so all
three are Drivers behind the one rotator Instrument.

So you *write* Drivers, and you *program against* Instruments. And when a piece of
hardware lives on another machine, you still program against an Instrument, a
`ProxyInstrument` that quietly forwards your calls across the Node. The rest of this
page works through each of those in turn: the Instrument model first, then writing a
Driver, then using one from afar through a `ProxyInstrument`.

## The Instrument model

Every instrument in `pqn-hardware`, real or simulated, is built on a single base type
called `Instrument`, defined in
[`src/pqn_hardware/instrument.py`](https://github.com/PublicQuantumNetwork/pqn-hardware/blob/master/src/pqn_hardware/instrument.py).
It's written as a
`typing.Protocol` (Python's way of describing a *shape* that other classes are expected
to match), but it's also a `dataclass`, so a Driver doesn't just match it from a
distance: it subclasses `Instrument` directly and fills in the pieces. In other words,
`Instrument` does double duty. It's the contract that describes what every instrument
exposes to the rest of the system, and it's the base class you start from when you write
a new one.

The contract itself is small, so it's worth building up a piece at a time.

At its core, an Instrument is an identity plus two groups of capabilities:

```python
@runtime_checkable
@dataclass(slots=True)
class Instrument(Protocol):
    name: str
    desc: str
    hw_address: str
    parameters: set[str] = field(default_factory=set)
    operations: dict[str, Callable[..., Any]] = field(default_factory=dict)
```
*Source: [`instrument.py:26-42`](https://github.com/PublicQuantumNetwork/pqn-hardware/blob/master/src/pqn_hardware/instrument.py#L26-L42)*

The identity fields are straightforward: a `name` the instrument is addressed by, a
human-readable `desc`, and an `hw_address` (a serial port, a USB id, whatever the
hardware is reached through).

These two groups are the heart of the model:

- **`parameters`** is a set of attribute *names*: values you **read and write**. A
  rotator's `degrees`, a dummy's `param_int`: state you query or set.
- **`operations`** is a dict mapping *names* to callables: *actions* you **invoke**. A
  rotator's `move_to`, a time tagger's `count_singles`: things the instrument *does*.

This split, values you get/set versus actions you call, is what makes an instrument
addressable from a distance. When code drives a remote instrument, the proxy uses these
two groups to decide whether an attribute access should read or write a value or
call a method (see *Using a ProxyInstrument* below, and the wire format on
{doc}`network`).

Because both groups are keyed by name, there's one rule on names:

```{note}
An instrument's `name` may not contain a `:` character. The `:` separates the parts of
a request when talking to a remote instrument, so a colon in the name would be
ambiguous ([`instrument.py:33`](https://github.com/PublicQuantumNetwork/pqn-hardware/blob/master/src/pqn_hardware/instrument.py#L33)).
```

The `@runtime_checkable` decorator means an ordinary `isinstance(x, Instrument)` check
works at runtime, so code can confirm something really is an instrument before driving
it.

### Anatomy of a Driver

#### Lifecycle

An Instrument has a start/stop lifecycle:

```python
    def start(self) -> None: ...
    def close(self) -> None: ...
```
*Source: [`instrument.py:47-48`](https://github.com/PublicQuantumNetwork/pqn-hardware/blob/master/src/pqn_hardware/instrument.py#L47-L48)*

These two look trivial, but they carry the whole relationship with the physical device,
and it's worth keeping them cleanly separated when you write a Driver.

The rule: **constructing the Instrument object should do nothing to the hardware; the
device should only be touched once `start()` is called.**
Building the object should only record where the device lives (its `name`, `desc`, and
`hw_address`, plus any driver-specific settings) and set sensible defaults. It should
not open a port, contact a controller, or move anything. Save all of that for `start()`:
opening the serial or USB connection, handshaking with the controller, homing a motor to
a known reference angle.

The reason is in how Instruments come to life. An Instrument Provider builds each one
straight from its config (`class_(name=..., desc=..., hw_address=..., **settings)`,
purely from the strings in a TOML file) and only *then* calls `start()`
([`instrument_provider.py:113`](https://github.com/PublicQuantumNetwork/pqn-hardware/blob/master/src/pqn_hardware/network/instrument_provider.py#L113)).
At construction time it has no idea whether the device is plugged in, powered, or even
reachable. If your constructor tried to open the port, a missing or busy device would
make the object impossible to *create*, and you would lose the clean line between an
instrument that is *configured* and one that is *connected*. Deferring every side effect
to `start()` keeps construction cheap and predictable, so an instrument can be created
freely and brought online deliberately.

`close()` is the other half of that bargain. Most of these devices hold an *exclusive*
resource (a serial port, a USB handle) that nothing else can open while it's in use.
If a process walks away without calling `close()`, the port can stay locked until the
hardware is power-cycled, and the device may be left in an undefined state. So a Driver
does its real connect-and-initialise in `start()` and is responsible for releasing
everything cleanly in `close()`.

#### Reporting state: `info`

An Instrument should be able to report its complete current state on demand, and that's
what `info` is for. It hands back a single read-only snapshot that captures everything
worth knowing about the instrument, its identity and every piece of live state, so a
caller can inspect it without having to read parameters one by one:

```python
    @property
    def info(self) -> InstrumentInfo: ...
```
*Source: [`instrument.py:50-51`](https://github.com/PublicQuantumNetwork/pqn-hardware/blob/master/src/pqn_hardware/instrument.py#L50-L51)*

That snapshot is an `InstrumentInfo`. The base class only holds the fields every
instrument has: its identity, plus a free-form `hw_status` for anything else worth
reporting:

```python
@dataclass(frozen=True, slots=True)
class InstrumentInfo:
    name: str = ""
    desc: str = ""
    hw_address: str = ""
    hw_status: dict[str, Any] = field(default_factory=dict)
```
*Source: [`instrument.py:18-23`](https://github.com/PublicQuantumNetwork/pqn-hardware/blob/master/src/pqn_hardware/instrument.py#L18-L23)*

You won't usually return a bare `InstrumentInfo`, though. When you write a Driver, you
define your own info class that extends `InstrumentInfo` with the state specific to your
device, and return *that* from `info`. The dummy driver's `DummyInfo` adds its three
parameter values; a rotator's `RotatorInfo` adds the current angle and offset. A caller
then gets back the full, typed state of whatever instrument it happens to be holding.

#### Instrument categories

The base `Instrument` describes any instrument at all. On top of it, the library defines
a more specific Instrument for each broad category of hardware:

- **`TimeTaggerInstrument`**
- **`RotatorInstrument`**
- **`PolarimeterInstrument`**

Each of these builds on `Instrument` (it still *is* an Instrument) and pins down a
**standard interface** for its category: the exact parameters and operations every
rotator, time tagger, or polarimeter is expected to expose. That shared interface is the
whole point. Because every rotator presents the same `degrees`, `move_to`, and `move_by`,
the rest of the system can be written against "a rotator" without caring whether the
physical device is a Thorlabs APT unit, a serial unit, or an ELLx unit. What each
category adds, and how you build a Driver on top of one, is covered in *Writing a Driver*
below.

## Writing a Driver

Writing a Driver means giving real behaviour to the lifecycle, parameters, operations,
and `info` from the previous section, for one specific piece of hardware. The clearest
way to see how is to build one up from scratch, and the repository already ships the
perfect specimen for that: `DummyInstrument`, a fake instrument with no hardware behind
it, used in tests and as a worked example. We'll assemble it piece by piece, then look at
how a real Driver differs.

### Assembling a Driver, step by step

A Driver is a `dataclass` that subclasses `Instrument`. Start with the class itself and
the state it keeps:

```python
@dataclass(slots=True)
class DummyInstrument(Instrument):
    _param_int: int = 2
    _param_str: str = "hello"
    _param_bool: bool = True
    connected: bool = False
```
*Source: [`dummies.py:17-22`](https://github.com/PublicQuantumNetwork/pqn-hardware/blob/master/src/pqn_hardware/drivers/dummies.py#L17-L22)*

The fields prefixed with `_` are the dummy's private state, the values a real Driver
would read off the hardware. (`name`, `desc`, and `hw_address` come from `Instrument`
itself, so they don't need repeating here.)

Next, declare what the instrument can do. Recall that an Instrument advertises its
capabilities in two places, `parameters` and `operations`; a Driver fills those in
inside `__post_init__`:

```python
    def __post_init__(self) -> None:
        self.parameters = {"param_int", "param_str", "param_bool"}
        self.operations = {
            "double_int": self.double_int,
            "lowercase_str": self.lowercase_str,
            "uppercase_str": self.uppercase_str,
            "toggle_bool": self.toggle_bool,
            "set_half_input_int": self.set_half_input_int,
        }
```
*Source: [`dummies.py:24-32`](https://github.com/PublicQuantumNetwork/pqn-hardware/blob/master/src/pqn_hardware/drivers/dummies.py#L24-L32)*

`parameters` is just the set of attribute names a caller may read and write;
`operations` maps each callable name to the bound method that implements it. Everything a
caller is allowed to do remotely has to be registered in one of these two.

Now the lifecycle. The dummy has nothing to connect to, so `start` and `close` only flip
a flag, but this is exactly where a real Driver would open its serial port and release
it again:

```python
    def start(self) -> None:
        self.connected = True

    def close(self) -> None:
        self.connected = False
```
*Source: [`dummies.py:45-49`](https://github.com/PublicQuantumNetwork/pqn-hardware/blob/master/src/pqn_hardware/drivers/dummies.py#L45-L49)*

A parameter is implemented as an ordinary property pair: a getter and a setter over the
private field:

```python
    @property
    @log_parameter
    def param_int(self) -> int:
        return self._param_int

    @param_int.setter
    @log_parameter
    def param_int(self, value: int) -> None:
        self._param_int = value
```
*Source: [`dummies.py:51-59`](https://github.com/PublicQuantumNetwork/pqn-hardware/blob/master/src/pqn_hardware/drivers/dummies.py#L51-L59)*

The `@log_parameter` and `@log_operation` decorators that appear here and below are
optional helpers from `instrument.py`: wrap a parameter accessor or an operation and
every read, write, and call is logged with timing. They aren't required for a working
Driver, but they're cheap observability, so the real drivers use them throughout.

An operation is just a method, registered in `operations` above:

```python
    @log_operation
    def double_int(self) -> int:
        self._param_int *= 2
        return self._param_int
```
*Source: [`dummies.py:81-84`](https://github.com/PublicQuantumNetwork/pqn-hardware/blob/master/src/pqn_hardware/drivers/dummies.py#L81-L84)*

Finally, `info`. As described earlier, a Driver returns its *own* info class carrying its
complete state. For the dummy that's `DummyInfo`, which extends `InstrumentInfo` with
the three parameter values:

```python
@dataclass(frozen=True, slots=True)
class DummyInfo(InstrumentInfo):
    param_int: int = 0
    param_str: str = ""
    param_bool: bool = False
```
*Source: [`dummies.py:10-14`](https://github.com/PublicQuantumNetwork/pqn-hardware/blob/master/src/pqn_hardware/drivers/dummies.py#L10-L14)*

```python
    @property
    def info(self) -> DummyInfo:
        return DummyInfo(
            name=self.name,
            desc=self.desc,
            hw_address=self.hw_address,
            param_int=self.param_int,
            param_str=self.param_str,
            param_bool=self.param_bool,
        )
```
*Source: [`dummies.py:34-43`](https://github.com/PublicQuantumNetwork/pqn-hardware/blob/master/src/pqn_hardware/drivers/dummies.py#L34-L43)*

That's a complete Driver: state, capabilities, lifecycle, accessors, and a snapshot.
Swap the flag-flipping for real serial I/O and you have the shape of every real Driver in
the package.

### Building on an Instrument category

Subclassing the base `Instrument` means wiring up everything by hand, as the dummy does.
When your hardware fits one of the Instrument categories, you *can* subclass that instead
and let it do some of the wiring for you. `RotatorInstrument`, for example, already
registers the standard rotator operations and parameter in its own `__post_init__`:

```python
    def __post_init__(self) -> None:
        self.operations["move_to"] = self.move_to
        self.operations["move_by"] = self.move_by
        self.parameters.add("degrees")
```
*Source: [`instrument.py:180-184`](https://github.com/PublicQuantumNetwork/pqn-hardware/blob/master/src/pqn_hardware/instrument.py#L180-L184)*

It even implements `move_to` and `move_by` for you, in terms of `degrees`:

```python
    def move_to(self, angle: float) -> None:
        self.degrees = angle

    def move_by(self, angle: float) -> None:
        self.degrees += angle
```
*Source: [`instrument.py:194-200`](https://github.com/PublicQuantumNetwork/pqn-hardware/blob/master/src/pqn_hardware/instrument.py#L194-L200)*

So a rotator Driver built on `RotatorInstrument` only has to supply the parts that are
genuinely hardware-specific: how to `start` and `close` the connection, how to read and
write `degrees`, and its `info`. `SerialRotator` is about as small as a real Driver gets:

```python
@dataclass(slots=True)
class SerialRotator(RotatorInstrument):
    _degrees: float = 0.0  # The hardware doesn't support position tracking
    _conn: serial.Serial = field(init=False, repr=False)

    def start(self) -> None:
        self._conn = serial.Serial(self.hw_address, baudrate=115200, timeout=1)
        self._conn.write(b"open_channel")
        self._conn.read(100)
        self._conn.write(b"motor_ready")
        self._conn.read(100)
        self.degrees = self.offset_degrees

    def close(self) -> None:
        self.degrees = 0
        self._conn.close()

    @property
    def degrees(self) -> float:
        return self._degrees

    @degrees.setter
    def degrees(self, degrees: float) -> None:
        self._conn.write(f"SRA {degrees}".encode())
        self._degrees = degrees
        _ = self._conn.readline().decode()
```
*Source: [`rotator.py:95-132`](https://github.com/PublicQuantumNetwork/pqn-hardware/blob/master/src/pqn_hardware/drivers/rotator.py#L95-L132)*

It never defines `move_to`, `move_by`, or `__post_init__`; all three come from
`RotatorInstrument`. Notice the payoff of the lifecycle rule from earlier: opening the
serial port lives entirely in `start()`, so constructing a `SerialRotator` from config
touches no hardware.

```{note}
Because construction does no I/O, an operation could be called before `start()` has run.
If that would misbehave on your hardware, guard against it: `APTRotator` raises
`DeviceNotStartedError` if you try to move it before its device handle exists
([`rotator.py:67`](https://github.com/PublicQuantumNetwork/pqn-hardware/blob/master/src/pqn_hardware/drivers/rotator.py#L67)).
```

### The drivers that ship today

The package ships these Drivers, grouped by the Instrument category each one implements:

| Category | Drivers | Hardware |
|---|---|---|
| `TimeTaggerInstrument` | [`SwabianTimeTagger`](https://github.com/PublicQuantumNetwork/pqn-hardware/blob/master/src/pqn_hardware/drivers/timetagger.py#L19) | Swabian Instruments time tagger |
| `RotatorInstrument` | [`APTRotator`](https://github.com/PublicQuantumNetwork/pqn-hardware/blob/master/src/pqn_hardware/drivers/rotator.py#L24), [`SerialRotator`](https://github.com/PublicQuantumNetwork/pqn-hardware/blob/master/src/pqn_hardware/drivers/rotator.py#L96), [`EllxRotator`](https://github.com/PublicQuantumNetwork/pqn-hardware/blob/master/src/pqn_hardware/drivers/rotator.py#L136) | Thorlabs APT mounts; a plain serial rotator; Thorlabs ELLx mounts |
| `PolarimeterInstrument` | [`ArduinoPolarimeter`](https://github.com/PublicQuantumNetwork/pqn-hardware/blob/master/src/pqn_hardware/drivers/polarimeter.py#L95) | Arduino-based polarimeter |
| `Instrument` (base) | [`DummyInstrument`](https://github.com/PublicQuantumNetwork/pqn-hardware/blob/master/src/pqn_hardware/drivers/dummies.py#L18) | none; test and example fixture |

The rotator row is the point made back in the orientation: one category, several Drivers.
A `RotatorInstrument` is a rotator whatever protocol it speaks, and the rest of the
system drives all three through the identical `degrees` / `move_to` / `move_by` interface.

## Using a ProxyInstrument

Everything so far has involved holding a Driver directly. In a running Node you rarely
do that. The real instruments are created and owned by an Instrument Provider, often on a
different machine, and your code reaches them over the Node's internal network through
the Router (how that fabric works is the subject of {doc}`network`).

What your code holds instead is a **ProxyInstrument**: a local stand-in that forwards
every call across the network to the real instrument. It satisfies the same Instrument
contract as any Driver, so your code behaves exactly as it would a local instrument,
with no idea the hardware is somewhere else.

```{mermaid}
flowchart LR
    A[Your code] --> B[ProxyInstrument]
    B -. across the Node .-> C[Router]
    C --> D[Instrument Provider]
    D --> E[Instrument + hardware]
```

The `Router` and `InstrumentProvider` hops in the middle are exactly what {doc}`network`
covers; here we only care about the two ends: your code, and the instrument it drives.

### Getting a ProxyInstrument

You obtain a proxy through a `Client`. Connect one, ask a provider what it hosts, then
request a device by name:

```python
from pqn_hardware.network.client import Client

client = Client()                                      # connect to the Router
devices = client.get_available_devices("provider1")    # what does provider1 host?
instrument = client.get_device("provider1", "dummy1")  # a ProxyInstrument for "dummy1"
```
*Source: [`tests/messaging/client.py:10-20`](https://github.com/PublicQuantumNetwork/pqn-hardware/blob/master/tests/messaging/client.py#L10-L20)*

`get_available_devices` returns a dict that maps each instrument the provider hosts to
its Driver class. Run against a provider hosting a single dummy, it gives:

```text
{'dummy1': <class 'pqn_hardware.drivers.dummies.DummyInstrument'>}
```

`get_device` then hands back a `ProxyInstrument` for one of those names. Ask for a name
the provider doesn't host and it raises a `PacketError` carrying the provider's reply
(`Instrument 'does_not_exist' not found.`), so it's worth checking `get_available_devices`
first when a name might be wrong.

### Using it

From here you use `instrument` exactly as if it were local. Call its operations, with or
without arguments:

```python
instrument.double_int()                  # operation, no arguments
instrument.set_half_input_int(10)        # positional argument
instrument.set_half_input_int(value=36)  # keyword argument
```
*Source: [`tests/messaging/client.py:25-39`](https://github.com/PublicQuantumNetwork/pqn-hardware/blob/master/tests/messaging/client.py#L25-L39)*

Read and write its parameters as ordinary attributes:

```python
current = instrument.param_int  # read a parameter
instrument.param_int = 42       # write a parameter
```
*Source: [`tests/messaging/client.py:42-49`](https://github.com/PublicQuantumNetwork/pqn-hardware/blob/master/tests/messaging/client.py#L42-L49)*

And ask for its state snapshot through `instrument.info`, just like a local Instrument.
Each of these quietly becomes a round-trip to the provider and back, but your code never
has to deal with that.

### What you can't do

A proxy only exposes what the instrument actually registered as a parameter or an
operation. Assigning anything else is rejected, rather than silently creating a local
attribute that would never reach the hardware:

```python
instrument.new_attr = 348  # raises AttributeError
```
*Source: [`tests/messaging/client.py:53-56`](https://github.com/PublicQuantumNetwork/pqn-hardware/blob/master/tests/messaging/client.py#L53-L56)*

### Closing

When you're finished, close the proxy. For a `ProxyInstrument`, `close()` tears down the
underlying network connection rather than touching any hardware; the real instrument
keeps running under its Instrument Provider:

```python
instrument.close()
```
*Source: [`client.py:266-267`](https://github.com/PublicQuantumNetwork/pqn-hardware/blob/master/src/pqn_hardware/network/client.py#L266-L267)*
