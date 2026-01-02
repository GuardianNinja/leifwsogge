try:
    import numpy as np # pyright: ignore[reportMissingImports]
except ImportError:
    import sys
    import os
    # Try to add a local numpy path if available
    local_numpy = os.path.join(os.path.dirname(__file__), 'numpy')
    if os.path.isdir(local_numpy):
        sys.path.insert(0, local_numpy)
        try:
            import numpy as np # pyright: ignore[reportMissingImports]
        except ImportError:
            raise ImportError("numpy is required for this module. Please install it using 'pip install numpy'.")
    else:
        raise ImportError("numpy is required for this module. Please install it using 'pip install numpy'.")

def simulate_ash_cloud(
    grid_size: int = 100,
    time_steps: int = 50,
    eruption_center: tuple[int, int] = (50, 50),
    eruption_strength: float = 1.0,
    wind_vector: tuple[float, float] = (1, 0.5),
    settling_rate: float = 0.01
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
        shifted: np.ndarray = np.ndarray  # type: ignore
        shifted = np.roll(ash, shift=(int(wind_vector[0]), int(wind_vector[1])), axis=(0, 1))
        ash = shifted * (1 - settling_rate)

    return ash
