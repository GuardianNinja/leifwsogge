
try:
    import numpy as np
except ImportError:
    np = None  # type: ignore
# Type hint for numpy to help static analysis tools
import typing as _typing
if _typing.TYPE_CHECKING:
    from numpy import ndarray # pyright: ignore[reportUnknownVariableType]

def simulate_deposition( # pyright: ignore[reportUnknownParameterType]
    ash_grid: 'ndarray', # pyright: ignore[reportUnknownParameterType]
    water_depth: float = 1500,
    settling_velocity: float = 0.5,
    ocean_current: tuple[float, float] = (0.2, -0.1)
)->np.ndarray: # pyright: ignore[reportUnknownMemberType]
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

    sediment: np.ndarray = np.copy(ash_grid)  # type: ignore[reportUnknownVariableType]

    for _ in range(steps):
        # Ensure shift is a tuple of ints, rounding if necessary
        shift = (
            int(round(float(ocean_current[0]))),
            int(round(float(ocean_current[1])))
        )
        sediment = np.roll( # pyright: ignore[reportUnknownVariableType] # pyright: ignore[reportUnknownMemberType] # pyright: ignore[reportUnknownMemberType] # pyright: ignore[reportUnknownMemberType] # type: ignore
            sediment,
            shift=shift,
            axis=(0, 1)
        )

    return sediment # pyright: ignore[reportUnknownVariableType]
