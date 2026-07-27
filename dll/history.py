"""
history.py
"""

from dll.state import SimulationState


class SimulationHistory:

    def __init__(self):

        self.clear()

    @property
    def data(self) -> dict[str, list]:

        return {
            "cycle": self.cycle,
            "ref_edge_time": self.ref_edge_time,
            "fb_edge_time": self.fb_edge_time,
            "phase_error": self.phase_error,
            "control": self.control,
            "delay": self.delay,
            "locked": self.locked,
        }

    def clear(self):

        self.cycle = []

        self.ref_edge_time = []

        self.fb_edge_time = []

        self.phase_error = []

        self.control = []

        self.delay = []

        self.locked = []

    def record(
        self,
        state: SimulationState,
    ):

        #
        # Store a snapshot of the current simulation state.
        #

        self.cycle.append(
            state.cycle
        )

        self.ref_edge_time.append(
            state.ref_edge_time
        )

        self.fb_edge_time.append(
            state.fb_edge_time
        )

        self.phase_error.append(
            state.phase_error
        )

        self.control.append(
            state.control
        )

        self.delay.append(
            state.delay
        )

        self.locked.append(
            state.locked
        )
       