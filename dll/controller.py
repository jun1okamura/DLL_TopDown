"""
controller.py
"""

from dll.params import DLLParams

class IdealLoopController:

    def __init__(self, params: DLLParams):

        self.loop_gain = (
            params.controller.loop_gain
        )

        self.t_ref = (
            params.clock.t_ref
        )

    def update(
        self,
        control: float,
        phase_error: float,
    ) -> float:

        control_delta = (
            self.loop_gain
            * phase_error
            / self.t_ref
        )

        updated_control = (
            control
            + control_delta
        )

        return updated_control