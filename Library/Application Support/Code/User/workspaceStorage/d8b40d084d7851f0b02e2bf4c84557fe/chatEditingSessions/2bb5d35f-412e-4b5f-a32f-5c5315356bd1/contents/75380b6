try:
    import numpy as np
    from numpy.typing import NDArray
except ImportError:
    raise ImportError("The 'numpy' package is required but not installed. Please install it with 'pip install numpy'.")
from volcanic.ash_dispersion import simulate_ash_cloud  # type: ignore
from volcanic.ocean_deposition import simulate_deposition  # type: ignore[import]
from volcanic.density_classifier import classify_sediment, ClassifiedSediment  # type: ignore[import]
from visualizations.ash_distribution_plot import plot_distribution  # type: ignore[import]

def main():
    ash_grid: NDArray = simulate_ash_cloud()
    sediment_layers = simulate_deposition(ash_grid)
    classified: ClassifiedSediment = classify_sediment(sediment_layers)
    plot_distribution(classified)

if __name__ == "__main__":
    main()
