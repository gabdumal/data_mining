import math
from collections.abc import Callable, Mapping
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from IPython.display import display
from sklearn.model_selection import (
    GridSearchCV,
    KFold,
    StratifiedKFold,
)

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
    "classifier__n_estimators": "N Estimators",
    "regressor__learning_rate": "Learning Rate",
    "regressor__loss": "Loss",
    "regressor__max_depth": "Max Depth",
    "regressor__min_samples_leaf": "Min Samples Leaf",
    "regressor__n_estimators": "N Estimators",
}


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


def _highlight_best_grid_search_metrics(
    data: pd.DataFrame,
    metrics: Mapping[str, Mapping[str, object]],
):
    """Highlight the best metric value within each CV seed."""

    styles = pd.DataFrame(
        "",
        index=data.index,
        columns=data.columns,
    )

    for metric_name, metric_config in metrics.items():
        if metric_name not in data.columns:
            continue

        for seed in data["Seed"].unique():
            seed_mask = data["Seed"] == seed
            seed_values = data.loc[seed_mask, metric_name]

            if metric_config["higher_is_better"]:
                best_value = seed_values.max()  # type: ignore
            else:
                best_value = seed_values.min()  # type: ignore

            best_mask = seed_mask & (data[metric_name] == best_value)

            styles.loc[best_mask, metric_name] = "font-weight: bold"

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


def _prepare_grid_search_results(
    grid_searches: Mapping[int, GridSearchCV],
    metrics: Mapping[str, Mapping[str, object]],
) -> pd.DataFrame:
    """Prepare individual GridSearchCV results for all CV seeds."""

    results: list[pd.DataFrame] = []

    if not grid_searches:
        raise ValueError("grid_searches must contain at least one GridSearchCV result.")

    for seed, grid_search in grid_searches.items():
        current_results = pd.DataFrame(grid_search.cv_results_).copy()

        parameter_columns = [
            column for column in current_results.columns if column.startswith("param_")
        ]

        metric_columns = []

        for metric_config in metrics.values():
            score_name = metric_config["score_name"]

            metric_columns.extend(
                [
                    f"mean_test_{score_name}",
                    f"std_test_{score_name}",
                ]
            )

        selected_columns = parameter_columns + metric_columns

        current_results = current_results[selected_columns].copy()

        # Rename parameter columns.
        rename_mapping = {
            column: column.removeprefix("param_") for column in parameter_columns
        }

        # Rename and transform metric columns.
        for metric_name, metric_config in metrics.items():
            score_name = metric_config["score_name"]
            multiplier = metric_config["score_multiplier"]

            mean_column = f"mean_test_{score_name}"
            std_column = f"std_test_{score_name}"

            rename_mapping[mean_column] = metric_name
            rename_mapping[std_column] = f"{metric_name} Std"

            if multiplier != 1:
                current_results[mean_column] *= multiplier  # type: ignore
                current_results[std_column] *= multiplier  # type: ignore

        current_results = current_results.rename(columns=rename_mapping)

        current_results.insert(
            0,
            "Seed",
            seed,
        )

        results.append(current_results)

    return pd.concat(
        results,
        ignore_index=True,
    )


def display_grid_search_results(
    grid_searches: Mapping[int, GridSearchCV],
    metrics: Mapping[str, Mapping[str, object]],
    sort_metric: str,
    caption: str = "Grid Search Results",
) -> None:
    """Display individual GridSearchCV results for all seeds."""

    data = _prepare_grid_search_results(
        grid_searches=grid_searches,
        metrics=metrics,
    )

    metric_config = metrics[sort_metric]

    data = data.sort_values(
        [
            "Seed",
            sort_metric,
        ],
        ascending=[
            True,
            not metric_config["higher_is_better"],
        ],
        ignore_index=True,
    )

    display_data = _prepare_grid_search_parameter_display(data)

    format_mapping = {}

    for metric_name in metrics:
        format_mapping[metric_name] = "{:.4f}"
        format_mapping[f"{metric_name} Std"] = "{:.4f}"

    styled_results = (
        display_data.style.hide(axis="index")
        .format(format_mapping)
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
            metrics=metrics,
        )
    )

    display(styled_results)


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

    return summary.loc[best_index]  # type: ignore


def get_best_grid_search_parameters(
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
        higher_is_better=metric_config["higher_is_better"],  # type: ignore
    )

    parameter_columns = [
        column for column in summary.columns if column.startswith("param_")
    ]

    return {
        parameter.removeprefix("param_"): _normalize_grid_search_parameter(
            best_row[parameter]
        )
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


# ---------------------------------------------------------------------------
# Run Grid Search
# ---------------------------------------------------------------------------

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
    seeds: list[int],
    param_grid,
    pipeline_builder: Callable,
    scoring: Mapping[str, str],
    refit: str,
    cv_builder: Callable,
):
    """Run GridSearchCV for multiple random seeds."""

    grid_searches: Mapping[int, GridSearchCV] = {}

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


# ---------------------------------------------------------------------------
# Serialization
# ---------------------------------------------------------------------------


def save_grid_searches(
    grid_searches: Mapping[int, GridSearchCV],
    file_path: str | Path,
) -> None:
    """Save fitted GridSearchCV objects to a file."""

    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(
        grid_searches,
        file_path,
        compress=3,
    )


def load_grid_searches(
    file_path: str | Path,
) -> Mapping[int, GridSearchCV]:
    """Load fitted GridSearchCV objects from a file."""

    return joblib.load(file_path)
