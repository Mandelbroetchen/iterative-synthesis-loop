# Design Prompt for Blueprint Completion
The following promt is generated from the two folders `idea` and `blueprint`. The purpose of this prompt is to overwrite files in `blueprint`, based on the generated instructions generated from `idea`.  

## Instructions
This part of the prompt is generated from `idea`

### Description
`description.md` is a markdown file that describes the main idea.
```
# Freefall of an apple
```

### Overwrite
`overwrite.json` is a json file that specifies which files are to be overwritten (generation, completion or correction). 
```
[
    {
        "path":"prompt/document.md"
    },
    {
        "path":"prompt/usecase-diagram.uml"
    },
    {
        "path":"prompt/class-diagram.uml"
    },
    {
        "path":"prompt/package-diagram.uml"
    },
    {
        "path":"prompt/write.json"
    }
]
```

## Blueprint
This part of the prompt describes current state of `blueprint`

### `blueprint/document.md`
This is a general documentation of the final project. 
```
# Freefall of an Apple - Physics Simulation

## Overview
This project simulates the freefall motion of an apple under Earth's gravity, demonstrating fundamental physics principles including Newton's laws of motion and kinematic equations.

## Core Concepts
- **Freefall**: Motion where gravity is the only force acting on an object
- **Gravity**: Constant acceleration of 9.81 m/s² near Earth's surface
- **Kinematics**: Study of motion without considering forces

## Key Features
1. Real-time position, velocity, and acceleration tracking
2. Time-based simulation with configurable parameters
3. Visual representation of the falling apple
4. Data export for analysis

## Mathematical Model
The simulation uses these kinematic equations:
- Position: y(t) = y₀ + v₀t + ½gt²
- Velocity: v(t) = v₀ + gt
- Acceleration: a = g (constant)

Where:
- y₀ = initial height
- v₀ = initial velocity
- g = gravitational acceleration (9.81 m/s²)
- t = time
```
### `blueprint/usecase-diagram.uml`
```
@startuml FreefallUseCaseDiagram

left to right direction

actor User
actor "Physics Engine" as Engine

rectangle "Freefall Simulation" {
  usecase "Configure Parameters" as UC1
  usecase "Run Simulation" as UC2
  usecase "Visualize Results" as UC3
  usecase "Export Data" as UC4
  usecase "Calculate Trajectory" as UC5
  usecase "Update Physics" as UC6
}

User --> UC1
User --> UC2
User --> UC3
User --> UC4
Engine --> UC5
Engine --> UC6

UC1 .> UC2 : includes
UC2 .> UC5 : includes
UC5 .> UC6 : includes
UC2 .> UC3 : includes
UC2 .> UC4 : extends

@enduml
```

### `blueprint/package-diagram.uml`
```
@startuml FreefallPackageDiagram

package "Freefall Simulation" {
  package "core" {
    [PhysicsEngine]
    [SimulationController]
  }

  package "ui" {
    [MainWindow]
    [VisualizationPanel]
    [ControlPanel]
  }

  package "models" {
    [Apple]
    [Environment]
    [Trajectory]
  }

  package "utils" {
    [DataExporter]
    [MathUtils]
  }
}

[PhysicsEngine] --> [Apple]
[PhysicsEngine] --> [Environment]
[SimulationController] --> [PhysicsEngine]
[SimulationController] --> [Trajectory]
[MainWindow] --> [VisualizationPanel]
[MainWindow] --> [ControlPanel]
[ControlPanel] --> [SimulationController]
[VisualizationPanel] --> [Trajectory]
[DataExporter] --> [Trajectory]

@enduml
```

### `blueprint/class-diagram.uml`
```
@startuml FreefallClassDiagram

class Apple {
  -mass: float
  -position: Vector2D
  -velocity: Vector2D
  -radius: float
  +updatePosition(time: float): void
  +getPosition(): Vector2D
  +getVelocity(): Vector2D
}

class Environment {
  -gravity: float
  -airResistance: float
  -wind: Vector2D
  +getGravity(): float
  +applyAirResistance(velocity: Vector2D): Vector2D
}

class PhysicsEngine {
  -apple: Apple
  -environment: Environment
  +calculateTrajectory(timeStep: float): Trajectory
  +updatePhysics(timeStep: float): void
}

class Trajectory {
  -points: List<Vector2D>
  -times: List<float>
  +addPoint(position: Vector2D, time: float): void
  +getPoints(): List<Vector2D>
  +getTimes(): List<float>
}

class SimulationController {
  -physicsEngine: PhysicsEngine
  -trajectory: Trajectory
  -isRunning: boolean
  +startSimulation(): void
  +pauseSimulation(): void
  +resetSimulation(): void
  +update(timeStep: float): void
}

class Vector2D {
  +x: float
  +y: float
  +add(v: Vector2D): Vector2D
  +subtract(v: Vector2D): Vector2D
  +multiply(scalar: float): Vector2D
}

PhysicsEngine "1" *-- "1" Apple
PhysicsEngine "1" *-- "1" Environment
SimulationController "1" *-- "1" PhysicsEngine
SimulationController "1" *-- "1" Trajectory
Apple "1" --> "1" Vector2D
Environment "1" --> "1" Vector2D

@enduml
```

## Output
Your response must strictly be a file "overwrite.py" that overwrites the files in `blueprint` as specified in `idea/overwrite.json`. Do not include any explanations or additional text. Only provide the complete content of the overwritten files.