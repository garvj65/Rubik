"""Visualization utilities for Rubik's Cube."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from typing import List, Dict, Tuple, Optional
from cube.model import Cube, Face, Color

# Define color mapping for visualization
COLOR_MAP = {
    Color.WHITE: '#FFFFFF',   # White
    Color.RED: '#FF0000',     # Red
    Color.GREEN: '#00FF00',   # Green
    Color.YELLOW: '#FFFF00',  # Yellow
    Color.ORANGE: '#FFA500',  # Orange
    Color.BLUE: '#0000FF',    # Blue
}

# Define the layout of the cube faces for visualization
# The layout is a 2D grid where each face is placed in a specific position
FACE_LAYOUT = {
    Face.UP: (0, 1),
    Face.LEFT: (1, 0),
    Face.FRONT: (1, 1),
    Face.RIGHT: (1, 2),
    Face.BACK: (1, 3),
    Face.DOWN: (2, 1),
}


def visualize_cube(cube: Cube, ax: Optional[plt.Axes] = None, 
                  show: bool = True) -> plt.Axes:
    """Visualize the cube in a 2D net representation.
    
    Args:
        cube: The cube to visualize
        ax: Optional matplotlib axes to draw on
        show: Whether to show the plot immediately
        
    Returns:
        The matplotlib axes with the visualization
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 8))
    
    # Clear the axes
    ax.clear()
    
    # Set limits and aspect ratio
    ax.set_xlim(-0.5, 3.5)
    ax.set_ylim(-0.5, 2.5)
    ax.set_aspect('equal')
    
    # Turn off axis
    ax.axis('off')
    
    # Draw each face
    for face, (row, col) in FACE_LAYOUT.items():
        colors = cube.get_face_colors(face)
        draw_face(ax, colors, row, col, cube.size)
    
    # Add face labels
    for face, (row, col) in FACE_LAYOUT.items():
        ax.text(col, row - 0.2, face.name, 
                ha='center', va='center', fontsize=12)
    
    # Add title
    ax.set_title(f"{cube.size}x{cube.size}x{cube.size} Rubik's Cube")
    
    if show:
        plt.tight_layout()
        plt.show()
    
    return ax


def draw_face(ax: plt.Axes, colors: List[List[Color]], 
             row: int, col: int, size: int):
    """Draw a single face of the cube.
    
    Args:
        ax: Matplotlib axes to draw on
        colors: 2D grid of colors for the face
        row: Row position in the layout
        col: Column position in the layout
        size: Size of the cube
    """
    # Calculate the size of each cubie
    cubie_size = 1.0 / size
    
    # Draw each cubie
    for i in range(size):
        for j in range(size):
            color = colors[i][j]
            x = col + j * cubie_size
            y = row + i * cubie_size
            
            rect = Rectangle(
                (x, y), cubie_size, cubie_size,
                facecolor=COLOR_MAP[color],
                edgecolor='black',
                linewidth=1
            )
            ax.add_patch(rect)


def visualize_move_sequence(cube: Cube, moves: List[str], 
                           delay: float = 0.5, save_gif: bool = False,
                           filename: str = 'cube_animation.gif'):
    """Visualize a sequence of moves on the cube.
    
    Args:
        cube: The cube to visualize
        moves: List of moves to apply
        delay: Delay between frames in seconds
        save_gif: Whether to save the animation as a GIF
        filename: Filename for the GIF if saving
    """
    # Create a copy of the cube to avoid modifying the original
    cube_copy = cube.copy()
    
    # Create figure and axes
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Visualize initial state
    visualize_cube(cube_copy, ax, show=False)
    plt.pause(delay)
    
    frames = []
    if save_gif:
        from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
        canvas = FigureCanvas(fig)
        canvas.draw()
        image = np.frombuffer(canvas.tostring_rgb(), dtype='uint8')
        image = image.reshape(canvas.get_width_height()[::-1] + (3,))
        frames.append(image)
    
    # Apply each move and visualize
    for move in moves:
        cube_copy.apply_move(move)
        visualize_cube(cube_copy, ax, show=False)
        plt.title(f"Move: {move}")
        plt.pause(delay)
        
        if save_gif:
            canvas.draw()
            image = np.frombuffer(canvas.tostring_rgb(), dtype='uint8')
            image = image.reshape(canvas.get_width_height()[::-1] + (3,))
            frames.append(image)
    
    # Save as GIF if requested
    if save_gif and frames:
        try:
            import imageio
            imageio.mimsave(filename, frames, duration=delay)
            print(f"Animation saved as {filename}")
        except ImportError:
            print("Could not save GIF. Please install imageio: pip install imageio")
    
    plt.show()


def print_cube(cube: Cube):
    """Print a text representation of the cube to the console.
    
    Args:
        cube: The cube to print
    """
    # Define symbols for each color
    color_symbols = {
        Color.WHITE: 'W',
        Color.RED: 'R',
        Color.GREEN: 'G',
        Color.YELLOW: 'Y',
        Color.ORANGE: 'O',
        Color.BLUE: 'B',
    }
    
    # Print each face
    for face in Face:
        print(f"\n{face.name}:")
        colors = cube.get_face_colors(face)
        
        for row in colors:
            print(' '.join(color_symbols[color] for color in row))
    
    print("\n")


def visualize_solution_steps(cube: Cube, solution: List[str], 
                            step_names: Optional[List[str]] = None,
                            delay: float = 1.0):
    """Visualize the steps of a solution with annotations.
    
    Args:
        cube: The cube to solve
        solution: List of moves in the solution
        step_names: Optional list of names for each step or group of moves
        delay: Delay between steps in seconds
    """
    # Create a copy of the cube
    cube_copy = cube.copy()
    
    # Create figure and axes
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # If no step names provided, treat each move as a separate step
    if step_names is None:
        step_names = [f"Move: {move}" for move in solution]
        step_moves = [[move] for move in solution]
    else:
        # Assume step_names corresponds to groups of moves
        # This requires solution to be pre-grouped
        step_moves = solution
    
    # Visualize initial state
    visualize_cube(cube_copy, ax, show=False)
    plt.title("Initial State")
    plt.pause(delay)
    
    # Apply each step and visualize
    for i, (step_name, moves) in enumerate(zip(step_names, step_moves)):
        if isinstance(moves, str):
            moves = [moves]  # Convert single move to list
            
        for move in moves:
            cube_copy.apply_move(move)
        
        visualize_cube(cube_copy, ax, show=False)
        plt.title(f"Step {i+1}: {step_name}")
        plt.pause(delay)
    
    plt.title("Solution Complete")
    plt.show()