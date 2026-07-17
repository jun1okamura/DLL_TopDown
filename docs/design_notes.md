# Design Notes

This document records engineering discussions, design decisions, alternatives, and unresolved issues during the development of the DLL Top-Down Time Domain Simulator.

Unlike `architecture.md`, which defines the approved software architecture, this document captures the reasoning behind engineering decisions.

---

# Parameter Definition

Status

Proposed

The Level 1 simulator separates immutable configuration data from mutable simulation state.

Parameters are grouped by functional blocks.

- Simulation
- Clock
- Controller
- Delay
- Lock

Each parameter shall have

- a physical meaning
- an explicit unit
- a valid range
- a default value

Derived parameters (for example, the reference period) shall be calculated automatically.

The parameter definition will be implemented in Issue #3.

---

# Simulation Principle

## Fundamental Philosophy

The simulator is based on the following principle.

> **Time is the primary simulation variable.**

Instead of solving voltages and currents, the simulator predicts the timing of future clock edges using behavioral models.

The simulator advances from one edge event to the next.

---

## Event-driven Simulation

Level 1 uses an event-driven simulation model.

No fixed simulation time step is introduced.

Only significant timing events are processed.

This approach enables rapid architectural exploration while preserving timing relationships.

---

# Engineering Decisions

## Reference Edge Generation

Status

**Confirmed**

Decision

The reference clock is considered ideal in Level 1.

No jitter or frequency variation is introduced.

Future versions will optionally include

- Random jitter
- Deterministic jitter
- Frequency offset

---

## Feedback Edge Generation

Status

**Proposed**

Current proposal

The feedback edge is generated using

```
Feedback Edge = Reference Edge + Current Delay
```

Advantages

- Simple implementation
- Easy to understand
- Suitable for Level 1

Future consideration

Investigate whether an independent event queue provides advantages when supporting more complex timing networks.

---

## Phase Error Definition

Status

**Under Review**

Candidate A

```
Phase Error = Reference Edge - Feedback Edge
```

Candidate B

```
Phase Error = Expected Feedback Edge - Actual Feedback Edge
```

Current direction

Candidate A is preferred because it directly represents timing difference between reference and feedback edges.

Final definition will be confirmed during implementation.

---

## Loop Controller

Status

**Proposed**

The controller updates the control value once per reference edge.

The Level 1 implementation will use an ideal discrete-time controller.

No analog dynamics are included.

---

## Delay Model

Status

**Proposed**

The delay model is assumed to be

- linear
- deterministic
- noiseless

Future versions may include

- saturation
- nonlinearity
- quantization
- mismatch

---

## Control Update Timing

Status

**Confirmed**

Decision

The updated control value affects the next simulation cycle.

```
Current cycle
    ↓
Phase Detector
    ↓
Controller
    ↓
Delay Update
    ↓
Next Cycle
```

This one-cycle latency models discrete-time behavior and avoids algebraic loops.

---

## Simulation State

Status

**Proposed**

Only dynamic variables belong to the simulation state.

Examples

- Reference Edge Time
- Feedback Edge Time
- Delay
- Control
- Phase Error
- Lock Status

Configuration values remain in the parameter definition.

---

# Deferred Features

The following topics are intentionally postponed.

## Analog Charge Pump

Deferred to Level 2.

Reason

Not required for validating event-driven architecture.

---

## Loop Filter

Deferred to Level 2.

Initially represented by an ideal discrete-time controller.

---

## Delay Cell Ripple

Deferred.

The influence of charge-pump ripple on delay will be introduced after the ideal simulator is verified.

---

## Device Noise

Deferred.

Noise mechanisms should not obscure verification of the simulation framework.

---

## Monte Carlo Simulation

Deferred.

Statistical analysis will be added after deterministic behavior has been validated.

---

# Open Questions

The following items remain under discussion.

## Feedback Edge Model

Should future versions maintain an event queue?

Current answer

Not required for Level 1.

---

## Delay Update Timing

Can multiple updates occur within one reference period?

Current answer

No.

One update per reference edge.

---

## Lock Criterion

How should lock be defined?

Candidates

- Phase error threshold
- Consecutive lock count
- RMS phase error

Decision deferred until Lock Detector implementation.

---

# Design Principles

The following principles should remain unchanged throughout the project.

- Documentation before implementation.
- Simplicity before optimization.
- Behavioral modeling before circuit modeling.
- Event-driven simulation before continuous-time simulation.
- Modular software architecture.
- Human engineering decisions supported by AI.

---

# Future Review

The following decisions should be revisited after Level 1 is complete.

- Phase error definition
- Feedback edge generation
- Delay update timing
- Lock criterion
- Controller algorithm

The architecture should evolve only after verifying that the current assumptions are insufficient.

### Observation

The delay model is implemented as a stateless component.
Given the same control input, it always produces the same delay output.
This design allows the simulator to remain independent of the specific delay implementation and simplifies replacement with nonlinear or jitter-aware models in future issues.