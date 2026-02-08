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


<insert src="./prompt-final/documentation.md"></insert>


### 1.2 Use Case Diagram
**File**: `prompt-final/usecase-diagram.uml`

Visual representation of actors, use cases, and system interactions (UML Use Case Diagram).


<insert src="./prompt-final/usecase-diagram.uml"></insert>


### 1.3 Package/Module Architecture
**File**: `prompt-final/package-diagram.uml`

Module structure, dependencies, and organization (UML Package Diagram).


<insert src="./prompt-final/package-diagram.uml"></insert>


### 1.4 Data Model & Class Structure
**File**: `prompt-final/class-diagram.uml`

Entity definitions, attributes, methods, and relationships (UML Class Diagram).


<insert src="./prompt-final/class-diagram.uml"></insert>

### 1.5 Project Patches
**File**: `prompt-final/patches.md`

<insert src="./prompt-final/patches.md"></insert>

---

## Part 2: Current Code State (Reference)

These files currently exist in `code-raw/` and represent the current implementation state. Update them according to the modes specified in `prompt-final/`.

### 2.1 Existing Code Files

<insert src="./code-raw"></insert>

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

<insert src="./global-prompt.md"></insert>
