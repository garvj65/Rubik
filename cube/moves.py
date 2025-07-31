"""Move engine for Rubik's Cube operations."""

from typing import Dict, List, Tuple, Set, Optional, Union
import numpy as np
from cube.model import Cube, Face, Color, Cubie

# Define basic moves for a Rubik's Cube
BASIC_MOVES = {
    'U': Face.UP,      # Up face clockwise
    'D': Face.DOWN,    # Down face clockwise
    'L': Face.LEFT,    # Left face clockwise
    'R': Face.RIGHT,   # Right face clockwise
    'F': Face.FRONT,   # Front face clockwise
    'B': Face.BACK,    # Back face clockwise
}

# Define rotation maps for each face
ROTATION_MAPS = {
    Face.UP: {
        Face.FRONT: Face.RIGHT,
        Face.RIGHT: Face.BACK,
        Face.BACK: Face.LEFT,
        Face.LEFT: Face.FRONT
    },
    Face.DOWN: {
        Face.FRONT: Face.LEFT,
        Face.LEFT: Face.BACK,
        Face.BACK: Face.RIGHT,
        Face.RIGHT: Face.FRONT
    },
    Face.LEFT: {
        Face.UP: Face.BACK,
        Face.BACK: Face.DOWN,
        Face.DOWN: Face.FRONT,
        Face.FRONT: Face.UP
    },
    Face.RIGHT: {
        Face.UP: Face.FRONT,
        Face.FRONT: Face.DOWN,
        Face.DOWN: Face.BACK,
        Face.BACK: Face.UP
    },
    Face.FRONT: {
        Face.UP: Face.LEFT,
        Face.LEFT: Face.DOWN,
        Face.DOWN: Face.RIGHT,
        Face.RIGHT: Face.UP
    },
    Face.BACK: {
        Face.UP: Face.RIGHT,
        Face.RIGHT: Face.DOWN,
        Face.DOWN: Face.LEFT,
        Face.LEFT: Face.UP
    }
}


def get_rotation_map(face: Face, prime: bool = False, double: bool = False) -> Dict[Face, Face]:
    """Get the rotation map for a given face rotation.
    
    Args:
        face: The face being rotated
        prime: Whether the rotation is counterclockwise (prime)
        double: Whether the rotation is 180 degrees (double)
        
    Returns:
        A mapping from old face to new face for cubies affected by the rotation
    """
    base_map = ROTATION_MAPS[face]
    
    if double:
        # Apply the rotation twice for a double move
        result = {}
        for old_face, new_face in base_map.items():
            result[old_face] = base_map.get(new_face, new_face)
        return result
    
    if prime:
        # Invert the mapping for a counterclockwise rotation
        return {new_face: old_face for old_face, new_face in base_map.items()}
    
    return base_map


def get_affected_positions(cube: Cube, face: Face, layer: int) -> Set[Tuple[int, int, int]]:
    """Get the positions of cubies affected by rotating the given face and layer.
    
    Args:
        cube: The cube being rotated
        face: The face being rotated
        layer: The layer being rotated (0-indexed from the face)
        
    Returns:
        A set of positions (x, y, z) affected by the rotation
    """
    size = cube.size
    max_idx = size - 1
    positions = set()
    
    # Convert layer from 0-indexed to actual position
    if face == Face.UP:
        layer_pos = max_idx - layer
    elif face == Face.DOWN:
        layer_pos = layer
    elif face == Face.LEFT:
        layer_pos = layer
    elif face == Face.RIGHT:
        layer_pos = max_idx - layer
    elif face == Face.FRONT:
        layer_pos = max_idx - layer
    elif face == Face.BACK:
        layer_pos = layer
    
    # Get all positions in the specified layer
    for i in range(size):
        for j in range(size):
            if face == Face.UP or face == Face.DOWN:
                x, y, z = i, layer_pos, j
            elif face == Face.LEFT or face == Face.RIGHT:
                x, y, z = layer_pos, i, j
            elif face == Face.FRONT or face == Face.BACK:
                x, y, z = i, j, layer_pos
            
            # Check if this position has a cubie
            if (x, y, z) in cube.cubies:
                positions.add((x, y, z))
    
    return positions


def rotate_positions(positions: Set[Tuple[int, int, int]], face: Face, 
                     prime: bool = False, double: bool = False, size: int = 3) -> Dict[Tuple[int, int, int], Tuple[int, int, int]]:
    """Calculate new positions for cubies after a face rotation.
    
    Args:
        positions: Set of positions to rotate
        face: The face being rotated
        prime: Whether the rotation is counterclockwise
        double: Whether the rotation is 180 degrees
        size: Size of the cube
        
    Returns:
        A mapping from old positions to new positions
    """
    max_idx = size - 1
    position_map = {}
    
    for x, y, z in positions:
        if face == Face.UP:
            # For UP face, x and z change
            if double:
                new_pos = (max_idx - x, y, max_idx - z)
            elif prime:
                new_pos = (z, y, max_idx - x)
            else:
                new_pos = (max_idx - z, y, x)
        
        elif face == Face.DOWN:
            # For DOWN face, x and z change
            if double:
                new_pos = (max_idx - x, y, max_idx - z)
            elif prime:
                new_pos = (max_idx - z, y, x)
            else:
                new_pos = (z, y, max_idx - x)
        
        elif face == Face.LEFT:
            # For LEFT face, y and z change
            if double:
                new_pos = (x, max_idx - y, max_idx - z)
            elif prime:
                new_pos = (x, z, max_idx - y)
            else:
                new_pos = (x, max_idx - z, y)
        
        elif face == Face.RIGHT:
            # For RIGHT face, y and z change
            if double:
                new_pos = (x, max_idx - y, max_idx - z)
            elif prime:
                new_pos = (x, max_idx - z, y)
            else:
                new_pos = (x, z, max_idx - y)
        
        elif face == Face.FRONT:
            # For FRONT face, x and y change
            if double:
                new_pos = (max_idx - x, max_idx - y, z)
            elif prime:
                new_pos = (y, max_idx - x, z)
            else:
                new_pos = (max_idx - y, x, z)
        
        elif face == Face.BACK:
            # For BACK face, x and y change
            if double:
                new_pos = (max_idx - x, max_idx - y, z)
            elif prime:
                new_pos = (max_idx - y, x, z)
            else:
                new_pos = (y, max_idx - x, z)
        
        position_map[(x, y, z)] = new_pos
    
    return position_map


def apply_face_rotation(cube: Cube, face: Face, layer: int = 0, 
                       prime: bool = False, double: bool = False):
    """Apply a rotation to a specific face and layer of the cube.
    
    Args:
        cube: The cube to rotate
        face: The face to rotate
        layer: The layer to rotate (0-indexed from the face)
        prime: Whether the rotation is counterclockwise
        double: Whether the rotation is 180 degrees
    """
    # Get affected positions
    positions = get_affected_positions(cube, face, layer)
    
    # Calculate new positions
    position_map = rotate_positions(positions, face, prime, double, cube.size)
    
    # Get rotation map for colors
    rotation_map = get_rotation_map(face, prime, double)
    
    # Create temporary copies of affected cubies
    temp_cubies = {}
    for pos in positions:
        temp_cubies[pos] = cube.cubies[pos]
    
    # Move cubies to their new positions and rotate their colors
    for old_pos, new_pos in position_map.items():
        # Get the cubie that was at the old position
        cubie = temp_cubies[old_pos]
        
        # Create a new cubie at the new position
        new_cubie = Cubie(new_pos, cube.size)
        
        # Copy colors with rotation
        for f, color in cubie.colors.items():
            new_face = rotation_map.get(f, f)
            new_cubie.colors[new_face] = color
        
        # Update the cube
        cube.cubies[new_pos] = new_cubie


def parse_move(move: str) -> Tuple[str, int, bool, bool]:
    """Parse a move string into its components.
    
    Args:
        move: A move in standard notation (e.g., "U", "R'", "F2", "r", "M", etc.)
        
    Returns:
        A tuple of (face_letter, layer, prime, double)
    """
    # Handle empty move
    if not move:
        raise ValueError("Empty move")
    
    # Extract the base move and any modifiers
    base = move[0]
    layer = 0  # Default to outer layer
    
    # Check for slice notation (e.g., "2R" for the second layer from the right)
    if len(move) > 1 and move[1].isdigit():
        layer = int(move[1]) - 1  # Convert to 0-indexed
        move = move[0] + move[2:]  # Remove the layer number
    # Check for lowercase notation (e.g., "r" for right slice)
    elif base.islower():
        base = base.upper()
        layer = 1  # Second layer (0-indexed)
    
    # Check for prime (counterclockwise) or double (180 degree) notation
    prime = "'" in move
    double = "2" in move
    
    return base, layer, prime, double


def apply_move(cube: Cube, move: str):
    """Apply a move to the cube.
    
    Args:
        cube: The cube to apply the move to
        move: A move in standard notation
    """
    # Parse the move
    face_letter, layer, prime, double = parse_move(move)
    
    # Handle special moves
    if face_letter == 'M':  # Middle slice (between L and R)
        apply_face_rotation(cube, Face.LEFT, 1, not prime, double)
    elif face_letter == 'E':  # Equatorial slice (between U and D)
        apply_face_rotation(cube, Face.DOWN, 1, prime, double)
    elif face_letter == 'S':  # Standing slice (between F and B)
        apply_face_rotation(cube, Face.FRONT, 1, prime, double)
    elif face_letter == 'X':  # Rotate entire cube on R axis
        for i in range(cube.size):
            apply_face_rotation(cube, Face.RIGHT, i, prime, double)
    elif face_letter == 'Y':  # Rotate entire cube on U axis
        for i in range(cube.size):
            apply_face_rotation(cube, Face.UP, i, prime, double)
    elif face_letter == 'Z':  # Rotate entire cube on F axis
        for i in range(cube.size):
            apply_face_rotation(cube, Face.FRONT, i, prime, double)
    else:
        # Regular face move
        face = BASIC_MOVES.get(face_letter)
        if face is None:
            raise ValueError(f"Unknown move: {move}")
        
        apply_face_rotation(cube, face, layer, prime, double)


def get_inverse_move(move: str) -> str:
    """Get the inverse of a move.
    
    Args:
        move: A move in standard notation
        
    Returns:
        The inverse move
    """
    # Parse the move
    face_letter, layer, prime, double = parse_move(move)
    
    # Double moves are their own inverse
    if double:
        return move
    
    # For other moves, toggle the prime modifier
    if prime:
        # Remove the prime
        return move.replace("'", "")
    else:
        # Add a prime
        if layer > 0 and face_letter.lower() in "rlfbud":
            # Handle slice notation
            return f"{face_letter.lower()}'" if layer == 1 else f"{layer+1}{face_letter}'"
        else:
            return f"{face_letter}'"


def get_inverse_sequence(moves: List[str]) -> List[str]:
    """Get the inverse of a sequence of moves.
    
    Args:
        moves: A list of moves in standard notation
        
    Returns:
        The inverse sequence of moves
    """
    return [get_inverse_move(move) for move in reversed(moves)]