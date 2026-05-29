# Instruments & drivers

A Node is surrounded by real equipment — rotators, time taggers, polarimeters — and
something has to turn "rotate this waveplate to 22.5°" into the actual bytes that make
the motor move. That's the job of this part of `pqn-hardware`: it gives every piece of
hardware a uniform shape in software, so the rest of the system can drive it without
knowing the messy details of any particular device.

Two ideas sit at the centre of that, and it helps to keep them apart from the start.

The first is the **Instrument** — the *software abstraction* for a piece of hardware.
It's a small contract that says what any instrument looks like: it has a name, it can be
started and closed, and it exposes some values you can read or write and some actions
you can call. The rest of the system only ever talks to this abstraction.

The second is the **Driver** — a *concrete implementation* of that contract for one
specific piece of hardware, like a Thorlabs rotator or a Swabian time tagger. The same
kind of instrument can have several Drivers: a rotator is still a rotator whether it
speaks the Thorlabs APT protocol, a plain serial protocol, or the ELLx protocol, so all
three are Drivers behind the one rotator Instrument.

So you *write* Drivers, and you *program against* Instruments. And when a piece of
hardware lives on another machine, you still program against an Instrument — a
`ProxyInstrument` that quietly forwards your calls across the Node. The rest of this
page works through each of those in turn: the Instrument model first, then writing a
Driver, then using one from afar through a `ProxyInstrument`.

## The Instrument model

Every instrument in `pqn-hardware`, real or simulated, is built on a single base type
called `Instrument`, defined in
[`src/pqn_hardware/instrument.py`](https://github.com/PublicQuantumNetwork/pqn-hardware/blob/master/src/pqn_hardware/instrument.py).
It's written as a
`typing.Protocol` — Python's way of describing a *shape* that other classes are expected
to match — but it's also a `dataclass`, so a Driver doesn't just match it from a
distance: it subclasses `Instrument` directly and fills in the pieces. In other words,
`Instrument` does double duty. It's the contract that describes what every instrument
exposes to the rest of the system, and it's the base class you start from when you write
a new one.

The contract itself is small, so it's worth building up a piece at a time.

At its core, an Instrument is an identity plus two collections of capabilities:

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

The two capability collections are the heart of the model:

- **`parameters`** is a set of attribute *names* — values you **read and write**. A
  rotator's `degrees`, a dummy's `param_int`: state you query or set.
- **`operations`** is a dict mapping *names* to callables — *actions* you **invoke**. A
  rotator's `move_to`, a time tagger's `count_singles`: things the instrument *does*.

This split — values you get/set versus actions you call — is what makes an instrument
addressable from a distance. When code drives a remote instrument, the proxy uses these
two collections to decide whether an attribute access should read or write a value or
call a method (see *Using a ProxyInstrument* below, and the wire format on
{doc}`network`).

Because the two collections are keyed by name, there's one rule on names:

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
Building the object should only record where the device lives — its `name`, `desc`, and
`hw_address`, plus any driver-specific settings — and set sensible defaults. It should
not open a port, contact a controller, or move anything. Save all of that for `start()`:
opening the serial or USB connection, handshaking with the controller, homing a motor to
a known reference angle.

The reason is in how Instruments come to life. An Instrument Provider builds each one
straight from its config — `class_(name=..., desc=..., hw_address=..., **settings)`,
purely from the strings in a TOML file — and only *then* calls `start()`
([`instrument_provider.py:113`](https://github.com/PublicQuantumNetwork/pqn-hardware/blob/master/src/pqn_hardware/network/instrument_provider.py#L113)).
At construction time it has no idea whether the device is plugged in, powered, or even
reachable. If your constructor tried to open the port, a missing or busy device would
make the object impossible to *create* — and you would lose the clean line between an
instrument that is *configured* and one that is *connected*. Deferring every side effect
to `start()` keeps construction cheap and predictable, so an instrument can be created
freely and brought online deliberately.

`close()` is the other half of that bargain. Most of these devices hold an *exclusive*
resource — a serial port, a USB handle — that nothing else can open while it's in use.
If a process walks away without calling `close()`, the port can stay locked until the
hardware is power-cycled, and the device may be left in an undefined state. So a Driver
does its real connect-and-initialise in `start()` and is responsible for releasing
everything cleanly in `close()`.

#### Reporting state: `info`

An Instrument should be able to report its complete current state on demand, and that's
what `info` is for. It hands back a single read-only snapshot that captures everything
worth knowing about the instrument — its identity and every piece of live state — so a
caller can inspect it without having to read parameters one by one:

```python
    @property
    def info(self) -> InstrumentInfo: ...
```
*Source: [`instrument.py:50-51`](https://github.com/PublicQuantumNetwork/pqn-hardware/blob/master/src/pqn_hardware/instrument.py#L50-L51)*

That snapshot is an `InstrumentInfo`. The base class only holds the fields every
instrument has — its identity, plus a free-form `hw_status` for anything else worth
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

Each of these builds on `Instrument` — it still *is* an Instrument — and pins down a
**standard interface** for its category: the exact parameters and operations every
rotator, time tagger, or polarimeter is expected to expose. That shared interface is the
whole point. Because every rotator presents the same `degrees`, `move_to`, and `move_by`,
the rest of the system can be written against "a rotator" without caring whether the
physical device is a Thorlabs APT unit, a serial unit, or an ELLx unit. What each
category adds, and how you build a Driver on top of one, is covered in *Writing a Driver*
below.

## Writing a Driver

> _Placeholder — drafted in sub-phase 3.2 (grill pending)._

## Using a ProxyInstrument

> _Placeholder — drafted in sub-phase 3.3 (grill pending)._
