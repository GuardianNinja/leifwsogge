import numpy as np

def simulate_deposition(
    ash_grid: np.ndarray,
    water_depth: float = 1500,
    settling_velocity=0.5,
    ocean_current=(0.2, -0.1)
)->np.ndarray:
    """
    Simulates ash settling through the water column and drifting along ocean currents.

    Parameters:
        ash_grid (np.ndarray): Airborne ash concentration grid.
        water_depth (float): Depth of water column in meters.
        settling_velocity (float): m/s settling speed of ash.
        ocean_current (tuple): (dx, dy) drift per time step.

    Returns:
        np.ndarray: Sediment layer deposited on the seafloor.
    """
    # grid_size = ash_grid.shape[0]  # Removed unused variable
    time_to_settle = water_depth / settling_velocity
    steps = int(time_to_settle)

    sediment = np.copy(ash_grid) # pyright: ignore[reportUnknownMemberType]

    for _ in range(steps):
        sediment = np.roll(
            sediment,
            shift=(int(ocean_current[0]), int(ocean_current[1])), # pyright: ignore[reportUnknownArgumentType]
            axis=(0, 1)
        )

    return sediment
