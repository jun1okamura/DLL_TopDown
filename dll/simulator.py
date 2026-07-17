"""
simulator.py

Level 1 Event-Driven DLL Simulator.

Issue #5 : Event Simulation Engine
Issue #6 : Ideal Delay Model
"""

from dll.delay_model import IdealDelayModel
from dll.params import DLLParams
from dll.state import SimulationState


class DLLSimulator:

    def __init__(self, params: DLLParams):

        self.params = params

        self.state = SimulationState.initial(params)

        self.delay_model = IdealDelayModel(params)

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

    def step(self) -> SimulationState:

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

        # The delay stored at the beginning of this step
        # determines the current feedback-edge timing.
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

        phase_error_ui = (
            abs(state.phase_error)
            / params.clock.t_ref
        )

        if (
            phase_error_ui
            <= params.lock.phase_threshold_ui
        ):

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
        # 6. Ideal Delay Model
        # --------------------------------------------------
        #

        # The newly calculated delay is used from
        # the next simulation cycle.
        state.delay = self.delay_model.update(
            state.control
        )

        #
        # --------------------------------------------------
        # 7. Record History
        # --------------------------------------------------
        #

        self.history["cycle"].append(
            state.cycle
        )

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

    def run(self) -> dict[str, list]:

        for _ in range(
            self.params.simulation.n_cycles
        ):

            self.step()

        return self.history