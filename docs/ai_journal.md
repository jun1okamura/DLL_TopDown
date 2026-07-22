# AI Journal

This journal records the collaboration between the project owner and AI during the development of the DLL Top-Down Time Domain Simulator.

---

# Journal 001

**Date**

2026-07-13

**Topic**

Project Skeleton

---

## Objective

Establish the project foundation before implementation.

---

## Human Decisions

- Define the project vision.
- Reconstruct the original event-driven simulation concept from engineering experience.
- Choose Python as the implementation language.
- Decide to use Git and GitHub from the beginning.
- Define the project as an educational and research asset.
- Approve the simulator philosophy:
  > *Time is the primary simulation variable.*

---

## AI Contributions

- Proposed the software architecture.
- Organized the project directory structure.
- Suggested the documentation hierarchy.
- Assisted in writing README.md.
- Proposed the event-driven simulator framework.
- Suggested development milestones.

---

## Decisions

- Project name:
  **DLL Top-Down Time Domain Simulator**
- Event-driven simulation will be implemented first.
- Documentation precedes implementation.
- AI collaboration will be documented throughout the project.

---

## Next Step

- Define simulation parameters.
- Define simulation state.
- Design the software architecture.
- Implement the event simulation engine.

---

## Lessons Learned

A clear software architecture established before implementation significantly improves the quality of AI-assisted development.

# Journal 002

Topic

Simulation Architecture

Human Decisions

- Approved Level 1 scope.
- Approved module structure.
- Approved event processing order.

AI Contributions

- Proposed simulator architecture.
- Reviewed module responsibilities.
- Identified unresolved timing issues.

Lessons Learned

Architecture should be finalized before parameter implementation.

# Journal 003

Topic

Parameter Definition

Human Decisions

- Approved immutable parameter design.
- Selected dataclass(frozen=True).
- Separated configuration from simulation state.

AI Contributions

- Proposed parameter hierarchy.
- Suggested executable specification tests.
- Reviewed parameter validation strategy.

Lessons Learned

Executable specification using pytest provides an effective verification method for configuration objects.

Next Step

Implement Simulation State.

# Journal 004

Topic

Simulation State

Human Decisions

- Approved mutable simulation-state design.
- Separated state initialization from simulation behavior.
- Approved in-place reset of the state object.

AI Contributions

- Proposed the SimulationState data structure.
- Defined initialization and reset responsibilities.
- Proposed executable specification tests.

Lessons Learned

Separating immutable parameters from mutable state produces a clear boundary between simulation configuration and execution.

Next Step

Implement the Event Simulation Engine.

# Journal 005

## Topic

Event Simulation Engine

## Human Decisions

- Approved the first executable event-driven simulation engine.
- Adopted the rule that updated delay is applied from the next simulation cycle.
- Confirmed the execution order follows the approved architecture.

## AI Contributions

- Proposed the DLLSimulator class.
- Implemented the Level 1 event-driven simulation flow.
- Proposed executable specification tests for simulator behavior.

## Lessons Learned

Separating Parameters, State, and Simulator results in a clean event-driven architecture that can later be extended by replacing each algorithm block with dedicated models.

## Next Step

Separate the delay model from the simulator.

# Journal 006

## Topic

Ideal Delay Model

## Human Decisions

- Separated the delay calculation from the simulation engine.
- Adopted a stateless delay model with deterministic behavior.
- Confirmed that the updated delay is applied from the next simulation cycle.

## AI Contributions

- Designed the IdealDelayModel interface.
- Proposed separation of delay calculation from the simulator.
- Developed executable specification tests.

## Lessons Learned

Separating behavioral models from the event engine greatly improves readability, testability, and future extensibility.

## Next Step

Implement the Phase/Frequency Detector (PFD).

# Journal 007

## Topic

Ideal Phase Detector

## Human Decisions

- Separated phase-error calculation from the simulation engine.
- Defined the phase-error sign convention.
- Confirmed that the phase detector should remain stateless and deterministic.

## AI Contributions

- Designed the IdealPhaseDetector interface.
- Proposed executable specification tests for phase-error behavior.
- Integrated the phase detector into DLLSimulator.

## Lessons Learned

Explicitly defining and testing the phase-error sign convention is important because the convention directly affects the behavior and stability of the loop controller.

Floating-point physical quantities should be compared using approximate equality in unit tests.

## Next Step

Implement the Ideal Loop Controller.

# Journal 008

## Topic

Ideal Loop Controller

## Human Decisions

- Separated the control-update algorithm from the simulation engine.
- Adopted a stateless and deterministic controller.
- Confirmed the control direction forms negative feedback with the phase detector and delay model.
- Approved the ideal discrete-time control equation.

## AI Contributions

- Proposed the `IdealLoopController` interface.
- Organized the controller as an independent component.
- Proposed executable specification tests.
- Reviewed integration with `DLLSimulator`.

## Lessons Learned

The phase-error sign convention, controller polarity, and delay sensitivity must be considered together to ensure negative feedback.

Separating the controller from the simulation engine improves testability and allows future replacement with PI or other controller models.

## Verification

All regression tests passed.

```text
45 passed