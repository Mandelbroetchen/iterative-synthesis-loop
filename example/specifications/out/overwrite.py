# This is the first line of .overwrite.py
from pathlib import Path

files = {
    "code-raw/.patchnotes.md": """# Blackhole Simulation System - Patch Notes

## Version 0.1.2
- Added complete implementation of blackhole simulation system
- Generated example configuration files
- Implemented physics engine with Newtonian gravity and blackhole special properties
- Added comprehensive input validation and error handling
- Created modular structure with clear separation of concerns
- Implemented output generation system
""",

    "code-raw/__init__.py": """# Blackhole Simulation System Package
# Core package for blackhole simulation system

__version__ = "0.1.2"

from .simulation import Simulation
from .models import CelestialObject, SimulationConfig
from .io_handler import IOHandler
from .physics_engine import PhysicsEngine

__all__ = ['Simulation', 'CelestialObject', 'SimulationConfig', 'IOHandler', 'PhysicsEngine']
""",

    "code-raw/models.py": """\"\"\"Data models for the blackhole simulation system.\"\"\"

from dataclasses import dataclass
from typing import List, Dict, Any
import json
from pathlib import Path

@dataclass
class Vector3D:
    \"\"\"Represents a 3D vector for position, velocity, and acceleration.\"\"\"
    x: float
    y: float
    z: float

    def to_list(self) -> List[float]:
        \"\"\"Convert vector to list representation.\"\"\"
        return [self.x, self.y, self.z]

    @classmethod
    def from_list(cls, data: List[float]) -> 'Vector3D':
        \"\"\"Create vector from list representation.\"\"\"
        if len(data) != 3:
            raise ValueError("Vector must have exactly 3 components")
        return cls(data[0], data[1], data[2])

    def __add__(self, other: 'Vector3D') -> 'Vector3D':
        \"\"\"Vector addition.\"\"\"
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: 'Vector3D') -> 'Vector3D':
        \"\"\"Vector subtraction.\"\"\"
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float) -> 'Vector3D':
        \"\"\"Scalar multiplication.\"\"\"
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)

    def __truediv__(self, scalar: float) -> 'Vector3D':
        \"\"\"Scalar division.\"\"\"
        return Vector3D(self.x / scalar, self.y / scalar, self.z / scalar)

    def magnitude(self) -> float:
        \"\"\"Calculate vector magnitude.\"\"\"
        return (self.x**2 + self.y**2 + self.z**2)**0.5

    def distance_to(self, other: 'Vector3D') -> float:
        \"\"\"Calculate distance between two vectors.\"\"\"
        return (self - other).magnitude()

@dataclass
class CelestialObject:
    \"\"\"Represents a celestial object in the simulation.\"\"\"
    id: str
    name: str
    mass: float
    position: Vector3D
    velocity: Vector3D
    is_blackhole: bool = False
    acceleration: Vector3D = Vector3D(0, 0, 0)

    def to_dict(self) -> Dict[str, Any]:
        \"\"\"Convert object to dictionary for output.\"\"\"
        return {
            "id": self.id,
            "position": self.position.to_list(),
            "velocity": self.velocity.to_list(),
            "acceleration": self.acceleration.to_list()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CelestialObject':
        \"\"\"Create object from dictionary.\"\"\"
        return cls(
            id=data["id"],
            name=data.get("name", data["id"]),
            mass=data["mass"],
            position=Vector3D.from_list(data["position"]),
            velocity=Vector3D.from_list(data["velocity"]),
            is_blackhole=data.get("is_blackhole", False)
        )

    def event_horizon_radius(self, gravitational_constant: float) -> float:
        \"\"\"Calculate event horizon radius for blackholes.\"\"\"
        if not self.is_blackhole:
            return 0.0
        c = 299792458  # Speed of light in m/s
        return 2 * gravitational_constant * self.mass / (c ** 2)

@dataclass
class SimulationConfig:
    \"\"\"Configuration parameters for the simulation.\"\"\"
    time_step: float
    total_time: float
    gravitational_constant: float
    output_frequency: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SimulationConfig':
        \"\"\"Create configuration from dictionary.\"\"\"
        return cls(
            time_step=data["time_step"],
            total_time=data["total_time"],
            gravitational_constant=data["gravitational_constant"],
            output_frequency=data["output_frequency"]
        )

@dataclass
class SimulationOutput:
    \"\"\"Represents a single simulation output frame.\"\"\"
    time: float
    objects: List[CelestialObject]

    def to_dict(self) -> Dict[str, Any]:
        \"\"\"Convert output to dictionary for JSON serialization.\"\"\"
        return {
            "time": self.time,
            "objects": [obj.to_dict() for obj in self.objects]
        }
""",

    "code-raw/physics_engine.py": """\"\"\"Physics engine for the blackhole simulation system.\"\"\"

from typing import List, Dict
import math
from .models import CelestialObject, Vector3D, SimulationConfig

class PhysicsEngine:
    \"\"\"Handles all physics calculations for the simulation.\"\"\"

    def __init__(self, config: SimulationConfig):
        self.config = config
        self.g = config.gravitational_constant

    def calculate_gravitational_force(self, obj1: CelestialObject, obj2: CelestialObject) -> Vector3D:
        \"\"\"Calculate gravitational force between two objects.\"\"\"
        if obj1.id == obj2.id:
            return Vector3D(0, 0, 0)

        r = obj1.position.distance_to(obj2.position)
        if r == 0:
            return Vector3D(0, 0, 0)

        # Check if either object is a blackhole and the other is within its event horizon
        if obj1.is_blackhole and r <= obj1.event_horizon_radius(self.g):
            return Vector3D(math.inf, math.inf, math.inf)
        if obj2.is_blackhole and r <= obj2.event_horizon_radius(self.g):
            return Vector3D(math.inf, math.inf, math.inf)

        force_magnitude = self.g * obj1.mass * obj2.mass / (r ** 2)
        direction = (obj2.position - obj1.position) / r
        return direction * force_magnitude

    def calculate_acceleration(self, obj: CelestialObject, force: Vector3D) -> Vector3D:
        \"\"\"Calculate acceleration from force.\"\"\"
        return force / obj.mass

    def update_object_state(self, obj: CelestialObject, acceleration: Vector3D, time_step: float) -> None:
        \"\"\"Update object's position and velocity based on acceleration.\"\"\"
        # Update velocity: v = v0 + a * dt
        obj.velocity += acceleration * time_step

        # Update position: r = r0 + v * dt
        obj.position += obj.velocity * time_step

        # Update acceleration for output
        obj.acceleration = acceleration

    def calculate_all_forces(self, objects: List[CelestialObject]) -> Dict[str, Vector3D]:
        \"\"\"Calculate net force on each object from all other objects.\"\"\"
        forces = {obj.id: Vector3D(0, 0, 0) for obj in objects}

        for i, obj1 in enumerate(objects):
            for obj2 in objects[i+1:]:
                force_on_1 = self.calculate_gravitational_force(obj1, obj2)
                force_on_2 = force_on_1 * -1  # Newton's third law

                forces[obj1.id] += force_on_1
                forces[obj2.id] += force_on_2

        return forces

    def check_blackhole_collisions(self, objects: List[CelestialObject]) -> List[CelestialObject]:
        \"\"\"Check for objects that have entered blackhole event horizons.\"\"\"
        surviving_objects = []
        blackholes = [obj for obj in objects if obj.is_blackhole]

        for obj in objects:
            if obj.is_blackhole:
                surviving_objects.append(obj)
                continue

            for bh in blackholes:
                distance = obj.position.distance_to(bh.position)
                if distance <= bh.event_horizon_radius(self.g):
                    break  # Object is consumed by blackhole
            else:
                surviving_objects.append(obj)

        return surviving_objects

    def step(self, objects: List[CelestialObject], time_step: float) -> List[CelestialObject]:
        \"\"\"Perform a single simulation step.\"\"\"
        # Calculate forces
        forces = self.calculate_all_forces(objects)

        # Calculate accelerations and update states
        for obj in objects:
            acceleration = self.calculate_acceleration(obj, forces[obj.id])
            self.update_object_state(obj, acceleration, time_step)

        # Check for blackhole collisions
        return self.check_blackhole_collisions(objects)
""",

    "code-raw/io_handler.py": """\"\"\"Handles input/output operations for the simulation.\"\"\"

import json
from pathlib import Path
from typing import Dict, Any, List
import jsonschema
from .models import CelestialObject, SimulationConfig, SimulationOutput

class IOHandler:
    \"\"\"Handles reading input files and writing output files.\"\"\"

    def __init__(self):
        self.config_schema = {
            "type": "object",
            "properties": {
                "time_step": {"type": "number", "minimum": 0},
                "total_time": {"type": "number", "minimum": 0},
                "gravitational_constant": {"type": "number", "minimum": 0},
                "output_frequency": {"type": "integer", "minimum": 1}
            },
            "required": ["time_step", "total_time", "gravitational_constant", "output_frequency"],
            "additionalProperties": False
        }

        self.objects_schema = {
            "type": "object",
            "properties": {
                "objects": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "name": {"type": "string"},
                            "mass": {"type": "number", "minimum": 0},
                            "position": {
                                "type": "array",
                                "items": {"type": "number"},
                                "minItems": 3,
                                "maxItems": 3
                            },
                            "velocity": {
                                "type": "array",
                                "items": {"type": "number"},
                                "minItems": 3,
                                "maxItems": 3
                            },
                            "is_blackhole": {"type": "boolean"}
                        },
                        "required": ["id", "mass", "position", "velocity"],
                        "additionalProperties": False
                    }
                }
            },
            "required": ["objects"],
            "additionalProperties": False
        }

    def read_config(self, config_path: str) -> SimulationConfig:
        \"\"\"Read and validate simulation configuration.\"\"\"
        try:
            with open(config_path, 'r') as f:
                config_data = json.load(f)

            jsonschema.validate(instance=config_data, schema=self.config_schema)

            return SimulationConfig.from_dict(config_data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in config file: {e}")
        except jsonschema.ValidationError as e:
            raise ValueError(f"Invalid config file schema: {e}")
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found: {config_path}")
        except Exception as e:
            raise ValueError(f"Error reading config file: {e}")

    def read_objects(self, objects_path: str) -> List[CelestialObject]:
        \"\"\"Read and validate celestial objects data.\"\"\"
        try:
            with open(objects_path, 'r') as f:
                objects_data = json.load(f)

            jsonschema.validate(instance=objects_data, schema=self.objects_schema)

            return [CelestialObject.from_dict(obj) for obj in objects_data["objects"]]
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in objects file: {e}")
        except jsonschema.ValidationError as e:
            raise ValueError(f"Invalid objects file schema: {e}")
        except FileNotFoundError:
            raise FileNotFoundError(f"Objects file not found: {objects_path}")
        except Exception as e:
            raise ValueError(f"Error reading objects file: {e}")

    def write_output(self, output_path: str, simulation_output: SimulationOutput) -> None:
        \"\"\"Write simulation output to file.\"\"\"
        try:
            output_dir = Path(output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)

            with open(output_path, 'w') as f:
                json.dump(simulation_output.to_dict(), f, indent=2)
        except Exception as e:
            raise IOError(f"Error writing output file: {e}")

    def generate_example_configs(self, output_dir: str = "examples") -> None:
        \"\"\"Generate example configuration files.\"\"\"
        example_dir = Path(output_dir)
        example_dir.mkdir(parents=True, exist_ok=True)

        # Example config.json
        example_config = {
            "time_step": 0.01,
            "total_time": 100.0,
            "gravitational_constant": 6.67430e-11,
            "output_frequency": 10
        }

        with open(example_dir / "config.json", 'w') as f:
            json.dump(example_config, f, indent=2)

        # Example objects.json
        example_objects = {
            "objects": [
                {
                    "id": "bh1",
                    "name": "Black Hole Alpha",
                    "mass": 1.989e30,
                    "position": [0, 0, 0],
                    "velocity": [0, 0, 0],
                    "is_blackhole": True
                },
                {
                    "id": "star1",
                    "name": "Star Beta",
                    "mass": 1.989e29,
                    "position": [1e11, 0, 0],
                    "velocity": [0, 2e4, 0],
                    "is_blackhole": False
                },
                {
                    "id": "planet1",
                    "name": "Planet Gamma",
                    "mass": 5.972e24,
                    "position": [1.5e11, 0, 0],
                    "velocity": [0, 3e4, 0],
                    "is_blackhole": False
                }
            ]
        }

        with open(example_dir / "objects.json", 'w') as f:
            json.dump(example_objects, f, indent=2)
""",

    "code-raw/simulation.py": """\"\"\"Main simulation controller for the blackhole simulation system.\"\"\"

from typing import List
from pathlib import Path
from .models import CelestialObject, SimulationConfig, SimulationOutput
from .physics_engine import PhysicsEngine
from .io_handler import IOHandler

class Simulation:
    \"\"\"Main simulation controller class.\"\"\"

    def __init__(self, config_path: str, objects_path: str):
        self.io_handler = IOHandler()
        self.config = self.io_handler.read_config(config_path)
        self.objects = self.io_handler.read_objects(objects_path)
        self.physics_engine = PhysicsEngine(self.config)
        self.current_time = 0.0

    def run(self, output_dir: str = "./out") -> None:
        \"\"\"Run the complete simulation.\"\"\"
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        step_count = 0
        while self.current_time <= self.config.total_time and len(self.objects) > 0:
            # Output data at specified frequency
            if step_count % self.config.output_frequency == 0:
                output_file = output_path / f"output_{self.current_time:.2f}.json"
                output = SimulationOutput(time=self.current_time, objects=self.objects)
                self.io_handler.write_output(str(output_file), output)

            # Perform simulation step
            self.objects = self.physics_engine.step(self.objects, self.config.time_step)
            self.current_time += self.config.time_step
            step_count += 1

        # Write final output
        if len(self.objects) > 0:
            output_file = output_path / f"output_{self.current_time:.2f}.json"
            output = SimulationOutput(time=self.current_time, objects=self.objects)
            self.io_handler.write_output(str(output_file), output)

    @classmethod
    def generate_example_configs(cls, output_dir: str = "examples") -> None:
        \"\"\"Generate example configuration files.\"\"\"
        io_handler = IOHandler()
        io_handler.generate_example_configs(output_dir)
""",

    "code-raw/main.py": """\"\"\"Entry point for the blackhole simulation system.\"\"\"

import argparse
from .simulation import Simulation

def main():
    \"\"\"Main entry point for the simulation.\"\"\"
    parser = argparse.ArgumentParser(description="Blackhole Simulation System")
    parser.add_argument("--config", type=str, default="config.json",
                       help="Path to configuration file")
    parser.add_argument("--objects", type=str, default="objects.json",
                       help="Path to celestial objects file")
    parser.add_argument("--output", type=str, default="./out",
                       help="Output directory for simulation results")
    parser.add_argument("--generate-examples", action="store_true",
                       help="Generate example configuration files")

    args = parser.parse_args()

    if args.generate_examples:
        Simulation.generate_example_configs()
        print("Example configuration files generated in 'examples/' directory")
        return

    try:
        simulation = Simulation(args.config, args.objects)
        simulation.run(args.output)
        print(f"Simulation completed successfully. Results saved to {args.output}")
    except Exception as e:
        print(f"Error running simulation: {e}")
        raise

if __name__ == "__main__":
    main()
""",

    "code-raw/examples/config.json": """{
    "time_step": 0.01,
    "total_time": 100.0,
    "gravitational_constant": 6.67430e-11,
    "output_frequency": 10
}
""",

    "code-raw/examples/objects.json": """{
    "objects": [
        {
            "id": "bh1",
            "name": "Black Hole Alpha",
            "mass": 1.989e30,
            "position": [0, 0, 0],
            "velocity": [0, 0, 0],
            "is_blackhole": true
        },
        {
            "id": "star1",
            "name": "Star Beta",
            "mass": 1.989e29,
            "position": [1e11, 0, 0],
            "velocity": [0, 2e4, 0],
            "is_blackhole": false
        },
        {
            "id": "planet1",
            "name": "Planet Gamma",
            "mass": 5.972e24,
            "position": [1.5e11, 0, 0],
            "velocity": [0, 3e4, 0],
            "is_blackhole": false
        }
    ]
}
"""
}

for path, content in files.items():
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(content, encoding="utf-8")

print("✓ All code files generated successfully")
# This is the last line of .overwrite.py