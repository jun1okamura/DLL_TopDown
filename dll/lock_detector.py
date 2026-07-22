"""
lock_detector.py

Lock detector for the Level 1 DLL simulator.

Issue #9 : Lock Detector
"""

from dll.params import DLLParams


class LockDetector:

    def __init__(self, params: DLLParams):

        # The phase-error threshold is normalized to
        # the reference-clock period and expressed in UI.
        self.phase_threshold_ui = (
            params.lock.phase_threshold_ui
        )

        self.required_lock_cycles = (
            params.lock.required_lock_cycles
        )

        self.t_ref = (
            params.clock.t_ref
        )

    def update(
        self,
        phase_error: float,
        lock_counter: int,
    ) -> tuple[int, bool]:

        # Convert the absolute phase error from seconds to UI.
        phase_error_ui = (
            abs(phase_error)
            / self.t_ref
        )

        # Lock requires the phase error to remain within
        # the threshold for consecutive reference cycles.
        if phase_error_ui <= self.phase_threshold_ui:

            updated_lock_counter = (
                lock_counter + 1
            )

        else:

            # A phase error outside the threshold breaks
            # the consecutive lock sequence.
            updated_lock_counter = 0

        locked = (
            updated_lock_counter
            >= self.required_lock_cycles
        )

        return (
            updated_lock_counter,
            locked,
        )
    