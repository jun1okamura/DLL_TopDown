"""
simulator.py

Level 1 Event-Driven DLL Simulator.

Issue #5 : Event Simulation Engine
Issue #6 : Ideal Delay Model
Issue #7 : Ideal Phase Detector
Issue #8 : Ideal Loop Controller
Issue #9 : Lock Detector
"""

from dll.params import DLLParams
from dll.state import SimulationState
from dll.phase_detector import IdealPhaseDetector
from dll.controller import IdealLoopController
from dll.delay_model import IdealDelayModel
from dll.lock_detector import LockDetector

class DLLSimulator:

    def __init__(self, params: DLLParams):

        self.params = params

        self.state = SimulationState.initial(params)

        self.phase_detector = IdealPhaseDetector()

        self.controller = IdealLoopController(params)

        self.lock_detector = LockDetector(params)

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
        # 3. Ideal Phase Detector
        # --------------------------------------------------
        #

        state.phase_error = self.phase_detector.update(
            state.ref_edge_time,
            state.fb_edge_time,
        )

        #
        # --------------------------------------------------
        # 4. Lock Detection
        # --------------------------------------------------
        #
        (state.lock_counter, state.locked,) = self.lock_detector.update(
            state.phase_error, 
            state.lock_counter,
        )

        #
        # --------------------------------------------------
        # 5. Controller
        # --------------------------------------------------
        #

        state.control = self.controller.update(
            state.control,
            state.phase_error,
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
    