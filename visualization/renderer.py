"""3D renderer for Rubik's Cube visualization."""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
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

# Define the normal vectors for each face
FACE_NORMALS = {
    Face.UP: (0, 1, 0),
    Face.DOWN: (0, -1, 0),
    Face.LEFT: (-1, 0, 0),
    Face.RIGHT: (1, 0, 0),
    Face.FRONT: (0, 0, 1),
    Face.BACK: (0, 0, -1),
}


def render_cube_3d(cube: Cube, ax: Optional[plt.Axes] = None,
                 show: bool = True, view_angles: Tuple[float, float] = (30, 30)):
    """Render the cube in 3D.
    
    Args:
        cube: The cube to render
        ax: Optional matplotlib 3D axes to draw on
        show: Whether to show the plot immediately
        view_angles: (elevation, azimuth) angles for the view
        
    Returns:
        The matplotlib 3D axes with the visualization
    """
    if ax is None:
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')
    
    # Clear the axes
    ax.clear()
    
    # Set the view angles
    ax.view_init(elev=view_angles[0], azim=view_angles[1])
    
    # Set limits
    ax.set_xlim(-cube.size, cube.size)
    ax.set_ylim(-cube.size, cube.size)
    ax.set_zlim(-cube.size, cube.size)
    
    # Turn off axis
    ax.set_axis_off()
    
    # Draw each cubie
    for position, cubie in cube.cubies.items():
        draw_cubie_3d(ax, cubie, cube.size)
    
    # Add title
    ax.set_title(f"{cube.size}x{cube.size}x{cube.size} Rubik's Cube")
    
    if show:
        plt.tight_layout()
        plt.show()
    
    return ax


def draw_cubie_3d(ax: plt.Axes, cubie, cube_size: int):
    """Draw a single cubie in 3D.
    
    Args:
        ax: Matplotlib 3D axes to draw on
        cubie: The cubie to draw
        cube_size: Size of the cube
    """
    x, y, z = cubie.position
    
    # Convert to coordinates centered at the origin
    x = x - (cube_size - 1) / 2
    y = y - (cube_size - 1) / 2
    z = z - (cube_size - 1) / 2
    
    # Define the vertices of the cubie
    size = 0.45  # Size of each cubie (slightly smaller than 0.5 to add gaps)
    vertices = [
        [x - size, y - size, z - size],  # 0: bottom-left-back
        [x + size, y - size, z - size],  # 1: bottom-right-back
        [x + size, y + size, z - size],  # 2: top-right-back
        [x - size, y + size, z - size],  # 3: top-left-back
        [x - size, y - size, z + size],  # 4: bottom-left-front
        [x + size, y - size, z + size],  # 5: bottom-right-front
        [x + size, y + size, z + size],  # 6: top-right-front
        [x - size, y + size, z + size],  # 7: top-left-front
    ]
    
    # Define the faces of the cubie
    faces = [
        [vertices[0], vertices[1], vertices[2], vertices[3]],  # Back face
        [vertices[4], vertices[5], vertices[6], vertices[7]],  # Front face
        [vertices[0], vertices[3], vertices[7], vertices[4]],  # Left face
        [vertices[1], vertices[5], vertices[6], vertices[2]],  # Right face
        [vertices[3], vertices[2], vertices[6], vertices[7]],  # Top face
        [vertices[0], vertices[1], vertices[5], vertices[4]],  # Bottom face
    ]
    
    # Define the face colors
    face_colors = [
        COLOR_MAP.get(cubie.get_color(Face.BACK), 'black'),
        COLOR_MAP.get(cubie.get_color(Face.FRONT), 'black'),
        COLOR_MAP.get(cubie.get_color(Face.LEFT), 'black'),
        COLOR_MAP.get(cubie.get_color(Face.RIGHT), 'black'),
        COLOR_MAP.get(cubie.get_color(Face.UP), 'black'),
        COLOR_MAP.get(cubie.get_color(Face.DOWN), 'black'),
    ]
    
    # Draw each face
    for i, (face, color) in enumerate(zip(faces, face_colors)):
        if color != 'black':  # Only draw colored faces
            poly = Poly3DCollection([face], alpha=1)
            poly.set_facecolor(color)
            poly.set_edgecolor('black')
            ax.add_collection3d(poly)


def animate_cube_3d(cube: Cube, moves: List[str], delay: float = 0.5,
                  save_gif: bool = False, filename: str = 'cube_animation.gif'):
    """Animate a sequence of moves on the cube in 3D.
    
    Args:
        cube: The cube to animate
        moves: List of moves to apply
        delay: Delay between frames in seconds
        save_gif: Whether to save the animation as a GIF
        filename: Filename for the GIF if saving
    """
    # Create a copy of the cube to avoid modifying the original
    cube_copy = cube.copy()
    
    # Create figure and axes
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Render initial state
    render_cube_3d(cube_copy, ax, show=False)
    plt.pause(delay)
    
    frames = []
    if save_gif:
        from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
        canvas = FigureCanvas(fig)
        canvas.draw()
        image = np.frombuffer(canvas.tostring_rgb(), dtype='uint8')
        image = image.reshape(canvas.get_width_height()[::-1] + (3,))
        frames.append(image)
    
    # Apply each move and render
    for move in moves:
        cube_copy.apply_move(move)
        render_cube_3d(cube_copy, ax, show=False)
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


def render_cube_3d_interactive(cube: Cube):
    """Render the cube in 3D with interactive controls.
    
    Args:
        cube: The cube to render
    """
    try:
        import ipywidgets as widgets
        from IPython.display import display
    except ImportError:
        print("Interactive mode requires ipywidgets. Please install it: pip install ipywidgets")
        return
    
    # Create figure and axes
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Initial render
    render_cube_3d(cube, ax, show=False)
    
    # Create sliders for view angles
    elevation_slider = widgets.FloatSlider(
        value=30,
        min=-90,
        max=90,
        step=5,
        description='Elevation:',
        continuous_update=False
    )
    
    azimuth_slider = widgets.FloatSlider(
        value=30,
        min=0,
        max=360,
        step=5,
        description='Azimuth:',
        continuous_update=False
    )
    
    # Create dropdown for moves
    move_dropdown = widgets.Dropdown(
        options=['U', 'D', 'L', 'R', 'F', 'B', "U'", "D'", "L'", "R'", "F'", "B'",
                'U2', 'D2', 'L2', 'R2', 'F2', 'B2'],
        value='U',
        description='Move:',
    )
    
    # Create button for applying moves
    apply_button = widgets.Button(
        description='Apply Move',
        button_style='success',
    )
    
    # Create button for resetting the cube
    reset_button = widgets.Button(
        description='Reset Cube',
        button_style='danger',
    )
    
    # Create output area for displaying the figure
    output = widgets.Output()
    
    # Define update function for view angles
    def update_view(change):
        with output:
            ax.view_init(elev=elevation_slider.value, azim=azimuth_slider.value)
            fig.canvas.draw_idle()
    
    # Define function for applying moves
    def apply_move(b):
        with output:
            cube.apply_move(move_dropdown.value)
            render_cube_3d(cube, ax, show=False)
            fig.canvas.draw_idle()
    
    # Define function for resetting the cube
    def reset_cube(b):
        with output:
            cube.reset()
            render_cube_3d(cube, ax, show=False)
            fig.canvas.draw_idle()
    
    # Connect the callbacks
    elevation_slider.observe(update_view, names='value')
    azimuth_slider.observe(update_view, names='value')
    apply_button.on_click(apply_move)
    reset_button.on_click(reset_cube)
    
    # Display the widgets and figure
    display(widgets.HBox([elevation_slider, azimuth_slider]))
    display(widgets.HBox([move_dropdown, apply_button, reset_button]))
    with output:
        plt.show()
    display(output)