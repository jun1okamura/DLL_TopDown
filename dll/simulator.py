"""
simulator.py

Level 1 Event-Driven DLL Simulator.

Issue #5 : Event Simulation Engine
"""

from dll.params import DLLParams
from dll.state import SimulationState


class DLLSimulator:
    """
    Level 1 event-driven DLL simulator.
    """

    def __init__(self, params: DLLParams):

        self.params = params

        self.state = SimulationState.initial(params)

        self.history = {
            "cycle": [],
            "ref_edge_time": [],
            "fb_edge_time": [],
            "phase_error": [],
            "control": [],
            "delay": [],
            "locked": [],
        }

    def reset(self):

        self.state.reset(self.params)

        for values in self.history.values():
            values.clear()

    def step(self):

        params = self.params
        state = self.state

        #
        # --------------------------------------------------
        # 1. Reference Edge
        # --------------------------------------------------
        #

        state.ref_edge_time = (
            state.cycle
            * params.clock.t_ref
        )

        #
        # --------------------------------------------------
        # 2. Feedback Edge
        # --------------------------------------------------
        #

        state.fb_edge_time = (
            state.ref_edge_time
            + state.delay
        )

        #
        # --------------------------------------------------
        # 3. Phase Error
        # --------------------------------------------------
        #

        state.phase_error = (
            state.ref_edge_time
            - state.fb_edge_time
        )

        #
        # --------------------------------------------------
        # 4. Lock Detection
        # --------------------------------------------------
        #

        phase_error_ui = abs(
            state.phase_error
        ) / params.clock.t_ref

        if phase_error_ui <= params.lock.phase_threshold_ui:

            state.lock_counter += 1

        else:

            state.lock_counter = 0

        state.locked = (
            state.lock_counter
            >= params.lock.required_lock_cycles
        )

        #
        # --------------------------------------------------
        # 5. Controller
        # --------------------------------------------------
        #

        state.control += (
            params.controller.loop_gain
            * state.phase_error
            / params.clock.t_ref
        )

        #
        # --------------------------------------------------
        # 6. Delay Line
        # --------------------------------------------------
        #

        state.delay = (
            params.delay.delay_init
            + state.control
            * params.delay.delay_gain
        )

        state.delay = max(
            params.delay.delay_min,
            min(
                state.delay,
                params.delay.delay_max,
            ),
        )

        #
        # --------------------------------------------------
        # 7. Record History
        # --------------------------------------------------
        #

        self.history["cycle"].append(state.cycle)

        self.history["ref_edge_time"].append(
            state.ref_edge_time
        )

        self.history["fb_edge_time"].append(
            state.fb_edge_time
        )

        self.history["phase_error"].append(
            state.phase_error
        )

        self.history["control"].append(
            state.control
        )

        self.history["delay"].append(
            state.delay
        )

        self.history["locked"].append(
            state.locked
        )

        #
        # --------------------------------------------------
        # 8. Advance Cycle
        # --------------------------------------------------
        #

        state.cycle += 1

        return state

    def run(self):

        for _ in range(
            self.params.simulation.n_cycles
        ):

            self.step()

        return self.history
    