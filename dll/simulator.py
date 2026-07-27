"""
simulator.py

Level 1 Event-Driven DLL Simulator.

Issue #5 : Event Simulation Engine
Issue #6 : Ideal Delay Model
Issue #7 : Ideal Phase Detector
Issue #8 : Ideal Loop Controller
Issue #9 : Lock Detector
Issue #10: Simulation History
Issue #11: Reference Clock
"""

from dll.params import DLLParams
from dll.state import SimulationState
from dll.phase_detector import IdealPhaseDetector
from dll.controller import IdealLoopController
from dll.delay_model import IdealDelayModel
from dll.lock_detector import LockDetector
from dll.history import SimulationHistory
from dll.reference_clock import ReferenceClock

class DLLSimulator:

    def __init__(self, params: DLLParams):

        self.params = params

        self.state = SimulationState.initial(params)

        self.reference_clock = ReferenceClock(params)

        self.phase_detector = IdealPhaseDetector()

        self.controller = IdealLoopController(params)

        self.lock_detector = LockDetector(params)

        self.delay_model = IdealDelayModel(params)

        self.history = SimulationHistory()

    def reset(self):

        self.state.reset(self.params)

        self.history.clear()

    def step(self) -> SimulationState:

        params = self.params
        state = self.state

        #
        # --------------------------------------------------
        # 1. Reference Edge
        # --------------------------------------------------
        #
        state.ref_edge_time = (
            self.reference_clock.update(
                state.cycle
            )
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
        self.history.record(state)

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

        return self.history.data
    