from typing import List, Tuple
import math

class OutputGenerator:
    """Generates output files and visualizations for the simulation."""

    def __init__(self, config):
        """Initialize the output generator with configuration.

        Args:
            config: Configuration manager instance
        """
        self.output_precision = config.get('output_precision')

    def generate_markdown(self, params: dict, results: List[Tuple[float, float, float]]) -> str:
        """Generate markdown output for the simulation.

        Args:
            params: Simulation parameters
            results: Simulation results

        Returns:
            Markdown content as string
        """
        if not results:
            return "# Simulation Results\n\nNo results to display."

        # Get summary statistics
        impact_time = self._get_impact_time(results)
        max_velocity = self._get_max_velocity(results)

        # Generate markdown content
        md_content = "# Apple Freefall Simulation Results\n\n"

        # Simulation parameters
        md_content += "## Simulation Parameters\n\n"
        md_content += f"- Initial height: {params['initial_height']:.2f} m\n"
        md_content += f"- Apple mass: {params['mass']:.2f} kg\n"
        md_content += f"- Air resistance: {'Enabled' if params['air_resistance'] else 'Disabled'}\n"
        if params['air_resistance']:
            md_content += f"- Drag coefficient: {params.get('drag_coefficient', 0.47)}\n"
            md_content += f"- Cross-sectional area: {params.get('cross_sectional_area', 0.01):.4f} m²\n"
        md_content += f"- Simulation duration: {params['simulation_time']:.2f} s\n\n"

        # Summary statistics
        md_content += "## Summary Statistics\n\n"
        md_content += f"- Time to impact: {impact_time:.{self.output_precision}f} s\n"
        md_content += f"- Maximum velocity: {max_velocity:.{self.output_precision}f} m/s\n\n"

        # Results table
        md_content += "## Detailed Results\n\n"
        md_content += "| Time (s) | Height (m) | Velocity (m/s) |\n"
        md_content += "|----------|------------|----------------|\n"

        # Add every 10th result to keep table manageable
        for time, position, velocity in results[::10]:
            md_content += f"| {time:.{self.output_precision}f} | {position:.{self.output_precision}f} | {velocity:.{self.output_precision}f} |\n"

        # ASCII graph
        md_content += "\n## Position vs Time Graph\n\n"
        md_content += "```\n"
        md_content += self._generate_ascii_graph(results)
        md_content += "```\n"

        return md_content

    def save_to_file(self, content: str, filename: str = "out.md") -> None:
        """Save content to a markdown file.

        Args:
            content: Content to save
            filename: Output filename
        """
        with open(filename, 'w') as f:
            f.write(content)

    def _get_impact_time(self, results: List[Tuple[float, float, float]]) -> float:
        """Get the time when the apple hits the ground.

        Args:
            results: Simulation results

        Returns:
            Time of impact
        """
        for time, position, _ in results:
            if position <= 0:
                return time
        return results[-1][0] if results else 0.0

    def _get_max_velocity(self, results: List[Tuple[float, float, float]]) -> float:
        """Get the maximum velocity reached during the simulation.

        Args:
            results: Simulation results

        Returns:
            Maximum velocity
        """
        return max(velocity for _, _, velocity in results) if results else 0.0

    def _generate_ascii_graph(self, results: List[Tuple[float, float, float]]) -> str:
        """Generate an ASCII graph of position vs time.

        Args:
            results: Simulation results

        Returns:
            ASCII graph as string
        """
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

            graph += f"{''.join(line)} {position:.1f}m\n"

        # Add time axis
        graph += "\nTime (s):\n"
        graph += "0" + " " * 46 + f"{results[-1][0]:.1f}\n"

        return graph
