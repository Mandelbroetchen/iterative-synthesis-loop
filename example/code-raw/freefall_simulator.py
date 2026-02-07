"""
Freefall Simulation Module
==========================

This module implements the physics calculations and simulation logic for freefall motion
under constant gravitational acceleration.
"""

class SimulationResult:
    """Container for simulation results at each time step."""

    def __init__(self):
        self.time = []
        self.position = []
        self.velocity = []
        self.acceleration = []

    def display(self):
        """Format simulation results as a table string."""
        header = "Time (s) | Position (m) | Velocity (m/s) | Acceleration (m/s²)"
        separator = "-" * len(header)
        rows = [f"{t:8.2f} | {h:12.2f} | {v:14.2f} | {a:18.2f}"
                for t, h, v, a in zip(self.time, self.position, self.velocity, self.acceleration)]
        return "\n".join([header, separator] + rows)

class FreefallSimulator:
    """Core physics engine for freefall simulation."""

    def __init__(self, h0: float, v0: float, dt: float, T: float, g: float = 9.81):
        """
        Initialize the freefall simulator with initial conditions.

        Args:
            h0: Initial height (meters)
            v0: Initial velocity (meters/second)
            dt: Time step (seconds)
            T: Total simulation duration (seconds)
            g: Gravitational acceleration (meters/second²), default 9.81
        """
        self.h0 = h0
        self.v0 = v0
        self.dt = dt
        self.T = T
        self.g = g

    def calculate_position(self, t: float) -> float:
        """Calculate position at time t using kinematic equation."""
        return self.h0 + self.v0 * t + 0.5 * self.g * t ** 2

    def calculate_velocity(self, t: float) -> float:
        """Calculate velocity at time t using kinematic equation."""
        return self.v0 + self.g * t

    def run_simulation(self) -> SimulationResult:
        """Run the simulation and return results at each time step."""
        result = SimulationResult()
        current_time = 0.0

        while current_time <= self.T + 1e-9:  # Account for floating point precision
            result.time.append(current_time)
            result.position.append(self.calculate_position(current_time))
            result.velocity.append(self.calculate_velocity(current_time))
            result.acceleration.append(self.g)
            current_time += self.dt

        return result
