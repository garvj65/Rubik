"""Example of how to implement a Rubik's Cube solver using the IDA* algorithm."""

import sys
import os
import time

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cube.model import Cube
from cube.visualization import visualize_cube
from solvers.base_solver import BaseSolver


class IDAStarSolver(BaseSolver):
    """A solver that uses the IDA* algorithm to find a solution.
    
    IDA* (Iterative Deepening A*) is a graph traversal and path search algorithm
    that can find the shortest path between a starting node and a goal node.
    It uses a depth-first search with a heuristic function to guide the search.
    """
    
    def __init__(self, cube, max_depth=20):
        """Initialize the solver.
        
        Args:
            cube: The cube to solve.
            max_depth: The maximum depth to search to.
        """
        super().__init__(cube)
        self.max_depth = max_depth
        self.solution = []
        self.solution_steps = []
        self.nodes_expanded = 0
    
    def solve(self):
        """Solve the cube using the IDA* algorithm.
        
        Returns:
            A list of moves that solve the cube.
        """
        # Reset the solution
        self.solution = []
        self.solution_steps = []
        self.nodes_expanded = 0
        
        # Make a copy of the cube to work with
        cube = self.cube.copy()
        
        # If the cube is already solved, return an empty solution
        if cube.is_solved():
            return []
        
        # Initialize the search
        bound = self._heuristic(cube)
        path = []
        
        # Perform the IDA* search
        while True:
            print(f"Searching with bound {bound}...")
            t = self._search(cube, path, 0, bound)
            if t == True:
                # We found a solution!
                self.solution = path.copy()
                self.solution_steps = [("IDA* Search", self.solution)]
                print(f"Nodes expanded: {self.nodes_expanded}")
                return self.solution
            if t == float('inf'):
                # No solution found within the bound
                print(f"No solution found within depth {self.max_depth}")
                return []
            bound = t
    
    def _search(self, cube, path, g, bound):
        """Perform a depth-first search with a heuristic function.
        
        Args:
            cube: The cube to search from.
            path: The path of moves taken so far.
            g: The cost of the path so far.
            bound: The current bound for the search.
            
        Returns:
            True if a solution is found, float('inf') if no solution is found within the bound,
            or the new bound to use for the next iteration.
        """
        self.nodes_expanded += 1
        
        # Calculate the heuristic value
        h = self._heuristic(cube)
        
        # Calculate the total cost
        f = g + h
        
        # If the total cost exceeds the bound, return the total cost as the new bound
        if f > bound:
            return f
        
        # If the cube is solved, return True
        if cube.is_solved():
            return True
        
        # If we've reached the maximum depth, return infinity
        if g >= self.max_depth:
            return float('inf')
        
        min_cost = float('inf')
        
        # Try each possible move
        for move in self._get_possible_moves(path):
            # Apply the move
            cube.apply_move(move)
            
            # Add the move to the path
            path.append(move)
            
            # Recursively search from this new state
            t = self._search(cube, path, g + 1, bound)
            
            # If a solution is found, return True
            if t == True:
                return True
            
            # Update the minimum cost
            min_cost = min(min_cost, t)
            
            # Remove the move from the path
            path.pop()
            
            # Undo the move
            cube.apply_move(self._get_inverse_move(move))
        
        return min_cost
    
    def _heuristic(self, cube):
        """Calculate a heuristic value for the cube.
        
        The heuristic is an estimate of how far the cube is from being solved.
        A good heuristic is admissible (never overestimates the distance to the goal)
        and consistent (satisfies the triangle inequality).
        
        Args:
            cube: The cube to calculate the heuristic for.
            
        Returns:
            A heuristic value for the cube.
        """
        # For demonstration purposes, we'll use a simple heuristic
        # that counts the number of misplaced stickers
        misplaced_stickers = 0
        
        # Check each face
        for face in cube.faces:
            # Get the center color of the face
            center_color = cube.get_face_center_color(face)
            
            # Get the cubies on the face
            cubies = cube.get_face_cubies(face)
            
            # Check each cubie
            for i in range(cube.size):
                for j in range(cube.size):
                    # Get the color of the cubie on this face
                    color = cubies[i][j].get_face_color(face)
                    
                    # If the color doesn't match the center color, it's misplaced
                    if color != center_color:
                        misplaced_stickers += 1
        
        # Divide by 8 to get a more reasonable estimate
        # (this is a common heuristic for Rubik's Cube)
        return misplaced_stickers // 8
    
    def _get_possible_moves(self, path):
        """Get the possible moves to try from the current state.
        
        To reduce the search space, we can apply some heuristics to eliminate moves
        that are unlikely to lead to a solution.
        
        Args:
            path: The path of moves taken so far.
            
        Returns:
            A list of possible moves to try.
        """
        # All possible moves
        all_moves = [
            "U", "U'", "U2",
            "D", "D'", "D2",
            "L", "L'", "L2",
            "R", "R'", "R2",
            "F", "F'", "F2",
            "B", "B'", "B2",
        ]
        
        # If there are no moves yet, return all possible moves
        if not path:
            return all_moves
        
        # Get the last move
        last_move = path[-1]
        
        # Don't apply the inverse of the last move
        inverse_last_move = self._get_inverse_move(last_move)
        
        # Don't apply a move on the same face as the last move
        last_face = last_move[0]
        
        # Filter the moves
        filtered_moves = [move for move in all_moves 
                         if move != inverse_last_move and move[0] != last_face]
        
        return filtered_moves
    
    def _get_inverse_move(self, move):
        """Get the inverse of a move.
        
        Args:
            move: The move to get the inverse of.
            
        Returns:
            The inverse of the move.
        """
        # Handle the case where the move is a double move (e.g., "U2")
        if len(move) == 2 and move[1] == "2":
            return move  # The inverse of a double move is the same move
        
        # Handle the case where the move is a counterclockwise move (e.g., "U'")
        if len(move) == 2 and move[1] == "'":
            return move[0]  # The inverse of a counterclockwise move is a clockwise move
        
        # Handle the case where the move is a clockwise move (e.g., "U")
        return move + "'"  # The inverse of a clockwise move is a counterclockwise move
    
    def get_solution_steps(self):
        """Get the solution steps.
        
        Returns:
            A list of tuples (step_name, moves) representing the solution steps.
        """
        return self.solution_steps


def main():
    """Demonstrate the IDA* solver."""
    # Create a cube
    cube = Cube(3)
    
    # Scramble the cube
    scramble_moves = cube.scramble(5)  # Use a short scramble for demonstration
    print(f"Scrambled the cube with moves: {scramble_moves}")
    
    # Visualize the scrambled cube
    visualize_cube(cube)
    
    # Create an IDA* solver
    ida_star_solver = IDAStarSolver(cube, max_depth=10)
    
    # Solve the cube
    print("\nSolving the cube using the IDA* algorithm...")
    start_time = time.time()
    solution = ida_star_solver.solve()
    end_time = time.time()
    
    # Print the solution
    print(f"Solution found in {end_time - start_time:.2f} seconds")
    print(f"Solution length: {len(solution)} moves")
    print(f"Solution: {solution}")
    
    # Apply the solution
    is_solved = ida_star_solver.apply_solution()
    print(f"\nCube is solved: {is_solved}")
    
    # Visualize the solved cube
    visualize_cube(cube)


if __name__ == "__main__":
    main()