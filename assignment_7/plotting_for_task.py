import math
from collections.abc import Mapping

import pandas as pd
from IPython.display import display
from sklearn.model_selection import GridSearchCV


def _build_target_distribution_table(
    train_target,
    test_target,
):
    """Build the train/test target distribution table."""
    train_counts = train_target.value_counts().sort_index()
    test_counts = test_target.value_counts().sort_index()

    distribution = pd.DataFrame(
        {
            "Train N": train_counts,
            "Test N": test_counts,
        }
    ).fillna(0)

    distribution["Total N"] = distribution["Train N"] + distribution["Test N"]

    distribution["Train %"] = distribution["Train N"] / distribution["Total N"] * 100

    distribution["Test %"] = distribution["Test N"] / distribution["Total N"] * 100

    general = pd.DataFrame(
        {
            "Age Group": ["General"],
            "Train N": [train_target.size],
            "Test N": [test_target.size],
            "Total N": [train_target.size + test_target.size],
            "Train %": [
                train_target.size / (train_target.size + test_target.size) * 100
            ],
            "Test %": [test_target.size / (train_target.size + test_target.size) * 100],
        }
    )

    distribution = distribution.reset_index(names="Age Group")

    return pd.concat(
        [distribution, general],
        ignore_index=True,
    )


def _display_target_distribution(
    distribution,
    title="Target Distribution Across Train and Test Sets",
):
    """Display the train/test target distribution."""
    table = distribution.copy()

    for column in ["Train %", "Test %"]:
        table[column] = table[column].map(lambda value: f"{value:.1f}%")

    display(table.style.hide(axis="index").set_caption(title))


def display_train_test_target_distribution(
    train_target,
    test_target,
):
    """Display the target distribution in train and test sets."""
    distribution = _build_target_distribution_table(
        train_target,
        test_target,
    )

    _display_target_distribution(distribution)

    return distribution


def _highlight_better_within_group(
    data_frame,
    group_column,
    metric_columns,
    higher_is_better=True,
):
    """Highlight the better metric value within each group."""

    styles = pd.DataFrame(
        "",
        index=data_frame.index,
        columns=data_frame.columns,
    )

    for _, group in data_frame.groupby(
        group_column,
        sort=False,
        observed=True,
    ):
        for metric in metric_columns:
            if higher_is_better:
                best_value = group[metric].max()
            else:
                best_value = group[metric].min()

            best_rows = group[metric].eq(best_value)

            styles.loc[
                group.index[best_rows],
                metric,
            ] = "font-weight: bold"

    return styles


def display_cross_validation_results(
    results,
    metric_columns,
    caption,
    group_column="Seed",
):
    """Display cross-validation results with better values highlighted."""

    styled_results = (
        results.style.hide(axis="index")
        .format({metric: "{:.3f}" for metric in metric_columns})
        .set_caption(caption)
        .apply(
            _highlight_better_within_group,
            axis=None,
            group_column=group_column,
            metric_columns=metric_columns,
            higher_is_better=True,
        )
    )

    display(styled_results)


def display_cross_validation_summary(
    comparison,
    metric_columns,
    caption,
):
    """Display mean ± standard deviation cross-validation results."""

    display_columns = [
        "Strategy",
        *metric_columns,
    ]

    styled_comparison = (
        comparison[display_columns].style.hide(axis="index").set_caption(caption)
    )

    for metric in metric_columns:
        mean_column = f"{metric} mean"

        maximum = comparison[mean_column].max()

        maximum_strategy = comparison.loc[
            comparison[mean_column].eq(maximum),
            "Strategy",
        ].iloc[0]

        def highlight_strategy(
            row,
            strategy=maximum_strategy,
            metric_name=metric,
        ):
            """Highlight the better strategy for a metric."""

            styles = [""] * len(row)

            if row["Strategy"] == strategy:
                column_index = row.index.get_loc(metric_name)
                styles[column_index] = "font-weight: bold"

            return styles

        styled_comparison = styled_comparison.apply(
            highlight_strategy,
            axis=1,
        )

    display(styled_comparison)


GRID_SEARCH_METRIC_COLUMNS = (
    "F1 Macro",
    "Balanced Accuracy",
    "Accuracy",
)

GRID_SEARCH_PARAMETER_LABELS = {
    "classifier__criterion": "Criterion",
    "classifier__max_depth": "Max Depth",
    "classifier__min_samples_split": "Min Samples Split",
    "classifier__min_samples_leaf": "Min Samples Leaf",
}


def _get_grid_search_parameter_columns(
    data_frame: pd.DataFrame,
) -> list[str]:
    """Return GridSearchCV parameter columns."""

    excluded_columns = {
        "Seed",
        "F1 Macro",
        "F1 Macro Std",
        "Balanced Accuracy",
        "Balanced Accuracy Std",
        "Accuracy",
        "Accuracy Std",
    }

    return [column for column in data_frame.columns if column not in excluded_columns]


def _prepare_grid_search_results(
    grid_searches: Mapping[int, GridSearchCV],
) -> pd.DataFrame:
    """Prepare individual GridSearchCV results for all CV seeds."""

    results: list[pd.DataFrame] = []

    metric_column_mapping = {
        "mean_test_f1_macro": "F1 Macro",
        "std_test_f1_macro": "F1 Macro Std",
        "mean_test_balanced_accuracy": "Balanced Accuracy",
        "std_test_balanced_accuracy": "Balanced Accuracy Std",
        "mean_test_accuracy": "Accuracy",
        "std_test_accuracy": "Accuracy Std",
    }

    required_metric_columns = list(metric_column_mapping)

    for seed, grid_search in grid_searches.items():
        current_results = pd.DataFrame(grid_search.cv_results_).copy()

        parameter_columns = [
            column for column in current_results.columns if column.startswith("param_")
        ]

        selected_columns = parameter_columns + required_metric_columns

        current_results = current_results[selected_columns].copy()

        parameter_rename_mapping = {
            column: column.removeprefix("param_") for column in parameter_columns
        }

        rename_mapping = {
            **parameter_rename_mapping,
            **metric_column_mapping,
        }

        current_results = current_results.rename(columns=rename_mapping)

        current_results.insert(
            0,
            "Seed",
            seed,
        )

        results.append(current_results)

    if not results:
        raise ValueError("grid_searches must contain at least one GridSearchCV result.")

    return pd.concat(
        results,
        ignore_index=True,
    )


def _prepare_grid_search_summary(
    grid_searches: Mapping[int, GridSearchCV],
) -> pd.DataFrame:
    """Aggregate GridSearchCV results across CV seeds."""

    data = _prepare_grid_search_results(grid_searches)

    parameter_columns = _get_grid_search_parameter_columns(data)

    if not parameter_columns:
        raise ValueError("No GridSearchCV parameter columns were found.")

    summary = (
        data.groupby(
            parameter_columns,
            dropna=False,
            observed=True,
        )
        .agg(
            {
                "F1 Macro": ["mean", "std"],
                "Balanced Accuracy": ["mean", "std"],
                "Accuracy": ["mean", "std"],
            }
        )
        .reset_index()
    )

    summary.columns = [
        (f"{metric} {stat}" if stat else metric) for metric, stat in summary.columns
    ]

    summary = summary.sort_values(
        [
            "F1 Macro mean",
            "Balanced Accuracy mean",
            "Accuracy mean",
        ],
        ascending=False,
        ignore_index=True,
    )

    return summary


def _format_grid_search_parameter_value(
    value: object,
) -> str:
    """Format a GridSearchCV parameter value for display."""

    if value is None:
        return "None"

    if isinstance(value, (int, float)):
        numeric_value = float(value)

        if math.isnan(numeric_value):
            return "None"

        if numeric_value.is_integer():
            return str(int(numeric_value))

    return str(value)


def _prepare_grid_search_parameter_display(
    data_frame: pd.DataFrame,
) -> pd.DataFrame:
    """Prepare GridSearchCV parameter columns for display."""

    display_data = data_frame.copy()

    display_data = display_data.rename(columns=GRID_SEARCH_PARAMETER_LABELS)

    if "Max Depth" in display_data.columns:
        display_data["Max Depth"] = display_data["Max Depth"].map(
            _format_grid_search_parameter_value
        )

    return display_data


def _format_mean_std(
    mean_values: pd.Series,
    std_values: pd.Series,
) -> pd.Series:
    """Format mean and standard deviation as a single string."""

    return pd.Series(
        [
            f"{mean_value:.4f} ± {std_value:.4f}"
            for mean_value, std_value in zip(
                mean_values,
                std_values,
            )
        ],
        index=mean_values.index,
        dtype="string",
    )


def _prepare_grid_search_summary_display(
    summary: pd.DataFrame,
) -> pd.DataFrame:
    """Prepare aggregated GridSearchCV results for display."""

    display_data = summary.copy()

    display_data = display_data.rename(columns=GRID_SEARCH_PARAMETER_LABELS)

    if "Max Depth" in display_data.columns:
        display_data["Max Depth"] = display_data["Max Depth"].map(
            _format_grid_search_parameter_value
        )

    display_data["F1 Macro"] = _format_mean_std(
        display_data["F1 Macro mean"],
        display_data["F1 Macro std"],
    )

    display_data["Balanced Accuracy"] = _format_mean_std(
        display_data["Balanced Accuracy mean"],
        display_data["Balanced Accuracy std"],
    )

    display_data["Accuracy"] = _format_mean_std(
        display_data["Accuracy mean"],
        display_data["Accuracy std"],
    )

    parameter_columns = [
        column
        for column in GRID_SEARCH_PARAMETER_LABELS.values()
        if column in display_data.columns
    ]

    return display_data[parameter_columns + list(GRID_SEARCH_METRIC_COLUMNS)]


def _highlight_best_grid_search_metrics(
    data_frame: pd.DataFrame,
) -> pd.DataFrame:
    """Highlight the best metric within each CV seed."""

    styles = pd.DataFrame(
        "",
        index=data_frame.index,
        columns=data_frame.columns,
    )

    if data_frame.empty:
        return styles

    for _, group in data_frame.groupby(
        "Seed",
        sort=False,
        observed=True,
    ):
        for metric in GRID_SEARCH_METRIC_COLUMNS:
            best_value = group[metric].max()

            best_indices = group.index[group[metric].eq(best_value)]

            for index in best_indices:
                styles.at[
                    index,
                    metric,
                ] = "font-weight: bold"

    return styles


def _highlight_best_grid_search_summary_metrics(
    data_frame: pd.DataFrame,
    best_rows: Mapping[str, int],
) -> pd.DataFrame:
    """Highlight the best cross-seed value for each summary metric."""

    styles = pd.DataFrame(
        "",
        index=data_frame.index,
        columns=data_frame.columns,
    )

    for metric, row_index in best_rows.items():
        styles.at[
            row_index,
            metric,
        ] = "font-weight: bold"

    return styles


def display_grid_search_results(
    grid_searches: Mapping[int, GridSearchCV],
    caption: str = "Grid Search Results",
) -> None:
    """Display individual GridSearchCV results for all seeds."""

    data = _prepare_grid_search_results(grid_searches)

    data = data.sort_values(
        [
            "Seed",
            "F1 Macro",
        ],
        ascending=[
            True,
            False,
        ],
        ignore_index=True,
    )

    display_data = _prepare_grid_search_parameter_display(data)

    styled_results = (
        display_data.style.hide(axis="index")
        .format(
            {
                "F1 Macro": "{:.4f}",
                "F1 Macro Std": "{:.4f}",
                "Balanced Accuracy": "{:.4f}",
                "Balanced Accuracy Std": "{:.4f}",
                "Accuracy": "{:.4f}",
                "Accuracy Std": "{:.4f}",
            }
        )
        .set_caption(caption)
        .set_table_styles(
            [
                {
                    "selector": "th",
                    "props": [
                        ("text-align", "center"),
                    ],
                },
                {
                    "selector": "td",
                    "props": [
                        ("text-align", "center"),
                    ],
                },
            ]
        )
        .apply(
            _highlight_best_grid_search_metrics,
            axis=None,
        )
    )

    display(styled_results)


def display_grid_search_summary(
    grid_searches: Mapping[int, GridSearchCV],
    caption: str = "Grid Search Summary",
) -> None:
    """Display cross-seed GridSearchCV summary."""

    summary = _prepare_grid_search_summary(grid_searches)

    best_rows = {
        "F1 Macro": summary["F1 Macro mean"].idxmax(),
        "Balanced Accuracy": (summary["Balanced Accuracy mean"].idxmax()),
        "Accuracy": summary["Accuracy mean"].idxmax(),
    }

    display_data = _prepare_grid_search_summary_display(summary)

    styled_summary = (
        display_data.style.hide(axis="index")
        .set_caption(caption)
        .set_table_styles(
            [
                {
                    "selector": "th",
                    "props": [
                        ("text-align", "center"),
                    ],
                },
                {
                    "selector": "td",
                    "props": [
                        ("text-align", "center"),
                    ],
                },
            ]
        )
        .apply(
            _highlight_best_grid_search_summary_metrics,
            axis=None,
            best_rows=best_rows,
        )
    )

    display(styled_summary)


def get_best_grid_search_parameters(
    grid_searches: Mapping[int, GridSearchCV],
) -> dict[str, object]:
    """Return the parameter configuration with the highest mean Macro F1."""

    summary = _prepare_grid_search_summary(grid_searches)

    parameter_columns = _get_grid_search_parameter_columns(summary)

    if summary.empty:
        raise ValueError("GridSearchCV summary is empty.")

    best_row = summary.iloc[0]

    best_parameters: dict[str, object] = {}

    for parameter in parameter_columns:
        value = best_row[parameter]

        if parameter == "classifier__max_depth":
            value = _format_grid_search_parameter_value(value)

            if value == "None":
                best_parameters[parameter] = None
            else:
                best_parameters[parameter] = int(value)
        elif isinstance(value, float) and value.is_integer():
            best_parameters[parameter] = int(value)
        else:
            best_parameters[parameter] = value

    return best_parameters
