# Code Generation Prompt from Design Artifacts

## Overview

You are a **code generation engine** responsible for implementing software based on detailed design specifications and architecture diagrams.

**Objective**: Generate or update code files in `code-raw/` according to explicit instructions in `prompt-final/`, using design artifacts as the single source of truth.

---

## Part 1: Design Specification (Input)

Everything in `prompt-final/` serves as your design input.

### 1.1 System Documentation
**File**: `prompt-final/documentation.md`

This document provides comprehensive system design including:
- Functional and non-functional requirements
- Architecture and design patterns
- Data models and relationships
- API specifications and interfaces
- Technical constraints and implementation notes


<file src = "documentation.md">

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

</file>


### 1.2 Use Case Diagram
**File**: `prompt-final/usecase-diagram.uml`

Visual representation of actors, use cases, and system interactions (UML Use Case Diagram).





### 1.3 Package/Module Architecture
**File**: `prompt-final/package-diagram.uml`

Module structure, dependencies, and organization (UML Package Diagram).





### 1.4 Data Model & Class Structure
**File**: `prompt-final/class-diagram.uml`

Entity definitions, attributes, methods, and relationships (UML Class Diagram).




### 1.5 Project Patches
**File**: `prompt-final/patches.md`

<file src = "patches.md">

also generate example config files
</file>

---

## Part 2: Current Code State (Reference)

These files currently exist in `code-raw/` and represent the current implementation state. Update them according to the modes specified in `prompt-final/`.

### 2.1 Existing Code Files

<file src = "patches.md">


</file>

<file src = "__init__.py">

# Blackhole Simulation System Package
# Core package for blackhole simulation system

__version__ = "0.1.1"

</file>

















---

## Part 3: Implementation Requirements

### Rules
2. **Respect the specified mode for each file**
3. **Follow the design artifacts strictly** - code must implement the documented design
4. **Preserve existing code** in completion and correction modes
5. **Ensure all code is production-ready** (properly tested, documented, error-handled)
6. **Maintain consistency** across all generated files and modules

### Code Quality Standards
- [ ] All code follows PEP 8 (or applicable language style guide)
- [ ] Functions and classes have docstrings
- [ ] Error handling is comprehensive
- [ ] No hardcoded values; use configuration/constants
- [ ] Code implements all specified use cases from diagram
- [ ] Data models match class diagram exactly
- [ ] Package structure matches package diagram
- [ ] All dependencies are clearly imported
- [ ] Generated code is syntactically correct
- [ ] Code aligns with design specification in documentation.md

---

## Part 4: Output Format (STRICT)

**You must respond with exactly one file: `overwrite.py`**

Requirements:
- Pure Python code only (no explanations, comments, or additional text)
- The code should be run from the folder `raw-code`
- Complete, production-ready code for each file
- UTF-8 encoding
- Creates directories if needed (`code-raw/` subdirectories)
- Successfully executes without errors

**Template Structure**:

```python
# This is the first line of .overwrite.py
from pathlib import Path

files = {
    "code-raw/.patchnotes.md": """[Complete patchnotes]""",
    "code-raw/__init__.py": """[Complete Python code]""",
    "code-raw/module1.py": """[Complete Python code]""",
    "code-raw/module2.py": """[Complete Python code]""",
    "code-raw/utils.py": """[Complete Python code]"""
}

for path, content in files.items():
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(content, encoding="utf-8")

print("✓ All code files generated successfully")
# This is the last line of .overwrite.py
```

<file src = "global-prompt.md">

Do not include any additional output or explanation beyond the Python code. Start the code of `.overwrite.py` with a single line `# This is the first line of overwrite.py` and end with a single line `# This is the last line of overwrite.py`. 
</file>
