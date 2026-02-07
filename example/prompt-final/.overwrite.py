from pathlib import Path

files = {
    "code-raw/freefall_simulator.py": """\"\"\"
Freefall Simulation Module
==========================

This module implements the physics calculations and simulation logic for freefall motion
under constant gravitational acceleration.
\"\"\"

class SimulationResult:
    \"\"\"Container for simulation results at each time step.\"\"\"

    def __init__(self):
        self.time = []
        self.position = []
        self.velocity = []
        self.acceleration = []

    def display(self):
        \"\"\"Format simulation results as a table string.\"\"\"
        header = \"Time (s) | Position (m) | Velocity (m/s) | Acceleration (m/s²)\"
        separator = \"-\" * len(header)
        rows = [f\"{t:8.2f} | {h:12.2f} | {v:14.2f} | {a:18.2f}\"
                for t, h, v, a in zip(self.time, self.position, self.velocity, self.acceleration)]
        return \"\\n\".join([header, separator] + rows)

class FreefallSimulator:
    \"\"\"Core physics engine for freefall simulation.\"\"\"

    def __init__(self, h0: float, v0: float, dt: float, T: float, g: float = 9.81):
        \"\"\"
        Initialize the freefall simulator with initial conditions.

        Args:
            h0: Initial height (meters)
            v0: Initial velocity (meters/second)
            dt: Time step (seconds)
            T: Total simulation duration (seconds)
            g: Gravitational acceleration (meters/second²), default 9.81
        \"\"\"
        self.h0 = h0
        self.v0 = v0
        self.dt = dt
        self.T = T
        self.g = g

    def calculate_position(self, t: float) -> float:
        \"\"\"Calculate position at time t using kinematic equation.\"\"\"
        return self.h0 + self.v0 * t + 0.5 * self.g * t ** 2

    def calculate_velocity(self, t: float) -> float:
        \"\"\"Calculate velocity at time t using kinematic equation.\"\"\"
        return self.v0 + self.g * t

    def run_simulation(self) -> SimulationResult:
        \"\"\"Run the simulation and return results at each time step.\"\"\"
        result = SimulationResult()
        current_time = 0.0

        while current_time <= self.T + 1e-9:  # Account for floating point precision
            result.time.append(current_time)
            result.position.append(self.calculate_position(current_time))
            result.velocity.append(self.calculate_velocity(current_time))
            result.acceleration.append(self.g)
            current_time += self.dt

        return result
""",
    "code-raw/input_handler.py": """\"\"\"
Input Handling Module
=====================

This module handles user input collection and validation for the freefall simulation.
\"\"\"

def get_float_input(prompt: str, min_val: float = None, max_val: float = None) -> float:
    \"\"\"
    Get and validate a float input from the user.

    Args:
        prompt: Input prompt message
        min_val: Minimum allowed value (inclusive)
        max_val: Maximum allowed value (inclusive)

    Returns:
        Validated float value

    Raises:
        ValueError: If input cannot be converted to float or is out of bounds
    \"\"\"
    while True:
        try:
            value = float(input(prompt))
            if min_val is not None and value < min_val:
                print(f\"Value must be ≥ {min_val}\")
                continue
            if max_val is not None and value > max_val:
                print(f\"Value must be ≤ {max_val}\")
                continue
            return value
        except ValueError:
            print(\"Please enter a valid number\")

def collect_parameters() -> dict:
    \"\"\"
    Collect all simulation parameters from user input.

    Returns:
        Dictionary containing all simulation parameters
    \"\"\"
    print(\"Freefall Simulation - Parameter Input\")
    print(\"------------------------------------\")

    params = {
        'h0': get_float_input(\"Initial height (m): \", min_val=0),
        'v0': get_float_input(\"Initial velocity (m/s): \"),
        'dt': get_float_input(\"Time step (s): \", min_val=0.001, max_val=10),
        'T': get_float_input(\"Total duration (s): \", min_val=0.001, max_val=3600),
        'g': get_float_input(\"Gravitational acceleration (m/s²) [default=9.81]: \", min_val=0) or 9.81
    }

    return params
""",
    "code-raw/output_formatter.py": """\"\"\"
Output Formatting Module
========================

This module handles the display and formatting of simulation results.
\"\"\"

def display_results(result):
    \"\"\"
    Display simulation results in a formatted table.

    Args:
        result: SimulationResult object containing the simulation data
    \"\"\"
    print(\"\\nFreefall Simulation Results\")
    print(\"===========================\")
    print(result.display())
    print(\"\\nSimulation complete.\")
""",
    "code-raw/main.py": """\"\"\"
Main Application Module
=======================

Entry point for the freefall simulation application.
\"\"\"

from input_handler import collect_parameters
from freefall_simulator import FreefallSimulator
from output_formatter import display_results

def main():
    \"\"\"Main application entry point.\"\"\"
    try:
        # Collect input parameters
        params = collect_parameters()

        # Initialize and run simulation
        simulator = FreefallSimulator(**params)
        result = simulator.run_simulation()

        # Display results
        display_results(result)

    except Exception as e:
        print(f\"An error occurred: {e}\")
        print(\"Please try again with valid inputs.\")

if __name__ == \"__main__":
    main()
"""
}

for path, content in files.items():
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(content, encoding="utf-8")

print("✓ All code files generated successfully")