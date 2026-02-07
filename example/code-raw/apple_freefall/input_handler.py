class InputHandler:
    """Handles user input for the freefall simulation."""

    @staticmethod
    def get_float_input(prompt: str, min_val: float = None, max_val: float = None) -> float:
        """Get a float input from the user with validation.

        Args:
            prompt: Input prompt message
            min_val: Minimum allowed value
            max_val: Maximum allowed value

        Returns:
            Validated float input
        """
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
        """Get a yes/no input from the user.

        Args:
            prompt: Input prompt message

        Returns:
            True for yes, False for no
        """
        while True:
            response = input(prompt).strip().lower()
            if response in ('y', 'yes'):
                return True
            elif response in ('n', 'no'):
                return False
            else:
                print("Please enter 'yes' or 'no'")

    def get_simulation_parameters(self) -> dict:
        """Get all simulation parameters from the user.

        Returns:
            Dictionary containing simulation parameters
        """
        print("\nApple Freefall Simulation Parameters")
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
