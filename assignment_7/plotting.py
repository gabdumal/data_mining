import itertools
from typing import Literal

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from IPython.display import HTML, display

from features import get_name_of_column

SET2_PALETTE = [
    plt.cm.Set2(index / (plt.cm.Set2.N - 1)) for index in range(plt.cm.Set2.N)
]
DEFAULT_COLOR = SET2_PALETTE[1]

colors = [
    SET2_PALETTE[1],
    *(color for index, color in enumerate(SET2_PALETTE) if index != 1),
]


def get_numerical_range(
    series: pd.Series,
):
    min_value, max_value = series.min(), series.max()
    if hasattr(min_value, "strftime") and hasattr(max_value, "strftime"):
        min_text = min_value.strftime("%Y-%m-%d")
        max_text = max_value.strftime("%Y-%m-%d")
    else:
        min_text = str(min_value)
        max_text = str(max_value)
    return f"[{min_text}, {max_text}]"


FeatureType = Literal["categorical", "numerical", "other"]


def display_feature_description(
    series: pd.Series,
    type_name: str,
    feature_type: FeatureType = "other",
    age_range: pd.Series | None = None,
):
    column_name = series.name

    if not isinstance(column_name, str):
        raise TypeError("The series must have a string column name.")

    descriptive_name = get_name_of_column(column_name)
    block_to_display = f"<table><caption>{descriptive_name}</caption><tbody>"

    block_to_display += f"""
    <tr><th>ID</th><td colspan="2">{series.name}</td></tr>
    <tr><th>Tipo</th><td colspan="2">{type_name}</td></tr>"""

    if feature_type == "categorical":
        values = sorted(series.dropna().unique().tolist())
        values_html = (
            "<ul style='list-style-type: none;'>"
            + "".join(f"<li>{v}</li>" for v in values)
            + "</ul>"
        )
        block_to_display += f"<tr><th>Valores</th><td>{values_html}</td></tr>"

    elif feature_type == "numerical":
        block_to_display += f"""<tr><th>Intervalo</th><td colspan="2">{get_numerical_range(series)}</td></tr>"""
        block_to_display += f"""
        <tr><th>Média</th><td colspan="2">{series.mean():.2f}</td></tr>
        <tr><th>Mediana</th><td colspan="2">{series.median():.2f}</td></tr>
        <tr><th>Desvio padrão</th><td colspan="2">{series.std():.2f}</td></tr>
        <tr><th rowspan="5">Percentil</th><th>05%</th><td>{series.quantile(0.05):.2f}</td></tr>
        <tr><th>25%</th><td>{series.quantile(0.25):.2f}</td></tr>
        <tr><th>50%</th><td>{series.quantile(0.5):.2f}</td></tr>
        <tr><th>75%</th><td>{series.quantile(0.75):.2f}</td></tr>
        <tr><th>95%</th><td>{series.quantile(0.95):.2f}</td></tr>"""
        if age_range is not None:
            set_boxplot_by_age_range(
                series=series,
                age_range=age_range,
                label=descriptive_name,
            )
        else:
            set_boxplot(
                series=series,
                label=descriptive_name,
            )

    display(HTML(block_to_display + "</tbody></table>"))
    plt.show()


def _set_boxplot(
    boxplot_data: list[np.ndarray],
    labels: list[str],
    label: str,
    xlabel: str,
    title: str | None,
    figsize: tuple[float, float],
    colors=None,
):
    if colors is None:
        colors = [DEFAULT_COLOR] * len(boxplot_data)

    fig, ax = plt.subplots(figsize=figsize)

    boxplot = ax.boxplot(
        boxplot_data,
        tick_labels=labels,
        patch_artist=True,
    )

    for box, color in zip(boxplot["boxes"], colors):
        box.set_facecolor(color)

    ax.set_xlabel(xlabel, fontsize=18)
    ax.set_ylabel(label, fontsize=18)

    if title is not None:
        ax.set_title(title, fontsize=20)

    ax.tick_params(axis="both", labelsize=16)
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    fig.tight_layout()
    return fig, ax


def set_boxplot(
    series: pd.Series,
    label: str | None = None,
    title: str | None = None,
    figsize: tuple[float, float] = (18, 9),
):
    data = series.dropna().to_numpy()

    if label is None:
        column_name = series.name
        label = (
            get_name_of_column(column_name)
            if isinstance(column_name, str)
            else str(column_name)
        )

    return _set_boxplot(
        boxplot_data=[data],
        labels=["Geral"],
        label=label,
        xlabel="Boxplot",
        title=title,
        figsize=figsize,
        colors=[DEFAULT_COLOR],
    )


def set_boxplot_by_age_range(
    series: pd.Series,
    age_range: pd.Series,
    label: str | None = None,
    title: str | None = None,
    figsize: tuple[float, float] = (18, 9),
):
    if len(series) != len(age_range):
        raise ValueError("series and age_range must have the same length.")

    data = pd.DataFrame(
        {
            "value": series,
            "age_range": age_range,
        }
    ).dropna(subset=["value", "age_range"])

    boxplot_data: list[np.ndarray] = [data["value"].to_numpy(dtype=float)]
    labels: list[str] = ["Geral"]

    for age_range_value in age_range.cat.categories:
        mask = data["age_range"] == age_range_value
        values = data["value"][mask].to_numpy(dtype=float)

        if len(values) == 0:
            continue

        boxplot_data.append(values)
        labels.append(str(age_range_value))

    if label is None:
        column_name = series.name
        label = (
            get_name_of_column(column_name)
            if isinstance(column_name, str)
            else str(column_name)
        )

    colors = [
        SET2_PALETTE[1],
        *(color for index, color in enumerate(SET2_PALETTE) if index != 1),
    ]

    colors = colors[: len(boxplot_data)]

    return _set_boxplot(
        boxplot_data=boxplot_data,
        labels=labels,
        label=label,
        xlabel="Faixa etária",
        title=title,
        colors=colors,
        figsize=figsize,
    )


def plot_bar_graph(
    series: pd.Series,
    label: str | None = None,
    title: str | None = None,
    show_value: bool = True,
    percentage_function=None,
    y_tick_step: int | None = None,
    sort_by: str = "natural",
    figsize=(18, 9),
    color=DEFAULT_COLOR,
):
    if sort_by == "natural":
        data = series.sort_index()
    elif sort_by == "frequency":
        data = series.sort_values(ascending=False)
    else:
        raise ValueError("sort_by must be either 'natural' or 'frequency'")

    values = data.to_numpy(dtype=float)

    fig, ax = plt.subplots(figsize=figsize)

    x = range(len(data))

    ax.bar(
        x,
        values,
        color=color,
        edgecolor="black",
    )

    ax.set_xticks(x)
    ax.set_xticklabels(
        data.index,
        rotation=45,
        ha="right",
        fontsize=16,
    )

    ax.tick_params(
        axis="y",
        labelsize=16,
    )

    x_axis_label = label

    if x_axis_label is None:
        column_name = series.name
        x_axis_label = (
            get_name_of_column(column_name)
            if isinstance(column_name, str)
            else str(column_name)
        )

    ax.set_xlabel(
        x_axis_label,
        fontsize=18,
    )

    ax.set_ylabel(
        "Quantidade",
        fontsize=18,
    )

    if title is not None:
        ax.set_title(
            title,
            fontsize=20,
        )

    if y_tick_step is not None:
        ax.set_yticks(
            range(
                0,
                int(data.max()) + y_tick_step,
                y_tick_step,
            )
        )

        ax.grid(
            axis="y",
            linestyle="--",
            alpha=0.5,
        )

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
                fontsize=16,
            )

        if len(values) > 0:
            ax.set_ylim(top=max(values) * 1.15)

    fig.tight_layout()
    plt.show()


def plot_bar_graph_of_frequency(
    series: pd.Series,
    label: str | None = None,
    title: str | None = None,
    show_value: bool = True,
    show_percentage: bool = True,
    y_tick_step: int | None = None,
    sort_by: str = "natural",
    figsize=(18, 9),
):
    if show_percentage:
        percentage_function = lambda value, data: value / len(series)
    else:
        percentage_function = None
    counts = series.value_counts()
    counts.name = series.name
    plot_bar_graph(
        series=counts,
        percentage_function=percentage_function,
        label=label,
        title=title,
        show_value=show_value,
        y_tick_step=y_tick_step,
        sort_by=sort_by,
        figsize=figsize,
    )


def plot_histogram(
    series: pd.Series,
    bin_width: float = 5,
    label: str | None = None,
    title: str | None = None,
    show_value: bool = True,
    percentage_function=lambda value, data: value / len(data),
    figsize=(18, 9),
    color=DEFAULT_COLOR,
):
    data = series.dropna()

    minimum = data.min()
    maximum = data.max()

    first_bin = minimum - minimum % bin_width

    bin_edges = np.arange(
        first_bin,
        maximum + bin_width,
        bin_width,
    ).tolist()

    fig, ax = plt.subplots(figsize=figsize)

    counts, bin_edges, _ = ax.hist(
        data,
        bins=bin_edges,
        color=color,
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

    ax.set_xlabel(
        x_axis_label,
        fontsize=18,
    )

    ax.set_ylabel(
        "Quantidade",
        fontsize=18,
    )

    if title is not None:
        ax.set_title(
            title,
            fontsize=20,
        )

    bin_centers = [(left + right) / 2 for left, right in itertools.pairwise(bin_edges)]

    ax.set_xticks(bin_centers)

    if bin_width == 1:
        bin_labels = [f"{left:.0f}" for left, _ in itertools.pairwise(bin_edges)]
    else:
        bin_labels = [
            f"{left:g}–{right:g}" for left, right in itertools.pairwise(bin_edges)
        ]

    ax.set_xticklabels(
        bin_labels,
        rotation=45,
        ha="right",
        fontsize=16,
    )

    ax.tick_params(
        axis="y",
        labelsize=16,
    )

    if show_value or percentage_function is not None:
        for count, center in zip(counts, bin_centers):
            count = float(count)

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

        ax.set_ylim(top=float(max(counts)) * 1.15)

    fig.tight_layout()
    plt.show()
