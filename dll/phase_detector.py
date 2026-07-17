"""
phase_detector.py

Ideal phase detector for the Level 1 DLL simulator.

Issue #7 : Ideal Phase Detector
"""


class IdealPhaseDetector:

    def update(
        self,
        ref_edge_time: float,
        fb_edge_time: float,
    ) -> float:

        # A positive phase error means that the
        # feedback edge arrives before the reference edge.
        #
        # A negative phase error means that the
        # feedback edge arrives after the reference edge.
        phase_error = (
            ref_edge_time
            - fb_edge_time
        )

        return phase_error
    