# Scalable Rubik's Cube Solver

This project implements a scalable algorithm for solving Rubik's Cubes of various sizes (2x2, 3x3, and 4x4), with a focus on NxN scalability. The implementation balances time and space complexity while providing an intuitive solution inspired by human problem-solving approaches.

The library provides comprehensive tools for simulating, visualizing, and solving Rubik's Cubes with support for different solving algorithms, 3D visualization, and machine learning integration.

## Project Structure

- `cube/` - Core cube representation and operations
  - `__init__.py` - Package initialization
  - `model.py` - Data structures for cube representation
  - `moves.py` - Move engine supporting various turns and rotations
  - `visualization.py` - Visual representation of the cube

- `solvers/` - Implementation of solving algorithms
  - `__init__.py` - Package initialization
  - `base_solver.py` - Base solver interface
  - `layer_by_layer.py` - Layer-by-layer solving approach
  - `kociemba.py` - Two-phase algorithm implementation
  - `reduction.py` - 4x4 reduction method
  - `supercube.py` - Solver for supercubes (where center orientation matters)

- `visualization/` - 3D visualization tools
  - `__init__.py` - Package initialization
  - `renderer.py` - 3D cube renderer

- `ml/` - Machine learning integration
  - `__init__.py` - Package initialization
  - `predictor.py` - ML model for predicting optimal moves

- `examples/` - Example usage and demonstrations
  - `__init__.py` - Package initialization
  - `demo.py` - Main demonstration
  - `custom_solver.py` - Custom solver example
  - `custom_visualization.py` - Custom visualization
  - `custom_predictor.py` - Custom ML predictor
  - `custom_cube.py` - Custom cube variants
  - `custom_algorithm.py` - Custom algorithm steps
  - `benchmark.py` - Performance benchmarking
  - `custom_heuristic.py` - Custom heuristics
  - `ida_star_solver.py` - IDA* implementation
  - `thistlethwaite_solver.py` - Thistlethwaite algorithm

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
  - Layer-by-Layer (beginner method)
  - Kociemba's Two-Phase Algorithm
  - Reduction Method (for 4x4)
  - Thistlethwaite's Algorithm
  - IDA* with pattern databases
- **Visualization**:
  - 2D cube representation
  - 3D rendering with matplotlib
  - Animation of move sequences
  - Interactive 3D visualization with ipywidgets
- **Supercube Support**: Handles supercubes where center orientation matters
- **Machine Learning Integration**:
  - Random move predictor
  - Heuristic-based predictor
  - Deep learning predictor (placeholder)
  - Reinforcement learning predictor (placeholder)
- **Benchmarking Tools**: Compare performance of different solving algorithms and predictors

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

## Usage Examples

### Basic Cube Operations

```python
from cube.model import Cube
from cube.visualization import visualize_cube

# Create a 3x3 cube
cube = Cube(3)

# Apply some moves
cube.apply_move("R")
cube.apply_move("U")
cube.apply_move("R'")

# Visualize the cube
visualize_cube(cube)

# Check if the cube is solved
print(f"Cube is solved: {cube.is_solved()}")

# Scramble the cube
scramble_moves = cube.scramble(20)
print(f"Scrambled with moves: {scramble_moves}")
```

### Solving a Cube

```python
from cube.model import Cube
from solvers.layer_by_layer import LayerByLayerSolver

# Create and scramble a cube
cube = Cube(3)
cube.scramble(20)

# Solve the cube
solver = LayerByLayerSolver(cube)
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

### Using Machine Learning Predictors

```python
from cube.model import Cube
from ml.predictor import HeuristicPredictor

# Create and scramble a cube
cube = Cube(3)
cube.scramble(5)

# Create a predictor
predictor = HeuristicPredictor()

# Get the next best move
best_move = predictor.predict_move(cube)
print(f"Best move: {best_move}")

# Apply the move
cube.apply_move(best_move)
```

## Implementation Details

The core of the implementation is a flexible cube representation that scales to different cube sizes. The solver algorithms are designed to work with this representation, with optimizations for specific cube sizes where appropriate.

The project includes multiple solving approaches, from beginner-friendly layer-by-layer methods to more advanced algorithms like Kociemba's two-phase algorithm, Thistlethwaite's algorithm, and IDA* with pattern databases.

## Extending the Library

### Creating a Custom Solver

See `examples/custom_solver.py` for a template on how to create your own solver by extending the `BaseSolver` class.

### Creating Custom Visualizations

See `examples/custom_visualization.py` for examples of creating custom visualization methods.

### Implementing Custom Predictors

See `examples/custom_predictor.py` for examples of implementing custom move prediction algorithms.

## Future Work

- Implement more advanced solving algorithms
- Optimize for larger cube sizes (5x5 and beyond)
- Enhance the machine learning models for better move prediction
- Add support for additional cube types and puzzles
- Improve 3D visualization with more interactive features
- Develop a web interface for the solver

## License

This project is licensed under the MIT License - see the LICENSE file for details.