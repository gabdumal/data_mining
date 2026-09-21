import math
from collections.abc import Mapping

import numpy as np
import pandas as pd
from IPython.display import display
from sklearn.model_selection import GridSearchCV

from collections.abc import Mapping, Callable
import math

import numpy as np
import pandas as pd

from sklearn.model_selection import (
    GridSearchCV,
    KFold,
    StratifiedKFold,
)


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
    "classifier__max_features": "Max Features",
    "classifier__n_estimators": "N estimators",
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
        "F1 Macro mean",
        "F1 Macro std",
        "Balanced Accuracy mean",
        "Balanced Accuracy std",
        "Accuracy mean",
        "Accuracy std",
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


# ---------------------------------------------------------------------------*
# Generic Grid Search
# ---------------------------------------------------------------------------*


def _build_grid_search(
    random_state: int,
    param_grid,
    pipeline_builder: Callable,
    scoring: Mapping[str, str],
    refit: str,
    cv,
):
    """Build a GridSearchCV for a model pipeline."""

    pipeline = pipeline_builder(
        random_state=random_state,
    )

    return GridSearchCV(
        estimator=pipeline,
        param_grid=param_grid,
        scoring=scoring,
        refit=refit,
        cv=cv,
        n_jobs=-1,
        return_train_score=False,
        error_score="raise",
    )


def _run_grid_searches(
    input_data,
    target_data,
    seeds,
    param_grid,
    pipeline_builder: Callable,
    scoring: Mapping[str, str],
    refit: str,
    cv_builder: Callable,
):
    """Run GridSearchCV for multiple random seeds."""

    grid_searches = {}

    for current_seed in seeds:
        cross_validation = cv_builder(
            random_state=current_seed,
        )

        grid_search = _build_grid_search(
            random_state=current_seed,
            param_grid=param_grid,
            pipeline_builder=pipeline_builder,
            scoring=scoring,
            refit=refit,
            cv=cross_validation,
        )

        grid_search.fit(
            input_data,
            target_data,
        )

        grid_searches[current_seed] = grid_search

    return grid_searches


def _build_stratified_cv(random_state: int):
    """Build stratified cross-validation for classification."""

    return StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=random_state,
    )


def _build_regression_cv(random_state: int):
    """Build cross-validation for regression."""

    return KFold(
        n_splits=5,
        shuffle=True,
        random_state=random_state,
    )


CLASSIFICATION_GRID_SEARCH_METRICS = {
    "F1 Macro": {
        "score_name": "f1_macro",
        "higher_is_better": True,
        "score_multiplier": 1,
    },
    "Balanced Accuracy": {
        "score_name": "balanced_accuracy",
        "higher_is_better": True,
        "score_multiplier": 1,
    },
    "Accuracy": {
        "score_name": "accuracy",
        "higher_is_better": True,
        "score_multiplier": 1,
    },
}


REGRESSION_GRID_SEARCH_METRICS = {
    "MAE": {
        "score_name": "mae",
        "higher_is_better": False,
        "score_multiplier": -1,
    },
    "RMSE": {
        "score_name": "rmse",
        "higher_is_better": False,
        "score_multiplier": -1,
    },
    "R²": {
        "score_name": "r2",
        "higher_is_better": True,
        "score_multiplier": 1,
    },
}


def _normalize_grid_search_parameter(
    value: object,
) -> object:
    """Normalize a GridSearchCV parameter value."""

    if value is None:
        return None

    if isinstance(value, float):
        if math.isnan(value):
            return None

        if value.is_integer():
            return int(value)

    if isinstance(value, np.integer):
        return int(value)

    return value


def _prepare_grid_search_summary(
    grid_searches: Mapping[int, GridSearchCV],
    metrics: Mapping[str, Mapping[str, object]],
) -> pd.DataFrame:
    """Prepare a cross-seed GridSearchCV summary."""

    if not grid_searches:
        raise ValueError("No GridSearchCV results were provided.")

    rows = []

    for random_state, grid_search in grid_searches.items():
        cv_results = pd.DataFrame(grid_search.cv_results_)

        parameter_columns = [
            column for column in cv_results.columns if column.startswith("param_")
        ]

        for _, row in cv_results.iterrows():
            result = {
                parameter: _normalize_grid_search_parameter(row[parameter])
                for parameter in parameter_columns
            }

            result["random_state"] = random_state

            for metric_name, metric_config in metrics.items():
                score_column = f"mean_test_{metric_config['score_name']}"

                result[metric_name] = (
                    row[score_column] * metric_config["score_multiplier"]
                )

            rows.append(result)

    results = pd.DataFrame(rows)

    parameter_columns = [
        column for column in results.columns if column.startswith("param_")
    ]

    summary = results.groupby(
        parameter_columns,
        dropna=False,
        as_index=False,
    ).agg({metric_name: ["mean", "std"] for metric_name in metrics})

    # Flatten the MultiIndex generated by .agg().
    flattened_columns = []

    for column in summary.columns:
        if isinstance(column, tuple):
            if column[1]:
                flattened_columns.append(f"{column[0]} {column[1]}")
            else:
                flattened_columns.append(column[0])
        else:
            flattened_columns.append(column)

    summary.columns = flattened_columns

    return summary


def _get_best_grid_search_row(
    summary: pd.DataFrame,
    selection_metric: str,
    higher_is_better: bool,
) -> pd.Series:
    """Return the best row according to a summary metric."""

    if summary.empty:
        raise ValueError("GridSearchCV summary is empty.")

    metric_column = f"{selection_metric} mean"

    if metric_column not in summary.columns:
        raise ValueError(f"Metric column '{metric_column}' was not found.")

    if higher_is_better:
        best_index = summary[metric_column].idxmax()
    else:
        best_index = summary[metric_column].idxmin()

    return summary.loc[best_index]


def _get_best_grid_search_parameters(
    grid_searches: Mapping[int, GridSearchCV],
    metrics: Mapping[str, Mapping[str, object]],
    selection_metric: str,
) -> dict[str, object]:
    """Return the parameters for the best cross-seed configuration."""

    if selection_metric not in metrics:
        raise ValueError(f"Unknown selection metric: {selection_metric}")

    summary = _prepare_grid_search_summary(
        grid_searches=grid_searches,
        metrics=metrics,
    )

    metric_config = metrics[selection_metric]

    best_row = _get_best_grid_search_row(
        summary=summary,
        selection_metric=selection_metric,
        higher_is_better=metric_config["higher_is_better"],
    )

    parameter_columns = [
        column for column in summary.columns if column.startswith("param_")
    ]

    return {
        parameter: _normalize_grid_search_parameter(best_row[parameter])
        for parameter in parameter_columns
    }


def _prepare_grid_search_summary_display(
    summary: pd.DataFrame,
    metrics: Mapping[str, Mapping[str, object]],
) -> pd.DataFrame:
    """Prepare a human-readable GridSearchCV summary."""

    parameter_columns = [
        column for column in summary.columns if column.startswith("param_")
    ]

    display_data = summary[parameter_columns].copy()

    # Make parameter names more readable.
    display_data.columns = [
        column.removeprefix("param_") for column in display_data.columns
    ]

    for metric_name in metrics:
        mean_column = f"{metric_name} mean"
        std_column = f"{metric_name} std"

        display_data[metric_name] = (
            summary[mean_column].map(lambda value: f"{value:.4f}")
            + " ± "
            + summary[std_column].map(lambda value: f"{value:.4f}")
        )

    return display_data


def display_grid_search_summary(
    grid_searches: Mapping[int, GridSearchCV],
    metrics: Mapping[str, Mapping[str, object]],
    selection_metric: str,
    caption: str = "Grid Search Summary",
) -> None:
    """Display a cross-seed GridSearchCV summary."""

    summary = _prepare_grid_search_summary(
        grid_searches=grid_searches,
        metrics=metrics,
    )

    display_data = _prepare_grid_search_summary_display(
        summary=summary,
        metrics=metrics,
    )

    best_rows = {}

    for metric_name, metric_config in metrics.items():
        metric_column = f"{metric_name} mean"

        if metric_config["higher_is_better"]:
            best_rows[metric_name] = summary[metric_column].idxmax()
        else:
            best_rows[metric_name] = summary[metric_column].idxmin()

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


def run_grid_searches_for_classification(
    input_data,
    target_data,
    seeds,
    param_grid,
    pipeline_builder,
):
    """Run classification GridSearchCV for multiple seeds."""

    return _run_grid_searches(
        input_data=input_data,
        target_data=target_data,
        seeds=seeds,
        param_grid=param_grid,
        pipeline_builder=pipeline_builder,
        scoring={
            "f1_macro": "f1_macro",
            "balanced_accuracy": "balanced_accuracy",
            "accuracy": "accuracy",
        },
        refit="f1_macro",
        cv_builder=_build_stratified_cv,
    )


def run_grid_searches_for_regression(
    input_data,
    target_data,
    seeds,
    param_grid,
    pipeline_builder,
):
    """Run regression GridSearchCV for multiple seeds."""

    return _run_grid_searches(
        input_data=input_data,
        target_data=target_data,
        seeds=seeds,
        param_grid=param_grid,
        pipeline_builder=pipeline_builder,
        scoring={
            "mae": "neg_mean_absolute_error",
            "rmse": "neg_root_mean_squared_error",
            "r2": "r2",
        },
        refit="mae",
        cv_builder=_build_regression_cv,
    )
