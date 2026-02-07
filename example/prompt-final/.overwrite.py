from pathlib import Path

files = {
    "code-raw/__init__.py": """# Apple Freefall Simulation Package
# Main package initialization file
""",
    "code-raw/main.py": """import sys
from apple_freefall.simulation import FreefallSimulation

def main():
    simulation = FreefallSimulation()
    simulation.run()

if __name__ == "__main__":
    main()
""",
    "code-raw/apple_freefall/__init__.py": """# Apple Freefall Simulation package initialization
""",
    "code-raw/apple_freefall/config.py": """import json
import os
from typing import Dict, Any

class ConfigManager:
    \"\"\"Manages configuration for the freefall simulation.\"\"\"

    DEFAULT_CONFIG = {
        "gravity": 9.81,
        "time_step": 0.01,
        "output_precision": 4,
        "air_density": 1.225,
        "default_drag_coefficient": 0.47,
        "default_cross_sectional_area": 0.01
    }

    def __init__(self, config_path: str = "config.json"):
        \"\"\"Initialize the configuration manager.

        Args:
            config_path: Path to the configuration file
        \"\"\"
        self.config_path = config_path
        self.config = self.DEFAULT_CONFIG.copy()
        self.load_config()

    def load_config(self) -> None:
        \"\"\"Load configuration from file or create default if not exists.\"\"\"
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    file_config = json.load(f)
                    self.config.update(file_config)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load config file. Using defaults. Error: {e}")

    def save_config(self) -> None:
        \"\"\"Save current configuration to file.\"\"\"
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=4)
        except IOError as e:
            print(f"Warning: Could not save config file. Error: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        \"\"\"Get a configuration value.

        Args:
            key: Configuration key
            default: Default value if key doesn't exist

        Returns:
            Configuration value or default
        \"\"\"
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        \"\"\"Set a configuration value.

        Args:
            key: Configuration key
            value: Value to set
        \"\"\"
        self.config[key] = value
""",
    "code-raw/apple_freefall/input_handler.py": """class InputHandler:
    \"\"\"Handles user input for the freefall simulation.\"\"\"

    @staticmethod
    def get_float_input(prompt: str, min_val: float = None, max_val: float = None) -> float:
        \"\"\"Get a float input from the user with validation.

        Args:
            prompt: Input prompt message
            min_val: Minimum allowed value
            max_val: Maximum allowed value

        Returns:
            Validated float input
        \"\"\"
        while True:
            try:
                value = float(input(prompt))
                if min_val is not None and value < min_val:
                    print(f"Value must be at least {min_val}")
                    continue
                if max_val is not None and value > max_val:
                    print(f"Value must be at most {max_val}")
                    continue
                return value
            except ValueError:
                print("Please enter a valid number")

    @staticmethod
    def get_yes_no_input(prompt: str) -> bool:
        \"\"\"Get a yes/no input from the user.

        Args:
            prompt: Input prompt message

        Returns:
            True for yes, False for no
        \"\"\"
        while True:
            response = input(prompt).strip().lower()
            if response in ('y', 'yes'):
                return True
            elif response in ('n', 'no'):
                return False
            else:
                print("Please enter 'yes' or 'no'")

    def get_simulation_parameters(self) -> dict:
        \"\"\"Get all simulation parameters from the user.

        Returns:
            Dictionary containing simulation parameters
        \"\"\"
        print("\\nApple Freefall Simulation Parameters")
        print("-----------------------------------")

        params = {
            'initial_height': self.get_float_input("Initial height (meters): ", min_val=0.1),
            'mass': self.get_float_input("Apple mass (kilograms): ", min_val=0.01),
            'air_resistance': self.get_yes_no_input("Enable air resistance? (yes/no): "),
            'simulation_time': self.get_float_input("Simulation duration (seconds): ", min_val=0.1)
        }

        if params['air_resistance']:
            params['drag_coefficient'] = self.get_float_input(
                "Drag coefficient (default 0.47): ", min_val=0.01, max_val=2.0
            )
            params['cross_sectional_area'] = self.get_float_input(
                "Cross-sectional area (m², default 0.01): ", min_val=0.0001, max_val=1.0
            )

        return params
""",
    "code-raw/apple_freefall/physics_engine.py": """import math
from typing import List, Tuple

class PhysicsEngine:
    \"\"\"Handles physics calculations for the freefall simulation.\"\"\"

    def __init__(self, config):
        \"\"\"Initialize the physics engine with configuration.

        Args:
            config: Configuration manager instance
        \"\"\"
        self.g = config.get('gravity')
        self.air_density = config.get('air_density')
        self.time_step = config.get('time_step')

    def calculate_freefall(self, params: dict) -> List[Tuple[float, float, float]]:
        \"\"\"Calculate freefall motion with optional air resistance.

        Args:
            params: Dictionary containing simulation parameters

        Returns:
            List of tuples (time, position, velocity) at each time step
        \"\"\"
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
        \"\"\"Get the time when the apple hits the ground.

        Args:
            results: Simulation results from calculate_freefall

        Returns:
            Time of impact or None if not found
        \"\"\"
        for time, position, _ in results:
            if position <= 0:
                return time
        return results[-1][0] if results else 0.0

    def get_max_velocity(self, results: List[Tuple[float, float, float]]) -> float:
        \"\"\"Get the maximum velocity reached during the simulation.

        Args:
            results: Simulation results from calculate_freefall

        Returns:
            Maximum velocity
        \"\"\"
        return max(velocity for _, _, velocity in results) if results else 0.0
""",
    "code-raw/apple_freefall/output_generator.py": """from typing import List, Tuple
import math

class OutputGenerator:
    \"\"\"Generates output files and visualizations for the simulation.\"\"\"

    def __init__(self, config):
        \"\"\"Initialize the output generator with configuration.

        Args:
            config: Configuration manager instance
        \"\"\"
        self.output_precision = config.get('output_precision')

    def generate_markdown(self, params: dict, results: List[Tuple[float, float, float]]) -> str:
        \"\"\"Generate markdown output for the simulation.

        Args:
            params: Simulation parameters
            results: Simulation results

        Returns:
            Markdown content as string
        \"\"\"
        if not results:
            return "# Simulation Results\\n\\nNo results to display."

        # Get summary statistics
        impact_time = self._get_impact_time(results)
        max_velocity = self._get_max_velocity(results)

        # Generate markdown content
        md_content = "# Apple Freefall Simulation Results\\n\\n"

        # Simulation parameters
        md_content += "## Simulation Parameters\\n\\n"
        md_content += f"- Initial height: {params['initial_height']:.2f} m\\n"
        md_content += f"- Apple mass: {params['mass']:.2f} kg\\n"
        md_content += f"- Air resistance: {'Enabled' if params['air_resistance'] else 'Disabled'}\\n"
        if params['air_resistance']:
            md_content += f"- Drag coefficient: {params.get('drag_coefficient', 0.47)}\\n"
            md_content += f"- Cross-sectional area: {params.get('cross_sectional_area', 0.01):.4f} m²\\n"
        md_content += f"- Simulation duration: {params['simulation_time']:.2f} s\\n\\n"

        # Summary statistics
        md_content += "## Summary Statistics\\n\\n"
        md_content += f"- Time to impact: {impact_time:.{self.output_precision}f} s\\n"
        md_content += f"- Maximum velocity: {max_velocity:.{self.output_precision}f} m/s\\n\\n"

        # Results table
        md_content += "## Detailed Results\\n\\n"
        md_content += "| Time (s) | Height (m) | Velocity (m/s) |\\n"
        md_content += "|----------|------------|----------------|\\n"

        # Add every 10th result to keep table manageable
        for time, position, velocity in results[::10]:
            md_content += f"| {time:.{self.output_precision}f} | {position:.{self.output_precision}f} | {velocity:.{self.output_precision}f} |\\n"

        # ASCII graph
        md_content += "\\n## Position vs Time Graph\\n\\n"
        md_content += "```\\n"
        md_content += self._generate_ascii_graph(results)
        md_content += "```\\n"

        return md_content

    def save_to_file(self, content: str, filename: str = "out.md") -> None:
        \"\"\"Save content to a markdown file.

        Args:
            content: Content to save
            filename: Output filename
        \"\"\"
        with open(filename, 'w') as f:
            f.write(content)

    def _get_impact_time(self, results: List[Tuple[float, float, float]]) -> float:
        \"\"\"Get the time when the apple hits the ground.

        Args:
            results: Simulation results

        Returns:
            Time of impact
        \"\"\"
        for time, position, _ in results:
            if position <= 0:
                return time
        return results[-1][0] if results else 0.0

    def _get_max_velocity(self, results: List[Tuple[float, float, float]]) -> float:
        \"\"\"Get the maximum velocity reached during the simulation.

        Args:
            results: Simulation results

        Returns:
            Maximum velocity
        \"\"\"
        return max(velocity for _, _, velocity in results) if results else 0.0

    def _generate_ascii_graph(self, results: List[Tuple[float, float, float]]) -> str:
        \"\"\"Generate an ASCII graph of position vs time.

        Args:
            results: Simulation results

        Returns:
            ASCII graph as string
        \"\"\"
        if not results:
            return "No data to graph"

        # Find max height for scaling
        max_height = max(position for _, position, _ in results)
        if max_height <= 0:
            return "No valid data to graph"

        # Scale factors
        height_scale = 20 / max_height
        time_scale = 50 / results[-1][0]

        # Generate graph
        graph = ""
        for time, position, _ in results[::5]:  # Sample every 5th point
            # Calculate position in graph
            graph_height = int(position * height_scale)
            if graph_height < 0:
                graph_height = 0

            # Create line
            line = [' '] * 50
            if graph_height > 0:
                line_pos = min(int(time * time_scale), 49)
                line[line_pos] = '*'

            graph += f"{''.join(line)} {position:.1f}m\\n"

        # Add time axis
        graph += "\\nTime (s):\\n"
        graph += "0" + " " * 46 + f"{results[-1][0]:.1f}\\n"

        return graph
""",
    "code-raw/apple_freefall/simulation.py": """from apple_freefall.config import ConfigManager
from apple_freefall.input_handler import InputHandler
from apple_freefall.physics_engine import PhysicsEngine
from apple_freefall.output_generator import OutputGenerator

class FreefallSimulation:
    \"\"\"Main simulation class for the apple freefall simulation.\"\"\"

    def __init__(self):
        \"\"\"Initialize the simulation with all components.\"\"\"
        self.config = ConfigManager()
        self.input_handler = InputHandler()
        self.physics_engine = PhysicsEngine(self.config)
        self.output_generator = OutputGenerator(self.config)

    def run(self) -> None:
        \"\"\"Run the complete simulation workflow.\"\"\"
        try:
            # Get simulation parameters from user
            params = self.input_handler.get_simulation_parameters()

            # Run physics simulation
            results = self.physics_engine.calculate_freefall(params)

            # Generate output
            md_content = self.output_generator.generate_markdown(params, results)
            self.output_generator.save_to_file(md_content)

            print("\\nSimulation complete! Results saved to out.md")

        except Exception as e:
            print(f"An error occurred during simulation: {e}")
""",
    "code-raw/config.json": """{
    "gravity": 9.81,
    "time_step": 0.01,
    "output_precision": 4,
    "air_density": 1.225,
    "default_drag_coefficient": 0.47,
    "default_cross_sectional_area": 0.01
}
"""
}

for path, content in files.items():
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(content, encoding="utf-8")

print("✓ All code files generated successfully")