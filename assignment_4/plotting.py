import matplotlib.pyplot as plt
import pandas as pd

from columns import get_name_of_column


def plot_bar_graph(
    series: pd.Series,
    label: str | None = None,
    title: str | None = None,
    show_percentage: bool = False,
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

    if show_percentage:
        total = data.sum()

        for i, value in enumerate(data):
            percentage = value / total * 100

            ax.text(
                i,
                value,
                f"{percentage:.1f}%",
                ha="center",
                va="bottom",
                fontsize=8,
            )

    fig.tight_layout()
    plt.show()
