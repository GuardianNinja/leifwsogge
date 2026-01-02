try:
    import numpy as np
except ImportError:
    raise ImportError("numpy is required for this module. Please install it using 'pip install numpy'.")

def simulate_ash_cloud(
    grid_size=100,
    time_steps=50,
    eruption_center=(50, 50),
    eruption_strength=1.0,
    wind_vector=(1, 0.5),
    settling_rate=0.01
):
    """
    Simulates airborne volcanic ash dispersion over a 2D grid.

    Parameters:
        grid_size (int): Size of the square simulation grid.
        time_steps (int): Number of simulation steps.
        eruption_center (tuple): (x, y) coordinates of eruption.
        eruption_strength (float): Initial ash concentration.
        wind_vector (tuple): (dx, dy) wind direction per step.
        settling_rate (float): Fraction of ash that settles per step.

    Returns:
        np.ndarray: Final ash concentration grid.
    """

    ash = np.zeros((grid_size, grid_size))
    x0, y0 = eruption_center
    ash[x0, y0] = eruption_strength

    for _ in range(time_steps):
        shifted = np