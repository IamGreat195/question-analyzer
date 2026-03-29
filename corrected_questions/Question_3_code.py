import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib.ticker as mticker
from matplotlib.lines import Line2D # To create a custom handle for asymptotes in legend

def create_visual():
    """
    Generates a graph plotting y = sin(x) and y = csc(x) with specified
    x and y axis ranges, labels, and asymptotes.
    """
    # Set a professional plotting style
    plt.style.use('seaborn-v0_8-darkgrid')

    # Figure and Axes setup
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

    # --- Plotting Functions ---
    # Use a high number of points for smooth curves
    x = np.linspace(-2 * np.pi, 2 * np.pi, 1000)

    # Function 1: y = sin(x)
    y_sin = np.sin(x)
    ax.plot(x, y_sin, label=r'$y = \sin(x)$', color='blue', linewidth=2.5)

    # Function 2: y = csc(x) (1/sin(x))
    # Handle asymptotes by setting values outside the y-axis range to NaN.
    # This creates breaks in the line at the asymptotes.
    y_csc = 1 / np.sin(x)
    # Clip values to ensure they are within the desired plot range for csc(x)
    y_csc[np.abs(y_csc) > 4] = np.nan
    ax.plot(x, y_csc, label=r'$y = \csc(x)$', color='red', linestyle='-', linewidth=2.5)

    # --- Vertical Asymptotes for csc(x) ---
    asymptote_x_vals = [-2 * np.pi, -np.pi, 0, np.pi, 2 * np.pi]
    for x_val in asymptote_x_vals:
        # Plot each asymptote. Only label the first one for the legend.
        ax.axvline(x=x_val, color='gray', linestyle='--', linewidth=1, zorder=0)

    # Custom legend entry for asymptotes
    asymptote_legend_handle = Line2D([0], [0], color='gray', linestyle='--', linewidth=1)


    # --- Axis Configuration ---
    # X-axis range and ticks
    ax.set_xlim(-2 * np.pi, 2 * np.pi)
    x_tick_positions = np.array([-2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2]) * np.pi
    x_tick_labels = [r'$-2\pi$', r'$-\frac{3\pi}{2}$', r'$-\pi$', r'$-\frac{\pi}{2}$', r'$0$',
                     r'$\frac{\pi}{2}$', r'$\pi$', r'$\frac{3\pi}{2}$', r'$2\pi$']
    ax.set_xticks(x_tick_positions)
    ax.set_xticklabels(x_tick_labels, fontsize=12)

    # Y-axis range and ticks
    ax.set_ylim(-4, 4)
    ax.set_yticks([-3, -2, -1, 0, 1, 2, 3])
    ax.set_yticklabels([-3, -2, -1, 0, 1, 2, 3], fontsize=12)

    # Labels
    ax.set_xlabel('x (radians)', fontsize=14, labelpad=10)
    ax.set_ylabel('y', fontsize=14, labelpad=10)

    # Legend
    # Get existing handles and labels
    handles, labels = ax.get_legend_handles_labels()
    # Add the custom asymptote handle and label
    handles.append(asymptote_legend_handle)
    labels.append('Asymptotes')
    
    ax.legend(handles, labels, loc='upper right', fontsize=12, frameon=True, fancybox=True, shadow=True)

    # Grid
    ax.grid(True, linestyle='--', alpha=0.6)

    # Ensure tight layout
    plt.tight_layout()

    # --- Save the plot ---
    output_dir = 'corrected_questions'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'Question_3_visual.png')
    plt.savefig(output_path, bbox_inches='tight')
    plt.close(fig) # Close the figure to free up memory