"""Demonstration of the Rubik's Cube solver."""

import sys
import os
import random
import time
import matplotlib.pyplot as plt

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cube.model import Cube, Face, Color
from cube.visualization import visualize_cube, visualize_move_sequence, print_cube
from visualization.renderer import render_cube_3d, animate_cube_3d
from solvers.layer_by_layer import LayerByLayerSolver
from solvers.kociemba import KociembaSolver
from solvers.reduction import ReductionSolver
from solvers.supercube import SupercubeSolver
from ml.predictor import RandomPredictor, HeuristicPredictor


def demo_cube_creation():
    """Demonstrate creating cubes of different sizes."""
    print("\n=== Cube Creation ===\n")
    
    # Create a 2x2 cube
    cube2 = Cube(2)
    print("Created a 2x2 cube")
    
    # Create a 3x3 cube
    cube3 = Cube(3)
    print("Created a 3x3 cube")
    
    # Create a 4x4 cube
    cube4 = Cube(4)
    print("Created a 4x4 cube")
    
    return cube2, cube3, cube4


def demo_cube_visualization(cube2, cube3, cube4):
    """Demonstrate visualizing cubes of different sizes."""
    print("\n=== Cube Visualization ===\n")
    
    # Visualize the 2x2 cube
    print("Visualizing a 2x2 cube")
    visualize_cube(cube2)
    
    # Visualize the 3x3 cube
    print("Visualizing a 3x3 cube")
    visualize_cube(cube3)
    
    # Visualize the 4x4 cube
    print("Visualizing a 4x4 cube")
    visualize_cube(cube4)
    
    # 3D visualization
    print("\n3D visualization of a 3x3 cube")
    render_cube_3d(cube3)


def demo_cube_moves(cube3):
    """Demonstrate applying moves to a cube."""
    print("\n=== Cube Moves ===\n")
    
    # Make a copy of the cube
    cube = cube3.copy()
    
    # Apply some moves
    moves = ["U", "R", "F", "L", "B", "D"]
    print(f"Applying moves: {moves}")
    
    # Visualize the move sequence
    visualize_move_sequence(cube, moves, delay=0.5)
    
    # Apply some more complex moves
    complex_moves = ["U2", "R'", "F2", "L'", "B2", "D'"]
    print(f"Applying complex moves: {complex_moves}")
    
    # Visualize the move sequence
    visualize_move_sequence(cube, complex_moves, delay=0.5)
    
    # Reset the cube
    cube.reset()
    print("Reset the cube to its solved state")
    
    # Scramble the cube
    scramble_moves = cube.scramble(20)
    print(f"Scrambled the cube with moves: {scramble_moves}")
    
    # Visualize the scrambled cube
    visualize_cube(cube)
    
    return cube


def demo_layer_by_layer_solver(cube):
    """Demonstrate the layer-by-layer solver."""
    print("\n=== Layer-by-Layer Solver ===\n")
    
    # Make a copy of the cube
    cube_copy = cube.copy()
    
    # Create a solver
    solver = LayerByLayerSolver(cube_copy)
    
    # Solve the cube
    print("Solving the cube using the layer-by-layer method...")
    start_time = time.time()
    solution = solver.solve()
    end_time = time.time()
    
    # Print the solution
    print(f"Solution found in {end_time - start_time:.2f} seconds")
    print(f"Solution length: {len(solution)} moves")
    print(f"Solution: {solution}")
    
    # Visualize the solution steps
    steps = solver.get_solution_steps()
    print(f"\nSolution steps:")
    for i, (step_name, moves) in enumerate(steps):
        print(f"Step {i+1}: {step_name} ({len(moves)} moves)")
    
    # Verify the solution
    is_solved = solver.apply_solution()
    print(f"\nCube is solved: {is_solved}")
    
    # Visualize the solved cube
    visualize_cube(cube_copy)
    
    return solution


def demo_kociemba_solver(cube):
    """Demonstrate the Kociemba solver."""
    print("\n=== Kociemba Solver ===\n")
    
    # Make a copy of the cube
    cube_copy = cube.copy()
    
    # Create a solver
    solver = KociembaSolver(cube_copy)
    
    # Solve the cube
    print("Solving the cube using Kociemba's two-phase algorithm...")
    start_time = time.time()
    solution = solver.solve()
    end_time = time.time()
    
    # Print the solution
    print(f"Solution found in {end_time - start_time:.2f} seconds")
    print(f"Solution length: {len(solution)} moves")
    print(f"Solution: {solution}")
    
    # Visualize the solution steps
    steps = solver.get_solution_steps()
    print(f"\nSolution steps:")
    for i, (step_name, moves) in enumerate(steps):
        print(f"Step {i+1}: {step_name} ({len(moves)} moves)")
    
    # Verify the solution
    is_solved = solver.apply_solution()
    print(f"\nCube is solved: {is_solved}")
    
    # Visualize the solved cube
    visualize_cube(cube_copy)
    
    return solution


def demo_reduction_solver(cube4):
    """Demonstrate the reduction solver for 4x4 cubes."""
    print("\n=== Reduction Solver for 4x4 ===\n")
    
    # Make a copy of the cube
    cube_copy = cube4.copy()
    
    # Scramble the cube
    scramble_moves = cube_copy.scramble(20)
    print(f"Scrambled the 4x4 cube with moves: {scramble_moves}")
    
    # Visualize the scrambled cube
    visualize_cube(cube_copy)
    
    # Create a solver
    solver = ReductionSolver(cube_copy)
    
    # Solve the cube
    print("Solving the 4x4 cube using the reduction method...")
    start_time = time.time()
    solution = solver.solve()
    end_time = time.time()
    
    # Print the solution
    print(f"Solution found in {end_time - start_time:.2f} seconds")
    print(f"Solution length: {len(solution)} moves")
    print(f"Solution: {solution}")
    
    # Visualize the solution steps
    steps = solver.get_solution_steps()
    print(f"\nSolution steps:")
    for i, (step_name, moves) in enumerate(steps):
        print(f"Step {i+1}: {step_name} ({len(moves)} moves)")
    
    # Verify the solution
    is_solved = solver.apply_solution()
    print(f"\nCube is solved: {is_solved}")
    
    # Visualize the solved cube
    visualize_cube(cube_copy)
    
    return solution


def demo_supercube_solver(cube3):
    """Demonstrate the supercube solver."""
    print("\n=== Supercube Solver ===\n")
    
    # Make a copy of the cube
    cube_copy = cube3.copy()
    
    # Scramble the cube
    scramble_moves = cube_copy.scramble(20)
    print(f"Scrambled the cube with moves: {scramble_moves}")
    
    # Visualize the scrambled cube
    visualize_cube(cube_copy)
    
    # Create a solver
    solver = SupercubeSolver(cube_copy)
    
    # Solve the cube
    print("Solving the supercube...")
    start_time = time.time()
    solution = solver.solve()
    end_time = time.time()
    
    # Print the solution
    print(f"Solution found in {end_time - start_time:.2f} seconds")
    print(f"Solution length: {len(solution)} moves")
    print(f"Solution: {solution}")
    
    # Visualize the solution steps
    steps = solver.get_solution_steps()
    print(f"\nSolution steps:")
    for i, (step_name, moves) in enumerate(steps):
        print(f"Step {i+1}: {step_name} ({len(moves)} moves)")
    
    # Verify the solution
    is_solved = solver.apply_solution()
    print(f"\nCube is solved: {is_solved}")
    
    # Visualize the solved cube
    visualize_cube(cube_copy)
    
    return solution


def demo_ml_predictors(cube3):
    """Demonstrate the machine learning predictors."""
    print("\n=== Machine Learning Predictors ===\n")
    
    # Make a copy of the cube
    cube_copy = cube3.copy()
    
    # Scramble the cube
    scramble_moves = cube_copy.scramble(5)  # Use a shorter scramble for demonstration
    print(f"Scrambled the cube with moves: {scramble_moves}")
    
    # Visualize the scrambled cube
    visualize_cube(cube_copy)
    
    # Create a random predictor
    random_predictor = RandomPredictor()
    
    # Predict some moves
    print("\nRandom Predictor:")
    random_moves = random_predictor.predict_moves(cube_copy, 5)
    print(f"Predicted moves: {random_moves}")
    
    # Create a heuristic predictor
    heuristic_predictor = HeuristicPredictor(lookahead=1)
    
    # Predict some moves
    print("\nHeuristic Predictor:")
    heuristic_moves = heuristic_predictor.predict_moves(cube_copy, 5)
    print(f"Predicted moves: {heuristic_moves}")
    
    # Apply the heuristic moves to the cube
    print("\nApplying heuristic moves to the cube...")
    for move in heuristic_moves:
        cube_copy.apply_move(move)
    
    # Visualize the cube after applying the moves
    visualize_cube(cube_copy)
    
    return heuristic_moves


def demo_3d_animation(cube3, moves):
    """Demonstrate 3D animation of moves."""
    print("\n=== 3D Animation ===\n")
    
    # Make a copy of the cube
    cube_copy = cube3.copy()
    
    # Animate the moves
    print(f"Animating moves: {moves}")
    animate_cube_3d(cube_copy, moves, delay=0.5)
    
    return cube_copy


def main():
    """Run the demonstration."""
    print("Rubik's Cube Solver Demonstration")
    
    # Create cubes of different sizes
    cube2, cube3, cube4 = demo_cube_creation()
    
    # Visualize the cubes
    demo_cube_visualization(cube2, cube3, cube4)
    
    # Demonstrate cube moves
    scrambled_cube = demo_cube_moves(cube3)
    
    # Demonstrate the layer-by-layer solver
    lbl_solution = demo_layer_by_layer_solver(scrambled_cube)
    
    # Demonstrate the Kociemba solver
    kociemba_solution = demo_kociemba_solver(scrambled_cube)
    
    # Demonstrate the reduction solver for 4x4 cubes
    reduction_solution = demo_reduction_solver(cube4)
    
    # Demonstrate the supercube solver
    supercube_solution = demo_supercube_solver(cube3)
    
    # Demonstrate the machine learning predictors
    ml_moves = demo_ml_predictors(cube3)
    
    # Demonstrate 3D animation
    demo_3d_animation(cube3, ml_moves)
    
    print("\nDemonstration complete!")


if __name__ == "__main__":
    main()