# DLL Top-Down Time Domain Simulator

A Python-based event-driven behavioral simulator for Delay Locked Loops (DLLs).

This project explores a top-down methodology for semiconductor timing design using **time-domain event simulation** rather than conventional transistor-level simulation.

The simulator is intended for architecture exploration, loop stability analysis, lock behavior verification, timing jitter evaluation, and semiconductor design education.

Unlike SPICE-based circuit simulators, this project models the behavior of a DLL using **edge events in the time domain**, enabling rapid architectural studies before circuit implementation.

---

# Vision

Modern semiconductor design requires exploring architectural ideas long before transistor-level implementation.

This project aims to provide an event-driven behavioral simulator that bridges the gap between system architecture and circuit design.

Beyond software development, this repository serves as a reference for:

- Top-down semiconductor design methodology
- Behavioral modeling
- Event-driven timing simulation
- AI-assisted engineering
- Open-source engineering education

---

# Philosophy

Traditional circuit simulators use **voltage** and **current** as state variables.

This simulator instead considers **time** as the primary state variable.

Each clock edge is represented by its timestamp, and the simulator predicts the timing of future events through behavioral models.

```
          Reference Edge
                 │
                 ▼
          Phase Detector
                 │
                 ▼
           Loop Filter
                 │
                 ▼
            Delay Model
                 │
                 ▼
           Feedback Edge
```

The simulation is therefore **event-driven** rather than **time-step driven**.

This approach provides orders-of-magnitude faster simulation for architecture exploration while preserving the essential timing behavior of the loop.

---

# Why not SPICE?

SPICE is indispensable for transistor-level verification.

However, many design decisions are architectural rather than circuit-level.

Designers often need to evaluate hundreds or thousands of parameter combinations before transistor sizing begins.

An event-driven behavioral simulator enables rapid exploration of:

- Lock behavior
- Loop stability
- Delay sensitivity
- Timing jitter
- Parameter optimization

This simulator complements SPICE rather than replacing it.

---

# AI-assisted Development

This project is also an experiment in collaborative engineering between human designers and AI.

The objective is not only to develop a DLL simulator, but also to document the complete engineering process:

- Design philosophy
- Architecture decisions
- Modeling assumptions
- Verification methodology
- Design evolution

The repository itself is intended to become an educational resource for future semiconductor designers.

---

# Objectives

The initial objectives are:

- Event-driven DLL simulation
- Lock behavior analysis
- Loop stability evaluation
- Delay model verification
- Timing jitter evaluation
- Parameter sensitivity analysis
- Educational platform for top-down timing design

---

# Development Roadmap

## Version 0.1

- [x] Project setup
- [x] Repository initialization
- [x] Design philosophy
- [x] Development environment

## Version 0.2

- [ ] Parameter definition
- [ ] Simulation state definition
- [ ] Architecture documentation

## Version 0.3

- [ ] Event simulation engine
- [ ] Reference clock model
- [ ] Delay model
- [ ] Phase detector

## Version 0.4

- [ ] Ideal DLL lock simulation
- [ ] Lock detector
- [ ] Waveform visualization

## Version 0.5

- [ ] Parameter sweep
- [ ] Metrics
- [ ] CSV export

## Version 0.6

- [ ] Charge pump model
- [ ] Loop filter
- [ ] VCDL behavioral model

## Version 0.7

- [ ] Jitter model
- [ ] Delay non-linearity
- [ ] Quantized delay
- [ ] Delay mismatch

## Version 1.0

- [ ] Complete DLL Top-Down Time Domain Simulator

---

# Project Structure

```
DLL_TopDown/
│
├── dll/
│   ├── params.py
│   ├── state.py
│   ├── simulator.py
│   ├── clock.py
│   ├── pfd.py
│   ├── delay_model.py
│   ├── lock_detector.py
│   ├── metrics.py
│   └── plots.py
│
├── docs/
│   ├── architecture.md
│   ├── design_notes.md
│   └── ai_journal.md
│
├── examples/
├── tests/
├── results/
│
└── run.py
```

---

# Design Principles

The simulator separates the following responsibilities:

- Design Parameters
- Simulation State
- Behavioral Models
- Event Simulation Engine
- Verification Metrics
- Visualization

Each functional block can be replaced independently without modifying the simulation engine.

---

# Future Extensions

Although the first target is a Delay Locked Loop, the simulation framework is intended to evolve into a general event-driven timing simulator supporting:

- Delay Locked Loops (DLL)
- Phase Locked Loops (PLL)
- Digital Controlled Oscillators (DCO)
- Clock Data Recovery (CDR)
- Clock Distribution Networks
- Timing Analysis
- Jitter Analysis

---

# Educational Goals

This project is being developed as an educational and research platform.

Students are encouraged not only to execute simulations, but also to understand:

- Why each model exists
- Which assumptions are made
- How abstractions are introduced
- How behavioral models relate to physical circuits

Understanding the modeling process is considered as important as understanding the simulation results.

---

# License

Apache License 2.0

---

# Author

Jun Okamura

Representative Director

OpenSUSI (Open Source Utilized Silicon Initiatives)

---

*"Time is the primary simulation variable."*
