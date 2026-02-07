"""
Main Application Module
=======================

Entry point for the freefall simulation application.
"""

from input_handler import collect_parameters
from freefall_simulator import FreefallSimulator
from output_formatter import display_results

def main():
    """Main application entry point."""
    try:
        # Collect input parameters
        params = collect_parameters()

        # Initialize and run simulation
        simulator = FreefallSimulator(**params)
        result = simulator.run_simulation()

        # Display results
        display_results(result)

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please try again with valid inputs.")

if __name__ == "__main__":
    main()
