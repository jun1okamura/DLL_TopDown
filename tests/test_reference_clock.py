"""
test_reference_clock.py
"""

from dll.params import DLLParams
from dll.reference_clock import ReferenceClock


#
# ============================================================
# Test Helper
# ============================================================
#

def create_clock() -> ReferenceClock:

    params = DLLParams.default()

    return ReferenceClock(
        params
    )


#
# ============================================================
# Constructor
# ============================================================
#

def test_create_reference_clock():

    clock = create_clock()

    assert isinstance(
        clock,
        ReferenceClock,
    )


#
# ============================================================
# Cycle Zero
# ============================================================
#

def test_cycle_zero():

    params = DLLParams.default()

    clock = ReferenceClock(
        params
    )

    assert (
        clock.update(0)
        == 0.0
    )


#
# ============================================================
# Cycle One
# ============================================================
#

def test_cycle_one():

    params = DLLParams.default()

    clock = ReferenceClock(
        params
    )

    assert (
        clock.update(1)
        == params.clock.t_ref
    )


#
# ============================================================
# Multiple Cycles
# ============================================================
#

def test_multiple_cycles():

    params = DLLParams.default()

    clock = ReferenceClock(
        params
    )

    for cycle in range(10):

        assert (
            clock.update(cycle)
            == cycle * params.clock.t_ref
        )


#
# ============================================================
# Repeatability
# ============================================================
#

def test_repeatability():

    clock = create_clock()

    value1 = clock.update(7)

    value2 = clock.update(7)

    assert value1 == value2


#
# ============================================================
# Parameters Are Not Modified
# ============================================================
#

def test_params_are_not_modified():

    params = DLLParams.default()

    original = (
        params.clock.t_ref,
    )

    clock = ReferenceClock(
        params
    )

    for cycle in range(10):

        clock.update(
            cycle
        )

    current = (
        params.clock.t_ref,
    )

    assert current == original