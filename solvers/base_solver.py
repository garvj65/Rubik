"""Base solver interface for Rubik's Cube solving algorithms."""

from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Optional, Set
from cube.model import Cube, Face, Color


class BaseSolver(ABC):
    """Abstract base class for Rubik's Cube solvers.
    
    This class defines the interface that all solvers must implement.
    Different solving algorithms can inherit from this class and provide
    their own implementation of the solve method.
    """
    
    def __init__(self, cube: Cube):
        """Initialize the solver with a cube.
        
        Args:
            cube: The cube to solve
        """
        self.cube = cube.copy()  # Work with a copy to avoid modifying the original
        self.original_cube = cube  # Keep a reference to the original cube
        self.solution = []  # List to store the solution moves
    
    @abstractmethod
    def solve(self) -> List[str]:
        """Solve the cube and return the solution moves.
        
        Returns:
            A list of moves that solve the cube
        """
        pass
    
    def apply_solution(self) -> bool:
        """Apply the solution to the original cube.
        
        Returns:
            True if the solution successfully solved the cube, False otherwise
        """
        # Apply the solution to the original cube
        for move in self.solution:
            self.original_cube.apply_move(move)
        
        # Check if the cube is solved
        return self.original_cube.is_solved()
    
    def get_solution_length(self) -> int:
        """Get the length of the solution.
        
        Returns:
            The number of moves in the solution
        """
        return len(self.solution)
    
    def optimize_solution(self) -> List[str]:
        """Optimize the solution by removing redundant moves.
        
        Returns:
            The optimized solution
        """
        # This is a simple optimization that removes obvious redundancies
        # More advanced optimizations could be implemented in subclasses
        
        if not self.solution:
            return []
        
        # Define move cancellations
        cancellations = {
            'U': {'U': 'U2', 'U2': "U'", "U'": ''},
            'D': {'D': 'D2', 'D2': "D'", "D'": ''},
            'L': {'L': 'L2', 'L2': "L'", "L'": ''},
            'R': {'R': 'R2', 'R2': "R'", "R'": ''},
            'F': {'F': 'F2', 'F2': "F'", "F'": ''},
            'B': {'B': 'B2', 'B2': "B'", "B'": ''},
        }
        
        # Apply cancellations
        optimized = []
        for move in self.solution:
            base_move = move[0]  # Get the face letter
            
            if not optimized or base_move != optimized[-1][0]:
                # Different face, just add the move
                optimized.append(move)
            else:
                # Same face, check for cancellation
                last_move = optimized.pop()
                combined = cancellations.get(base_move, {}).get(last_move, None)
                
                if combined:
                    if combined != '':
                        optimized.append(combined)
                else:
                    # No cancellation rule, add both moves back
                    optimized.append(last_move)
                    optimized.append(move)
        
        self.solution = optimized
        return optimized
    
    def reset(self):
        """Reset the solver to its initial state."""
        self.cube = self.original_cube.copy()
        self.solution = []
    
    def add_move(self, move: str):
        """Add a move to the solution and apply it to the cube.
        
        Args:
            move: The move to add
        """
        self.solution.append(move)
        self.cube.apply_move(move)
    
    def add_moves(self, moves: List[str]):
        """Add multiple moves to the solution and apply them to the cube.
        
        Args:
            moves: The moves to add
        """
        for move in moves:
            self.add_move(move)
    
    def get_solution_steps(self) -> List[Tuple[str, List[str]]]:
        """Get the solution as a list of named steps with their moves.
        
        This method should be overridden by subclasses to provide a more
        meaningful breakdown of the solution steps.
        
        Returns:
            A list of (step_name, moves) tuples
        """
        return [("Complete Solution", self.solution)]