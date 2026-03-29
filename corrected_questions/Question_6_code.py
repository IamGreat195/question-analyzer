import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

def create_visual():
    """
    Generates a matplotlib figure containing four geometric shapes labeled A, B, C, D.
    One shape (A) has exactly two lines of symmetry, while the others (B, C, D) do not.
    The figure is styled for publication quality and saved as 'Question_6_visual.png'.
    """
    # Set professional styling for fonts and overall appearance
    plt.rcParams.update({
        'font.size': 12,
        'font.family': 'serif',
        'axes.labelsize': 10,
        'xtick.labelsize': 8,
        'ytick.labelsize': 8,
        'figure.titlesize': 14,
        'figure.autolayout': False # Manually handle layout with tight_layout
    })

    # Create a figure and a 2x2 grid of subplots
    fig, axes = plt.subplots(2, 2, figsize=(10, 8), dpi=300)
    axes = axes.flatten() # Flatten the 2x2 array of axes for easy iteration

    # Define common plot limits for consistent sizing and padding around shapes
    plot_lim = 3.5

    # --- Shape A: Non-square rectangle (Exactly two lines of symmetry) ---
    ax = axes[0]
    ax.set_aspect('equal', adjustable='box') # Ensure correct proportions (e.g., squares look square)
    width_A, height_A = 4, 2 # Example dimensions for a non-square rectangle
    rect_A_vertices = [
        (-width_A / 2, -height_A / 2),
        (width_A / 2, -height_A / 2),
        (width_A / 2, height_A / 2),
        (-width_A / 2, height_A / 2)
    ]
    rect_A = patches.Polygon(rect_A_vertices, closed=True, edgecolor='blue', facecolor='lightblue', linewidth=2)
    ax.add_patch(rect_A)
    ax.text(-plot_lim + 0.5, plot_lim - 0.5, 'A', fontsize=16, va='top', ha='left', weight='bold')
    ax.set_xlim(-plot_lim, plot_lim)
    ax.set_ylim(-plot_lim, plot_lim)
    ax.axis('off') # Hide axes for a clean geometry diagram

    # --- Shape B: Regular Hexagon (Six lines of symmetry) ---
    ax = axes[1]
    ax.set_aspect('equal', adjustable='box')
    side_B = 1.8 # Side length (and circumradius) of the regular hexagon
    hexagon_vertices = []
    for i in range(6):
        # Calculate vertices for a regular hexagon centered at origin, rotated to have flat top/bottom
        angle_rad = np.radians(60 * i + 30) # Add 30 degrees to align a side horizontally
        x = side_B * np.cos(angle_rad)
        y = side_B * np.sin(angle_rad)
        hexagon_vertices.append((x, y))
    hexagon_B = patches.Polygon(hexagon_vertices, closed=True, edgecolor='green', facecolor='lightgreen', linewidth=2)
    ax.add_patch(hexagon_B)
    ax.text(-plot_lim + 0.5, plot_lim - 0.5, 'B', fontsize=16, va='top', ha='left', weight='bold')
    ax.set_xlim(-plot_lim, plot_lim)
    ax.set_ylim(-plot_lim, plot_lim)
    ax.axis('off')

    # --- Shape C: Symmetrical Pentagon (One vertical line of symmetry) ---
    ax = axes[2]
    ax.set_aspect('equal', adjustable='box')
    # Custom vertices for a house-like pentagon with only vertical symmetry
    pentagon_vertices = [
        (0, 2.5),        # Top point
        (-2.0, 0.5),     # Left-middle point
        (-1.5, -2.0),    # Bottom-left point
        (1.5, -2.0),     # Bottom-right point
        (2.0, 0.5)       # Right-middle point
    ]
    pentagon_C = patches.Polygon(pentagon_vertices, closed=True, edgecolor='red', facecolor='pink', linewidth=2)
    ax.add_patch(pentagon_C)
    ax.text(-plot_lim + 0.5, plot_lim - 0.5, 'C', fontsize=16, va='top', ha='left', weight='bold')
    ax.set_xlim(-plot_lim, plot_lim)
    ax.set_ylim(-plot_lim, plot_lim)
    ax.axis('off')

    # --- Shape D: Isosceles Trapezoid (One vertical line of symmetry) ---
    ax = axes[3]
    ax.set_aspect('equal', adjustable='box')
    upper_base_D = 2.5
    lower_base_D = 4.5
    height_D = 2.5
    trapezoid_vertices = [
        (-upper_base_D / 2, height_D / 2),
        (upper_base_D / 2, height_D / 2),
        (lower_base_D / 2, -height_D / 2),
        (-lower_base_D / 2, -height_D / 2)
    ]
    trapezoid_D = patches.Polygon(trapezoid_vertices, closed=True, edgecolor='purple', facecolor='plum', linewidth=2)
    ax.add_patch(trapezoid_D)
    ax.text(-plot_lim + 0.5, plot_lim - 0.5, 'D', fontsize=16, va='top', ha='left', weight='bold')
    ax.set_xlim(-plot_lim, plot_lim)
    ax.set_ylim(-plot_lim, plot_lim)
    ax.axis('off')

    # Adjust layout to prevent overlapping titles/labels and add padding
    plt.tight_layout(pad=3.0)

    # Create the output directory if it doesn't exist
    output_dir = 'corrected_questions'
    os.makedirs(output_dir, exist_ok=True)

    # Define the file path for saving the figure
    file_path = os.path.join(output_dir, 'Question_6_visual.png')

    # Save the figure with high quality and tight bounding box
    plt.savefig(file_path, bbox_inches='tight')
    plt.close(fig) # Close the figure to free up memory