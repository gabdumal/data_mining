import itertools
from collections.abc import Callable
from typing import Literal

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from IPython.display import HTML, display

from data import df
from features import get_name_of_feature

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

FIGSIZE = (18, 9)

TITLE_FONTSIZE = 20
AXIS_LABEL_FONTSIZE = 18
TICK_FONTSIZE = 16
VALUE_FONTSIZE = 16
LEGEND_FONTSIZE = 14
LEGEND_TITLE_FONTSIZE = 15

SET2_PALETTE = [
    plt.cm.Set2(index / (plt.cm.Set2.N - 1)) for index in range(plt.cm.Set2.N)
]

DEFAULT_COLOR = SET2_PALETTE[1]


# ---------------------------------------------------------------------------
# General helpers
# ---------------------------------------------------------------------------


def _get_series_label(series: pd.Series) -> str:
    column_name = series.name

    if isinstance(column_name, str):
        return get_name_of_feature(column_name)

    return str(column_name)


def _get_colors(
    amount: int,
    start_index: int = 0,
) -> list:
    return [
        SET2_PALETTE[index % len(SET2_PALETTE)]
        for index in range(start_index, start_index + amount)
    ]


def _get_age_group_colors(
    amount: int,
    contains_general: bool = True,
) -> list:
    """
    First color is reserved for 'General' (Set2[1]).
    Remaining colors follow the Set2 palette while skipping Set2[1].
    """
    age_group_colors = [color for index, color in enumerate(SET2_PALETTE) if index != 1]

    if contains_general:
        age_group_colors.insert(0, DEFAULT_COLOR)

    return age_group_colors[:amount]


def _configure_axes(
    ax,
    xlabel: str | None = None,
    ylabel: str | None = None,
    title: str | None = None,
):
    if xlabel is not None:
        ax.set_xlabel(
            xlabel,
            fontsize=AXIS_LABEL_FONTSIZE,
        )

    if ylabel is not None:
        ax.set_ylabel(
            ylabel,
            fontsize=AXIS_LABEL_FONTSIZE,
        )

    if title is not None:
        ax.set_title(
            title,
            fontsize=TITLE_FONTSIZE,
        )

    ax.tick_params(
        axis="both",
        labelsize=TICK_FONTSIZE,
    )

    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.5,
    )


def _annotate_bars(
    ax,
    bars,
    formatter: Callable[[float], str] = lambda value: f"{value:.0f}",
    fontsize: int = VALUE_FONTSIZE,
):
    for bar in bars:
        value = bar.get_height()

        if value <= 0:
            continue

        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value,
            formatter(value),
            ha="center",
            va="bottom",
            fontsize=fontsize,
        )


def _set_y_limit_for_annotations(
    ax,
    values,
    padding: float = 1.20,
):
    values = np.asarray(values)

    if len(values) == 0:
        return

    maximum = values.max()

    if maximum > 0:
        ax.set_ylim(top=float(maximum) * padding)


def _finish_plot(fig):
    fig.tight_layout()
    plt.show()


# ---------------------------------------------------------------------------
# Numerical description
# ---------------------------------------------------------------------------


def get_numerical_range(
    series: pd.Series,
):
    min_value = series.min()
    max_value = series.max()

    if hasattr(min_value, "strftime") and hasattr(max_value, "strftime"):
        min_text = min_value.strftime("%Y-%m-%d")
        max_text = max_value.strftime("%Y-%m-%d")
    else:
        min_text = str(min_value)
        max_text = str(max_value)

    return f"[{min_text}, {max_text}]"


# ---------------------------------------------------------------------------
# Feature description
# ---------------------------------------------------------------------------

FeatureType = Literal[
    "categorical",
    "numerical",
    "other",
]


def display_feature_description(
    series: pd.Series,
    type_name: str,
    feature_type: FeatureType = "other",
    age_group: pd.Series | None = None,
):
    column_name = series.name

    if not isinstance(column_name, str):
        raise TypeError("The series must have a string column name.")

    descriptive_name = get_name_of_feature(column_name)

    block_to_display = f"""
    <table>
        <caption>{descriptive_name}</caption>
        <tbody>
            <tr>
                <th>ID</th>
                <td colspan="2">{column_name}</td>
            </tr>
            <tr>
                <th>Tipo</th>
                <td colspan="2">{type_name}</td>
            </tr>
    """

    if feature_type == "categorical":
        values = sorted(series.dropna().unique().tolist())

        values_html = (
            "<ul style='list-style-type: none;'>"
            + "".join(f"<li>{value}</li>" for value in values)
            + "</ul>"
        )

        block_to_display += f"""
            <tr>
                <th>Valores</th>
                <td>{values_html}</td>
            </tr>
        """

    elif feature_type == "numerical":
        block_to_display += f"""
            <tr>
                <th>Intervalo</th>
                <td colspan="2">
                    {get_numerical_range(series)}
                </td>
            </tr>
            <tr>
                <th>Média</th>
                <td colspan="2">{series.mean():.2f}</td>
            </tr>
            <tr>
                <th>Mediana</th>
                <td colspan="2">{series.median():.2f}</td>
            </tr>
            <tr>
                <th>Desvio padrão</th>
                <td colspan="2">{series.std():.2f}</td>
            </tr>
            <tr>
                <th rowspan="5">Percentil</th>
                <th>05%</th>
                <td>{series.quantile(0.05):.2f}</td>
            </tr>
            <tr>
                <th>25%</th>
                <td>{series.quantile(0.25):.2f}</td>
            </tr>
            <tr>
                <th>50%</th>
                <td>{series.quantile(0.50):.2f}</td>
            </tr>
            <tr>
                <th>75%</th>
                <td>{series.quantile(0.75):.2f}</td>
            </tr>
            <tr>
                <th>95%</th>
                <td>{series.quantile(0.95):.2f}</td>
            </tr>
        """

        if age_group is None:
            set_boxplot(
                series=series,
                label=descriptive_name,
            )
        else:
            set_boxplot_by_age_group(
                series=series,
                age_group=age_group,
                label=descriptive_name,
            )

    block_to_display += """
        </tbody>
    </table>
    """

    display(HTML(block_to_display))


# ---------------------------------------------------------------------------
# Boxplots
# ---------------------------------------------------------------------------


def _set_boxplot(
    boxplot_data: list[np.ndarray],
    labels: list[str],
    label: str,
    xlabel: str,
    title: str | None = None,
    figsize: tuple[float, float] = FIGSIZE,
    colors: list | None = None,
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

    _configure_axes(
        ax=ax,
        xlabel=xlabel,
        ylabel=label,
        title=title,
    )

    fig.tight_layout()

    return fig, ax


def set_boxplot(
    series: pd.Series,
    label: str | None = None,
    title: str | None = None,
    figsize: tuple[float, float] = FIGSIZE,
):
    data = series.dropna().to_numpy(dtype=float)

    if label is None:
        label = _get_series_label(series)

    return _set_boxplot(
        boxplot_data=[data],
        labels=["General"],
        label=label,
        xlabel="Boxplot",
        title=title,
        figsize=figsize,
        colors=[DEFAULT_COLOR],
    )


def set_boxplot_by_age_group(
    series: pd.Series,
    age_group: pd.Series,
    label: str | None = None,
    title: str | None = None,
    figsize: tuple[float, float] = FIGSIZE,
):
    if len(series) != len(age_group):
        raise ValueError("series and age_group must have the same length.")

    data = pd.DataFrame(
        {
            "value": series,
            "age_group": age_group,
        }
    ).dropna(subset=["value", "age_group"])

    boxplot_data: list[np.ndarray] = [data["value"].to_numpy(dtype=float)]

    labels: list[str] = ["General"]

    for age_group_value in age_group.cat.categories:
        mask = data["age_group"] == age_group_value

        values = data["value"][mask].to_numpy(dtype=float)

        if len(values) == 0:
            continue

        boxplot_data.append(values)
        labels.append(str(age_group_value))

    if label is None:
        label = _get_series_label(series)

    colors = _get_age_group_colors(len(boxplot_data))

    return _set_boxplot(
        boxplot_data=boxplot_data,
        labels=labels,
        label=label,
        xlabel="Age group",
        title=title,
        figsize=figsize,
        colors=colors,
    )


# ---------------------------------------------------------------------------
# Simple bar graph
# ---------------------------------------------------------------------------

SortBy = Literal[
    "natural",
    "frequency",
]


def plot_bar_graph(
    series: pd.Series,
    label: str | None = None,
    title: str | None = None,
    show_value: bool = True,
    percentage_function: Callable | None = None,
    y_tick_step: int | None = None,
    sort_by: SortBy = "natural",
    figsize: tuple[float, float] = FIGSIZE,
    color=DEFAULT_COLOR,
):
    if sort_by == "natural":
        data = series.sort_index()
    elif sort_by == "frequency":
        data = series.sort_values(ascending=False)
    else:
        raise ValueError("sort_by must be either 'natural' or 'frequency'")

    values = data.to_numpy(dtype=float)

    if label is None:
        label = _get_series_label(series)

    fig, ax = plt.subplots(figsize=figsize)

    x = np.arange(len(data))

    bars = ax.bar(
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
        fontsize=TICK_FONTSIZE,
    )

    _configure_axes(
        ax=ax,
        xlabel=label,
        ylabel="Amount",
        title=title,
    )

    if y_tick_step is not None:
        ax.set_yticks(
            range(
                0,
                int(data.max()) + y_tick_step,
                y_tick_step,
            )
        )

    if show_value or percentage_function is not None:

        def formatter(value):
            text = ""

            if show_value:
                text += f"{value:.0f}"

            if percentage_function is not None:
                if show_value:
                    text += "\n"

                percentage = percentage_function(
                    value,
                    data,
                )

                text += f"{percentage:.1%}"

            return text

        _annotate_bars(
            ax,
            bars,
            formatter=formatter,
        )

        _set_y_limit_for_annotations(
            ax,
            values,
        )

    _finish_plot(fig)


# ---------------------------------------------------------------------------
# Frequency bar graph
# ---------------------------------------------------------------------------


def plot_bar_graph_of_frequency(
    series: pd.Series,
    label: str | None = None,
    title: str | None = None,
    show_value: bool = True,
    show_percentage: bool = True,
    y_tick_step: int | None = None,
    sort_by: SortBy = "natural",
    figsize: tuple[float, float] = FIGSIZE,
):
    counts = series.value_counts()
    counts.name = series.name

    percentage_function = None

    if show_percentage:
        total = len(series.dropna())

        percentage_function = lambda value, data: value / total

    plot_bar_graph(
        series=counts,
        label=label,
        title=title,
        show_value=show_value,
        percentage_function=percentage_function,
        y_tick_step=y_tick_step,
        sort_by=sort_by,
        figsize=figsize,
    )


# ---------------------------------------------------------------------------
# Grouped bar graph
# ---------------------------------------------------------------------------


def plot_grouped_bar_graph(
    data: pd.DataFrame,
    label: str,
    xlabel: str = "Age group",
    ylabel: str = "Amount",
    title: str | None = None,
    show_value: bool = True,
    figsize: tuple[float, float] = FIGSIZE,
):
    if data.empty:
        raise ValueError("Data must contain at least one row and one column.")

    fig, ax = plt.subplots(figsize=figsize)

    x = np.arange(len(data.index))
    number_of_groups = len(data.columns)

    width = 0.8 / number_of_groups

    colors = _get_colors(number_of_groups)

    for index, column in enumerate(data.columns):
        offset = (index - (number_of_groups - 1) / 2) * width

        bars = ax.bar(
            x + offset,
            data[column],
            width,
            label=str(column),
            color=colors[index],
            edgecolor="black",
        )

        if show_value:
            _annotate_bars(
                ax,
                bars,
                formatter=lambda value: f"{value:.0f}",
            )

    ax.set_xticks(x)
    ax.set_xticklabels(
        data.index,
        fontsize=TICK_FONTSIZE,
    )

    _configure_axes(
        ax=ax,
        xlabel=xlabel,
        ylabel=ylabel,
        title=title,
    )

    ax.legend(
        title=label,
        fontsize=LEGEND_FONTSIZE,
        title_fontsize=LEGEND_TITLE_FONTSIZE,
        ncol=number_of_groups,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.12),
    )

    all_values = data.to_numpy().ravel()

    if show_value:
        _set_y_limit_for_annotations(
            ax,
            all_values,
        )

    _finish_plot(fig)


def plot_bar_graph_of_frequency_by_age_group(
    series: pd.Series,
    age_group: pd.Series = df["age_group"],
    label: str | None = None,
    title: str | None = None,
    columns: list | None = None,
    figsize: tuple[float, float] = FIGSIZE,
):
    if len(series) != len(age_group):
        raise ValueError("series and age_group must have the same length.")

    frequency = pd.crosstab(
        age_group,
        series,
    )

    if hasattr(age_group.dtype, "categories"):
        frequency = frequency.reindex(
            index=age_group.cat.categories,
            fill_value=0,
        )

    if columns is not None:
        frequency = frequency.reindex(
            columns=columns,
            fill_value=0,
        )

    if label is None:
        label = _get_series_label(series)

    plot_grouped_bar_graph(
        data=frequency,
        label=label,
        title=title,
        figsize=figsize,
    )


# ---------------------------------------------------------------------------
# Histogram
# ---------------------------------------------------------------------------


def _get_histogram_bins(
    series: pd.Series,
    bin_width: float,
) -> np.ndarray:
    data = series.dropna()

    if data.empty:
        raise ValueError("Cannot create a histogram from an empty series.")

    if bin_width <= 0:
        raise ValueError("bin_width must be greater than zero.")

    minimum = data.min()
    maximum = data.max()

    first_bin = minimum - minimum % bin_width

    bin_edges = np.arange(
        first_bin,
        maximum + bin_width,
        bin_width,
    )

    if len(bin_edges) < 2:
        bin_edges = np.array(
            [
                first_bin,
                first_bin + bin_width,
            ]
        )

    return bin_edges


def _format_histogram_bins(
    bin_edges: np.ndarray,
    bin_width: float,
) -> list[str]:
    if bin_width == 1:
        return [f"{left:.0f}" for left, _ in itertools.pairwise(bin_edges)]

    return [f"{left:g}–{right:g}" for left, right in itertools.pairwise(bin_edges)]


def _plot_histogram_on_axis(
    ax,
    data: pd.Series,
    bin_edges: np.ndarray,
    color,
    show_value: bool = True,
    percentage_function=None,
):
    counts, actual_bin_edges, _ = ax.hist(
        data,
        bins=bin_edges,
        color=color,
        edgecolor="black",
        rwidth=0.8,
    )

    if show_value or percentage_function is not None:
        bin_centers = (actual_bin_edges[:-1] + actual_bin_edges[1:]) / 2

        for count, center in zip(counts, bin_centers):
            count = float(count)

            if count == 0:
                continue

            text = ""

            if show_value:
                text += f"{int(count)}"

            if percentage_function is not None:
                if show_value:
                    text += "\n"

                percentage = percentage_function(count, data)
                text += f"{percentage:.1%}"

            ax.text(
                center,
                count,
                text,
                ha="center",
                va="bottom",
                fontsize=VALUE_FONTSIZE,
            )

    _set_y_limit_for_annotations(
        ax,
        counts,
        padding=1.25,
    )

    return counts, actual_bin_edges


def plot_histogram(
    series: pd.Series,
    bin_width: float = 5,
    label: str | None = None,
    title: str | None = None,
    show_value: bool = True,
    show_percentage: bool = True,
    figsize: tuple[float, float] = FIGSIZE,
    color=DEFAULT_COLOR,
):
    data = series.dropna()

    if data.empty:
        raise ValueError("Cannot create a histogram from an empty series.")

    if bin_width <= 0:
        raise ValueError("bin_width must be greater than zero.")

    if label is None:
        label = _get_series_label(series)

    bin_edges = _get_histogram_bins(
        series=data,
        bin_width=bin_width,
    )

    percentage_function = lambda value, data: (
        value / len(data) if show_percentage else None
    )

    fig, ax = plt.subplots(figsize=figsize)

    _, actual_bin_edges = _plot_histogram_on_axis(
        ax=ax,
        data=data,
        bin_edges=bin_edges,
        color=color,
        show_value=show_value,
        percentage_function=percentage_function,
    )

    # Put one tick at the center of each actual bar.
    bin_centers = (actual_bin_edges[:-1] + actual_bin_edges[1:]) / 2

    ax.set_xticks(bin_centers)
    ax.set_xticklabels(
        _format_histogram_bins(
            actual_bin_edges,
            bin_width,
        ),
        rotation=45,
        ha="right",
        fontsize=TICK_FONTSIZE,
    )

    _configure_axes(
        ax,
        xlabel=label,
        ylabel="Amount",
        title=title,
    )

    _finish_plot(fig)


def plot_histogram_by_age_group(
    series: pd.Series,
    age_group: pd.Series = df["age_group"],
    bin_width: float = 2,
    label: str | None = None,
    title: str | None = None,
    show_value: bool = True,
    show_percentage: bool = True,
    figsize: tuple[float, float] = (18, 27),
):
    if len(series) != len(age_group):
        raise ValueError("series and age_group must have the same length.")

    if label is None:
        label = _get_series_label(series)

    data = pd.DataFrame(
        {
            "value": series,
            "age_group": age_group,
        }
    ).dropna(subset=["value", "age_group"])

    # Use the same bins for every histogram.
    bin_edges = _get_histogram_bins(
        data["value"],
        bin_width,
    )

    groups: list[tuple[str, pd.Series]] = []

    for age_group_value in age_group.cat.categories:
        mask = data["age_group"] == age_group_value
        group_data = data["value"][mask]

        if group_data.empty:
            continue

        groups.append((str(age_group_value), group_data))

    colors = _get_age_group_colors(len(groups), contains_general=False)

    fig, axes = plt.subplots(
        nrows=len(groups),
        ncols=1,
        figsize=figsize,
        sharex=True,
    )

    # np.ndarray when there are multiple plots,
    # but a single Axes object when there is only one.
    axes = np.atleast_1d(axes)

    for index, (
        group_name,
        group_data,
    ) in enumerate(groups):
        ax = axes[index]

        counts, _, _ = ax.hist(
            group_data,
            bins=bin_edges,
            color=colors[index],
            edgecolor="black",
            rwidth=0.8,
        )

        ax.set_ylabel(
            group_name,
            fontsize=AXIS_LABEL_FONTSIZE,
        )

        ax.tick_params(
            axis="y",
            labelsize=TICK_FONTSIZE,
        )

        ax.grid(
            axis="y",
            linestyle="--",
            alpha=0.5,
        )

        if show_value or show_percentage:
            total = len(group_data)

            for count, left, right in zip(
                counts,
                bin_edges[:-1],
                bin_edges[1:],
            ):
                if count == 0:
                    continue

                center = (left + right) / 2

                text = ""

                if show_value:
                    text += f"{int(count)}"

                if show_percentage:
                    if show_value:
                        text += "\n"

                    text += f"{count / total:.1%}"

                ax.text(
                    center,
                    count,
                    text,
                    ha="center",
                    va="bottom",
                    fontsize=VALUE_FONTSIZE,
                )

        _set_y_limit_for_annotations(
            ax,
            counts,
            padding=1.25,
        )

    axes[-1].set_xlabel(
        label,
        fontsize=AXIS_LABEL_FONTSIZE,
    )

    bin_labels = _format_histogram_bins(
        bin_edges,
        bin_width,
    )

    axes[-1].set_xticks(
        [(left + right) / 2 for left, right in itertools.pairwise(bin_edges)]
    )

    axes[-1].set_xticklabels(
        bin_labels,
        rotation=45,
        ha="right",
        fontsize=TICK_FONTSIZE,
    )

    if title is not None:
        fig.suptitle(
            title,
            fontsize=TITLE_FONTSIZE,
        )

    fig.tight_layout()

    if title is not None:
        fig.subplots_adjust(top=0.95)

    plt.show()
