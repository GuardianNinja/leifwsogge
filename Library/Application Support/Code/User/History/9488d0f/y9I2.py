try:
    import numpy as np
except ImportError:
    raise ImportError("The 'numpy' package is required but not installed. Please install it with 'pip install numpy'.")
from volcanic.ash_dispersion import simulate_ash_cloud  # type: ignore
from volcanic.ocean_deposition import simulate_deposition  # type: ignore[import]
from volcanic.density_classifier import classify_sediment, ClassifiedSediment  # type: ignore[import]
from visualizations.ash_distribution_plot import plot_distribution  # type: ignore[import]

def main():
    ash_grid: np.ndarray = simulate_ash_cloud()
    from typing import Any  # Add at function scope to avoid global import if not needed
    sediment_layers: Any = simulate_deposition(ash_grid) # pyright: ignore[reportUnknownVariableType]
    classified: ClassifiedSediment = classify_sediment(sediment_layers) # pyright: ignore[reportUnknownVariableType]
    plot_distribution(classified)

if __name__ == "__main__":
    main()
