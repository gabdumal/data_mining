import math
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import TypeAlias, TypedDict

import joblib
import numpy as np
import pandas as pd
from IPython.display import display
from pandas.io.formats.style import Styler
from sklearn.model_selection import (
    GridSearchCV,
    KFold,
    StratifiedKFold,
)


class GridSearchMetricConfig(TypedDict):
    """Configuration for a GridSearchCV metric."""

    score_name: str
    higher_is_better: bool
    score_multiplier: float


GridSearchMetrics: TypeAlias = Mapping[
    str,
    GridSearchMetricConfig,
]

MeanStd: TypeAlias = tuple[float, float]


CLASSIFICATION_GRID_SEARCH_METRICS: dict[
    str,
    GridSearchMetricConfig,
] = {
    "F1 Macro": {
        "score_name": "f1_macro",
        "higher_is_better": True,
        "score_multiplier": 1.0,
    },
    "Balanced Accuracy": {
        "score_name": "balanced_accuracy",
        "higher_is_better": True,
        "score_multiplier": 1.0,
    },
    "Accuracy": {
        "score_name": "accuracy",
        "higher_is_better": True,
        "score_multiplier": 1.0,
    },
}


REGRESSION_GRID_SEARCH_METRICS: dict[
    str,
    GridSearchMetricConfig,
] = {
    "MAE": {
        "score_name": "mae",
        "higher_is_better": False,
        "score_multiplier": -1.0,
    },
    "RMSE": {
        "score_name": "rmse",
        "higher_is_better": False,
        "score_multiplier": -1.0,
    },
    "R²": {
        "score_name": "r2",
        "higher_is_better": True,
        "score_multiplier": 1.0,
    },
}


GRID_SEARCH_TABLE_STYLES = [
    {
        "selector": "th",
        "props": [
            ("text-align", "center"),
            ("padding", "6px 12px"),
            ("white-space", "nowrap"),
        ],
    },
    {
        "selector": "td",
        "props": [
            ("text-align", "center"),
            ("padding", "4px 12px"),
        ],
    },
]


def _get_grid_search_parameter_columns(
    data_frame: pd.DataFrame,
) -> list[str]:
    """Return GridSearchCV parameter columns."""

    return [column for column in data_frame.columns if column.startswith("param_")]


def _get_grid_search_metric_columns(
    metrics: GridSearchMetrics,
) -> list[str]:
    """Return human-readable metric names."""

    return list(metrics)


def _get_grid_search_cv_metric_columns(
    metrics: GridSearchMetrics,
) -> list[str]:
    """Return GridSearchCV result-column names for configured metrics."""

    columns: list[str] = []

    for metric_config in metrics.values():
        score_name = metric_config["score_name"]

        columns.extend(
            [
                f"mean_test_{score_name}",
                f"std_test_{score_name}",
            ]
        )

    return columns


def _format_grid_search_parameter_label(
    parameter: str,
) -> str:
    """Convert a GridSearchCV parameter name into a display label."""

    parameter = parameter.removeprefix("param_")

    # classifier__max_depth -> max_depth
    # regressor__learning_rate -> learning_rate
    parameter = parameter.split(
        "__",
        maxsplit=1,
    )[-1]

    return parameter.replace(
        "_",
        " ",
    ).title()


def _normalize_grid_search_parameter(
    value: object,
) -> object:
    """Normalize a GridSearchCV parameter value."""

    if value is None:
        return None

    if isinstance(value, bool):
        return value

    if isinstance(value, np.integer):
        return int(value)

    if isinstance(value, np.floating):
        numeric_value = float(value)

        if math.isnan(numeric_value):
            return None

        if numeric_value.is_integer():
            return int(numeric_value)

        return numeric_value

    if isinstance(value, float):
        if math.isnan(value):
            return None

        if value.is_integer():
            return int(value)

    return value


def _format_grid_search_parameter_value(
    value: object,
) -> str:
    """Format a GridSearchCV parameter value for display."""

    normalized_value = _normalize_grid_search_parameter(value)

    if normalized_value is None:
        return "None"

    return str(normalized_value)


def _format_mean_std_value(
    value: object,
) -> str:
    """Format a mean/std pair."""

    if not isinstance(value, tuple) or len(value) != 2:
        raise ValueError(f"Expected a (mean, std) tuple, got {value!r}.")

    mean_value, std_value = value

    if not isinstance(mean_value, (int, float, np.integer, np.floating)):
        raise ValueError(f"Expected numeric mean/std values, got {value!r}.")  # noqa: TRY004

    if not isinstance(std_value, (int, float, np.integer, np.floating)):
        raise ValueError(f"Expected numeric mean/std values, got {value!r}.")  # noqa: TRY004

    return f"{float(mean_value):.4f} ± {float(std_value):.4f}"


def _prepare_grid_search_parameter_display(
    data_frame: pd.DataFrame,
) -> pd.DataFrame:
    """Prepare GridSearchCV parameter columns for display."""

    parameter_columns = _get_grid_search_parameter_columns(data_frame)

    display_data = data_frame[parameter_columns].copy()

    display_data.columns = [
        _format_grid_search_parameter_label(column) for column in parameter_columns
    ]

    for column in display_data.columns:
        display_data[column] = display_data[column].map(
            _format_grid_search_parameter_value
        )

    return display_data


def _style_grid_search_table(
    data_frame: pd.DataFrame,
    caption: str,
    format_mapping: Mapping[str, str] | None = None,
) -> Styler:
    """Create the standard GridSearchCV table style."""

    styled_data = data_frame.style.hide(axis="index")

    if format_mapping is not None:
        styled_data = styled_data.format(format_mapping)  # type: ignore

    return styled_data.set_caption(caption).set_table_styles(GRID_SEARCH_TABLE_STYLES)  # type: ignore


def _highlight_best_grid_search_metrics(
    display_data: pd.DataFrame,
    source_data: pd.DataFrame,
    metrics: GridSearchMetrics,
) -> pd.DataFrame:
    """Highlight the best metric value within each seed."""

    if "Seed" not in display_data.columns:
        raise ValueError("display_data must contain a 'Seed' column.")

    if "Seed" not in source_data.columns:
        raise ValueError("source_data must contain a 'Seed' column.")

    if not display_data.index.equals(source_data.index):
        raise ValueError("display_data and source_data must have identical indices.")

    styles = pd.DataFrame(
        "",
        index=display_data.index,
        columns=display_data.columns,
    )

    for metric_name, metric_config in metrics.items():
        if metric_name not in display_data.columns:
            raise ValueError(f"Metric '{metric_name}' is missing from display_data.")

        if metric_name not in source_data.columns:
            raise ValueError(f"Metric '{metric_name}' is missing from source_data.")

        metric_values = pd.to_numeric(
            source_data[metric_name],
            errors="raise",
        )

        for seed in source_data["Seed"].unique():
            seed_mask = source_data["Seed"] == seed
            seed_values = metric_values.loc[seed_mask]

            if metric_config["higher_is_better"]:
                best_value = seed_values.max()
            else:
                best_value = seed_values.min()

            winner_mask = seed_mask & metric_values.eq(best_value)

            styles.loc[
                winner_mask,
                metric_name,
            ] = "font-weight: bold"

    return styles


def _highlight_best_grid_search_summary_metrics(
    data_frame: pd.DataFrame,
    summary: pd.DataFrame,
    metrics: GridSearchMetrics,
) -> pd.DataFrame:
    """Highlight the best cross-seed mean for each metric."""

    styles = pd.DataFrame(
        "",
        index=data_frame.index,
        columns=data_frame.columns,
    )

    for metric_name, metric_config in metrics.items():
        mean_column = f"{metric_name} mean"

        if mean_column not in summary.columns:
            raise ValueError(f"Missing summary column: {mean_column}")

        values = pd.to_numeric(
            summary[mean_column],
            errors="raise",
        )

        if metric_config["higher_is_better"]:
            best_value = values.max()
        else:
            best_value = values.min()

        winner_mask = values.eq(best_value)

        styles.loc[
            winner_mask,
            metric_name,
        ] = "font-weight: bold"

    return styles


def _prepare_grid_search_metric_display(
    data_frame: pd.DataFrame,
    metrics: GridSearchMetrics,
) -> pd.DataFrame:
    """Combine GridSearchCV mean/std metric columns for display."""

    display_data = pd.DataFrame(index=data_frame.index)

    for metric_name in metrics:
        mean_column = metric_name
        std_column = f"{metric_name} Std"

        if mean_column not in data_frame.columns:
            raise ValueError(f"Missing metric column: {mean_column}")

        if std_column not in data_frame.columns:
            raise ValueError(f"Missing metric standard-deviation column: {std_column}")

        display_data[metric_name] = [
            (
                float(mean_value),
                float(std_value),
            )
            for mean_value, std_value in zip(
                data_frame[mean_column],
                data_frame[std_column],
                strict=True,
            )
        ]

    return display_data


def _prepare_grid_search_results(
    grid_searches: Mapping[int, GridSearchCV],
    metrics: GridSearchMetrics,
) -> pd.DataFrame:
    """Prepare individual GridSearchCV results for all CV seeds."""

    if not grid_searches:
        raise ValueError("grid_searches must contain at least one GridSearchCV result.")

    results: list[pd.DataFrame] = []

    required_metric_columns = _get_grid_search_cv_metric_columns(metrics)

    for seed, grid_search in grid_searches.items():
        current_results = pd.DataFrame(grid_search.cv_results_).copy()

        parameter_columns = _get_grid_search_parameter_columns(current_results)

        selected_columns = parameter_columns + required_metric_columns

        missing_columns = [
            column
            for column in selected_columns
            if column not in current_results.columns
        ]

        if missing_columns:
            raise ValueError(
                f"GridSearchCV results are missing columns: {missing_columns}"
            )

        current_results = current_results[selected_columns].copy()

        rename_mapping = {
            f"mean_test_{config['score_name']}": metric_name
            for metric_name, config in metrics.items()
        }

        rename_mapping.update(
            {
                f"std_test_{config['score_name']}": (f"{metric_name} Std")
                for metric_name, config in metrics.items()
            }
        )

        for metric_config in metrics.values():
            mean_column = f"mean_test_{metric_config['score_name']}"
            std_column = f"std_test_{metric_config['score_name']}"

            multiplier = metric_config["score_multiplier"]

            current_results[mean_column] = (
                pd.to_numeric(
                    current_results[mean_column],
                    errors="raise",
                )
                * multiplier
            )

            current_results[std_column] = pd.to_numeric(
                current_results[std_column],
                errors="raise",
            ) * abs(multiplier)

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


def _prepare_grid_search_summary(
    grid_searches: Mapping[int, GridSearchCV],
    metrics: GridSearchMetrics,
) -> pd.DataFrame:
    """Prepare a cross-seed GridSearchCV summary."""

    results = _prepare_grid_search_results(
        grid_searches=grid_searches,
        metrics=metrics,
    )

    parameter_columns = _get_grid_search_parameter_columns(results)

    metric_columns = _get_grid_search_metric_columns(metrics)

    summary = results.groupby(
        parameter_columns,
        dropna=False,
        as_index=False,
    )[metric_columns].agg(["mean", "std"])

    flattened_columns: list[str] = []

    for column in summary.columns:
        if isinstance(column, tuple):
            first, second = column

            flattened_columns.append(str(first) if not second else f"{first} {second}")
        else:
            flattened_columns.append(str(column))

    summary.columns = flattened_columns

    return summary


def _prepare_grid_search_summary_display(
    summary: pd.DataFrame,
    metrics: GridSearchMetrics,
) -> pd.DataFrame:
    """Prepare a human-readable GridSearchCV summary."""

    parameter_columns = _get_grid_search_parameter_columns(summary)

    parameter_data = _prepare_grid_search_parameter_display(summary)

    display_data = parameter_data.copy()

    for metric_name in metrics:
        mean_column = f"{metric_name} mean"
        std_column = f"{metric_name} std"

        if mean_column not in summary.columns or std_column not in summary.columns:
            raise ValueError(f"Missing summary columns for metric '{metric_name}'.")

        values: list[MeanStd] = [
            (
                float(mean_value),
                float(std_value),
            )
            for mean_value, std_value in zip(
                summary[mean_column],
                summary[std_column],
                strict=True,
            )
        ]

        display_data[metric_name] = values

    # Keep parameter columns before metrics.
    return display_data[
        [
            *[
                _format_grid_search_parameter_label(column)
                for column in parameter_columns
            ],
            *metrics,
        ]
    ]


def _get_best_grid_search_row(
    summary: pd.DataFrame,
    selection_metric: str,
    metric_config: GridSearchMetricConfig,
) -> pd.Series:
    """Return the best summary row according to one metric."""

    if summary.empty:
        raise ValueError("GridSearchCV summary is empty.")

    metric_column = f"{selection_metric} mean"

    if metric_column not in summary.columns:
        raise ValueError(f"Metric column '{metric_column}' was not found.")

    values = pd.to_numeric(
        summary[metric_column],
        errors="raise",
    ).to_numpy(dtype=float)

    if not np.isfinite(values).any():
        raise ValueError(f"Metric '{selection_metric}' contains no finite values.")

    if metric_config["higher_is_better"]:
        best_position = int(np.nanargmax(values))
    else:
        best_position = int(np.nanargmin(values))

    return summary.iloc[best_position]


def get_best_grid_search_parameters(
    grid_searches: Mapping[int, GridSearchCV],
    metrics: GridSearchMetrics,
    selection_metric: str,
) -> dict[str, object]:
    """Return parameters for the best cross-seed configuration."""

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
        metric_config=metric_config,
    )

    parameter_columns = _get_grid_search_parameter_columns(summary)

    return {
        parameter.removeprefix("param_"): (
            _normalize_grid_search_parameter(best_row[parameter])
        )
        for parameter in parameter_columns
    }


def display_grid_search_results(
    grid_searches: Mapping[int, GridSearchCV],
    metrics: GridSearchMetrics,
    sort_metric: str,
    caption: str = "Grid Search Results",
) -> None:
    """Display individual GridSearchCV results for all CV seeds."""

    if sort_metric not in metrics:
        raise ValueError(f"Unknown sort metric: {sort_metric}")

    data = _prepare_grid_search_results(
        grid_searches=grid_searches,
        metrics=metrics,
    )

    metric_config = metrics[sort_metric]

    data = data.sort_values(
        by=[
            "Seed",
            sort_metric,
        ],
        ascending=[
            True,
            not metric_config["higher_is_better"],
        ],
        ignore_index=True,
    )

    parameter_display = _prepare_grid_search_parameter_display(data)

    metric_display = _prepare_grid_search_metric_display(
        data,
        metrics,
    )

    display_data = pd.concat(
        [
            data[["Seed"]].reset_index(drop=True),
            parameter_display.reset_index(drop=True),
            metric_display.reset_index(drop=True),
        ],
        axis=1,
    )

    format_mapping = {metric_name: _format_mean_std_value for metric_name in metrics}

    styled_results = _style_grid_search_table(
        data_frame=display_data,
        caption=caption,
        format_mapping=format_mapping,  # type: ignore
    ).apply(
        _highlight_best_grid_search_metrics,
        axis=None,
        source_data=data,
        metrics=metrics,
    )

    display(styled_results)


def display_grid_search_summary(
    grid_searches: Mapping[int, GridSearchCV],
    metrics: GridSearchMetrics,
    sort_metric: str,
    caption: str = "Grid Search Summary",
) -> None:
    """Display a cross-seed GridSearchCV summary."""

    if sort_metric not in metrics:
        raise ValueError(f"Unknown sort metric: {sort_metric}")

    summary = _prepare_grid_search_summary(
        grid_searches=grid_searches,
        metrics=metrics,
    )

    metric_config = metrics[sort_metric]

    summary = summary.sort_values(
        by=f"{sort_metric} mean",
        ascending=not metric_config["higher_is_better"],
        ignore_index=True,
    )

    display_data = _prepare_grid_search_summary_display(
        summary=summary,
        metrics=metrics,
    )

    format_mapping = {metric_name: _format_mean_std_value for metric_name in metrics}

    styled_summary = _style_grid_search_table(
        data_frame=display_data,
        caption=caption,
        format_mapping=format_mapping,  # type: ignore
    )

    styled_summary = styled_summary.apply(
        _highlight_best_grid_search_summary_metrics,
        axis=None,
        summary=summary,
        metrics=metrics,
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
