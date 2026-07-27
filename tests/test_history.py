"""
test_history.py
"""

from dll.history import SimulationHistory
from dll.params import DLLParams
from dll.state import SimulationState


#
# ============================================================
# Test Helper
# ============================================================
#

def create_state() -> SimulationState:

    params = DLLParams.default()

    state = SimulationState.initial(
        params
    )

    return state


#
# ============================================================
# Constructor
# ============================================================
#

def test_create_history():

    history = SimulationHistory()

    assert isinstance(
        history,
        SimulationHistory,
    )


#
# ============================================================
# Initial History
# ============================================================
#

def test_initial_history_is_empty():

    history = SimulationHistory()

    assert history.data == {

        "cycle": [],

        "ref_edge_time": [],

        "fb_edge_time": [],

        "phase_error": [],

        "control": [],

        "delay": [],

        "locked": [],

    }


#
# ============================================================
# Record One State
# ============================================================
#

def test_record_state():

    history = SimulationHistory()

    state = create_state()

    state.cycle = 3

    state.ref_edge_time = 30e-9

    state.fb_edge_time = 32e-9

    state.phase_error = -2e-9

    state.control = -0.1

    state.delay = 2e-9

    state.locked = False

    history.record(
        state
    )

    assert history.data["cycle"] == [3]

    assert history.data["ref_edge_time"] == [30e-9]

    assert history.data["fb_edge_time"] == [32e-9]

    assert history.data["phase_error"] == [-2e-9]

    assert history.data["control"] == [-0.1]

    assert history.data["delay"] == [2e-9]

    assert history.data["locked"] == [False]


#
# ============================================================
# Record Multiple States
# ============================================================
#

def test_record_multiple_states():

    history = SimulationHistory()

    state = create_state()

    for cycle in range(3):

        state.cycle = cycle

        state.ref_edge_time = cycle * 10e-9

        state.fb_edge_time = cycle * 10e-9 + 2e-9

        state.phase_error = -2e-9

        state.control = -0.1 * cycle

        state.delay = 2e-9

        state.locked = (cycle == 2)

        history.record(
            state
        )

    assert history.data["cycle"] == [

        0,

        1,

        2,

    ]

    assert history.data["locked"] == [

        False,

        False,

        True,

    ]


#
# ============================================================
# Snapshot
# ============================================================
#

def test_record_creates_snapshot():

    history = SimulationHistory()

    state = create_state()

    state.cycle = 1

    state.control = 0.25

    state.delay = 5e-9

    history.record(
        state
    )

    state.cycle = 100

    state.control = 999.0

    state.delay = 999e-9

    assert history.data["cycle"] == [1]

    assert history.data["control"] == [0.25]

    assert history.data["delay"] == [5e-9]


#
# ============================================================
# Clear History
# ============================================================
#

def test_clear_history():

    history = SimulationHistory()

    state = create_state()

    history.record(
        state
    )

    history.clear()

    assert history.data == {

        "cycle": [],

        "ref_edge_time": [],

        "fb_edge_time": [],

        "phase_error": [],

        "control": [],

        "delay": [],

        "locked": [],

    }


#
# ============================================================
# History Length
# ============================================================
#

def test_history_fields_have_same_length():

    history = SimulationHistory()

    state = create_state()

    for cycle in range(5):

        state.cycle = cycle

        history.record(
            state
        )

    lengths = [

        len(values)

        for values in history.data.values()

    ]

    assert len(

        set(lengths)

    ) == 1

    assert lengths[0] == 5


#
# ============================================================
# Repeatability
# ============================================================
#

def test_repeatability():

    history1 = SimulationHistory()

    history2 = SimulationHistory()

    for history in (

        history1,

        history2,

    ):

        state = create_state()

        for cycle in range(3):

            state.cycle = cycle

            state.control = cycle

            history.record(
                state
            )

    assert history1.data == history2.data


#
# ============================================================
# State Integrity
# ============================================================
#

def test_state_is_not_modified():

    history = SimulationHistory()

    state = create_state()

    original = (

        state.cycle,

        state.ref_edge_time,

        state.fb_edge_time,

        state.phase_error,

        state.control,

        state.delay,

        state.locked,

        state.lock_counter,

    )

    history.record(
        state
    )

    current = (

        state.cycle,

        state.ref_edge_time,

        state.fb_edge_time,

        state.phase_error,

        state.control,

        state.delay,

        state.locked,

        state.lock_counter,

    )

    assert current == original
    