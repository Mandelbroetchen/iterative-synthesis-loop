import math
from typing import List, Tuple

class PhysicsEngine:
    """Handles physics calculations for the freefall simulation."""

    def __init__(self, config):
        """Initialize the physics engine with configuration.

        Args:
            config: Configuration manager instance
        """
        self.g = config.get('gravity')
        self.air_density = config.get('air_density')
        self.time_step = config.get('time_step')

    def calculate_freefall(self, params: dict) -> List[Tuple[float, float, float]]:
        """Calculate freefall motion with optional air resistance.

        Args:
            params: Dictionary containing simulation parameters

        Returns:
            List of tuples (time, position, velocity) at each time step
        """
        results = []
        time = 0.0
        position = params['initial_height']
        velocity = 0.0

        # Set up air resistance parameters if enabled
        if params['air_resistance']:
            drag_coefficient = params.get('drag_coefficient', 0.47)
            cross_sectional_area = params.get('cross_sectional_area', 0.01)
        else:
            drag_coefficient = 0.0
            cross_sectional_area = 0.0

        while time <= params['simulation_time'] and position >= 0:
            # Calculate acceleration
            if params['air_resistance']:
                air_resistance = 0.5 * self.air_density * drag_coefficient * cross_sectional_area * velocity**2
                acceleration = self.g - (air_resistance / params['mass'])
            else:
                acceleration = self.g

            # Update velocity and position using Euler integration
            velocity += acceleration * self.time_step
            position -= velocity * self.time_step

            # Ensure position doesn't go below ground
            if position < 0:
                position = 0

            results.append((time, position, velocity))
            time += self.time_step

        return results

    def get_impact_time(self, results: List[Tuple[float, float, float]]) -> float:
        """Get the time when the apple hits the ground.

        Args:
            results: Simulation results from calculate_freefall

        Returns:
            Time of impact or None if not found
        """
        for time, position, _ in results:
            if position <= 0:
                return time
        return results[-1][0] if results else 0.0

    def get_max_velocity(self, results: List[Tuple[float, float, float]]) -> float:
        """Get the maximum velocity reached during the simulation.

        Args:
            results: Simulation results from calculate_freefall

        Returns:
            Maximum velocity
        """
        return max(velocity for _, _, velocity in results) if results else 0.0
