"""
delay_model.py

Ideal delay model for the Level 1 DLL simulator.

Issue #6 : Ideal Delay Model
"""

from dll.params import DLLParams


class IdealDelayModel:
    """
    Ideal linear delay model.

    The delay is modeled as

        delay = delay_init + control * delay_gain

    and is limited to the configured minimum and
    maximum delay values.
    """

    def __init__(self, params: DLLParams):

        self.delay_init = params.delay.delay_init
        self.delay_gain = params.delay.delay_gain
        self.delay_min = params.delay.delay_min
        self.delay_max = params.delay.delay_max

    def update(self, control: float) -> float:
        """
        Calculate the delay corresponding to the
        supplied control value.
        """

        delay = (
            self.delay_init
            + control * self.delay_gain
        )

        delay = max(
            self.delay_min,
            min(delay, self.delay_max),
        )

        return delay