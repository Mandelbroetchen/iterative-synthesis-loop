from apple_freefall.config import ConfigManager
from apple_freefall.input_handler import InputHandler
from apple_freefall.physics_engine import PhysicsEngine
from apple_freefall.output_generator import OutputGenerator

class FreefallSimulation:
    """Main simulation class for the apple freefall simulation."""

    def __init__(self):
        """Initialize the simulation with all components."""
        self.config = ConfigManager()
        self.input_handler = InputHandler()
        self.physics_engine = PhysicsEngine(self.config)
        self.output_generator = OutputGenerator(self.config)

    def run(self) -> None:
        """Run the complete simulation workflow."""
        try:
            # Get simulation parameters from user
            params = self.input_handler.get_simulation_parameters()

            # Run physics simulation
            results = self.physics_engine.calculate_freefall(params)

            # Generate output
            md_content = self.output_generator.generate_markdown(params, results)
            self.output_generator.save_to_file(md_content)

            print("\nSimulation complete! Results saved to out.md")

        except Exception as e:
            print(f"An error occurred during simulation: {e}")
