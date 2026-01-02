import numpy as np
from numpy import ndarray # pyright: ignore[reportMissingImports]

from typing import Dict, Any

def classify_sediment(sediment_grid: ndarray) -> Dict[str, Any]: # pyright: ignore[reportInvalidTypeForm]
    """
    Classifies sediment into elemental categories based on density bands.

    Density bands (simplified):
        Fine ash (Si, Al): lowest 33%
        Medium ash (Fe, Mg): middle 33%
        Coarse ash (Pb, U): highest 33%

    Parameters:
        sediment_grid (np.ndarray): Seafloor sediment concentration.

    Returns:
        dict: Elemental layers { "Si_Al": grid, "Fe_Mg": grid, "Pb_U": grid }
    """

    flat = sediment_grid.flatten()
    thresholds = np.percentile(flat, [33, 66]) # pyright: ignore[reportOptionalMemberAccess]

    fine_mask = sediment_grid <= thresholds[0]
    medium_mask = (sediment_grid > thresholds[0]) & (sediment_grid <= thresholds[1])
    coarse_mask = sediment_grid > thresholds[1]

    return {
        "Si_Al": sediment_grid * fine_mask,
        "Fe_Mg": sediment_grid * medium_mask,
        "Pb_U": sediment_grid * coarse_mask
    }
