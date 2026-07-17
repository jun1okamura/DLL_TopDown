"""
test_phase_detector.py

Unit tests for phase_detector.py

Issue #7 : Ideal Phase Detector
"""

import pytest

from dll.phase_detector import IdealPhaseDetector


# ============================================================
# Constructor
# ============================================================

def test_create_phase_detector():

    detector = IdealPhaseDetector()

    assert isinstance(detector, IdealPhaseDetector)


# ============================================================
# Zero Phase Error
# ============================================================

def test_zero_phase_error():

    detector = IdealPhaseDetector()

    phase_error = detector.update(
        ref_edge_time=10e-9,
        fb_edge_time=10e-9,
    )

    assert phase_error == pytest.approx(0.0)


# ============================================================
# Feedback Edge Arrives Late
# ============================================================

def test_feedback_edge_late():

    detector = IdealPhaseDetector()

    phase_error = detector.update(
        ref_edge_time=10e-9,
        fb_edge_time=12e-9,
    )

    assert phase_error == pytest.approx(-2e-9)


# ============================================================
# Feedback Edge Arrives Early
# ============================================================

def test_feedback_edge_early():

    detector = IdealPhaseDetector()

    phase_error = detector.update(
        ref_edge_time=10e-9,
        fb_edge_time=8e-9,
    )

    assert phase_error == pytest.approx(2e-9)


# ============================================================
# Absolute Edge Time Independence
# ============================================================

def test_phase_error_depends_only_on_time_difference():

    detector = IdealPhaseDetector()

    phase_error1 = detector.update(
        ref_edge_time=10e-9,
        fb_edge_time=12e-9,
    )

    phase_error2 = detector.update(
        ref_edge_time=100e-9,
        fb_edge_time=102e-9,
    )

    assert phase_error1 == pytest.approx(phase_error2)


# ============================================================
# Deterministic Behavior
# ============================================================

def test_repeatability():

    detector = IdealPhaseDetector()

    phase_error1 = detector.update(
        ref_edge_time=25e-9,
        fb_edge_time=27e-9,
    )

    phase_error2 = detector.update(
        ref_edge_time=25e-9,
        fb_edge_time=27e-9,
    )

    assert phase_error1 == phase_error2