# Freefall of an Apple - System Documentation

## 1. Purpose and Goals
This system simulates the freefall motion of an apple under constant gravitational acceleration. The program takes initial parameters as input and outputs the evolution of physical variables (position, velocity, acceleration) over time.

### Key Objectives:
- Model one-dimensional freefall motion with constant acceleration
- Calculate and display position, velocity, and acceleration at discrete time intervals
- Provide a simple, educational demonstration of basic physics principles

## 2. Functional Requirements

### 2.1 Input Requirements
The system shall accept the following input parameters:
- Initial height (h₀): Starting position of the apple (meters)
- Initial velocity (v₀): Starting velocity of the apple (meters/second)
- Time step (Δt): Interval between calculations (seconds)
- Total duration (T): Total simulation time (seconds)
- Gravitational acceleration (g): Typically 9.81 m/s² (meters/second²)

### 2.2 Processing Requirements
The system shall:
1. Calculate position at each time step using:
   h(t) = h₀ + v₀ * t + 0.5 * g * t²
2. Calculate velocity at each time step using:
   v(t) = v₀ + g * t
3. Calculate acceleration (constant):
   a(t) = g
4. Iterate through time steps from t = 0 to t = T in increments of Δt

### 2.3 Output Requirements
The system shall output a table showing:
- Time (t)
- Position (h)
- Velocity (v)
- Acceleration (a)

## 3. Technical Architecture

### 3.1 System Components
1. **Input Handler**: Collects and validates user input
2. **Physics Engine**: Performs freefall calculations
3. **Output Formatter**: Formats results for display

### 3.2 Key Constraints
- Assumes constant gravitational acceleration (no air resistance)
- One-dimensional motion only
- No collision detection (apple falls indefinitely)

### 3.3 Assumptions
- Earth's gravity (g = 9.81 m/s²) unless specified otherwise
- Perfectly vertical freefall
- Time steps are uniform

## 4. Mathematical Model

The system implements the following equations of motion:

1. Position as a function of time:
   h(t) = h₀ + v₀ * t + (1/2) * g * t²

2. Velocity as a function of time:
   v(t) = v₀ + g * t

3. Acceleration (constant):
   a(t) = g

## 5. Example Use Case

**Scenario**: Simulate an apple falling from 10 meters with initial velocity of 0 m/s.

**Input**:
- h₀ = 10 m
- v₀ = 0 m/s
- Δt = 0.1 s
- T = 1.5 s
- g = 9.81 m/s²

**Expected Output**:
```
Time (s) | Position (m) | Velocity (m/s) | Acceleration (m/s²)
---------------------------------------------------------------
0.0      | 10.00        | 0.00           | 9.81
0.1      | 9.95         | 0.98           | 9.81
0.2      | 9.80         | 1.96           | 9.81
...      | ...          | ...            | ...
1.5      | 2.53         | 14.72          | 9.81
```
