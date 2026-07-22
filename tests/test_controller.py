"""
test_controller.py
"""

import pytest

from dll.controller import IdealLoopController
from dll.params import DLLParams


#
# ============================================================
# Constructor
# ============================================================
#

def test_create_controller():

    params = DLLParams.default()

    controller = IdealLoopController(params)

    assert isinstance(
        controller,
        IdealLoopController,
    )


#
# ============================================================
# Zero Phase Error
# ============================================================
#

def test_zero_phase_error():

    params = DLLParams.default()

    controller = IdealLoopController(params)

    control = controller.update(
        control=0.5,
        phase_error=0.0,
    )

    assert control == pytest.approx(0.5)


#
# ============================================================
# Positive Phase Error
# ============================================================
#

def test_positive_phase_error():

    params = DLLParams.default()

    controller = IdealLoopController(params)

    control = controller.update(
        control=0.0,
        phase_error=1e-9,
    )

    assert control > 0.0


#
# ============================================================
# Negative Phase Error
# ============================================================
#

def test_negative_phase_error():

    params = DLLParams.default()

    controller = IdealLoopController(params)

    control = controller.update(
        control=0.0,
        phase_error=-1e-9,
    )

    assert control < 0.0


#
# ============================================================
# Ideal Update Equation
# ============================================================
#

def test_control_update_equation():

    params = DLLParams.default()

    controller = IdealLoopController(params)

    control = 0.5

    phase_error = 2e-9

    updated = controller.update(
        control,
        phase_error,
    )

    expected = (
        control
        + params.controller.loop_gain
        * phase_error
        / params.clock.t_ref
    )

    assert updated == pytest.approx(expected)


#
# ============================================================
# Linearity
# ============================================================
#

def test_linearity():

    params = DLLParams.default()

    controller = IdealLoopController(params)

    control1 = controller.update(
        control=0.0,
        phase_error=1e-9,
    )

    control2 = controller.update(
        control=0.0,
        phase_error=2e-9,
    )

    assert control2 == pytest.approx(
        control1 * 2.0
    )


#
# ============================================================
# Repeatability
# ============================================================
#

def test_repeatability():

    params = DLLParams.default()

    controller = IdealLoopController(params)

    control1 = controller.update(
        control=0.25,
        phase_error=3e-9,
    )

    control2 = controller.update(
        control=0.25,
        phase_error=3e-9,
    )

    assert control1 == pytest.approx(
        control2
    )


#
# ============================================================
# Stateless Behavior
# ============================================================
#

def test_stateless():

    params = DLLParams.default()

    controller = IdealLoopController(params)

    first = controller.update(
        control=0.0,
        phase_error=1e-9,
    )

    second = controller.update(
        control=0.0,
        phase_error=1e-9,
    )

    assert first == pytest.approx(
        second
    )


#
# ============================================================
# Parameters Are Not Modified
# ============================================================
#

def test_params_are_not_modified():

    params = DLLParams.default()

    loop_gain = params.controller.loop_gain

    t_ref = params.clock.t_ref

    controller = IdealLoopController(params)

    controller.update(
        control=0.3,
        phase_error=2e-9,
    )

    assert (
        params.controller.loop_gain
        == loop_gain
    )

    assert (
        params.clock.t_ref
        == t_ref
    )