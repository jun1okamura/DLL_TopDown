# DLL Top-Down Time Domain Simulator

A Python-based event-driven behavioral simulator for Delay Locked Loops (DLLs).

The simulator is intended for top-down architecture exploration, loop stability analysis, lock behavior verification, and timing jitter evaluation. Unlike SPICE-based circuit simulators, this project models the behavior of a DLL using **time-domain edge events**, making it suitable for rapid architectural studies and educational purposes.

---

## Philosophy

Traditional circuit simulators use voltage and current as state variables.

This simulator instead considers **time** as the primary state variable.

Each clock edge is represented by its timestamp, and the simulator predicts the timing of the next edge by propagating events through behavioral models.

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

The simulation is therefore **event-driven** rather than time-step driven.

---

## Objectives

- Event-driven DLL simulation
- DLL lock behavior analysis
- Loop stability evaluation
- Delay model verification
- Timing jitter evaluation
- Educational platform for top-down timing design

---

## Features (Planned)

### Level 1
- Ideal edge-event simulation
- Ideal phase detector
- Ideal delay model
- Lock detector
- Parameter sweep

### Level 2
- Charge pump model
- Loop filter
- VCDL behavioral model
- Delay non-linearity
- Delay quantization
- Input clock jitter

### Level 3
- Charge pump ripple
- Multi-stage delay line
- Device mismatch
- Monte Carlo simulation
- Statistical jitter analysis

---

## Project Structure

```
DLL_TopDown/
│
├── dll/
│   ├── params.py
│   ├── simulator.py
│   ├── state.py
│   ├── pfd.py
│   ├── delay_model.py
│   ├── lock_detector.py
│   ├── metrics.py
│   └── plots.py
│
├── examples/
├── tests/
├── docs/
├── results/
│
└── run.py
```

---

## Design Concept

The simulator separates:

- Design Parameters
- Behavioral Models
- Simulation Engine
- Verification Metrics
- Visualization

Each functional block can be replaced independently without modifying the simulator core.

---

## Future Extensions

The event-driven simulation engine is intended to become a common platform for:

- Delay Locked Loops (DLL)
- Phase Locked Loops (PLL)
- Clock Data Recovery (CDR)
- Clock Distribution Networks
- Timing Jitter Analysis

---

## License

Apache License 2.0

---

## Author

OpenSUSI