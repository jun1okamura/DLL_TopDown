"""
test_state.py

Unit tests for state.py

Issue #4 : Simulation State
"""

from dll.params import DLLParams
from dll.state import SimulationState

# ============================================================
# Initial State
# ============================================================

def test_create_initial_state():

    # The simulator shall be able to create
    # an initial state from the parameter set.

    params = DLLParams.default()

    state = SimulationState.initial(params)

    assert state.cycle == 0

    assert state.ref_edge_time == 0.0

    assert state.fb_edge_time == params.delay.delay_init

    assert state.phase_error == 0.0

    assert state.control == params.controller.control_init

    assert state.delay == params.delay.delay_init

    assert state.locked is False

    assert state.lock_counter == 0


# ============================================================
# Mutable State
# ============================================================

def test_state_is_mutable():

    # SimulationState is expected to change
    # during simulation.

    params = DLLParams.default()

    state = SimulationState.initial(params)

    state.cycle += 1
    state.control = 0.25
    state.delay = 12e-9

    assert state.cycle == 1
    assert state.control == 0.25
    assert state.delay == 12e-9


# ============================================================
# Reset
# ============================================================

def test_reset_state():

    # Reset shall restore the initial state
    # using the supplied parameter set.

    params = DLLParams.default()

    state = SimulationState.initial(params)

    state.cycle = 100
    state.phase_error = 1e-9
    state.control = 0.5
    state.delay = 15e-9
    state.locked = True
    state.lock_counter = 25

    state.reset(params)

    assert state.cycle == 0

    assert state.ref_edge_time == 0.0

    assert state.fb_edge_time == params.delay.delay_init

    assert state.phase_error == 0.0

    assert state.control == params.controller.control_init

    assert state.delay == params.delay.delay_init

    assert state.locked is False

    assert state.lock_counter == 0


# ============================================================
# Parameter Independence
# ============================================================

def test_state_does_not_modify_parameters():

    # Updating the simulation state shall never
    # modify the immutable parameter set.

    params = DLLParams.default()

    state = SimulationState.initial(params)

    state.delay = 18e-9
    state.control = 0.75

    assert params.delay.delay_init == 8e-9
    assert params.controller.control_init == 0.0
