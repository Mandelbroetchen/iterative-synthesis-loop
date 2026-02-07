"""
Freefall Simulation Module
==========================

This module implements the physics calculations and simulation logic for freefall motion
under constant gravitational acceleration.
"""

from typing import List, Optional, Tuple
import math

class SimulationResult:
    """Container for simulation results at each time step."""

    def __init__(self, time: List[float], position: List[float], velocity: List[float],
                 acceleration: List[float], impact_time: Optional[float] = None):
        """
        Initialize simulation results.

        Args:
            time: List of time values
            position: List of position values
            velocity: List of velocity values
            acceleration: List of acceleration values
            impact_time: Time when ground collision occurred (None if no collision)
        """
        self.time = time
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.impact_time = impact_time
        self.completed = impact_time is None

    def display(self) -> str:
        """Format simulation results as a table string."""
        header = "Time (s) | Position (m) | Velocity (m/s) | Acceleration (m/s²)"
        separator = "-" * len(header)
        rows = []
        for t, h, v, a in zip(self.time, self.position, self.velocity, self.acceleration):
            if h <= 0 and len(rows) > 0:
                break
            rows.append(f"{t:8.2f} | {max(h, 0.0):12.2f} | {v:14.2f} | {a:18.2f}")
        return "\n".join([header, separator] + rows)

    def get_summary(self) -> str:
        """Get a summary of simulation parameters and results."""
        summary = [
            "Simulation Parameters:",
            f"- Initial height: {self.position[0] if self.position else 0:.2f} m",
            f"- Initial velocity: {self.velocity[0] if self.velocity else 0:.2f} m/s",
            f"- Time step: {self.time[1] - self.time[0] if len(self.time) > 1 else 0:.2f} s",
            f"- Gravitational acceleration: {self.acceleration[0] if self.acceleration else 0:.2f} m/s²"
        ]
        if self.impact_time is not None:
            summary.append(f"- Ground collision at: {self.impact_time:.2f} s")
        return "\n".join(summary)

    def get_final_values(self) -> Tuple[float, float, float]:
        """Get the final position, velocity, and acceleration values."""
        if not self.time:
            return (0.0, 0.0, 0.0)
        return (self.position[-1], self.velocity[-1], self.acceleration[-1])

class InputValidator:
    """Handles validation of input parameters for the simulation."""

    @staticmethod
    def validate_height(h0: float) -> bool:
        """Validate initial height."""
        return h0 >= 0

    @staticmethod
    def validate_velocity(v0: float) -> bool:
        """Validate initial velocity."""
        return True  # Velocity can be any real number

    @staticmethod
    def validate_time_step(dt: float) -> bool:
        """Validate time step."""
        return dt > 0

    @staticmethod
    def validate_duration(T: float) -> bool:
        """Validate total duration."""
        return T > 0

    @staticmethod
    def validate_gravity(g: float) -> bool:
        """Validate gravitational acceleration."""
        return g >= 0

    @staticmethod
    def validate_all(h0: float, v0: float, dt: float, T: float, g: float) -> bool:
        """Validate all input parameters."""
        return (InputValidator.validate_height(h0) and
                InputValidator.validate_velocity(v0) and
                InputValidator.validate_time_step(dt) and
                InputValidator.validate_duration(T) and
                InputValidator.validate_gravity(g))

class WarningGenerator:
    """Generates warning messages for simulation events."""

    @staticmethod
    def ground_collision_warning(impact_time: float) -> str:
        """Generate warning for ground collision."""
        return f"Warning: Simulation stopped early - object hit the ground at t ≈ {impact_time:.2f} s"

    @staticmethod
    def early_termination_warning() -> str:
        """Generate warning for early termination."""
        return "Warning: Simulation terminated early due to ground collision"

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

        Raises:
            ValueError: If input parameters are invalid
        """
        if not InputValidator.validate_all(h0, v0, dt, T, g):
            raise ValueError("Invalid input parameters")

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

    def detect_ground_collision(self, t: float, h: float) -> bool:
        """Check if ground collision has occurred."""
        return h <= 0

    def run_simulation(self) -> SimulationResult:
        """Run the simulation and return results at each time step."""
        time_points = []
        position_values = []
        velocity_values = []
        acceleration_values = []
        impact_time = None

        current_time = 0.0
        while current_time <= self.T + 1e-9:  # Account for floating point precision
            h = self.calculate_position(current_time)
            v = self.calculate_velocity(current_time)

            time_points.append(current_time)
            position_values.append(h)
            velocity_values.append(v)
            acceleration_values.append(self.g)

            if self.detect_ground_collision(current_time, h) and impact_time is None:
                impact_time = current_time
                # Add one more step to show the impact
                if current_time + self.dt <= self.T + 1e-9:
                    current_time += self.dt
                    h = self.calculate_position(current_time)
                    v = self.calculate_velocity(current_time)
                    time_points.append(current_time)
                    position_values.append(h)
                    velocity_values.append(v)
                    acceleration_values.append(self.g)
                break

            current_time += self.dt

        return SimulationResult(time_points, position_values, velocity_values,
                              acceleration_values, impact_time)
