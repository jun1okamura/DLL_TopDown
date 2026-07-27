"""
reference_clock.py
"""

from dll.params import DLLParams


class ReferenceClock:

    def __init__(
        self,
        params: DLLParams,
    ):

        self.t_ref = (
            params.clock.t_ref
        )

    def update(
        self,
        cycle: int,
    ) -> float:

        return (
            cycle
            * self.t_ref
        )
