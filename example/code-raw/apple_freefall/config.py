import json
import os
from typing import Dict, Any

class ConfigManager:
    """Manages configuration for the freefall simulation."""

    DEFAULT_CONFIG = {
        "gravity": 9.81,
        "time_step": 0.01,
        "output_precision": 4,
        "air_density": 1.225,
        "default_drag_coefficient": 0.47,
        "default_cross_sectional_area": 0.01
    }

    def __init__(self, config_path: str = "config.json"):
        """Initialize the configuration manager.

        Args:
            config_path: Path to the configuration file
        """
        self.config_path = config_path
        self.config = self.DEFAULT_CONFIG.copy()
        self.load_config()

    def load_config(self) -> None:
        """Load configuration from file or create default if not exists."""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    file_config = json.load(f)
                    self.config.update(file_config)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load config file. Using defaults. Error: {e}")

    def save_config(self) -> None:
        """Save current configuration to file."""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=4)
        except IOError as e:
            print(f"Warning: Could not save config file. Error: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value.

        Args:
            key: Configuration key
            default: Default value if key doesn't exist

        Returns:
            Configuration value or default
        """
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value.

        Args:
            key: Configuration key
            value: Value to set
        """
        self.config[key] = value
