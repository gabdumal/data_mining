import matplotlib.pyplot as plt
import pandas as pd

from data import names_of_columns


def generate_histogram(
    series: pd.Series, label: str | None = None, bins: int | None = None
):
    plt.figure(figsize=(10, 5))
    plt.ylabel("Quantidade")
    plt.xlabel(label if label != None else names_of_columns[series.name])
    plt.hist(
        series.dropna(),
        bins=bins,
    )
    plt.show()


def generate_bar_graph(series: pd.Series, label: str | None = None):
    counts = series.value_counts()
    fig, ax = plt.subplots(figsize=(10, 5))
    x = range(len(counts))
    ax.bar(x, counts.values)
    ax.set_xticks(x)
    ax.set_xticklabels(
        counts.index,
        rotation=45,
        ha="right",
    )
    ax.set_xlabel(label if label != None else names_of_columns[series.name])
    ax.set_ylabel("Quantidade")
    fig.tight_layout()
    plt.show()
