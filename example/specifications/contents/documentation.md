# Blackhole Simulation System Documentation

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
