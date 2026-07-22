"""
test_lock_detector.py

Unit tests for lock_detector.py.

Issue #9 : Lock Detector
"""

import pytest

from dll.lock_detector import LockDetector
from dll.params import DLLParams


#
# ============================================================
# Constructor
# ============================================================
#

def test_create_lock_detector():

    params = DLLParams.default()

    detector = LockDetector(params)

    assert isinstance(
        detector,
        LockDetector,
    )


#
# ============================================================
# Zero Phase Error
# ============================================================
#

def test_zero_phase_error():

    params = DLLParams.default()

    detector = LockDetector(params)

    lock_counter, locked = detector.update(
        phase_error=0.0,
        lock_counter=0,
    )

    assert lock_counter == 1
    assert locked is False


#
# ============================================================
# Error Within Threshold
# ============================================================
#

def test_error_within_threshold():

    params = DLLParams.default()

    detector = LockDetector(params)

    phase_error = (
        params.lock.phase_threshold_ui
        * params.clock.t_ref
        * 0.5
    )

    lock_counter, locked = detector.update(
        phase_error=phase_error,
        lock_counter=0,
    )

    assert lock_counter == 1
    assert locked is False


#
# ============================================================
# Error At Threshold
# ============================================================
#

def test_error_at_threshold():

    params = DLLParams.default()

    detector = LockDetector(params)

    phase_error = (
        params.lock.phase_threshold_ui
        * params.clock.t_ref
    )

    lock_counter, locked = detector.update(
        phase_error=phase_error,
        lock_counter=0,
    )

    assert lock_counter == 1
    assert locked is False


#
# ============================================================
# Positive and Negative Errors
# ============================================================
#

def test_positive_and_negative_errors_are_equivalent():

    params = DLLParams.default()

    detector = LockDetector(params)

    phase_error = (
        params.lock.phase_threshold_ui
        * params.clock.t_ref
        * 0.5
    )

    positive_result = detector.update(
        phase_error=phase_error,
        lock_counter=0,
    )

    negative_result = detector.update(
        phase_error=-phase_error,
        lock_counter=0,
    )

    assert positive_result == negative_result


#
# ============================================================
# Error Outside Threshold
# ============================================================
#

def test_error_outside_threshold():

    params = DLLParams.default()

    detector = LockDetector(params)

    phase_error = (
        params.lock.phase_threshold_ui
        * params.clock.t_ref
        * 2.0
    )

    lock_counter, locked = detector.update(
        phase_error=phase_error,
        lock_counter=5,
    )

    assert lock_counter == 0
    assert locked is False


#
# ============================================================
# Not Locked Before Required Cycles
# ============================================================
#

def test_not_locked_before_required_cycles():

    params = DLLParams.default()

    detector = LockDetector(params)

    lock_counter = (
        params.lock.required_lock_cycles
        - 2
    )

    lock_counter, locked = detector.update(
        phase_error=0.0,
        lock_counter=lock_counter,
    )

    assert lock_counter == (
        params.lock.required_lock_cycles
        - 1
    )

    assert locked is False


#
# ============================================================
# Lock After Required Cycles
# ============================================================
#

def test_lock_after_required_cycles():

    params = DLLParams.default()

    detector = LockDetector(params)

    lock_counter = 0
    locked = False

    for _ in range(
        params.lock.required_lock_cycles
    ):

        lock_counter, locked = detector.update(
            phase_error=0.0,
            lock_counter=lock_counter,
        )

    assert lock_counter == (
        params.lock.required_lock_cycles
    )

    assert locked is True


#
# ============================================================
# Lock Lost After Large Error
# ============================================================
#

def test_lock_is_lost_after_large_error():

    params = DLLParams.default()

    detector = LockDetector(params)

    lock_counter = (
        params.lock.required_lock_cycles
    )

    phase_error = (
        params.lock.phase_threshold_ui
        * params.clock.t_ref
        * 2.0
    )

    lock_counter, locked = detector.update(
        phase_error=phase_error,
        lock_counter=lock_counter,
    )

    assert lock_counter == 0
    assert locked is False


#
# ============================================================
# Repeatability
# ============================================================
#

def test_repeatability():

    params = DLLParams.default()

    detector = LockDetector(params)

    phase_error = (
        params.lock.phase_threshold_ui
        * params.clock.t_ref
        * 0.5
    )

    result1 = detector.update(
        phase_error=phase_error,
        lock_counter=3,
    )

    result2 = detector.update(
        phase_error=phase_error,
        lock_counter=3,
    )

    assert result1 == result2


#
# ============================================================
# Parameters Are Not Modified
# ============================================================
#

def test_params_are_not_modified():

    params = DLLParams.default()

    phase_threshold_ui = (
        params.lock.phase_threshold_ui
    )

    required_lock_cycles = (
        params.lock.required_lock_cycles
    )

    t_ref = params.clock.t_ref

    detector = LockDetector(params)

    detector.update(
        phase_error=0.0,
        lock_counter=0,
    )

    assert (
        params.lock.phase_threshold_ui
        == pytest.approx(phase_threshold_ui)
    )

    assert (
        params.lock.required_lock_cycles
        == required_lock_cycles
    )

    assert (
        params.clock.t_ref
        == pytest.approx(t_ref)
    )