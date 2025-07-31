"""Example of how to benchmark different solving algorithms."""

import sys
import os
import time
import random
import matplotlib.pyplot as plt
import numpy as np

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cube.model import Cube
from solvers.kociemba import KociembaSolver


def benchmark_solvers(cube_size=3, num_scrambles=10, scramble_lengths=[5, 10, 15, 20]):
    """Benchmark different solvers on cubes with different scramble lengths.
    
    Args:
        cube_size: The size of the cube to benchmark.
        num_scrambles: The number of scrambles to test for each scramble length.
        scramble_lengths: The lengths of scrambles to test.
        
    Returns:
        A dictionary of results, where the keys are solver names and the values are
        dictionaries with keys 'times', 'solution_lengths', and 'success_rates'.
    """
    # Create the solvers to benchmark
    solvers = {
        "Kociemba": lambda cube: KociembaSolver(cube),
    }
    
    # Initialize the results dictionary
    results = {}
    for solver_name in solvers:
        results[solver_name] = {
            "times": [],
            "solution_lengths": [],
            "success_rates": [],
        }
    
    # Benchmark each solver on each scramble length
    for scramble_length in scramble_lengths:
        # Initialize the results for this scramble length
        for solver_name in solvers:
            results[solver_name]["times"].append([])
            results[solver_name]["solution_lengths"].append([])
            results[solver_name]["success_rates"].append(0)
        
        # Test each solver on multiple scrambles of this length
        for i in range(num_scrambles):
            # Create a cube
            cube = Cube(cube_size)
            
            # Scramble the cube
            scramble_moves = cube.scramble(scramble_length)
            
            # Test each solver
            for solver_name, solver_factory in solvers.items():
                # Make a copy of the cube for this solver
                cube_copy = cube.copy()
                
                # Create the solver
                solver = solver_factory(cube_copy)
                
                # Solve the cube and measure the time
                start_time = time.time()
                solution = solver.solve()
                end_time = time.time()
                
                # Record the results
                solve_time = end_time - start_time
                solution_length = len(solution)
                success = solver.apply_solution() and cube_copy.is_solved()
                
                # Add the results to the dictionary
                results[solver_name]["times"][-1].append(solve_time)
                results[solver_name]["solution_lengths"][-1].append(solution_length)
                if success:
                    results[solver_name]["success_rates"][-1] += 1
        
        # Calculate the average success rate for this scramble length
        for solver_name in solvers:
            results[solver_name]["success_rates"][-1] /= num_scrambles
    
    return results, scramble_lengths


def plot_benchmark_results(results, scramble_lengths):
    """Plot the benchmark results.
    
    Args:
        results: The benchmark results, as returned by benchmark_solvers.
        scramble_lengths: The lengths of scrambles that were tested.
    """
    # Create a figure with three subplots
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
    
    # Plot the average solve times
    for solver_name, solver_results in results.items():
        avg_times = [np.mean(times) for times in solver_results["times"]]
        ax1.plot(scramble_lengths, avg_times, marker='o', label=solver_name)
    
    ax1.set_xlabel("Scramble Length")
    ax1.set_ylabel("Average Solve Time (s)")
    ax1.set_title("Average Solve Time vs. Scramble Length")
    ax1.legend()
    ax1.grid(True)
    
    # Plot the average solution lengths
    for solver_name, solver_results in results.items():
        avg_solution_lengths = [np.mean(lengths) for lengths in solver_results["solution_lengths"]]
        ax2.plot(scramble_lengths, avg_solution_lengths, marker='o', label=solver_name)
    
    ax2.set_xlabel("Scramble Length")
    ax2.set_ylabel("Average Solution Length")
    ax2.set_title("Average Solution Length vs. Scramble Length")
    ax2.legend()
    ax2.grid(True)
    
    # Plot the success rates
    for solver_name, solver_results in results.items():
        ax3.plot(scramble_lengths, solver_results["success_rates"], marker='o', label=solver_name)
    
    ax3.set_xlabel("Scramble Length")
    ax3.set_ylabel("Success Rate")
    ax3.set_title("Success Rate vs. Scramble Length")
    ax3.legend()
    ax3.grid(True)
    
    # Adjust the layout and show the plot
    plt.tight_layout()
    plt.show()


def main():
    """Run the benchmarks."""
    # Benchmark the solvers
    print("Benchmarking solvers...")
    solver_results, scramble_lengths = benchmark_solvers(
        cube_size=3,
        num_scrambles=5,  # Use a small number for demonstration
        scramble_lengths=[5, 10, 15],  # Use a small range for demonstration
    )
    
    # Plot the solver benchmark results
    print("Plotting solver benchmark results...")
    plot_benchmark_results(solver_results, scramble_lengths)


if __name__ == "__main__":
    main()