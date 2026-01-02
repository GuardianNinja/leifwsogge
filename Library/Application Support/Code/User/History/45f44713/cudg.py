
def plot_distribution(classified_layers):
    """
    Plots the elemental sediment distribution.

    Parameters:
        classified_layers (dict): Output from classify_sediment().
    """

    try:
    except ImportError:
        try:
            import sys
            import importlib
            plt = importlib.import_module('matplotlib.pyplot')
        except Exception:
            raise ImportError("matplotlib is required for plotting. Please install it with 'pip install matplotlib'.")

    axes = plt.subplots(1, 3, figsize=(15, 5))[1]  # pyright: ignore[reportUnknownMemberType]

    elements = ["Si_Al", "Fe_Mg", "Pb_U"]
    titles = [
        "Fine Ash (Si, Al)",
        "Medium Ash (Fe, Mg)",
        "Coarse Ash (Pb, U)"
    ]


    import numpy as np
    for ax, key, title in zip(axes, elements, titles):  # pyright: ignore[reportUnknownArgumentType]
        ax: Axes
        data: np.ndarray = classified_layers[key]
        im: AxesImage = ax.imshow(data, cmap="inferno")
        ax.set_title(title)
        plt.colorbar(im, ax=ax)  # type: ignore

    plt.tight_layout() # pyright: ignore[reportUnknownMemberType]
    plt.show()  # type: ignore[reportUnknownMemberType]
