"""Example of how to implement a custom heuristic for solving the Rubik's Cube."""

import sys
import os
import random
import time

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cube.model import Cube, Face, Color
from cube.visualization import visualize_cube
from solvers.base_solver import BaseSolver


class HeuristicSolver(BaseSolver):
    """A solver that uses a heuristic to guide the search for a solution.
    
    This solver uses the A* search algorithm with a custom heuristic to find a solution.
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
        self.visited_states = set()
    
    def solve(self):
        """Solve the cube using the A* search algorithm.
        
        Returns:
            A list of moves that solve the cube.
        """
        # Reset the solution
        self.solution = []
        self.solution_steps = []
        self.visited_states = set()
        
        # Make a copy of the cube to work with
        cube = self.cube.copy()
        
        # If the cube is already solved, return an empty solution
        if cube.is_solved():
            return []
        
        # Initialize the search
        start_state = (cube.get_state_string(), [])
        self.visited_states.add(start_state[0])
        
        # Initialize the priority queue with the start state
        # The priority is the heuristic value of the state
        queue = [(self._heuristic(cube), start_state)]
        
        # Perform the A* search
        while queue:
            # Get the state with the lowest priority
            _, (state_string, moves) = min(queue)
            queue.remove((self._heuristic(cube), (state_string, moves)))
            
            # If we've reached the maximum depth, skip this state
            if len(moves) >= self.max_depth:
                continue
            
            # Restore the cube to this state
            cube.reset()
            for move in moves:
                cube.apply_move(move)
            
            # Try each possible move
            for move in self._get_possible_moves(moves):
                # Apply the move
                cube.apply_move(move)
                
                # Check if the cube is solved
                if cube.is_solved():
                    # We found a solution!
                    self.solution = moves + [move]
                    self.solution_steps = [("A* Search", self.solution)]
                    return self.solution
                
                # Get the new state
                new_state_string = cube.get_state_string()
                
                # If we haven't visited this state before, add it to the queue
                if new_state_string not in self.visited_states:
                    self.visited_states.add(new_state_string)
                    new_moves = moves + [move]
                    new_state = (new_state_string, new_moves)
                    new_priority = len(new_moves) + self._heuristic(cube)
                    queue.append((new_priority, new_state))
                
                # Undo the move
                cube.apply_move(self._get_inverse_move(move))
        
        # If we get here, we couldn't find a solution
        return []
    
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
        # Count the number of misplaced cubies
        misplaced_cubies = 0
        
        # Check each cubie
        for position, cubie in cube.cubies.items():
            # Get the colors of the cubie
            colors = cubie.colors
            
            # Check if the cubie is in the correct position
            if not self._is_cubie_in_correct_position(position, colors):
                misplaced_cubies += 1
        
        return misplaced_cubies
    
    def _is_cubie_in_correct_position(self, position, colors):
        """Check if a cubie is in the correct position.
        
        Args:
            position: The position of the cubie.
            colors: The colors of the cubie.
            
        Returns:
            True if the cubie is in the correct position, False otherwise.
        """
        # In a real implementation, this would check if the cubie is in the correct position
        # For demonstration purposes, we'll just return a random boolean
        return random.choice([True, False])
    
    def _get_possible_moves(self, moves):
        """Get the possible moves to try from the current state.
        
        To reduce the search space, we can apply some heuristics to eliminate moves
        that are unlikely to lead to a solution.
        
        Args:
            moves: The moves that have been applied so far.
            
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
        if not moves:
            return all_moves
        
        # Get the last move
        last_move = moves[-1]
        
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


class PatternDatabaseSolver(BaseSolver):
    """A solver that uses pattern databases to guide the search for a solution.
    
    Pattern databases are precomputed tables that store the exact distance from
    any state to the goal state for a subset of the puzzle. By using multiple
    pattern databases that cover disjoint sets of pieces, we can get a more
    accurate heuristic.
    """
    
    def __init__(self, cube):
        """Initialize the solver.
        
        Args:
            cube: The cube to solve.
        """
        super().__init__(cube)
        self.solution = []
        self.solution_steps = []
        
        # Initialize the pattern databases
        self._initialize_pattern_databases()
    
    def _initialize_pattern_databases(self):
        """Initialize the pattern databases.
        
        In a real implementation, this would load precomputed pattern databases
        from disk or compute them on the fly.
        """
        # For demonstration purposes, we'll just create empty dictionaries
        self.corner_database = {}
        self.edge_database = {}
    
    def solve(self):
        """Solve the cube using pattern databases.
        
        Returns:
            A list of moves that solve the cube.
        """
        # Reset the solution
        self.solution = []
        self.solution_steps = []
        
        # Make a copy of the cube to work with
        cube = self.cube.copy()
        
        # If the cube is already solved, return an empty solution
        if cube.is_solved():
            return []
        
        # In a real implementation, this would use the pattern databases
        # to guide the search for a solution
        # For demonstration purposes, we'll just return a placeholder
        self.solution = ["U", "R", "U'", "R'"]
        self.solution_steps = [("Pattern Database Search", self.solution)]
        
        return self.solution
    
    def get_solution_steps(self):
        """Get the solution steps.
        
        Returns:
            A list of tuples (step_name, moves) representing the solution steps.
        """
        return self.solution_steps


def main():
    """Demonstrate the custom heuristics."""
    # Create a cube
    cube = Cube(3)
    
    # Scramble the cube
    scramble_moves = cube.scramble(5)  # Use a short scramble for demonstration
    print(f"Scrambled the cube with moves: {scramble_moves}")
    
    # Visualize the scrambled cube
    visualize_cube(cube)
    
    # Create a heuristic solver
    heuristic_solver = HeuristicSolver(cube, max_depth=10)
    
    # Solve the cube
    print("\nSolving the cube using the heuristic solver...")
    start_time = time.time()
    heuristic_solution = heuristic_solver.solve()
    end_time = time.time()
    
    # Print the solution
    print(f"Solution found in {end_time - start_time:.2f} seconds")
    print(f"Solution length: {len(heuristic_solution)} moves")
    print(f"Solution: {heuristic_solution}")
    
    # Apply the solution
    is_solved = heuristic_solver.apply_solution()
    print(f"\nCube is solved: {is_solved}")
    
    # Visualize the solved cube
    visualize_cube(cube)
    
    # Create a pattern database solver
    pattern_db_solver = PatternDatabaseSolver(cube)
    
    # Scramble the cube again
    cube.reset()
    scramble_moves = cube.scramble(5)  # Use a short scramble for demonstration
    print(f"\nScrambled the cube with moves: {scramble_moves}")
    
    # Visualize the scrambled cube
    visualize_cube(cube)
    
    # Solve the cube
    print("\nSolving the cube using the pattern database solver...")
    start_time = time.time()
    pattern_db_solution = pattern_db_solver.solve()
    end_time = time.time()
    
    # Print the solution
    print(f"Solution found in {end_time - start_time:.2f} seconds")
    print(f"Solution length: {len(pattern_db_solution)} moves")
    print(f"Solution: {pattern_db_solution}")
    
    # Apply the solution
    is_solved = pattern_db_solver.apply_solution()
    print(f"\nCube is solved: {is_solved}")
    
    # Visualize the solved cube
    visualize_cube(cube)


if __name__ == "__main__":
    main()