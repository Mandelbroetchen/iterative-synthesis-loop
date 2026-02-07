"""
Unit tests for the Freefall Simulator module.
"""

import unittest
from freefall_simulator import FreefallSimulator, SimulationResult, InputValidator

class TestFreefallSimulator(unittest.TestCase):
    """Test cases for the FreefallSimulator class."""

    def test_initialization_valid(self):
        """Test valid initialization of FreefallSimulator."""
        simulator = FreefallSimulator(h0=10.0, v0=0.0, dt=0.1, T=2.0, g=9.81)
        self.assertEqual(simulator.h0, 10.0)
        self.assertEqual(simulator.v0, 0.0)
        self.assertEqual(simulator.dt, 0.1)
        self.assertEqual(simulator.T, 2.0)
        self.assertEqual(simulator.g, 9.81)

    def test_initialization_invalid(self):
        """Test invalid initialization of FreefallSimulator."""
        with self.assertRaises(ValueError):
            FreefallSimulator(h0=-1.0, v0=0.0, dt=0.1, T=2.0, g=9.81)
        with self.assertRaises(ValueError):
            FreefallSimulator(h0=10.0, v0=0.0, dt=0.0, T=2.0, g=9.81)
        with self.assertRaises(ValueError):
            FreefallSimulator(h0=10.0, v0=0.0, dt=0.1, T=0.0, g=9.81)
        with self.assertRaises(ValueError):
            FreefallSimulator(h0=10.0, v0=0.0, dt=0.1, T=2.0, g=-9.81)

    def test_calculate_position(self):
        """Test position calculation."""
        simulator = FreefallSimulator(h0=10.0, v0=0.0, dt=0.1, T=2.0, g=9.81)
        self.assertAlmostEqual(simulator.calculate_position(0.0), 10.0)
        self.assertAlmostEqual(simulator.calculate_position(1.0), 14.905, places=3)

    def test_calculate_velocity(self):
        """Test velocity calculation."""
        simulator = FreefallSimulator(h0=10.0, v0=0.0, dt=0.1, T=2.0, g=9.81)
        self.assertAlmostEqual(simulator.calculate_velocity(0.0), 0.0)
        self.assertAlmostEqual(simulator.calculate_velocity(1.0), 9.81, places=2)

    def test_detect_ground_collision(self):
        """Test ground collision detection."""
        simulator = FreefallSimulator(h0=10.0, v0=0.0, dt=0.1, T=2.0, g=9.81)
        self.assertFalse(simulator.detect_ground_collision(0.0, 10.0))
        self.assertTrue(simulator.detect_ground_collision(0.0, 0.0))
        self.assertTrue(simulator.detect_ground_collision(0.0, -1.0))

    def test_run_simulation_no_collision(self):
        """Test simulation without ground collision."""
        simulator = FreefallSimulator(h0=100.0, v0=0.0, dt=0.1, T=1.0, g=9.81)
        result = simulator.run_simulation()
        self.assertIsNone(result.impact_time)
        self.assertTrue(result.completed)
        self.assertEqual(len(result.time), 11)  # 0.0 to 1.0 in steps of 0.1

    def test_run_simulation_with_collision(self):
        """Test simulation with ground collision."""
        simulator = FreefallSimulator(h0=10.0, v0=0.0, dt=0.1, T=2.0, g=9.81)
        result = simulator.run_simulation()
        self.assertIsNotNone(result.impact_time)
        self.assertFalse(result.completed)
        self.assertLess(result.impact_time, 2.0)

    def test_simulation_result_methods(self):
        """Test SimulationResult methods."""
        result = SimulationResult(
            time=[0.0, 0.1, 0.2],
            position=[10.0, 9.5, 8.0],
            velocity=[0.0, -0.981, -1.962],
            acceleration=[9.81, 9.81, 9.81],
            impact_time=None
        )
        self.assertIn("Simulation Parameters:", result.get_summary())
        self.assertIn("Time (s)", result.display())
        final_pos, final_vel, final_acc = result.get_final_values()
        self.assertEqual(final_pos, 8.0)
        self.assertEqual(final_vel, -1.962)
        self.assertEqual(final_acc, 9.81)

class TestInputValidator(unittest.TestCase):
    """Test cases for the InputValidator class."""

    def test_validate_height(self):
        """Test height validation."""
        self.assertTrue(InputValidator.validate_height(0.0))
        self.assertTrue(InputValidator.validate_height(10.0))
        self.assertFalse(InputValidator.validate_height(-1.0))

    def test_validate_velocity(self):
        """Test velocity validation."""
        self.assertTrue(InputValidator.validate_velocity(0.0))
        self.assertTrue(InputValidator.validate_velocity(10.0))
        self.assertTrue(InputValidator.validate_velocity(-10.0))

    def test_validate_time_step(self):
        """Test time step validation."""
        self.assertTrue(InputValidator.validate_time_step(0.1))
        self.assertFalse(InputValidator.validate_time_step(0.0))
        self.assertFalse(InputValidator.validate_time_step(-0.1))

    def test_validate_duration(self):
        """Test duration validation."""
        self.assertTrue(InputValidator.validate_duration(1.0))
        self.assertFalse(InputValidator.validate_duration(0.0))
        self.assertFalse(InputValidator.validate_duration(-1.0))

    def test_validate_gravity(self):
        """Test gravity validation."""
        self.assertTrue(InputValidator.validate_gravity(9.81))
        self.assertTrue(InputValidator.validate_gravity(0.0))
        self.assertFalse(InputValidator.validate_gravity(-9.81))

    def test_validate_all(self):
        """Test all parameter validation."""
        self.assertTrue(InputValidator.validate_all(10.0, 0.0, 0.1, 2.0, 9.81))
        self.assertFalse(InputValidator.validate_all(-10.0, 0.0, 0.1, 2.0, 9.81))
        self.assertFalse(InputValidator.validate_all(10.0, 0.0, 0.0, 2.0, 9.81))
        self.assertFalse(InputValidator.validate_all(10.0, 0.0, 0.1, 0.0, 9.81))
        self.assertFalse(InputValidator.validate_all(10.0, 0.0, 0.1, 2.0, -9.81))

if __name__ == "__main__":
    unittest.main()
