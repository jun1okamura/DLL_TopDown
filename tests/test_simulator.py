"""
test_simulator.py

Unit tests for simulator.py

Issue #5 : Event Simulation Engine
"""

from dll.params import DLLParams
from dll.simulator import DLLSimulator


# ============================================================
# Constructor
# ============================================================

def test_create_simulator():

    params = DLLParams.default()

    sim = DLLSimulator(params)

    assert sim.params is params

    assert sim.state.cycle == 0


# ============================================================
# One Step
# ============================================================

def test_step_advances_cycle():

    params = DLLParams.default()

    sim = DLLSimulator(params)

    sim.step()

    assert sim.state.cycle == 1


# ============================================================
# Reference Edge
# ============================================================

def test_reference_edge_updates():

    params = DLLParams.default()

    sim = DLLSimulator(params)

    sim.step()

    assert sim.state.ref_edge_time == 0.0

    sim.step()

    assert sim.state.ref_edge_time == params.clock.t_ref


# ============================================================
# Feedback Edge
# ============================================================

def test_delay_is_applied_next_cycle():

    params = DLLParams.default()

    sim = DLLSimulator(params)

    #
    # Cycle 0
    #
    sim.step()

    first_delay = sim.state.delay

    #
    # Cycle 1
    #
    sim.step()

    assert (
        sim.state.fb_edge_time
        == sim.state.ref_edge_time + first_delay
    )
    
# ============================================================
# History
# ============================================================

def test_history_is_recorded():

    params = DLLParams.default()

    sim = DLLSimulator(params)

    sim.step()

    assert len(sim.history["cycle"]) == 1
    assert len(sim.history["delay"]) == 1
    assert len(sim.history["control"]) == 1


# ============================================================
# Run
# ============================================================

def test_run_multiple_cycles():

    params = DLLParams.default()

    sim = DLLSimulator(params)

    sim.run()

    assert (
        sim.state.cycle
        == params.simulation.n_cycles
    )

    assert (
        len(sim.history["cycle"])
        == params.simulation.n_cycles
    )


# ============================================================
# Reset
# ============================================================

def test_reset():

    params = DLLParams.default()

    sim = DLLSimulator(params)

    sim.run()

    sim.reset()

    assert sim.state.cycle == 0

    assert len(sim.history["cycle"]) == 0

    assert sim.state.locked is False


# ============================================================
# Delay Limit
# ============================================================

def test_delay_is_limited():

    params = DLLParams.default()

    sim = DLLSimulator(params)

    for _ in range(100):

        sim.step()

    assert (
        params.delay.delay_min
        <= sim.state.delay
        <= params.delay.delay_max
    )
