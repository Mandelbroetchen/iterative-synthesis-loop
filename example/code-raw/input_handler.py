"""
Input Handling Module
=====================

This module handles user input collection and validation for the freefall simulation.
"""

def get_float_input(prompt: str, min_val: float = None, max_val: float = None) -> float:
    """
    Get and validate a float input from the user.

    Args:
        prompt: Input prompt message
        min_val: Minimum allowed value (inclusive)
        max_val: Maximum allowed value (inclusive)

    Returns:
        Validated float value

    Raises:
        ValueError: If input cannot be converted to float or is out of bounds
    """
    while True:
        try:
            value = float(input(prompt))
            if min_val is not None and value < min_val:
                print(f"Value must be ≥ {min_val}")
                continue
            if max_val is not None and value > max_val:
                print(f"Value must be ≤ {max_val}")
                continue
            return value
        except ValueError:
            print("Please enter a valid number")

def collect_parameters() -> dict:
    """
    Collect all simulation parameters from user input.

    Returns:
        Dictionary containing all simulation parameters
    """
    print("Freefall Simulation - Parameter Input")
    print("------------------------------------")

    params = {
        'h0': get_float_input("Initial height (m): ", min_val=0),
        'v0': get_float_input("Initial velocity (m/s): "),
        'dt': get_float_input("Time step (s): ", min_val=0.001, max_val=10),
        'T': get_float_input("Total duration (s): ", min_val=0.001, max_val=3600),
        'g': get_float_input("Gravitational acceleration (m/s²) [default=9.81]: ", min_val=0) or 9.81
    }

    return params
