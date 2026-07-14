"""
test_params.py

Unit tests for params.py

Issue #3 : Parameter Definition
"""

import pytest

from dll.params import (
    DLLParams,
    SimulationParams,
    ClockParams,
    ControllerParams,
    DelayParams,
    LockParams,
)


# ============================================================
# Default Parameter Set
# ============================================================

def test_default_parameter_set():

    # The simulator shall provide
    # a complete default parameter set.

    params = DLLParams.default()

    assert isinstance(params.simulation, SimulationParams)
    assert isinstance(params.clock, ClockParams)
    assert isinstance(params.controller, ControllerParams)
    assert isinstance(params.delay, DelayParams)
    assert isinstance(params.lock, LockParams)


# ============================================================
# Reference Clock
# ============================================================

def test_reference_period():

    # Reference period is derived
    # from the reference frequency.

    params = DLLParams.default()

    assert params.clock.f_ref == 100e6
    assert params.clock.t_ref == pytest.approx(10e-9)


# ============================================================
# Controller
# ============================================================

def test_controller_default_range():

    params = DLLParams.default()

    assert params.controller.control_min \
        <= params.controller.control_init \
        <= params.controller.control_max


def test_invalid_controller_range():

    with pytest.raises(ValueError):

        ControllerParams(
            control_min=1.0,
            control_max=0.0,
        )


# ============================================================
# Delay Model
# ============================================================

def test_delay_default_range():

    params = DLLParams.default()

    assert params.delay.delay_min \
        <= params.delay.delay_init \
        <= params.delay.delay_max


def test_invalid_delay():

    with pytest.raises(ValueError):

        DelayParams(
            delay_init=100e-9,
        )


# ============================================================
# Lock Detector
# ============================================================

def test_lock_parameter():

    params = DLLParams.default()

    assert params.lock.phase_threshold_ui > 0
    assert params.lock.required_lock_cycles > 0
    assert params.lock.timeout_cycles > 0


# ============================================================
# Simulation
# ============================================================

def test_simulation_cycles():

    params = DLLParams.default()

    assert params.simulation.n_cycles > 0


def test_invalid_simulation_cycles():

    with pytest.raises(ValueError):

        SimulationParams(
            n_cycles=0,
        )


# ============================================================
# Parameter Immutability
# ============================================================

def test_parameters_are_immutable():

    params = DLLParams.default()

    with pytest.raises(Exception):

        params.clock.f_ref = 200e6