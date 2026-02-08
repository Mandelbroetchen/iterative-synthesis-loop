# This is the first line of overwrite.py
from pathlib import Path

files = {
    "prompt-final/documentation.md": """# Blackhole Simulation System Documentation

## 1. Introduction
This document describes the design and implementation of a blackhole simulation system that models celestial objects based on user-provided configurations.

### 1.1 Purpose
The system simulates gravitational interactions between celestial objects, with a focus on blackhole physics, based on configurable parameters.

### 1.2 Scope
- Reads configuration from `config.json` and `objects.json`
- Performs physics calculations
- Outputs simulation data to `./out/` directory

## 2. System Requirements

### 2.1 Functional Requirements
1. **Configuration Input**: Read physical parameters from `config.json`
2. **Object Input**: Read celestial object data from `objects.json`
3. **Simulation Execution**: Perform physics calculations based on input data
4. **Data Output**: Write simulation results to `./out/` directory

### 2.2 Non-Functional Requirements
- **Performance**: Efficient handling of complex gravitational calculations
- **Accuracy**: Physically accurate modeling of celestial mechanics
- **Extensibility**: Modular design for future physics model enhancements

## 3. System Architecture

### 3.1 High-Level Overview
The system follows a modular architecture with clear separation between:
- Input processing
- Physics simulation
- Output generation

### 3.2 Data Flow
1. User provides `config.json` and `objects.json`
2. System loads and validates input data
3. Simulation engine processes physics calculations
4. Results are written to output directory

## 4. Detailed Design

### 4.1 Input Data Model
The system expects two JSON input files:

**config.json** (Simulation Parameters):
```json
{
    "time_step": 0.01,
    "total_time": 100.0,
    "gravitational_constant": 6.67430e-11,
    "output_frequency": 10
}
```

**objects.json** (Celestial Objects):
```json
{
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
        }
    ]
}
```

### 4.2 Physics Model
The system implements Newtonian gravity with special handling for blackholes:

1. Gravitational force between objects:
   F = G * (m1 * m2) / r^2

2. Blackhole special properties:
   - Event horizon radius: r_s = 2GM/c^2
   - Objects crossing event horizon are removed from simulation

### 4.3 Output Format
Simulation results are written as JSON files in `./out/` with the following structure:
```json
{
    "time": 1.0,
    "objects": [
        {
            "id": "bh1",
            "position": [0, 0, 0],
            "velocity": [0, 0, 0],
            "acceleration": [0, 0, 0]
        }
    ]
}
```

## 5. Implementation Considerations

### 5.1 Error Handling
- Validate input JSON schemas
- Check for division by zero in physics calculations
- Handle file I/O errors gracefully

### 5.2 Performance Optimization
- Use vectorized operations for physics calculations
- Implement spatial partitioning for large numbers of objects
- Consider parallel processing for computationally intensive simulations

## 6. Testing Strategy

### 6.1 Unit Tests
- Input validation tests
- Physics calculation tests
- Output generation tests

### 6.2 Integration Tests
- End-to-end simulation tests
- Configuration parameter tests
- Blackhole-specific behavior tests

## 7. Future Enhancements
- Add general relativity effects
- Implement visualization module
- Support for more complex object types
- Parallel processing for large simulations
""",
    "prompt-final/usecase-diagram.puml": """@startuml usecase-diagram

left to right direction

actor User as user

rectangle "Blackhole Simulation System" {
    usecase "Provide Configuration" as UC1
    usecase "Provide Celestial Objects" as UC2
    usecase "Run Simulation" as UC3
    usecase "View Results" as UC4
}

user --> UC1
user --> UC2
user --> UC3
user --> UC4

UC1 ..> UC3 : includes
UC2 ..> UC3 : includes

@enduml
""",
    "prompt-final/package-diagram.puml": """@startuml package-diagram

package "Blackhole Simulation" {
    package "input" {
        [ConfigReader]
        [ObjectReader]
    }

    package "simulation" {
        [PhysicsEngine]
        [BlackholeHandler]
    }

    package "output" {
        [DataWriter]
    }

    package "models" {
        [CelestialObject]
        [SimulationConfig]
    }
}

[ConfigReader] --> [SimulationConfig]
[ObjectReader] --> [CelestialObject]
[PhysicsEngine] --> [CelestialObject]
[PhysicsEngine] --> [BlackholeHandler]
[PhysicsEngine] --> [SimulationConfig]
[DataWriter] --> [CelestialObject]

@enduml
""",
    "prompt-final/class-diagram.puml": """@startuml class-diagram

class CelestialObject {
    +String id
    +String name
    +double mass
    +double[3] position
    +double[3] velocity
    +boolean is_blackhole
    +{method} update_position(double dt)
    +{method} update_velocity(double dt)
}

class Blackhole {
    +double event_horizon_radius
    +{method} calculate_event_horizon()
}

class SimulationConfig {
    +double time_step
    +double total_time
    +double gravitational_constant
    +int output_frequency
}

class PhysicsEngine {
    +SimulationConfig config
    +List<CelestialObject> objects
    +{method} calculate_gravitational_force(CelestialObject a, CelestialObject b)
    +{method} update_simulation()
    +{method} check_collisions()
}

class DataWriter {
    +{method} write_output(double time, List<CelestialObject> objects)
}

class ConfigReader {
    +{method} read_config(String path)
}

class ObjectReader {
    +{method} read_objects(String path)
}

CelestialObject <|-- Blackhole
PhysicsEngine "1" *-- "*" CelestialObject
PhysicsEngine "1" --> "1" SimulationConfig
DataWriter "1" --> "*" CelestialObject
ConfigReader "1" --> "1" SimulationConfig
ObjectReader "1" --> "*" CelestialObject

@enduml
""",
    "prompt-final/.patchnotes.md": """# Patch Notes

## Initial Version
- Created comprehensive system documentation
- Added UML diagrams:
  - Use case diagram
  - Package diagram
  - Class diagram
- Established project structure and requirements
- Defined input/output formats
- Documented physics model and implementation considerations
"""

}

for path, content in files.items():
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(content, encoding="utf-8")

print("✓ All files updated successfully")
# This is the last line of overwrite.py