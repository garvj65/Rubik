"""Real-time 3D Rubik's Cube solver with interactive visualization."""

import sys
import os
import time
import threading
from typing import List, Optional

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cube.model import Cube
from solvers.layer_by_layer import LayerByLayerSolver
from solvers.kociemba import KociembaSolver
from visualization.renderer import render_cube_3d
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np


class RealTime3DSolver:
    """Real-time 3D Rubik's Cube solver with live visualization."""
    
    def __init__(self, cube_size: int = 3):
        """Initialize the real-time solver.
        
        Args:
            cube_size: Size of the cube (default 3x3x3)
        """
        self.cube = Cube(cube_size)
        self.solver = LayerByLayerSolver()
        self.kociemba_solver = KociembaSolver()
        self.solution_moves = []
        self.current_move_index = 0
        self.is_solving = False
        self.solve_speed = 1.0  # moves per second
        
        # Visualization setup
        self.fig = None
        self.ax = None
        self.animation = None
        
    def scramble_cube(self, num_moves: int = 20) -> List[str]:
        """Scramble the cube with random moves.
        
        Args:
            num_moves: Number of random moves to apply
            
        Returns:
            List of moves used for scrambling
        """
        scramble_moves = self.cube.scramble(num_moves)
        print(f"Scrambled cube with moves: {' '.join(scramble_moves)}")
        return scramble_moves
    
    def solve_cube(self, algorithm: str = "layer_by_layer") -> List[str]:
        """Solve the cube and return the solution moves.
        
        Args:
            algorithm: Solving algorithm to use ('layer_by_layer' or 'kociemba')
            
        Returns:
            List of moves to solve the cube
        """
        print(f"Solving cube using {algorithm} algorithm...")
        
        if algorithm == "kociemba":
            try:
                solution = self.kociemba_solver.solve(self.cube)
            except Exception as e:
                print(f"Kociemba solver failed: {e}. Falling back to layer-by-layer.")
                solution = self.solver.solve(self.cube)
        else:
            solution = self.solver.solve(self.cube)
        
        if solution:
            print(f"Solution found: {' '.join(solution)} ({len(solution)} moves)")
            self.solution_moves = solution
            self.current_move_index = 0
            return solution
        else:
            print("No solution found!")
            return []
    
    def setup_3d_visualization(self):
        """Setup the 3D matplotlib visualization."""
        self.fig = plt.figure(figsize=(12, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_title("Real-time 3D Rubik's Cube Solver", fontsize=16)
        
        # Add control buttons
        plt.subplots_adjust(bottom=0.2)
        
        # Initial render
        self.render_current_state()
        
    def render_current_state(self):
        """Render the current state of the cube."""
        if self.ax is None:
            return
            
        self.ax.clear()
        self.ax.set_title("Real-time 3D Rubik's Cube Solver", fontsize=16)
        
        # Render the cube using the existing renderer
        try:
            render_cube_3d(self.cube, ax=self.ax)
        except Exception as e:
            print(f"Rendering error: {e}")
            # Fallback simple visualization
            self._render_simple_cube()
        
        # Add status text
        status_text = f"Solved: {self.cube.is_solved()}\n"
        if self.solution_moves:
            status_text += f"Solution: {len(self.solution_moves)} moves\n"
            status_text += f"Progress: {self.current_move_index}/{len(self.solution_moves)}"
        
        self.ax.text2D(0.02, 0.98, status_text, transform=self.ax.transAxes, 
                      verticalalignment='top', fontsize=10,
                      bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        plt.draw()
    
    def _render_simple_cube(self):
        """Simple fallback cube visualization."""
        # Draw a simple wireframe cube
        size = self.cube.size
        
        # Define cube vertices
        vertices = np.array([
            [0, 0, 0], [size, 0, 0], [size, size, 0], [0, size, 0],  # bottom face
            [0, 0, size], [size, 0, size], [size, size, size], [0, size, size]  # top face
        ])
        
        # Define edges
        edges = [
            [0, 1], [1, 2], [2, 3], [3, 0],  # bottom face
            [4, 5], [5, 6], [6, 7], [7, 4],  # top face
            [0, 4], [1, 5], [2, 6], [3, 7]   # vertical edges
        ]
        
        # Draw edges
        for edge in edges:
            points = vertices[edge]
            self.ax.plot3D(*points.T, 'b-', linewidth=2)
        
        # Set equal aspect ratio
        self.ax.set_xlim([0, size])
        self.ax.set_ylim([0, size])
        self.ax.set_zlim([0, size])
    
    def animate_solution(self, interval: int = 1000):
        """Animate the solution step by step.
        
        Args:
            interval: Time between moves in milliseconds
        """
        if not self.solution_moves:
            print("No solution to animate!")
            return
        
        def update_frame(frame):
            if self.current_move_index < len(self.solution_moves):
                move = self.solution_moves[self.current_move_index]
                print(f"Applying move {self.current_move_index + 1}/{len(self.solution_moves)}: {move}")
                
                self.cube.apply_move(move)
                self.current_move_index += 1
                
                self.render_current_state()
                
                if self.current_move_index >= len(self.solution_moves):
                    print("Solution complete!")
                    self.is_solving = False
            
            return []
        
        self.is_solving = True
        self.animation = FuncAnimation(self.fig, update_frame, 
                                     frames=len(self.solution_moves),
                                     interval=interval, repeat=False)
    
    def interactive_solve(self):
        """Run an interactive solving session."""
        print("=== Real-time 3D Rubik's Cube Solver ===")
        print("Commands:")
        print("  's' - Scramble cube")
        print("  'solve' - Solve with layer-by-layer")
        print("  'kociemba' - Solve with Kociemba algorithm")
        print("  'animate' - Animate current solution")
        print("  'reset' - Reset cube to solved state")
        print("  'show' - Show current 3D visualization")
        print("  'q' - Quit")
        print()
        
        # Setup visualization
        self.setup_3d_visualization()
        
        while True:
            command = input("Enter command: ").strip().lower()
            
            if command == 'q':
                break
            elif command == 's':
                self.scramble_cube()
                self.render_current_state()
            elif command == 'solve':
                self.solve_cube("layer_by_layer")
            elif command == 'kociemba':
                self.solve_cube("kociemba")
            elif command == 'animate':
                if self.solution_moves:
                    self.animate_solution()
                    plt.show()
                else:
                    print("No solution to animate. Solve the cube first.")
            elif command == 'reset':
                self.cube.reset()
                self.solution_moves = []
                self.current_move_index = 0
                self.render_current_state()
                print("Cube reset to solved state.")
            elif command == 'show':
                self.render_current_state()
                plt.show(block=False)
            else:
                print("Unknown command. Try 's', 'solve', 'animate', 'reset', 'show', or 'q'.")
    
    def auto_solve_demo(self):
        """Demonstrate automatic solving with real-time visualization."""
        print("=== Automatic Solving Demo ===")
        
        # Setup visualization
        self.setup_3d_visualization()
        
        # Scramble
        print("Scrambling cube...")
        self.scramble_cube(15)
        self.render_current_state()
        plt.show(block=False)
        plt.pause(2)
        
        # Solve
        print("Finding solution...")
        self.solve_cube("layer_by_layer")
        plt.pause(1)
        
        # Animate solution
        print("Animating solution...")
        self.animate_solution(interval=800)
        plt.show()


def main():
    """Main function to run the real-time 3D solver."""
    try:
        solver = RealTime3DSolver()
        
        print("Choose mode:")
        print("1. Interactive mode")
        print("2. Auto-solve demo")
        
        choice = input("Enter choice (1 or 2): ").strip()
        
        if choice == "1":
            solver.interactive_solve()
        elif choice == "2":
            solver.auto_solve_demo()
        else:
            print("Invalid choice. Running interactive mode.")
            solver.interactive_solve()
            
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()