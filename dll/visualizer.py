"""
visualizer.py

Visualization utilities for the DLL simulator.
"""

import matplotlib.pyplot as plt

from matplotlib.figure import Figure

from dll.history import SimulationHistory


class Visualizer:

    def plot_delay(
        self,
        history: SimulationHistory,
    ) -> Figure:

        data = history.data

        fig, ax = plt.subplots(
            figsize=(8, 5),
        )

        ax.plot(
            data["cycle"],
            data["delay"],
            linewidth=2,
        )

        ax.set_title("Delay")
        ax.set_xlabel("Cycle")
        ax.set_ylabel("Delay (s)")

        ax.grid(
            which="major",
            linestyle="--",
            alpha=0.5,
        )

        fig.tight_layout()

        return fig

    def plot_control(
        self,
        history: SimulationHistory,
    ) -> Figure:

        data = history.data

        fig, ax = plt.subplots(
            figsize=(8, 5),
        )

        ax.plot(
            data["cycle"],
            data["control"],
            linewidth=2,
        )

        ax.set_title("Control")
        ax.set_xlabel("Cycle")
        ax.set_ylabel("Control")

        ax.grid(
            which="major",
            linestyle="--",
            alpha=0.5,
        )

        fig.tight_layout()

        return fig
    