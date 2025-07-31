"""Example of how to implement a custom visualization."""

import sys
import os
import matplotlib.pyplot as plt
import numpy as np

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cube.model import Cube, Face, Color


def custom_visualize_cube(cube, ax=None, show=True):
    """Visualize a cube using a custom visualization.
    
    This is a simple 2D visualization that shows the cube as a net.
    
    Args:
        cube: The cube to visualize.
        ax: The matplotlib axis to plot on. If None, a new figure is created.
        show: Whether to show the plot.
        
    Returns:
        The matplotlib axis.
    """
    # Create a new figure if needed
    if ax is None:
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111)
    
    # Define the layout of the net
    # The net is a 2D representation of the cube
    # We'll use a 4x3 grid to represent the 6 faces
    # The layout is as follows:
    #     [U]
    # [L][F][R][B]
    #     [D]
    
    # Define the positions of the faces in the grid
    face_positions = {
        Face.UP: (0, 1),
        Face.LEFT: (1, 0),
        Face.FRONT: (1, 1),
        Face.RIGHT: (1, 2),
        Face.BACK: (1, 3),
        Face.DOWN: (2, 1),
    }
    
    # Define the colors for the faces
    face_colors = {
        Color.WHITE: 'white',
        Color.YELLOW: 'yellow',
        Color.GREEN: 'green',
        Color.BLUE: 'blue',
        Color.RED: 'red',
        Color.ORANGE: 'orange',
    }
    
    # Define the size of each cell in the grid
    cell_size = 1.0
    
    # Draw the faces
    for face in Face:
        # Get the position of the face in the grid
        grid_row, grid_col = face_positions[face]
        
        # Get the cubies on the face
        cubies = cube.get_face_cubies(face)
        
        # Draw the cubies
        for i in range(cube.size):
            for j in range(cube.size):
                # Get the color of the cubie
                color = cubies[i][j].get_face_color(face)
                
                # Calculate the position of the cubie in the grid
                x = grid_col * (cube.size + 1) * cell_size + j * cell_size
                y = grid_row * (cube.size + 1) * cell_size + i * cell_size
                
                # Draw the cubie
                rect = plt.Rectangle((x, y), cell_size, cell_size, 
                                    facecolor=face_colors[color], 
                                    edgecolor='black')
                ax.add_patch(rect)
    
    # Set the limits of the plot
    ax.set_xlim(0, 4 * (cube.size + 1) * cell_size)
    ax.set_ylim(0, 3 * (cube.size + 1) * cell_size)
    
    # Set the aspect ratio to be equal
    ax.set_aspect('equal')
    
    # Remove the axes
    ax.set_axis_off()
    
    # Add a title
    ax.set_title(f"{cube.size}x{cube.size} Rubik's Cube")
    
    # Show the plot if requested
    if show:
        plt.tight_layout()
        plt.show()
    
    return ax


def custom_visualize_move_sequence(cube, moves, delay=0.5):
    """Visualize a sequence of moves using a custom visualization.
    
    Args:
        cube: The cube to visualize.
        moves: The sequence of moves to apply.
        delay: The delay between moves in seconds.
    """
    # Create a copy of the cube
    cube_copy = cube.copy()
    
    # Create a figure
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111)
    
    # Visualize the initial state
    custom_visualize_cube(cube_copy, ax=ax, show=False)
    plt.pause(delay)
    
    # Apply the moves one by one and visualize the cube after each move
    for move in moves:
        # Apply the move
        cube_copy.apply_move(move)
        
        # Clear the axis
        ax.clear()
        
        # Visualize the cube
        custom_visualize_cube(cube_copy, ax=ax, show=False)
        
        # Add a title
        ax.set_title(f"{cube_copy.size}x{cube_copy.size} Rubik's Cube - Move: {move}")
        
        # Pause to show the move
        plt.pause(delay)
    
    # Show the final state
    plt.show()


def main():
    """Demonstrate the custom visualization."""
    # Create a cube
    cube = Cube(3)
    
    # Visualize the cube
    print("Visualizing a 3x3 cube using a custom visualization")
    custom_visualize_cube(cube)
    
    # Scramble the cube
    scramble_moves = cube.scramble(10)
    print(f"Scrambled the cube with moves: {scramble_moves}")
    
    # Visualize the scrambled cube
    custom_visualize_cube(cube)
    
    # Apply some moves and visualize the sequence
    moves = ["U", "R", "F", "L", "B", "D"]
    print(f"Applying moves: {moves}")
    custom_visualize_move_sequence(cube, moves, delay=1.0)


if __name__ == "__main__":
    main()