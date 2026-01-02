from volcanic.ash_dispersion import simulate_ash_cloud
from volcanic.ocean_deposition import simulate_deposition
from volcanic.density_classifier import classify_sediment
from visualizations.ash_distribution_plot import plot_distribution

def main():
    ash_grid = simulate_ash_cloud()
    sediment_layers = simulate_deposition(ash_grid)
    classified = classify_sediment(sediment_layers)
    plot_distribution(classified)

if __name__ == "__main__":
    main()
