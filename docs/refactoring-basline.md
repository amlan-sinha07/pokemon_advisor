# Refactoring Baseline

## 1. Initial State Before Refactoring

### Working Features

- CLI menu
- Pokémon loading
- Fuzzy search
- Team recommendations
- Move recommendations
- Type effectiveness

### Identified Issues

- C++ stdout contained debugging information.
- Executable naming and invocation were inconsistent.
- Some modules mixed calculation logic with terminal output.
- JSON loading and file paths needed improvement.

### Initial Testing Limitations

- No automated regression suite.
- Data loading depended on relative file paths.
- Python-C++ integration lacked sufficient automated verification.

---

## 2. Refactoring Outcomes

### Testing

- Introduced pytest-based regression tests.
- Added tests for the type calculator and data loader.
- Added tests for Pokémon and Move models.
- Added tests for box management and advisors.
- Added tests for the Python-C++ damage calculation interface.
- Added scraper tests.

**Current test result: 53 passed.**

### Python Improvements

- Improved JSON loading and error handling.
- Introduced pathlib-based project paths.
- Improved Pokémon and move data validation.
- Improved cache handling.
- Removed redundant code and imports.
- Improved error handling for user input.

### C++ Integration

- Removed debug output from standard output.
- Established a numerical output protocol.
- Improved Python subprocess handling.
- Added timeout and return-code checks.
- Verified Python-C++ communication with standalone test inputs.
- Added Python fallback calculation.

### Code Organization

- Preserved existing module responsibilities.
- Improved separation between data loading and model construction.
- Improved testability of calculation and recommendation modules.

---

## 3. Remaining Limitations

- Some domain modules still contain terminal output.
- Pre-match scoring remains a heuristic.
- Pokémon and move data require validation against the actual Pokémon Champions roster and mechanics.
- More integration and edge-case tests are desirable.
- The damage formula is a simplified level-50 estimate rather than a complete battle simulator.

---

## 4. Refactoring Principle

The objective is to improve internal structure, reliability, maintainability and testability without intentionally changing existing application behavior.

Major architectural expansion is deferred until the existing application foundation is stable.