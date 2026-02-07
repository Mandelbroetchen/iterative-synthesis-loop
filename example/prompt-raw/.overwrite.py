from pathlib import Path

files = {
    "prompt-final/document.md": """# Freefall of an Apple - System Documentation

## 1. Purpose and Goals
This system simulates the freefall motion of an apple under constant gravitational acceleration. The program takes initial parameters as input and outputs the evolution of physical variables (position, velocity, acceleration) over time.

### Key Objectives:
- Model one-dimensional freefall motion with constant acceleration
- Calculate and display position, velocity, and acceleration at discrete time intervals
- Provide a simple, educational demonstration of basic physics principles
- Allow customization of gravitational acceleration for different planetary environments

## 2. Functional Requirements

### 2.1 Input Requirements
The system shall accept the following input parameters:
- Initial height (h₀): Starting position of the apple (meters)
- Initial velocity (v₀): Starting velocity of the apple (meters/second)
- Time step (Δt): Interval between calculations (seconds)
- Total duration (T): Total simulation time (seconds)
- Gravitational acceleration (g): Acceleration due to gravity (meters/second²), defaulting to Earth's gravity (9.81 m/s²)

### 2.2 Processing Requirements
The system shall:
1. Validate all input parameters to ensure they are physically plausible:
   - Initial height must be ≥ 0
   - Time step must be > 0
   - Total duration must be > 0
   - Gravitational acceleration must be ≥ 0
2. Calculate position at each time step using:
   h(t) = h₀ + v₀ * t + 0.5 * g * t²
3. Calculate velocity at each time step using:
   v(t) = v₀ + g * t
4. Calculate acceleration (constant):
   a(t) = g
5. Iterate through time steps from t = 0 to t = T in increments of Δt
6. Handle edge cases where the apple would hit the ground (h(t) ≤ 0) by stopping the simulation

### 2.3 Output Requirements
The system shall output:
1. A table showing the evolution of variables at each time step:
   - Time (t)
   - Position (h)
   - Velocity (v)
   - Acceleration (a)
2. A summary of input parameters used for the simulation
3. A warning if the simulation stopped early due to the apple hitting the ground

## 3. Technical Architecture

### 3.1 System Components
1. **Input Handler**: Collects and validates user input
2. **Physics Engine**: Performs freefall calculations
3. **Simulation Controller**: Manages the simulation loop and time steps
4. **Output Formatter**: Formats results for display
5. **Ground Detection**: Monitors for collision with ground level

### 3.2 Key Constraints
- Assumes constant gravitational acceleration (no air resistance)
- One-dimensional motion only
- Ground level is fixed at h = 0
- Time steps are uniform
- No energy loss during ground collision (perfectly elastic collision for demonstration purposes)

### 3.3 Assumptions
- Earth's gravity (g = 9.81 m/s²) unless specified otherwise
- Perfectly vertical freefall
- No external forces other than gravity
- The apple is treated as a point mass
- Ground collision is detected when position ≤ 0

## 4. Mathematical Model

The system implements the following equations of motion for constant acceleration:

1. Position as a function of time:
   h(t) = h₀ + v₀ * t + (1/2) * g * t²

2. Velocity as a function of time:
   v(t) = v₀ + g * t

3. Acceleration (constant):
   a(t) = g

For ground collision detection:
- The simulation stops when h(t) ≤ 0
- The time of impact is calculated by solving h(t) = 0:
  t_impact = [-v₀ ± sqrt(v₀² + 2 * g * h₀)] / g
  (only the positive root is physically meaningful)

## 5. Example Use Cases

### 5.1 Basic Freefall Simulation
**Scenario**: Simulate an apple falling from 10 meters with initial velocity of 0 m/s on Earth.

**Input**:
- h₀ = 10 m
- v₀ = 0 m/s
- Δt = 0.1 s
- T = 1.5 s
- g = 9.81 m/s²

**Expected Output**:
```
Simulation Parameters:
- Initial height: 10.00 m
- Initial velocity: 0.00 m/s
- Time step: 0.10 s
- Total duration: 1.50 s
- Gravitational acceleration: 9.81 m/s²

Results:
Time (s) | Position (m) | Velocity (m/s) | Acceleration (m/s²)
---------------------------------------------------------------
0.0      | 10.00        | 0.00           | 9.81
0.1      | 9.95         | 0.98           | 9.81
0.2      | 9.80         | 1.96           | 9.81
...      | ...          | ...            | ...
1.4      | 3.64         | 13.73          | 9.81
1.5      | 2.53         | 14.72          | 9.81
```

### 5.2 Ground Collision Detection
**Scenario**: Simulate an apple falling from 5 meters with initial velocity of 0 m/s, showing ground collision.

**Input**:
- h₀ = 5 m
- v₀ = 0 m/s
- Δt = 0.05 s
- T = 2.0 s
- g = 9.81 m/s²

**Expected Output**:
```
Simulation Parameters:
- Initial height: 5.00 m
- Initial velocity: 0.00 m/s
- Time step: 0.05 s
- Total duration: 2.00 s
- Gravitational acceleration: 9.81 m/s²

Warning: Simulation stopped early - apple hit the ground at t ≈ 1.01 s

Results:
Time (s) | Position (m) | Velocity (m/s) | Acceleration (m/s²)
---------------------------------------------------------------
0.00     | 5.00         | 0.00           | 9.81
0.05     | 4.98         | 0.49           | 9.81
...      | ...          | ...            | ...
1.00     | 0.09         | 9.81           | 9.81
1.05     | -0.40        | 10.30          | 9.81
```

### 5.3 Lunar Freefall Simulation
**Scenario**: Simulate an apple falling on the Moon (g = 1.62 m/s²).

**Input**:
- h₀ = 10 m
- v₀ = 0 m/s
- Δt = 0.2 s
- T = 4.0 s
- g = 1.62 m/s²

**Expected Output**:
```
Simulation Parameters:
- Initial height: 10.00 m
- Initial velocity: 0.00 m/s
- Time step: 0.20 s
- Total duration: 4.00 s
- Gravitational acceleration: 1.62 m/s²

Results:
Time (s) | Position (m) | Velocity (m/s) | Acceleration (m/s²)
---------------------------------------------------------------
0.0      | 10.00        | 0.00           | 1.62
0.2      | 9.97         | 0.32           | 1.62
0.4      | 9.87         | 0.65           | 1.62
...      | ...          | ...            | ...
3.8      | 3.57         | 6.16           | 1.62
4.0      | 2.96         | 6.48           | 1.62
```

## 6. Design Decisions

### 6.1 Ground Collision Handling
- The system implements ground collision detection to provide more realistic simulations
- When position ≤ 0, the simulation stops and reports the impact time
- This feature helps demonstrate the physical reality of objects not passing through the ground

### 6.2 Time Step Selection
- The system allows customizable time steps to balance accuracy and computational efficiency
- Smaller time steps provide more accurate results but require more calculations
- The default time step (if not specified) is set to 0.1 seconds for reasonable accuracy

### 6.3 Gravitational Acceleration
- The system allows customization of gravitational acceleration to support:
  - Educational demonstrations of physics on different planets
  - Comparison of freefall behavior in different gravitational fields
  - Special cases like zero gravity or microgravity environments

## 7. Limitations and Future Enhancements

### 7.1 Current Limitations
- No air resistance or drag forces
- Only one-dimensional motion
- Perfectly elastic collision with ground
- No visualization of results
- No energy calculations

### 7.2 Future Enhancements
- Add air resistance for more realistic simulations
- Implement two-dimensional motion (projectile motion)
- Add energy calculations (potential and kinetic energy)
- Include visualization of the freefall trajectory
- Add support for variable gravitational fields
- Implement more sophisticated collision physics
""",
    "prompt-final/usecase-diagram.uml": """@startuml usecase-diagram

left to right direction

actor User

rectangle FreefallSimulation {
  usecase (Input Parameters) as UC1
  usecase (Run Simulation) as UC2
  usecase (View Results) as UC3
  usecase (Set Gravitational Acceleration) as UC4
  usecase (Detect Ground Collision) as UC5
}

User --> UC1
User --> UC2
User --> UC3
User --> UC4

UC1 .> UC2 : includes
UC2 .> UC3 : includes
UC2 .> UC5 : includes

@enduml
""",
    "prompt-final/package-diagram.uml": """@startuml package-diagram

package "Freefall Simulation" {
  package "Input" {
    [Parameter Collector]
    [Input Validator]
  }

  package "Physics" {
    [Freefall Calculator]
    [Ground Detector]
  }

  package "Simulation" {
    [Simulation Controller]
  }

  package "Output" {
    [Result Formatter]
    [Warning Generator]
  }
}

[Parameter Collector] --> [Input Validator]
[Input Validator] --> [Simulation Controller]
[Simulation Controller] --> [Freefall Calculator]
[Freefall Calculator] --> [Ground Detector]
[Simulation Controller] --> [Result Formatter]
[Ground Detector] --> [Warning Generator]

@enduml
""",
    "prompt-final/class-diagram.uml": """@startuml class-diagram

class FreefallSimulator {
  -h0: float
  -v0: float
  -dt: float
  -T: float
  -g: float
  +__init__(h0: float, v0: float, dt: float, T: float, g: float = 9.81)
  +validate_inputs(): bool
  +calculate_position(t: float): float
  +calculate_velocity(t: float): float
  +run_simulation(): SimulationResult
  -detect_ground_collision(t: float, h: float): bool
}

class SimulationResult {
  +time: list[float]
  +position: list[float]
  +velocity: list[float]
  +acceleration: list[float]
  +impact_time: float | None
  +completed: bool
  +__init__(time: list, position: list, velocity: list, acceleration: list, impact_time: float | None)
  +display(): str
  +get_summary(): str
}

class InputValidator {
  +validate_height(h0: float): bool
  +validate_velocity(v0: float): bool
  +validate_time_step(dt: float): bool
  +validate_duration(T: float): bool
  +validate_gravity(g: float): bool
  +validate_all(h0: float, v0: float, dt: float, T: float, g: float): bool
}

class WarningGenerator {
  +ground_collision_warning(impact_time: float): str
  +early_termination_warning(): str
}

FreefallSimulator --> SimulationResult : produces >
FreefallSimulator --> InputValidator : uses >
FreefallSimulator --> WarningGenerator : uses >

@enduml
"""
}

for path, content in files.items():
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(content, encoding="utf-8")

print("✓ All files updated successfully")