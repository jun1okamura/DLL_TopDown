"""
run.py

Example program for the DLL top-down simulator.
"""

import matplotlib.pyplot as plt

from dll.params import DLLParams
from dll.simulator import DLLSimulator
from dll.visualizer import Visualizer


def main() -> None:

    params = DLLParams.default()

    simulator = DLLSimulator(params)

    simulator.run()

    visualizer = Visualizer()

    fig1 = visualizer.plot_delay(
        simulator.history,
    )

    fig2 = visualizer.plot_control(
        simulator.history,
    )

    plt.show()

if __name__ == "__main__":
    main()
