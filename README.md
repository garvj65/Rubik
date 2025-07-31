# Scalable Rubik's Cube Solver

This project implements a scalable algorithm for solving Rubik's Cubes of various sizes (2x2, 3x3, and 4x4), with a focus on NxN scalability. The implementation balances time and space complexity while providing an intuitive solution inspired by human problem-solving approaches.

The library provides comprehensive tools for simulating, visualizing, and solving Rubik's Cubes with support for different solving algorithms and 3D visualization.

## Project Structure

- `cube/` - Core cube representation and operations
  - `__init__.py` - Package initialization
  - `model.py` - Data structures for cube representation
  - `moves.py` - Move engine supporting various turns and rotations

- `solvers/` - Implementation of solving algorithms
  - `__init__.py` - Package initialization
  - `base_solver.py` - Base solver interface
  - `kociemba.py` - Two-phase algorithm implementation
  - `reduction.py` - 4x4 reduction method
  - `supercube.py` - Solver for supercubes (where center orientation matters)

- `visualization/` - 3D visualization tools
  - `__init__.py` - Package initialization
  - `renderer.py` - 3D cube renderer

- `examples/` - Example usage and demonstrations
  - `__init__.py` - Package initialization
  - `demo.py` - Main demonstration
  - `custom_solver.py` - Custom solver example
  - `custom_cube.py` - Custom cube variants
  - `custom_algorithm.py` - Custom algorithm steps
  - `benchmark.py` - Performance benchmarking
  - `custom_heuristic.py` - Custom heuristics
  - `ida_star_solver.py` - IDA* implementation
  - `thistlethwaite_solver.py` - Thistlethwaite algorithm
  - `realtime_3d_solver.py` - Real-time 3D solver with interactive visualization

- `tests/` - Unit tests
  - `__init__.py` - Package initialization
  - `test_cube.py` - Tests for cube functionality
  
- `setup.py` - Package installation script
- `requirements.txt` - Project dependencies
- `run_tests.py` - Script to run all tests

## Features

- **Flexible Cube Model**: Scalable design supporting 2x2, 3x3, 4x4, and potentially larger cubes
- **Efficient Data Structures**: Layered cubie matrix and cubie objects for optimal representation
- **Comprehensive Move Engine**: Support for various turns and rotations
- **Multiple Solving Algorithms**:
  - Kociemba's Two-Phase Algorithm
  - Reduction Method (for 4x4)
  - Thistlethwaite's Algorithm
  - IDA* with pattern databases
- **Visualization**:
  - 3D rendering with matplotlib
  - Animation of move sequences
  - Interactive 3D visualization with ipywidgets
- **Supercube Support**: Handles supercubes where center orientation matters
- **Benchmarking Tools**: Compare performance of different solving algorithms

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/rubik.git
cd rubik

# Install the package and dependencies
pip install -e .
```

Or install directly using pip:

```bash
pip install -r requirements.txt
```

## How to Run

The main entry point for the interactive 3D solver is `examples/realtime_3d_solver.py`.

To run the interactive solver:

```bash
python examples/realtime_3d_solver.py
```

This will open a window with a 3D representation of the cube. You can interact with the solver using the command line.

The script also supports an automatic demo mode:

```bash
python examples/realtime_3d_solver.py
```
Then choose option 2.

## Usage Examples

### Basic Cube Operations

```python
from cube.model import Cube
from visualization.renderer import render_cube_3d

# Create a 3x3 cube
cube = Cube(3)

# Apply some moves
cube.apply_move("R")
cube.apply_move("U")
cube.apply_move("R'")

# Visualize the cube
render_cube_3d(cube)

# Check if the cube is solved
print(f"Cube is solved: {cube.is_solved()}")

# Scramble the cube
scramble_moves = cube.scramble(20)
print(f"Scrambled with moves: {scramble_moves}")
```

### Solving a Cube

```python
from cube.model import Cube
from solvers.kociemba import KociembaSolver

# Create and scramble a cube
cube = Cube(3)
cube.scramble(20)

# Solve the cube
solver = KociembaSolver(cube)
solution = solver.solve()

# Apply the solution
solver.apply_solution()

# Get the solution steps
steps = solver.get_solution_steps()
for step_name, moves in steps:
    print(f"{step_name}: {moves}")
```

### 3D Visualization

```python
from cube.model import Cube
from visualization.renderer import render_cube_3d, animate_cube_3d

# Create and scramble a cube
cube = Cube(3)
cube.scramble(10)

# Render the cube in 3D
render_cube_3d(cube)

# Animate a sequence of moves
moves = ["R", "U", "R'", "U'", "R'", "F", "R", "F'"]
animate_cube_3d(cube, moves)
```

## Implementation Details

The core of the implementation is a flexible cube representation that scales to different cube sizes. The solver algorithms are designed to work with this representation, with optimizations for specific cube sizes where appropriate.

The project includes multiple solving approaches, from advanced algorithms like Kociemba's two-phase algorithm, Thistlethwaite's algorithm, and IDA* with pattern databases.

## Extending the Library

### Creating a Custom Solver

See `examples/custom_solver.py` for a template on how to create your own solver by extending the `BaseSolver` class.

## Future Work

- Implement more advanced solving algorithms
- Optimize for larger cube sizes (5x5 and beyond)
- Improve 3D visualization with more interactive features
- Develop a web interface for the solver

## License

This project is licensed under the MIT License - see the LICENSE file for details.