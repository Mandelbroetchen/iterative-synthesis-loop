# Apple Freefall Simulation System Documentation

## 1. Introduction
### 1.1 Purpose
The Apple Freefall Simulation is a Python application that models the freefall motion of an apple under Earth's gravity. The system allows users to input physical parameters and visualize the apple's trajectory over time, demonstrating basic principles of kinematics.

### 1.2 Goals
- Provide an educational tool for understanding freefall motion
- Allow users to experiment with different physical parameters
- Generate clear output of the simulation results
- Implement a simple configuration system for simulation parameters

### 1.3 Scope
The system will:
- Accept user input for physical parameters (initial height, mass, etc.)
- Read simulation parameters from a config.json file
- Calculate the apple's position over time during freefall
- Output the evaluation results to out.md
- Handle basic error cases for invalid inputs

## 2. Functional Requirements

### 2.1 Core Requirements
| ID | Requirement | Description |
|----|-------------|-------------|
| FR-01 | User Input | System shall accept user input for physical parameters |
| FR-02 | Configuration | System shall read simulation parameters from config.json |
| FR-03 | Freefall Calculation | System shall calculate apple's position over time during freefall |
| FR-04 | Output Generation | System shall write simulation results to out.md |
| FR-05 | Time Step Simulation | System shall simulate motion using configurable time steps |

### 2.2 Input Requirements
| ID | Requirement | Description |
|----|-------------|-------------|
| FR-06 | Initial Height | System shall accept initial height of the apple |
| FR-07 | Mass Input | System shall accept mass of the apple |
| FR-08 | Air Resistance Toggle | System shall allow enabling/disabling air resistance |
| FR-09 | Simulation Duration | System shall accept total simulation time |

## 3. System Architecture

### 3.1 Technical Stack
- **Language**: Python 3.8+
- **Configuration**: JSON for simulation parameters
- **Physics Model**: Basic kinematics equations
- **Output**: Markdown file generation

### 3.2 Component Overview
1. **Input Handler**: Collects user input for physical parameters
2. **Configuration Manager**: Reads and validates config.json
3. **Physics Engine**: Calculates freefall motion
4. **Output Generator**: Writes results to out.md

## 4. Design Decisions

### 4.1 Physics Model
- Using simplified kinematic equations for freefall motion
- Earth's gravity (g = 9.81 m/s²) as constant acceleration
- Optional air resistance modeled as proportional to velocity squared
- Time-stepped simulation for accurate results

### 4.2 Input Handling
- Command-line interface for user input
- Input validation for physical parameters
- Default values for optional parameters

### 4.3 Configuration
- JSON format for easy modification
- Configurable time step for simulation accuracy
- Configurable output precision

## 5. Mathematical Model

### 5.1 Basic Freefall (No Air Resistance)
Position as a function of time:

y(t) = y_0 - 0.5 * g * t^2

Velocity as a function of time:

v(t) = -g * t

Where:
- y(t) is the height at time t
- y_0 is the initial height
- g is the acceleration due to gravity (9.81 m/s²)
- v(t) is the velocity at time t

### 5.2 Freefall with Air Resistance
Air resistance force:

F_air = 0.5 * ρ * C_d * A * v^2

Where:
- ρ is the air density
- C_d is the drag coefficient
- A is the cross-sectional area
- v is the velocity

Net acceleration:

a = g - (F_air / m)

Where:
- m is the mass of the apple

## 6. User Interface Design

### 6.1 Input Flow
1. Prompt for initial height (meters)
2. Prompt for apple mass (kilograms)
3. Prompt for air resistance toggle (yes/no)
4. If air resistance enabled, prompt for drag coefficient and cross-sectional area
5. Prompt for simulation duration (seconds)

### 6.2 Output Format
The out.md file will contain:
- Simulation parameters
- Table of time, position, and velocity values
- Graph of position vs. time (ASCII art)
- Summary statistics (max velocity, time to impact)

## 7. Implementation Plan

### 7.1 Development Phases
1. **Core Physics**: Implement basic freefall calculations
2. **Input Handling**: Develop user input collection
3. **Configuration**: Implement config.json reading
4. **Output Generation**: Create out.md writer
5. **Testing**: Validate physics calculations and edge cases

### 7.2 Testing Strategy
- Unit tests for physics calculations
- Integration tests for input/output flow
- Validation tests for edge cases (zero height, negative mass)
- Performance tests for large time steps

## 8. Glossary
- **Freefall**: Motion of an object under the influence of gravity only
- **Kinematics**: Study of motion without considering forces
- **Air Resistance**: Force opposing motion through air
- **Time Step**: Interval between calculations in the simulation
