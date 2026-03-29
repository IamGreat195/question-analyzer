import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def create_visual():
    """
    Generates a geometrically accurate diagram showing a square inscribed within a circle,
    with the region between the circle and the square shaded.
    """

    # Calculations based on the problem description:
    # 1. Perimeter of the square = 32
    # 2. Side length (s) of the square = Perimeter / 4 = 32 / 4 = 8
    # 3. When a square is inscribed in a circle, the diagonal of the square
    #    is equal to the diameter of the circle.
    # 4. Diagonal (d) of the square = s√2 = 8√2
    # 5. Diameter (D) of the circle = 8√2
    # 6. Radius (r) of the circle = D / 2 = (8√2) / 2 = 4√2
    
    side_square = 8
    radius_circle = (side_square * np.sqrt(2)) / 2 # = 4 * sqrt(2)

    # Set up the figure and axes
    fig, ax = plt.subplots(figsize=(8, 8), dpi=300)
    ax.set_aspect('equal') # Crucial for accurate geometric representation
    ax.axis('off') # Turn off axes, ticks, and labels for a clean diagram

    # Define colors
    # A light grey color is used to represent the 'shaded' region.
    # The square is filled with white to create the visual effect of it being
    # 'cut out' from the shaded circle.
    shaded_color = '#d3d3d3' # Light grey
    square_fill_color = 'white'
    border_color = 'black'
    line_width = 1.5

    # 1. Draw the circle
    # Centered at (0,0) for simplicity.
    circle = patches.Circle((0, 0), radius_circle,
                            facecolor=shaded_color, edgecolor=border_color,
                            linewidth=line_width, zorder=1)
    ax.add_patch(circle)

    # 2. Define the vertices of the inscribed square
    # For a square inscribed in a circle of radius 'r' centered at (0,0),
    # with its vertices rotated 45 degrees relative to the axes,
    # the coordinates of the vertices (x,y) satisfy x^2 + y^2 = r^2.
    # Since it's a square rotated by 45 degrees, x=y for the vertex on the first quadrant.
    # Thus, 2x^2 = r^2 => x = r / sqrt(2).
    # With r = 4*sqrt(2), x = (4*sqrt(2)) / sqrt(2) = 4.
    
    vertex_coord = radius_circle / np.sqrt(2) # = 4

    vertices = np.array([
        [vertex_coord, vertex_coord],      # Top-right
        [-vertex_coord, vertex_coord],     # Top-left
        [-vertex_coord, -vertex_coord],    # Bottom-left
        [vertex_coord, -vertex_coord]      # Bottom-right
    ])

    # 3. Draw the square
    # The square is drawn on top of the circle (higher zorder) and filled with white
    # to create the visual of the region between the circle and square being shaded.
    square = patches.Polygon(vertices,
                             closed=True, facecolor=square_fill_color,
                             edgecolor=border_color, linewidth=line_width, zorder=2)
    ax.add_patch(square)

    # Set appropriate limits for the plot to provide some padding around the circle
    padding = 0.5
    limit = radius_circle + padding
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)

    # Save the figure to the specified path
    plt.savefig('corrected_questions/Question_2_visual.png', bbox_inches='tight')
    plt.close(fig) # Close the figure to free up memory