

def plot_distribution(classified_layers):
    """
    Plots the elemental sediment distribution.

    Parameters:
        classified_layers (dict): Output from classify_sediment().
    """


    try:
        import matplotlib.pyplot as plt
        from matplotlib.axes import Axes
    except ImportError:
        raise ImportError("matplotlib is not installed. Please install it with 'pip install matplotlib'.")

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
        im = ax.imshow(data, cmap="inferno")
        ax.set_title(title) # pyright: ignore[reportUnknownMemberType]
        plt.colorbar(im, ax=ax)  # type: ignore

    plt.tight_layout() # pyright: ignore[reportUnknownMemberType]
    plt.show()  # type: ignore[reportUnknownMemberType]
