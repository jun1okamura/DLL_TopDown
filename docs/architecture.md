# Simulation Architecture

## Purpose

This document defines the software architecture of the **DLL Top-Down Time Domain Simulator**.

The objective is to establish a clear and extensible event-driven simulation framework before implementation.

The architecture is intended to support future extensions while keeping the Level 1 simulator as simple as possible.

---

# Scope

## Level 1

Level 1 implements an **ideal event-driven behavioral DLL simulator**.

The primary objective is to verify

- DLL lock behavior
- Loop convergence
- Delay evolution
- Timing relationships

without considering transistor-level effects.

### Included

- Reference Clock
- Phase Detector (PFD)
- Loop Controller
- Delay Model
- Feedback Edge Generation
- Simulation State
- Lock Detector
- Metrics
- Event-driven Simulation Engine

### Excluded

The following features are intentionally excluded from Level 1.

- Charge Pump Ripple
- Analog Loop Filter
- Delay Cell Nonlinearity
- Delay Quantization
- Device Noise
- Process Variation
- Delay Cell Mismatch
- Multi-stage Delay Propagation
- Monte Carlo Analysis

These features will be introduced incrementally in future versions.

---

# Simulation Philosophy

Unlike SPICE-based simulators, this simulator does not solve electrical quantities.

The primary simulation variable is

> **Time**

Every clock edge is represented by its timestamp.

Behavioral models predict the timing of future events.

The simulator therefore advances from one event to the next instead of stepping through time.

---

# Top-Level Architecture

```
                   Simulator
          +----------------------+
          | Parameters           |
          | SimulationState      |
          +----------------------+
                     │
      ┌──────────────┼──────────────┐
      ▼              ▼              ▼
ReferenceClock  LoopController   Metrics
      │
      ▼
PhaseDetector
      │
      ▼
DelayModel
      │
      ▼
Feedback Edge
```

The simulator owns

- Parameters
- Simulation State

and controls the execution order of every module.

---

# Module Responsibilities

## Simulator

Controls the overall simulation sequence.

Responsibilities

- Initialize simulation
- Execute one simulation cycle
- Update simulation state
- Invoke all behavioral models
- Collect metrics

---

## Reference Clock

Generates reference clock edge timestamps.

Output

- Reference Edge Time

---

## Phase Detector

Calculates the timing error between

- Reference Edge
- Feedback Edge

Output

- Phase Error

---

## Loop Controller

Calculates the next control value using the phase error.

The Level 1 controller is an ideal discrete-time controller.

Output

- Control Value

---

## Delay Model

Converts the control value into delay.

The Level 1 model assumes an ideal linear delay characteristic.

Output

- Delay

---

## Feedback Edge Generator

Generates the next feedback edge timestamp.

Output

- Feedback Edge Time

---

## Simulation State

Stores all dynamic variables.

The state evolves once per reference clock edge.

---

## Lock Detector

Determines whether the DLL has reached lock.

Outputs

- Lock Status
- Lock Counter

---

## Metrics

Collects simulation statistics.

Examples

- Lock Time
- Phase Error
- Delay History
- Control History

---

# Data Flow

The simulator exchanges the following information.

```
Reference Edge
        │
        ▼
Phase Detector
        │
 Phase Error
        │
        ▼
Loop Controller
        │
 Control
        │
        ▼
Delay Model
        │
 Delay
        │
        ▼
Feedback Edge
```

Only timing information is propagated between modules.

---

# Event Processing Order

One simulation cycle consists of the following sequence.

1. Generate the reference edge.
2. Generate the feedback edge using the current delay.
3. Calculate the phase error.
4. Update the lock detector.
5. Calculate the new control value.
6. Update the delay.
7. Store the simulation state.
8. Record simulation metrics.

The updated delay is applied to the **next** reference edge.

This one-cycle delay is intentional and models the discrete-time nature of the loop.

---

# Timing Convention

The simulator uses SI units.

| Quantity | Unit |
|-----------|------|
| Time | second |
| Delay | second |
| Phase Error | second |
| Frequency | Hz |

An optional normalized phase error (UI) may also be calculated for analysis.

---

# Parameters and State

Simulation parameters are constant during one simulation.

Examples

- Reference frequency
- Initial delay
- Loop gain
- Lock threshold

Simulation state changes every cycle.

Examples

- Current cycle
- Reference edge time
- Feedback edge time
- Delay
- Control
- Phase error
- Lock status

Separating parameters from state improves readability and future extensibility.

---

# Planned File Structure

```
dll/
    __init__.py
    params.py
    state.py
    simulator.py

    clock.py
    pfd.py
    controller.py
    delay_model.py

    lock_detector.py
    metrics.py
    plots.py
```

Each module should have a single responsibility.

The simulator coordinates interactions between modules.

---

# Deferred Features

The following features are planned after Level 1.

- Charge Pump
- Loop Filter
- VCDL Model
- Delay Nonlinearity
- Delay Quantization
- Device Noise
- Process Variation
- Multi-stage Delay Line
- Monte Carlo Simulation
- PLL Support
- CDR Support

---

# Design Principles

The simulator follows the following principles.

- Event-driven simulation
- Time as the primary state variable
- Modular architecture
- Documentation-first development
- AI-assisted engineering
- Top-down semiconductor design

The architecture should remain simple, readable, and extensible.