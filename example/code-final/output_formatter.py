"""
Output Formatting Module
========================

This module handles the display and formatting of simulation results.
"""

from freefall_simulator import SimulationResult, WarningGenerator

def display_results(result: SimulationResult):
    """
    Display simulation results in a formatted table.

    Args:
        result: SimulationResult object containing the simulation data
    """
    print("\nFreefall Simulation Results")
    print("=" * 30)
    print(result.get_summary())

    if result.impact_time is not None:
        print("\n" + WarningGenerator.ground_collision_warning(result.impact_time))

    print("\nResults:")
    print(result.display())

    final_pos, final_vel, final_acc = result.get_final_values()
    print(f"\nFinal values:")
    print(f"- Position: {final_pos:.2f} m")
    print(f"- Velocity: {final_vel:.2f} m/s")
    print(f"- Acceleration: {final_acc:.2f} m/s²")

    print("\nSimulation complete.")
