"""
params.py

Parameter definitions for the DLL Top-Down Time Domain Simulator.

Issue #3 : Parameter Definition
"""

from dataclasses import dataclass
from typing import Optional


# ============================================================
# Simulation Parameters
# ============================================================

# Parameters that control the simulation itself.
#
# These values define "how" the simulator runs,
# not the behavior of the DLL.


@dataclass(frozen=True)
class SimulationParams:

    n_cycles: int = 1000
    random_seed: Optional[int] = None
    verbose: bool = False

    def __post_init__(self):

        if self.n_cycles <= 0:
            raise ValueError("n_cycles must be positive.")


# ============================================================
# Reference Clock Parameters
# ============================================================

# The reference clock is assumed to be ideal.
#
# Level 1 intentionally ignores
#
#   - jitter
#   - frequency drift
#   - phase noise
#
# The reference period is always derived from the
# reference frequency to avoid inconsistent settings.


@dataclass(frozen=True)
class ClockParams:

    # Reference frequency [Hz]
    f_ref: float = 100e6

    def __post_init__(self):

        if self.f_ref <= 0:
            raise ValueError("Reference frequency must be positive.")

    @property
    def t_ref(self) -> float:

        # Reference period [s]
        return 1.0 / self.f_ref


# ============================================================
# Loop Controller Parameters
# ============================================================

# The controller updates the control value once
# per reference edge.
#
# Level 1 assumes an ideal discrete-time controller.
#
# Example
#
# control[n+1]
#     = control[n]
#     + loop_gain * phase_error[n]
#
# The exact algorithm will be implemented
# in Issue #5.


@dataclass(frozen=True)
class ControllerParams:

    # Loop gain [dimensionless]
    loop_gain: float = 0.05

    # Initial controller output
    control_init: float = 0.0

    # Allowed controller range
    control_min: float = -1.0
    control_max: float = 1.0

    def __post_init__(self):

        if self.loop_gain <= 0:
            raise ValueError("loop_gain must be positive.")

        if self.control_min >= self.control_max:
            raise ValueError("Invalid controller range.")

        if not (self.control_min <= self.control_init <= self.control_max):
            raise ValueError("control_init is outside control range.")


# ============================================================
# Delay Model Parameters
# ============================================================

# Level 1 uses an ideal linear delay model.
#
# delay
#
#     = delay_init
#     + control * delay_gain
#
# Future versions may introduce
#
#   - saturation
#   - nonlinearity
#   - quantization
#   - mismatch


@dataclass(frozen=True)
class DelayParams:

    # Initial delay [s]
    delay_init: float = 8.0e-9

    # Delay sensitivity [s / control]
    delay_gain: float = 1.0e-9

    # Allowed delay range [s]
    delay_min: float = 0.0
    delay_max: float = 20.0e-9

    def __post_init__(self):

        if self.delay_gain <= 0:
            raise ValueError("delay_gain must be positive.")

        if self.delay_min >= self.delay_max:
            raise ValueError("Invalid delay range.")

        if not (self.delay_min <= self.delay_init <= self.delay_max):
            raise ValueError("delay_init is outside delay range.")


# ============================================================
# Lock Detector Parameters
# ============================================================

# The DLL is considered locked when
#
# phase_error
#
# remains smaller than
#
# phase_threshold_ui
#
# for
#
# required_lock_cycles
#
# consecutive reference cycles.


@dataclass(frozen=True)
class LockParams:

    # Lock threshold [UI]
    phase_threshold_ui: float = 0.01

    # Required consecutive cycles
    required_lock_cycles: int = 10

    # Maximum simulation cycles
    timeout_cycles: int = 1000

    def __post_init__(self):

        if self.phase_threshold_ui <= 0:
            raise ValueError("phase_threshold_ui must be positive.")

        if self.required_lock_cycles <= 0:
            raise ValueError("required_lock_cycles must be positive.")

        if self.timeout_cycles <= 0:
            raise ValueError("timeout_cycles must be positive.")


# ============================================================
# Top-Level Parameter Container
# ============================================================

# DLLParams is the only parameter object visible
# from the simulator.
#
# All parameter groups are collected here.
#
# Parameter values remain immutable during
# one simulation run.


@dataclass(frozen=True)
class DLLParams:

    simulation: SimulationParams
    clock: ClockParams
    controller: ControllerParams
    delay: DelayParams
    lock: LockParams

    @classmethod
    def default(cls):

        # Create the default parameter set.

        return cls(
            simulation=SimulationParams(),
            clock=ClockParams(),
            controller=ControllerParams(),
            delay=DelayParams(),
            lock=LockParams(),
        )