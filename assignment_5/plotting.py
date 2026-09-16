import matplotlib.pyplot as plt
import pandas as pd

from columns import get_name_of_column
import itertools


def plot_bar_graph(
    series: pd.Series,
    label: str | None = None,
    title: str | None = None,
    show_value: bool = False,
    percentage_function=None,
    y_tick_step: int | None = None,
    sort_by: str = "natural",
):
    if sort_by == "natural":
        data = series.sort_index()
    elif sort_by == "frequency":
        data = series.sort_values(ascending=False)
    else:
        raise ValueError("sort_by must be either 'natural' or 'frequency'")

    values = data.to_numpy(dtype=float)

    fig, ax = plt.subplots(figsize=(20, 10))

    x = range(len(data))

    ax.bar(x, values)

    ax.set_xticks(x)
    ax.set_xticklabels(
        data.index,
        rotation=45,
        ha="right",
    )

    x_axis_label = label

    if x_axis_label is None:
        column_name = series.name
        x_axis_label = (
            get_name_of_column(column_name)
            if isinstance(column_name, str)
            else str(column_name)
        )

    ax.set_xlabel(x_axis_label)
    ax.set_ylabel("Quantidade")

    if title is not None:
        ax.set_title(title)

    if y_tick_step is not None:
        ax.set_yticks(
            range(
                0,
                int(data.max()) + y_tick_step,
                y_tick_step,
            )
        )
        ax.grid(axis="y", linestyle="--", alpha=0.5)

    if show_value or percentage_function is not None:
        for i, value in enumerate(data):
            auxiliary_text = ""

            if show_value:
                auxiliary_text += f"{value:.0f}"

            if percentage_function is not None:
                if show_value:
                    auxiliary_text += "\n"

                percentage = percentage_function(value, data)
                auxiliary_text += f"{percentage:.1%}"

            ax.text(
                i,
                value,
                auxiliary_text,
                ha="center",
                va="bottom",
                fontsize=8,
            )

    fig.tight_layout()
    plt.show()


def plot_histogram(
    series: pd.Series,
    bin_width: int,
    label: str | None = None,
    title: str | None = None,
    show_value: bool = False,
    percentage_function=None,
):
    data = series.dropna()

    minimum = int(data.min())
    maximum = int(data.max())

    first_bin = minimum - minimum % bin_width

    bin_edges = range(
        first_bin,
        maximum + bin_width + 1,
        bin_width,
    )

    fig, ax = plt.subplots(figsize=(24, 10))

    counts, bin_edges, _ = ax.hist(
        data,
        bins=bin_edges,
        edgecolor="black",
        rwidth=0.8,
    )

    x_axis_label = label

    if x_axis_label is None:
        column_name = series.name
        x_axis_label = (
            get_name_of_column(column_name)
            if isinstance(column_name, str)
            else str(column_name)
        )

    ax.set_xlabel(x_axis_label, fontsize=18)
    ax.set_ylabel("Quantidade", fontsize=18)

    if title is not None:
        ax.set_title(title, fontsize=20)

    bin_centers = [(left + right) / 2 for left, right in itertools.pairwise(bin_edges)]

    ax.set_xticks(bin_centers)

    ax.set_xticklabels(
        [
            f"{left:.0f}–{right - 1:.0f}"
            for left, right in itertools.pairwise(bin_edges)
        ],
        rotation=45,
        ha="right",
        fontsize=16,
    )

    ax.tick_params(axis="y", labelsize=16)

    if show_value or percentage_function is not None:
        for count, center in zip(counts, bin_centers):
            if count == 0:
                continue

            auxiliary_text = ""

            if show_value:
                auxiliary_text += f"{int(count)}"

            if percentage_function is not None:
                if show_value:
                    auxiliary_text += "\n"

                percentage = percentage_function(count, data)
                auxiliary_text += f"{percentage:.1%}"

            ax.text(
                center,
                count,
                auxiliary_text,
                ha="center",
                va="bottom",
                fontsize=16,
            )
        ax.set_ylim(top=max(counts) * 1.15)

    fig.tight_layout()
    plt.show()
