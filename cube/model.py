"""Core data structures for representing Rubik's Cubes of various sizes."""

import random
import numpy as np
from enum import Enum
from typing import List, Tuple, Dict, Optional, Union


class Face(Enum):
    """Enum representing the six faces of a Rubik's Cube."""
    UP = 0
    RIGHT = 1
    FRONT = 2
    DOWN = 3
    LEFT = 4
    BACK = 5


class Color(Enum):
    """Enum representing the six colors of a Rubik's Cube."""
    WHITE = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    ORANGE = 4
    BLUE = 5


class Cubie:
    """Represents a single cubie (small cube) in the Rubik's Cube.
    
    A cubie can be a corner (3 faces), an edge (2 faces), a center (1 face),
    or an internal piece (0 faces, only present in cubes larger than 3x3).
    """
    def __init__(self, position: Tuple[int, int, int], size: int):
        """Initialize a cubie at the given position in a cube of the given size.
        
        Args:
            position: (x, y, z) coordinates where each coordinate is in range [0, size-1]
            size: Size of the cube (e.g., 3 for a 3x3x3 cube)
        """
        self.position = position
        self.size = size
        self.colors = {}
        self._init_colors()
    
    def _init_colors(self):
        """Initialize the colors of the cubie based on its position."""
        x, y, z = self.position
        max_idx = self.size - 1
        
        # Determine which faces this cubie has and assign colors
        if x == 0:
            self.colors[Face.LEFT] = Color.ORANGE
        elif x == max_idx:
            self.colors[Face.RIGHT] = Color.RED
            
        if y == 0:
            self.colors[Face.DOWN] = Color.YELLOW
        elif y == max_idx:
            self.colors[Face.UP] = Color.WHITE
            
        if z == 0:
            self.colors[Face.BACK] = Color.BLUE
        elif z == max_idx:
            self.colors[Face.FRONT] = Color.GREEN
    
    def is_corner(self) -> bool:
        """Check if this cubie is a corner piece (has 3 faces)."""
        return len(self.colors) == 3
    
    def is_edge(self) -> bool:
        """Check if this cubie is an edge piece (has 2 faces)."""
        return len(self.colors) == 2
    
    def is_center(self) -> bool:
        """Check if this cubie is a center piece (has 1 face)."""
        return len(self.colors) == 1
    
    def is_internal(self) -> bool:
        """Check if this cubie is an internal piece (has 0 faces)."""
        return len(self.colors) == 0
    
    def get_color(self, face: Face) -> Optional[Color]:
        """Get the color of the cubie on the given face."""
        return self.colors.get(face)
    
    def set_color(self, face: Face, color: Color):
        """Set the color of the cubie on the given face."""
        if face in self.colors:
            self.colors[face] = color
    
    def rotate(self, rotation_map: Dict[Face, Face]):
        """Rotate the cubie according to the given rotation map.
        
        Args:
            rotation_map: A mapping from old face to new face
        """
        new_colors = {}
        for face, color in self.colors.items():
            if face in rotation_map:
                new_colors[rotation_map[face]] = color
            else:
                new_colors[face] = color
        self.colors = new_colors


class Cube:
    """Represents a Rubik's Cube of any size (NxNxN)."""
    def __init__(self, size: int):
        """Initialize a solved cube of the given size.
        
        Args:
            size: Size of the cube (e.g., 2 for 2x2x2, 3 for 3x3x3, etc.)
        """
        if size < 2:
            raise ValueError("Cube size must be at least 2")
        
        self.size = size
        self.cubies = {}
        self._init_cubies()
        
        # Store the move history
        self.move_history = []
    
    def _init_cubies(self):
        """Initialize all cubies in the cube."""
        for x in range(self.size):
            for y in range(self.size):
                for z in range(self.size):
                    # Skip internal cubies for optimization
                    if (0 < x < self.size - 1 and 
                        0 < y < self.size - 1 and 
                        0 < z < self.size - 1):
                        continue
                    
                    position = (x, y, z)
                    self.cubies[position] = Cubie(position, self.size)
    
    def get_face_cubies(self, face: Face) -> List[Cubie]:
        """Get all cubies on the given face."""
        result = []
        max_idx = self.size - 1
        
        for position, cubie in self.cubies.items():
            x, y, z = position
            
            if (face == Face.UP and y == max_idx) or \
               (face == Face.DOWN and y == 0) or \
               (face == Face.LEFT and x == 0) or \
               (face == Face.RIGHT and x == max_idx) or \
               (face == Face.FRONT and z == max_idx) or \
               (face == Face.BACK and z == 0):
                result.append(cubie)
        
        return result
    
    def get_face_colors(self, face: Face) -> List[List[Color]]:
        """Get the colors of all cubies on the given face as a 2D grid."""
        cubies = self.get_face_cubies(face)
        result = [[None for _ in range(self.size)] for _ in range(self.size)]
        
        for cubie in cubies:
            x, y, z = cubie.position
            color = cubie.get_color(face)
            
            if face == Face.UP:
                row, col = self.size - 1 - z, x
            elif face == Face.DOWN:
                row, col = z, x
            elif face == Face.LEFT:
                row, col = y, z
            elif face == Face.RIGHT:
                row, col = y, self.size - 1 - z
            elif face == Face.FRONT:
                row, col = y, x
            elif face == Face.BACK:
                row, col = y, self.size - 1 - x
            
            result[row][col] = color
        
        return result
    
    def is_solved(self) -> bool:
        """Check if the cube is solved (all faces have a single color)."""
        for face in Face:
            colors = self.get_face_colors(face)
            first_color = colors[0][0]
            
            for row in colors:
                for color in row:
                    if color != first_color:
                        return False
        
        return True
    
    def apply_move(self, move: str):
        """Apply a move to the cube.
        
        Args:
            move: A move in standard notation (e.g., "U", "R'", "F2", etc.)
        """
        from cube.moves import apply_move
        apply_move(self, move)
        self.move_history.append(move)
    
    def apply_moves(self, moves: List[str]):
        """Apply a sequence of moves to the cube."""
        for move in moves:
            self.apply_move(move)
    
    def scramble(self, num_moves: int = 20):
        """Scramble the cube with random moves."""
        from cube.moves import BASIC_MOVES
        
        moves = []
        for _ in range(num_moves):
            # Choose a random face
            face = random.choice(list("URFDLB"))
            
            # Choose a random direction (normal, prime, or double)
            direction = random.choice(["", "'", "2"])
            
            # For 4x4 and larger, also consider slice moves
            if self.size >= 4:
                # 50% chance to do a slice move for larger cubes
                if random.random() < 0.5:
                    # For 4x4, we have inner slice moves
                    layer = random.randint(1, self.size - 2)
                    face = face.lower() + str(layer)
            
            move = face + direction
            moves.append(move)
        
        self.apply_moves(moves)
        return moves
    
    def reset(self):
        """Reset the cube to its solved state."""
        self.cubies = {}
        self._init_cubies()
        self.move_history = []
    
    def get_state_string(self) -> str:
        """Get a string representation of the cube state.
        
        This can be used for hashing or comparison.
        """
        state = ""
        for face in Face:
            colors = self.get_face_colors(face)
            for row in colors:
                for color in row:
                    state += str(color.value)
        return state
    
    def copy(self) -> 'Cube':
        """Create a deep copy of the cube."""
        new_cube = Cube(self.size)
        
        # Copy the cubies
        for position, cubie in self.cubies.items():
            new_cube.cubies[position] = Cubie(position, self.size)
            for face, color in cubie.colors.items():
                new_cube.cubies[position].colors[face] = color
        
        # Copy the move history
        new_cube.move_history = self.move_history.copy()
        
        return new_cube