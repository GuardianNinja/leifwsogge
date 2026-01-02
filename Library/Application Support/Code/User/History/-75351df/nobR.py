"""
utils.py — Plotting and CSV export utilities
Space Leaf Corp — Internal Use Only
"""

import pandas as pd  # type: ignore
import matplotlib.pyplot as plt

def export_csv(df: pd.DataFrame, filename: str):
    df.to_csv(filename, index=False) # pyright: ignore[reportUnknownMemberType]

def plot_series(t, series_dict, title, xlabel="Days", ylabel="Value", filename=None): # pyright: ignore[reportMissingParameterType]
    plt.figure(figsize=(10,5))
    for label, arr in series_dict.items():
        plt.plot(t, arr, label=label)
    plt.title(title) # pyright: ignore[reportUnknownMemberType]
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(visible=True)
    legend = plt.legend()  # type: ignore[no-untyped-call]
    if filename:
        plt.savefig(filename, dpi=150)
    plt.show()
