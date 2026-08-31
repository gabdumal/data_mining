import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from data import names_of_columns


def plot_histogram(
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


def plot_bar_graph(series: pd.Series, label: str | None = None):
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


def plot_boxplots_with_clusters_for_numerical_columns(
    data_frame: pd.DataFrame, numerical_columns: list[str]
):
    n = len(numerical_columns)

    fig, axes = plt.subplots(
        nrows=(n + 1) // 2, ncols=2, figsize=(14, 5 * ((n + 1) // 2))
    )

    axes = axes.flatten()

    for ax, col in zip(axes, numerical_columns):
        sns.boxplot(data=data_frame, x="cluster", y=col, ax=ax)

        ax.set_title(f"{col} por cluster")
        ax.set_xlabel("Cluster")
        ax.set_ylabel(names_of_columns[col])

    # remove eixos vazios
    for ax in axes[n:]:
        ax.remove()

    plt.tight_layout()
    plt.show()


def plot_boxplot_pair_with_clusters(data_frame: pd.DataFrame, x_axis: str, y_axis: str):
    fig, ax = plt.subplots(figsize=(14, 6))

    sns.boxplot(
        data=data_frame,
        x=x_axis,
        y=y_axis,
        hue="cluster",
        ax=ax,
        palette="tab10",
    )
    ax.set_title(
        f"{names_of_columns[y_axis]} by {names_of_columns[x_axis]} and cluster"
    )
    ax.set_xlabel(names_of_columns[x_axis])
    ax.set_ylabel(names_of_columns[y_axis])

    plt.tight_layout()
    plt.show()


def plot_scatterplot_with_clusters(data_frame: pd.DataFrame, x_axis: str, y_axis: str):
    sns.scatterplot(
        data=data_frame,
        x=x_axis,
        y=y_axis,
        hue="cluster",
        palette="tab10",
    )
    plt.title(f"Clusters: {names_of_columns[x_axis]} × {names_of_columns[y_axis]}")
    plt.show()


def plot_scatterplot_pair_with_clusters(
    data_frame: pd.DataFrame, x_axis: str, y_axis: str
):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # XY plot
    sns.scatterplot(
        data=data_frame,
        x=x_axis,
        y=y_axis,
        hue="cluster",
        palette="tab10",
        ax=axes[0],
    )
    axes[0].set_title(
        f"Clusters: {names_of_columns[x_axis]} × {names_of_columns[y_axis]}"
    )

    # YX plot
    sns.scatterplot(
        data=data_frame,
        x=y_axis,
        y=x_axis,
        hue="cluster",
        palette="tab10",
        ax=axes[1],
    )
    axes[1].set_title(
        f"Clusters: {names_of_columns[y_axis]} × {names_of_columns[x_axis]}"
    )

    plt.tight_layout()
    plt.show()


def plot_cluster_as_pillar_graph(data_frame: pd.DataFrame, categorical_column: str):
    proportions = (
        pd.crosstab(
            data_frame["cluster"], data_frame[categorical_column], normalize="index"
        )
        * 100
    )

    ax = proportions.plot(kind="bar", stacked=True, figsize=(10, 5))

    plt.title(f"{names_of_columns[categorical_column]} por cluster")
    plt.xlabel("Cluster")
    plt.ylabel("Proporção (%)")
    plt.legend(
        title=names_of_columns[categorical_column],
        bbox_to_anchor=(1.02, 1),
        loc="upper left",
    )
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()


def plot_numerical_by_categorical_and_cluster(
    data_frame: pd.DataFrame, numerical_column: str, categorical_column: str
):
    g = sns.displot(
        data=data_frame,
        x=numerical_column,
        col=categorical_column,
        hue="cluster",
        bins=15,
        kde=False,
        palette="tab10",
        element="step",
        stat="count",
        common_bins=True,
        common_norm=False,
        height=4,
        aspect=1.2,
    )

    g.set_axis_labels(names_of_columns[numerical_column], "Frequência")
    g.set_titles(f"{names_of_columns[categorical_column]}: " + "{col_name}")
    g.figure.suptitle(
        f"Distribuição de {names_of_columns[numerical_column]} por {names_of_columns[categorical_column]} e Cluster",
        y=1.05,
    )

    plt.show()
