import matplotlib.pyplot as plt
import numpy as np
import os

def create_visual():
    """
    Generates a matplotlib graph of a polynomial function f(x) = -x^2 - 3
    that satisfies the given conditions:
    - Maximum at (0, -3).
    - Rises in Quadrant 3 towards (0, -3).
    - Falls in Quadrant 4 from (0, -3).
    - Y-intercept at (0, -3).
    The graph is saved as 'corrected_questions/Question_1_visual.png'.
    """

    # Set professional styling for the plot
    plt.style.use('seaborn-v0_8-darkgrid')
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.size': 10,
        'axes.labelsize': 12,
        'axes.titlesize': 14,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'lines.linewidth': 2,
        'lines.markersize': 6,
        'grid.linestyle': '--',
        'grid.alpha': 0.7
    })

    fig, ax = plt.subplots(figsize=(8, 6), dpi=300)

    # Define the polynomial function (example: y = -x^2 - 3)
    x = np.linspace(-3.5, 3.5, 400)
    y = -x**2 - 3

    # Plot the curve
    ax.plot(x, y, color='dodgerblue', label='f(x) = -x² - 3')

    # Mark the key point: maximum and y-intercept at (0, -3)
    ax.plot(0, -3, 'ro', markersize=8, zorder=5, label='Maximum / Y-intercept (0, -3)')
    ax.annotate('(0, -3)', xy=(0, -3), xytext=(0.5, -2.5),
                arrowprops=dict(facecolor='black', shrink=0.05, width=0.8, headwidth=6),
                fontsize=10, color='red')

    # Add labels and title
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.set_title('Graph of Polynomial Function f(x)')

    # Set axis limits to clearly show the behavior around (0, -3)
    # and the relevant quadrants (Q3 and Q4).
    ax.set_xlim(-4, 4)
    ax.set_ylim(-12, 0) # Extend below -3 and up to 0 to show x-axis

    # Draw the x and y axes clearly
    ax.axhline(0, color='black', linewidth=1.0)
    ax.axvline(0, color='black', linewidth=1.0)

    # Add grid
    ax.grid(True, linestyle='--', alpha=0.6)

    # Add a legend
    ax.legend(loc='lower left')

    # Ensure the output directory exists
    output_dir = 'corrected_questions'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'Question_1_visual.png')

    # Save the figure
    plt.savefig(output_path, bbox_inches='tight')
    plt.close(fig)

if __name__ == '__main__':
    create_visual()