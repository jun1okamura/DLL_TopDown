"""
state.py

Mutable state definition for the DLL Top-Down Time Domain Simulator.

Issue #4 : Simulation State
"""

from dataclasses import dataclass

from dll.params import DLLParams


# ============================================================
# Simulation State
# ============================================================

# SimulationState represents one mutable snapshot of the DLL.
#
# Parameters describe the fixed simulation configuration.
# State represents values that evolve during simulation.
#
# Behavioral calculations are intentionally excluded from this
# class. The simulation engine will update these fields.


@dataclass
class SimulationState:

    # Number of completed simulation cycles.
    cycle: int

    # Current reference-clock edge timestamp [s].
    ref_edge_time: float

    # Current feedback edge timestamp [s].
    fb_edge_time: float

    # Current phase error [s].
    #
    # The exact sign convention remains an implementation decision
    # for the phase detector and is not defined by this data class.
    phase_error: float

    # Current controller output [dimensionless].
    control: float

    # Current delay-line delay [s].
    delay: float

    # Current lock indication.
    locked: bool

    # Number of consecutive cycles satisfying the lock criterion.
    lock_counter: int

    @classmethod
    def initial(cls, params: DLLParams) -> "SimulationState":

        # Initial values are derived from the approved parameter set.
        #
        # Keeping initialization in one place avoids duplicated
        # assumptions in the simulator and test code.

        return cls(
            cycle=0,
            ref_edge_time=0.0,
            fb_edge_time=params.delay.delay_init,
            phase_error=0.0,
            control=params.controller.control_init,
            delay=params.delay.delay_init,
            locked=False,
            lock_counter=0,
        )

    def reset(self, params: DLLParams) -> None:

        # Reset modifies the existing object instead of replacing it.
        #
        # This allows other simulator components to retain a reference
        # to the same state object throughout a simulation session.

        initial_state = type(self).initial(params)

        self.cycle = initial_state.cycle
        self.ref_edge_time = initial_state.ref_edge_time
        self.fb_edge_time = initial_state.fb_edge_time
        self.phase_error = initial_state.phase_error
        self.control = initial_state.control
        self.delay = initial_state.delay
        self.locked = initial_state.locked
        self.lock_counter = initial_state.lock_counter
        
            