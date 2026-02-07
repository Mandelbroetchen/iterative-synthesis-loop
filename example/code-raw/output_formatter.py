"""
Output Formatting Module
========================

This module handles the display and formatting of simulation results.
"""

def display_results(result):
    """
    Display simulation results in a formatted table.

    Args:
        result: SimulationResult object containing the simulation data
    """
    print("\nFreefall Simulation Results")
    print("===========================")
    print(result.display())
    print("\nSimulation complete.")
