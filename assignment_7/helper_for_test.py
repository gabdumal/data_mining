from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Literal, Protocol, cast

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
import pandas as pd
from IPython.display import display
from pandas.io.formats.style import Styler
from sklearn.base import BaseEstimator
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    precision_recall_fscore_support,
    r2_score,
)

from features import AGE_GROUP_ORDER, group_age
from helper_for_analysis import DEFAULT_COLOR, PALETTE

# =============================================================================
# Constants
# =============================================================================


CLASSIFICATION_TEST_METRICS: dict[str, bool] = {
    "Accuracy": True,
    "Balanced Accuracy": True,
    "Macro F1": True,
}

REGRESSION_TEST_METRICS: dict[str, bool] = {
    "MAE": False,
    "RMSE": False,
    "R²": True,
}

TABLE_STYLES = [
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


Task = Literal["classification", "regression"]


# =============================================================================
# Protocols and data classes
# =============================================================================


class PredictiveModel(Protocol):
    """Protocol for the fitted models used in this module."""

    def fit(
        self,
        X: pd.DataFrame,
        y: pd.Series,
    ) -> PredictiveModel: ...

    def predict(
        self,
        X: pd.DataFrame,
    ) -> npt.NDArray[Any]: ...

    def set_params(
        self,
        **params: object,
    ) -> PredictiveModel: ...


class PipelineModel(PredictiveModel, Protocol):
    """Protocol for fitted sklearn/imblearn pipelines."""

    named_steps: Mapping[str, object]


MetricCalculator = Callable[
    [pd.Series, pd.Series],
    dict[str, float],
]


@dataclass
class ModelTestResults:
    """Store repeated test-set predictions, metrics, and feature importances."""

    model_name: str
    task: Task
    predictions: dict[int, pd.Series]
    seed_metrics: pd.DataFrame
    feature_importances: dict[int, pd.Series]


# =============================================================================
# Generic validation and formatting helpers
# =============================================================================


def _require_columns(
    data_frame: pd.DataFrame,
    required_columns: Sequence[str],
    context: str,
) -> None:
    """Raise a descriptive error when required columns are missing."""

    missing_columns = [
        column for column in required_columns if column not in data_frame.columns
    ]

    if missing_columns:
        raise ValueError(
            f"{context} is missing required columns: {', '.join(missing_columns)}"
        )


def _validate_predictions_against_target(
    predictions: Mapping[int, pd.Series],
    target_data_for_test: pd.Series,
) -> None:
    """Validate prediction indices against the fixed test-set index."""

    if not predictions:
        raise ValueError("predictions must contain at least one seed.")

    for seed, predicted_values in predictions.items():
        if not predicted_values.index.equals(target_data_for_test.index):
            raise ValueError(
                f"Prediction index for seed {seed} does not match "
                "the target test-set index."
            )


def _format_mean_std(
    mean_value: float,
    std_value: float,
) -> str:
    """Format a mean and standard deviation."""

    return f"{mean_value:.4f} ± {std_value:.4f}"


def _style_table(
    data_frame: pd.DataFrame,
    caption: str,
    format_mapping: Mapping[str, str] | None = None,
    hide_index: bool = True,
) -> Styler:
    """Create a consistently styled table."""

    styled_data = data_frame.style

    if hide_index:
        styled_data = styled_data.hide(axis="index")

    if format_mapping is not None:
        styled_data = styled_data.format(format_mapping)  # type: ignore

    return styled_data.set_caption(caption).set_table_styles(TABLE_STYLES)  # type: ignore


def _highlight_seed_metric_winners(
    data_frame: pd.DataFrame,
    metric_directions: Mapping[str, bool],
) -> pd.DataFrame:
    """Highlight the best metric values independently within each seed."""

    _require_columns(
        data_frame,
        ["Seed", *metric_directions],
        "_highlight_seed_metric_winners",
    )

    styles = pd.DataFrame(
        "",
        index=data_frame.index,
        columns=data_frame.columns,
    )

    for metric_name, higher_is_better in metric_directions.items():
        numeric_values = pd.to_numeric(
            data_frame[metric_name],
            errors="coerce",
        )

        for seed in data_frame["Seed"].unique():
            seed_mask = data_frame["Seed"] == seed
            seed_values = numeric_values.loc[seed_mask].dropna()

            if seed_values.empty:
                continue

            best_value = seed_values.max() if higher_is_better else seed_values.min()

            winner_mask = seed_mask & numeric_values.eq(best_value)
            styles.loc[winner_mask, metric_name] = "font-weight: bold"

    return styles


def _highlight_best_summary_metrics(
    data_frame: pd.DataFrame,
    summary: pd.DataFrame,
    metric_directions: Mapping[str, bool],
) -> pd.DataFrame:
    """Highlight the best mean metric value across models."""

    metric_mean_columns = [f"{metric} mean" for metric in metric_directions]

    _require_columns(
        summary,
        ["Model", *metric_mean_columns],
        "_highlight_best_summary_metrics",
    )

    styles = pd.DataFrame(
        "",
        index=data_frame.index,
        columns=data_frame.columns,
    )

    for metric_name, higher_is_better in metric_directions.items():
        numeric_column = f"{metric_name} mean"
        display_column = metric_name

        if higher_is_better:
            best_value = summary[numeric_column].max()
        else:
            best_value = summary[numeric_column].min()

        winner_mask = summary[numeric_column].eq(best_value)
        styles.loc[winner_mask, display_column] = "font-weight: bold"

    return styles


# =============================================================================
# Feature importance
# =============================================================================


def _extract_model_feature_names(
    model: BaseEstimator,
) -> np.ndarray:
    """Extract feature names generated by the fitted preprocessing pipeline."""

    if not hasattr(model, "named_steps"):
        raise ValueError("The model must be a fitted pipeline.")

    named_steps = model.named_steps  # type: ignore

    original_feature_names = getattr(
        model,
        "feature_names_in_",
        None,
    )

    # -----------------------------------------------------------------------
    # Pipelines with a final OneHotEncoder / ColumnTransformer
    # -----------------------------------------------------------------------

    for step in reversed(named_steps.values()):
        get_feature_names_out = getattr(
            step,
            "get_feature_names_out",
            None,
        )

        if not callable(get_feature_names_out):
            continue

        # When the transformation receives an ndarray (as in the
        # SMOTENC pipeline), explicitly provide the original feature
        # names so sklearn does not generate x0, x1, ..., x10.
        if original_feature_names is not None:
            try:
                feature_names = get_feature_names_out(
                    original_feature_names,
                )
            except (TypeError, ValueError):
                feature_names = get_feature_names_out()
        else:
            feature_names = get_feature_names_out()

        return np.asarray(
            feature_names,
            dtype=str,
        )

    if original_feature_names is not None:
        return np.asarray(
            original_feature_names,
            dtype=str,
        )

    raise ValueError("Could not determine the model feature names.")


def _extract_feature_importances(
    model: PipelineModel,
    estimator_step: str,
) -> pd.Series:
    """Extract feature importances from a fitted tree-based pipeline."""

    if estimator_step not in model.named_steps:
        raise ValueError(f"Could not find `{estimator_step}` in the pipeline.")

    estimator = model.named_steps[estimator_step]

    importance_attribute = getattr(
        estimator,
        "feature_importances_",
        None,
    )

    if importance_attribute is None:
        raise ValueError(
            f"{type(estimator).__name__} does not provide `feature_importances_`."
        )

    importances = np.asarray(
        cast(npt.ArrayLike, importance_attribute),
        dtype=float,
    )

    feature_names = _extract_model_feature_names(model)  # type: ignore

    if len(importances) != len(feature_names):
        raise ValueError(
            "The number of feature names does not match the number "
            "of feature importances: "
            f"{len(feature_names)} != {len(importances)}."
        )

    cleaned_feature_names = np.asarray(
        [feature_name.split("__", maxsplit=1)[-1] for feature_name in feature_names],
        dtype=str,
    )

    return pd.Series(
        importances,
        index=cleaned_feature_names,
        name="Importance",
    ).sort_values(
        ascending=False,
    )


def prepare_feature_importance_summary(
    results: ModelTestResults,
) -> pd.DataFrame:
    """Aggregate feature importance across model seeds."""

    if not results.feature_importances:
        raise ValueError("Model results contain no feature importances.")

    importance_data = pd.concat(
        results.feature_importances,
        axis=1,
    )

    summary = (
        pd.DataFrame(
            {
                "Feature": importance_data.index,
                "Importance mean": importance_data.mean(axis=1),
                "Importance std": importance_data.std(axis=1),
            }
        )
        .sort_values(
            by="Importance mean",
            ascending=False,
        )
        .reset_index(drop=True)
    )

    return summary


def display_feature_importance(
    results: ModelTestResults,
    caption: str = "Feature Importance Across Seeds",
) -> None:
    """Display mean feature importance across model seeds."""

    summary = prepare_feature_importance_summary(results)

    display_data = pd.DataFrame(
        {
            "Feature": summary["Feature"],
            "Importance": [
                _format_mean_std(
                    float(mean_value),
                    float(std_value),
                )
                for mean_value, std_value in zip(
                    summary["Importance mean"],
                    summary["Importance std"],
                    strict=True,
                )
            ],
        }
    )

    display(
        _style_table(
            display_data,
            caption=caption,
        )
    )


def prepare_grouped_feature_importance(
    results: ModelTestResults,
) -> pd.DataFrame:
    """
    Group one-hot encoded mouth_condition features into one feature.

    Aggregation is performed per seed before calculating the mean and
    standard deviation across seeds.
    """

    if not results.feature_importances:
        raise ValueError(f"Model '{results.model_name}' has no feature importances.")

    grouped_by_seed: dict[int, pd.Series] = {}

    for seed, importances in results.feature_importances.items():
        mouth_condition_mask = importances.index.str.startswith("mouth_condition_")

        other_importances = importances.loc[~mouth_condition_mask].copy()

        mouth_condition_importance = importances.loc[mouth_condition_mask].sum()

        other_importances["mouth_condition"] = mouth_condition_importance

        grouped_by_seed[seed] = other_importances

    importance_data = pd.concat(
        grouped_by_seed,
        axis=1,
    )

    summary = (
        pd.DataFrame(
            {
                "Feature": importance_data.index,
                "Importance mean": importance_data.mean(axis=1),
                "Importance std": importance_data.std(axis=1),
            }
        )
        .sort_values(
            "Importance mean",
            ascending=False,
        )
        .reset_index(drop=True)
    )

    return summary


FEATURE_IMPORTANCE_ORDER: tuple[str, ...] = (
    "amount_of_h",
    "amount_of_r",
    "amount_of_te",
    "amount_of_m3f",
    "amount_of_m3i",
    "amount_of_cpum",
    "mouth_condition",
    "amount_of_im",
    "amount_of_p",
    "amount_of_di",
    "amount_of_c",
)


SET3_COLORS = plt.get_cmap("Set3").colors  # type: ignore

FEATURE_IMPORTANCE_COLORS = {
    feature: SET3_COLORS[index]
    for index, feature in enumerate(FEATURE_IMPORTANCE_ORDER)
}


def plot_feature_importance_pie(
    results: ModelTestResults,
    title: str | None = None,
) -> None:
    """Plot grouped feature importance with a side legend."""

    summary = prepare_grouped_feature_importance(results)

    colors = [FEATURE_IMPORTANCE_COLORS[feature] for feature in summary["Feature"]]

    figure, axis = plt.subplots(
        figsize=(10, 7),
    )

    wedges, _ = axis.pie(
        summary["Importance mean"],
        colors=colors,
        startangle=90,
    )

    legend_labels = [
        f"{feature}: {importance:.1%}"
        for feature, importance in zip(
            summary["Feature"],
            summary["Importance mean"],
            strict=True,
        )
    ]

    axis.legend(
        wedges,
        legend_labels,
        title="Features",
        loc="center left",
        bbox_to_anchor=(1.0, 0.5),
        frameon=False,
    )

    axis.set_title(title or f"{results.model_name} — Feature Importance")

    axis.axis("equal")

    figure.tight_layout()
    plt.show()


def plot_feature_importance_pies(
    model_results: Mapping[str, ModelTestResults],
) -> None:
    """Plot one feature-importance pie chart for each model."""

    if not model_results:
        raise ValueError("model_results must contain at least one model.")

    for results in model_results.values():
        plot_feature_importance_pie(
            results,
            title=(f"{results.model_name} — Grouped Feature Importance"),
        )


# =============================================================================
# Model evaluation
# =============================================================================


def _calculate_classification_metrics(
    target_data_for_test: pd.Series,
    predicted_series: pd.Series,
) -> dict[str, float]:
    """Calculate classification test metrics."""

    return {
        "Accuracy": accuracy_score(
            target_data_for_test,
            predicted_series,
        ),
        "Balanced Accuracy": balanced_accuracy_score(
            target_data_for_test,
            predicted_series,
        ),
        "Macro F1": f1_score(
            target_data_for_test,
            predicted_series,
            average="macro",
            zero_division=0,
        ),
    }  # type: ignore


def _calculate_regression_metrics(
    target_data_for_test: pd.Series,
    predicted_series: pd.Series,
) -> dict[str, float]:
    """Calculate regression test metrics."""

    rmse = float(
        np.sqrt(
            mean_squared_error(
                target_data_for_test,
                predicted_series,
            )
        )
    )

    return {
        "MAE": mean_absolute_error(
            target_data_for_test,
            predicted_series,
        ),
        "RMSE": rmse,
        "R²": r2_score(
            target_data_for_test,
            predicted_series,
        ),
    }


def _run_model_test_evaluation(
    model_name: str,
    task: Task,
    model_factory: Callable[[int], PredictiveModel],
    best_parameters: Mapping[str, object],
    input_data_for_train: pd.DataFrame,
    target_data_for_train: pd.Series,
    input_data_for_test: pd.DataFrame,
    target_data_for_test: pd.Series,
    seeds: Sequence[int],
    metric_calculator: MetricCalculator,
    estimator_step: str,
) -> ModelTestResults:
    """Fit and evaluate a predictive model across repeated test runs."""

    if not seeds:
        raise ValueError("seeds must contain at least one seed.")

    predictions: dict[int, pd.Series] = {}
    metric_rows: list[dict[str, object]] = []
    feature_importances: dict[int, pd.Series] = {}

    for current_seed in seeds:
        model = model_factory(current_seed)

        model.set_params(**best_parameters)

        model.fit(
            input_data_for_train,
            target_data_for_train,
        )

        predicted_values = np.asarray(
            model.predict(input_data_for_test),
        )

        if predicted_values.ndim != 1:
            raise ValueError(
                f"Expected one-dimensional predictions, got "
                f"shape {predicted_values.shape}."
            )

        predicted_series = pd.Series(
            predicted_values,
            index=target_data_for_test.index,
            name="prediction",
        )

        predictions[current_seed] = predicted_series

        metric_row: dict[str, object] = {
            "Model": model_name,
            "Seed": current_seed,
        }

        metric_row.update(
            metric_calculator(
                target_data_for_test,
                predicted_series,
            )
        )

        metric_rows.append(metric_row)

        pipeline_model = cast(
            PipelineModel,
            model,
        )

        feature_importances[current_seed] = _extract_feature_importances(
            pipeline_model,
            estimator_step=estimator_step,
        )

    return ModelTestResults(
        model_name=model_name,
        task=task,
        predictions=predictions,
        seed_metrics=pd.DataFrame(metric_rows),
        feature_importances=feature_importances,
    )


def run_classification_model_test_evaluation(
    model_name: str,
    model_factory: Callable[[int], PredictiveModel],
    best_parameters: Mapping[str, object],
    input_data_for_train: pd.DataFrame,
    target_data_for_train: pd.Series,
    input_data_for_test: pd.DataFrame,
    target_data_for_test: pd.Series,
    seeds: Sequence[int],
) -> ModelTestResults:
    """Fit and evaluate a classification model on a fixed test set."""

    return _run_model_test_evaluation(
        model_name=model_name,
        task="classification",
        model_factory=model_factory,
        best_parameters=best_parameters,
        input_data_for_train=input_data_for_train,
        target_data_for_train=target_data_for_train,
        input_data_for_test=input_data_for_test,
        target_data_for_test=target_data_for_test,
        seeds=seeds,
        metric_calculator=_calculate_classification_metrics,
        estimator_step="classifier",
    )


def run_regression_model_test_evaluation(
    model_name: str,
    model_factory: Callable[[int], PredictiveModel],
    best_parameters: Mapping[str, object],
    input_data_for_train: pd.DataFrame,
    target_data_for_train: pd.Series,
    input_data_for_test: pd.DataFrame,
    target_data_for_test: pd.Series,
    seeds: Sequence[int],
) -> ModelTestResults:
    """Fit and evaluate a regression model on a fixed test set."""

    return _run_model_test_evaluation(
        model_name=model_name,
        task="regression",
        model_factory=model_factory,
        best_parameters=best_parameters,
        input_data_for_train=input_data_for_train,
        target_data_for_train=target_data_for_train,
        input_data_for_test=input_data_for_test,
        target_data_for_test=target_data_for_test,
        seeds=seeds,
        metric_calculator=_calculate_regression_metrics,
        estimator_step="regressor",
    )


# =============================================================================
# Test metrics
# =============================================================================


def prepare_seed_test_results(
    model_results: Mapping[str, ModelTestResults],
) -> pd.DataFrame:
    """Combine seed-level test metrics for all models."""

    if not model_results:
        raise ValueError("model_results must contain at least one model.")

    data_frames = [results.seed_metrics for results in model_results.values()]

    return (
        pd.concat(
            data_frames,
            ignore_index=True,
        )
        .sort_values(
            by=["Seed", "Model"],
        )
        .reset_index(drop=True)
    )


def prepare_test_summary(
    seed_test_results: pd.DataFrame,
    metric_directions: Mapping[str, bool],
    sort_metric: str,
) -> pd.DataFrame:
    """Calculate mean and standard deviation across test seeds."""

    metric_columns = list(metric_directions)

    if sort_metric not in metric_directions:
        raise ValueError(f"Unknown sort metric: {sort_metric}")

    _require_columns(
        seed_test_results,
        ["Model", *metric_columns],
        "seed_test_results",
    )

    summary = (
        seed_test_results.groupby("Model")[metric_columns]
        .agg(["mean", "std"])
        .reset_index()
    )

    flattened_columns: list[str] = []

    for column in summary.columns:
        if isinstance(column, tuple):
            first, second = column

            flattened_columns.append(
                str(first) if second == "" else f"{first} {second}"
            )
        else:
            flattened_columns.append(str(column))

    summary.columns = flattened_columns

    return summary.sort_values(
        by=f"{sort_metric} mean",
        ascending=not metric_directions[sort_metric],
    ).reset_index(drop=True)


def prepare_test_summary_display(
    summary: pd.DataFrame,
    metric_directions: Mapping[str, bool],
) -> pd.DataFrame:
    """Prepare a human-readable cross-seed summary table."""

    _require_columns(
        summary,
        [
            "Model",
            *[
                column
                for metric in metric_directions
                for column in (
                    f"{metric} mean",
                    f"{metric} std",
                )
            ],
        ],
        "summary",
    )

    display_data = summary[["Model"]].copy()

    for metric_name in metric_directions:
        display_data[metric_name] = [
            _format_mean_std(
                float(mean_value),
                float(std_value),
            )
            for mean_value, std_value in zip(
                summary[f"{metric_name} mean"],
                summary[f"{metric_name} std"],
                strict=True,
            )
        ]

    return display_data


def display_seed_test_results(
    data_frame: pd.DataFrame,
    metric_directions: Mapping[str, bool],
    caption: str = "Test Performance by Seed",
) -> None:
    """Display seed-level test metrics."""

    format_mapping = {metric_name: "{:.4f}" for metric_name in metric_directions}

    styled_data = _style_table(
        data_frame,
        caption=caption,
        format_mapping=format_mapping,
    ).apply(
        _highlight_seed_metric_winners,
        axis=None,
        metric_directions=metric_directions,
    )

    display(styled_data)


def display_test_summary(
    summary: pd.DataFrame,
    metric_directions: Mapping[str, bool],
    caption: str = "Test Performance Across Seeds",
) -> None:
    """Display cross-seed model comparison."""

    display_data = prepare_test_summary_display(
        summary,
        metric_directions,
    )

    styled_data = _style_table(
        display_data,
        caption=caption,
    ).apply(
        _highlight_best_summary_metrics,
        axis=None,
        summary=summary,
        metric_directions=metric_directions,
    )

    display(styled_data)


# =============================================================================
# Classification: per-age-group analysis
# =============================================================================


def _convert_predictions_to_age_groups(
    results: ModelTestResults,
    predictions: pd.Series,
) -> pd.Series:
    """Convert model predictions to the common ordered age-group representation."""

    if results.task == "classification":
        age_groups = predictions

    elif results.task == "regression":
        age_groups = group_age(
            pd.to_numeric(
                predictions,
                errors="raise",
            )
        )

    else:
        raise ValueError(f"Unsupported model task: {results.task}")

    return pd.Series(
        pd.Categorical(
            age_groups,
            categories=AGE_GROUP_ORDER,
            ordered=True,
        ),
        index=predictions.index,
        name="prediction",
    )


def prepare_per_age_group_test_metrics(
    model_results: Mapping[str, ModelTestResults],
    target_data_for_test: pd.Series,
) -> pd.DataFrame:
    """Calculate per-age-group metrics across all classification seeds."""

    rows: list[dict[str, object]] = []

    for model_name, results in model_results.items():
        if results.task != "classification":
            raise ValueError(f"Model '{model_name}' is not a classification model.")

        _validate_predictions_against_target(
            results.predictions,
            target_data_for_test,
        )

        for seed, predictions in results.predictions.items():
            precision, recall, f1, support = precision_recall_fscore_support(
                target_data_for_test,
                predictions,
                labels=AGE_GROUP_ORDER,
                zero_division=0,
            )

            for (
                age_group,
                precision_value,
                recall_value,
                f1_value,
                support_value,
            ) in zip(
                AGE_GROUP_ORDER,
                precision,  # type: ignore
                recall,  # type: ignore
                f1,  # type: ignore
                support,  # type: ignore
                strict=True,
            ):
                rows.append(
                    {
                        "Model": model_name,
                        "Seed": seed,
                        "Age Group": age_group,
                        "Precision": float(precision_value),
                        "Recall": float(recall_value),
                        "F1": float(f1_value),
                        "Support": int(support_value),
                    }
                )

    if not rows:
        raise ValueError("No classification results were provided.")

    return pd.DataFrame(rows)


def prepare_per_age_group_summary(
    per_age_group_results: pd.DataFrame,
) -> pd.DataFrame:
    """Aggregate per-age-group metrics across seeds."""

    _require_columns(
        per_age_group_results,
        [
            "Model",
            "Age Group",
            "Precision",
            "Recall",
            "F1",
            "Support",
        ],
        "per_age_group_results",
    )

    summary = (
        per_age_group_results.groupby(
            ["Model", "Age Group"],
            observed=True,
        )
        .agg(
            Precision_mean=("Precision", "mean"),
            Precision_std=("Precision", "std"),
            Recall_mean=("Recall", "mean"),
            Recall_std=("Recall", "std"),
            F1_mean=("F1", "mean"),
            F1_std=("F1", "std"),
            Support=("Support", "first"),
        )
        .reset_index()
        .rename(
            columns={
                "Precision_mean": "Precision mean",
                "Precision_std": "Precision std",
                "Recall_mean": "Recall mean",
                "Recall_std": "Recall std",
                "F1_mean": "F1 mean",
                "F1_std": "F1 std",
            }
        )
    )

    age_order = {age_group: index for index, age_group in enumerate(AGE_GROUP_ORDER)}

    summary["_Age Order"] = summary["Age Group"].map(age_order)

    return (
        summary.sort_values(
            by=["Model", "_Age Order"],
        )
        .drop(columns="_Age Order")
        .reset_index(drop=True)
    )


def prepare_per_age_group_display(
    summary: pd.DataFrame,
) -> pd.DataFrame:
    """Prepare readable per-age-group metrics."""

    return pd.DataFrame(
        {
            "Model": summary["Model"],
            "Age Group": summary["Age Group"],
            "Support": summary["Support"],
            "Precision": [
                _format_mean_std(
                    float(mean_value),
                    float(std_value),
                )
                for mean_value, std_value in zip(
                    summary["Precision mean"],
                    summary["Precision std"],
                    strict=True,
                )
            ],
            "Recall": [
                _format_mean_std(
                    float(mean_value),
                    float(std_value),
                )
                for mean_value, std_value in zip(
                    summary["Recall mean"],
                    summary["Recall std"],
                    strict=True,
                )
            ],
            "F1": [
                _format_mean_std(
                    float(mean_value),
                    float(std_value),
                )
                for mean_value, std_value in zip(
                    summary["F1 mean"],
                    summary["F1 std"],
                    strict=True,
                )
            ],
        }
    )


def display_per_age_group_summary(
    summary: pd.DataFrame,
    caption: str = "Per-Age-Group Test Performance Across Seeds",
) -> None:
    """Display per-age-group model performance."""

    display_data = prepare_per_age_group_display(summary)

    display(
        _style_table(
            display_data,
            caption=caption,
        )
    )


# =============================================================================
# Classification: confusion matrices
# =============================================================================


def prepare_mean_confusion_matrix(
    results: ModelTestResults,
    target_data_for_test: pd.Series,
) -> tuple[np.ndarray, np.ndarray]:
    """Calculate mean raw and row-normalized confusion matrices."""

    if not results.predictions:
        raise ValueError(f"Model '{results.model_name}' has no predictions.")

    # The actual target is always numeric age for this analysis.
    actual_age_groups = group_age(
        pd.to_numeric(
            target_data_for_test,
            errors="raise",
        )
    )

    raw_matrices: list[np.ndarray] = []
    normalized_matrices: list[np.ndarray] = []

    for predictions in results.predictions.values():
        predicted_age_groups = _convert_predictions_to_age_groups(
            results,
            predictions,
        )

        if not predicted_age_groups.index.equals(actual_age_groups.index):
            raise ValueError(
                "Prediction index does not match the target test-set index."
            )

        matrix = confusion_matrix(
            actual_age_groups,
            predicted_age_groups,
            labels=AGE_GROUP_ORDER,
        ).astype(float)

        raw_matrices.append(matrix)

        row_sums = matrix.sum(
            axis=1,
            keepdims=True,
        )

        normalized_matrix = np.divide(
            matrix,
            row_sums,
            out=np.zeros_like(matrix),
            where=row_sums != 0,
        )

        normalized_matrices.append(normalized_matrix)

    mean_raw_matrix = np.mean(
        raw_matrices,
        axis=0,
    )

    mean_normalized_matrix = (
        np.mean(
            normalized_matrices,
            axis=0,
        )
        * 100
    )

    return (
        mean_raw_matrix,
        mean_normalized_matrix,
    )


def prepare_confusion_matrix_table(
    matrix: npt.NDArray[np.float64],
) -> pd.DataFrame:
    """Prepare a confusion matrix as a labeled DataFrame."""

    return pd.DataFrame(
        matrix,
        index=AGE_GROUP_ORDER,
        columns=AGE_GROUP_ORDER,
    )


def display_confusion_matrix_table(
    matrix: npt.NDArray[np.float64],
    caption: str,
    percentage: bool = False,
) -> None:
    """Display a confusion matrix as an HTML table."""

    display_data = prepare_confusion_matrix_table(matrix).copy()

    display_data.index.name = "Actual"
    display_data.columns.name = "Predicted"

    format_string = "{:.1f}%" if percentage else "{:.2f}"

    display(
        _style_table(
            display_data,
            caption=caption,
            format_mapping={column: format_string for column in display_data.columns},
            hide_index=False,
        )
    )


def plot_mean_confusion_matrix(
    results: ModelTestResults,
    target_data_for_test: pd.Series,
    title: str,
) -> None:
    """Plot the mean row-normalized age-group confusion matrix."""

    _, normalized_matrix = prepare_mean_confusion_matrix(
        results,
        target_data_for_test,
    )

    figure, axis = plt.subplots(
        figsize=(8, 7),
    )

    image = axis.imshow(
        normalized_matrix,
        vmin=0,
        vmax=100,
        cmap="Oranges",
    )

    figure.colorbar(
        image,
        ax=axis,
        label="Percentage",
    )

    positions = np.arange(len(AGE_GROUP_ORDER))

    axis.set_xticks(
        positions,
        AGE_GROUP_ORDER,
    )

    axis.set_yticks(
        positions,
        AGE_GROUP_ORDER,
    )

    axis.set_xlabel("Predicted age group")
    axis.set_ylabel("Actual age group")
    axis.set_title(title)

    for row_index in range(len(AGE_GROUP_ORDER)):
        for column_index in range(len(AGE_GROUP_ORDER)):
            value = normalized_matrix[
                row_index,
                column_index,
            ]

            axis.text(
                column_index,
                row_index,
                f"{value:.1f}%",
                ha="center",
                va="center",
            )

    figure.tight_layout()
    plt.show()


# =============================================================================
# Classification: distribution analysis
# =============================================================================


def prepare_prediction_distribution(
    results: ModelTestResults,
    target_data_for_test: pd.Series,
) -> pd.DataFrame:
    """Calculate actual and predicted age-group distributions."""

    actual_age_groups = group_age(
        pd.to_numeric(
            target_data_for_test,
            errors="raise",
        )
    )

    actual_counts = actual_age_groups.value_counts().reindex(
        AGE_GROUP_ORDER,
        fill_value=0,
    )

    predicted_counts: list[np.ndarray] = []

    for predictions_for_seed in results.predictions.values():
        predicted_age_groups = _convert_predictions_to_age_groups(
            results,
            predictions_for_seed,
        )

        counts = predicted_age_groups.value_counts().reindex(
            AGE_GROUP_ORDER,
            fill_value=0,
        )

        predicted_counts.append(counts.to_numpy())

    if not predicted_counts:
        raise ValueError(f"Model '{results.model_name}' has no predictions.")

    predicted_counts_array = np.vstack(predicted_counts)

    return pd.DataFrame(
        {
            "Age Group": AGE_GROUP_ORDER,
            "Actual": actual_counts.to_numpy(),
            "Predicted mean": predicted_counts_array.mean(axis=0),
            "Predicted std": predicted_counts_array.std(axis=0),
        }
    )


def plot_actual_vs_predicted_distribution(
    model_results: Mapping[str, ModelTestResults],
    target_data_for_test: pd.Series,
    title: str = "Actual vs Predicted Age-Group Distribution",
) -> None:
    """Plot actual and mean predicted age-group counts."""

    if not model_results:
        raise ValueError("model_results must contain at least one model.")

    model_names = list(model_results)

    number_of_series = len(model_names) + 1
    bar_width = 0.8 / number_of_series

    x_positions = np.arange(len(AGE_GROUP_ORDER))

    # The actual test target is always numeric age.
    actual_age_groups = group_age(
        pd.to_numeric(
            target_data_for_test,
            errors="raise",
        )
    )

    actual_counts = (
        actual_age_groups.value_counts()
        .reindex(
            AGE_GROUP_ORDER,
            fill_value=0,
        )
        .to_numpy()
    )

    figure, axis = plt.subplots(
        figsize=(12, 6),
    )

    actual_offsets = x_positions - (number_of_series - 1) * bar_width / 2

    axis.bar(
        actual_offsets,
        actual_counts,
        width=bar_width,
        color=PALETTE[0],
        label="Actual",
    )

    for model_index, (
        model_name,
        results,
    ) in enumerate(
        model_results.items(),
        start=1,
    ):
        distribution = prepare_prediction_distribution(
            results,
            target_data_for_test,
        )

        offsets = (
            x_positions
            - (number_of_series - 1) * bar_width / 2
            + model_index * bar_width
        )

        axis.bar(
            offsets,
            distribution["Predicted mean"],
            width=bar_width,
            yerr=distribution["Predicted std"],
            capsize=4,
            color=PALETTE[model_index % len(PALETTE)],
            label=model_name,
        )

    axis.set_xticks(
        x_positions,
        AGE_GROUP_ORDER,
    )

    axis.set_xlabel("Age group")
    axis.set_ylabel("Number of patients")
    axis.set_title(title)
    axis.legend()

    figure.tight_layout()
    plt.show()


def plot_actual_vs_predicted_age(
    results: ModelTestResults,
    target_data_for_test: pd.Series,
) -> None:
    """Plot predicted age against actual age for a regression model."""

    if results.task != "regression":
        raise ValueError(f"Model '{results.model_name}' is not a regression model.")

    actual_age = pd.to_numeric(
        target_data_for_test,
        errors="raise",
    )

    prediction_data = []

    for predictions in results.predictions.values():
        prediction_data.append(
            pd.to_numeric(
                predictions,
                errors="raise",
            ).to_numpy()
        )

    predicted_age = np.vstack(prediction_data)

    # Mean prediction across seeds.
    mean_predicted_age = predicted_age.mean(axis=0)

    # Use the complete actual-age range for both axes.
    minimum_age = float(actual_age.min())
    maximum_age = float(actual_age.max())

    figure, axis = plt.subplots(
        figsize=(8, 7),
    )

    axis.scatter(
        actual_age,
        mean_predicted_age,
        alpha=0.7,
        color=DEFAULT_COLOR,
    )

    axis.plot(
        [minimum_age, maximum_age],
        [minimum_age, maximum_age],
        linestyle="--",
    )

    axis.set_xlim(
        minimum_age,
        maximum_age,
    )

    axis.set_ylim(
        minimum_age,
        maximum_age,
    )

    axis.set_xlabel("Actual age")
    axis.set_ylabel("Predicted age")

    axis.set_title(f"{results.model_name} — Actual vs Predicted Age")

    axis.grid(
        alpha=0.2,
    )

    figure.tight_layout()
    plt.show()


def plot_age_residuals(
    results: ModelTestResults,
    target_data_for_test: pd.Series,
) -> None:
    """Plot regression residuals against actual age."""

    if results.task != "regression":
        raise ValueError(f"Model '{results.model_name}' is not a regression model.")

    actual_age = pd.to_numeric(
        target_data_for_test,
        errors="raise",
    )

    predictions = np.vstack(
        [
            pd.to_numeric(
                seed_predictions,
                errors="raise",
            ).to_numpy()
            for seed_predictions in results.predictions.values()
        ]
    )

    mean_predicted_age = predictions.mean(axis=0)

    residuals = mean_predicted_age - actual_age.to_numpy()

    figure, axis = plt.subplots(
        figsize=(9, 6),
    )

    axis.scatter(
        actual_age,
        residuals,
        alpha=0.7,
        color=DEFAULT_COLOR,
    )

    axis.axhline(
        0,
        linestyle="--",
    )

    axis.set_xlabel("Actual age")
    axis.set_ylabel("Residual (predicted − actual)")
    axis.set_title(f"{results.model_name} — Residuals vs Actual Age")

    axis.grid(
        alpha=0.2,
    )

    figure.tight_layout()
    plt.show()


# =============================================================================
# Classification: F1 plot
# =============================================================================


def plot_per_age_group_f1(
    per_age_group_summary: pd.DataFrame,
    title: str = "Per-Age-Group F1 Across Seeds",
) -> None:
    """Plot mean F1 with standard deviation by age group."""

    _require_columns(
        per_age_group_summary,
        [
            "Model",
            "Age Group",
            "F1 mean",
            "F1 std",
        ],
        "per_age_group_summary",
    )

    models = list(per_age_group_summary["Model"].unique())

    if not models:
        raise ValueError("per_age_group_summary contains no models.")

    x_positions = np.arange(len(AGE_GROUP_ORDER))

    bar_width = 0.8 / len(models)

    figure, axis = plt.subplots(
        figsize=(11, 6),
    )

    for model_index, model_name in enumerate(models):
        model_data = (
            per_age_group_summary[per_age_group_summary["Model"] == model_name]
            .set_index("Age Group")
            .reindex(AGE_GROUP_ORDER)
        )

        offsets = x_positions + (model_index - (len(models) - 1) / 2) * bar_width

        axis.bar(
            offsets,
            model_data["F1 mean"],
            width=bar_width,
            yerr=model_data["F1 std"],
            capsize=4,
            label=model_name,
            color=PALETTE[model_index % len(PALETTE)],
        )

    axis.set_xticks(
        x_positions,
        AGE_GROUP_ORDER,
    )

    axis.set_ylim(0, 1)
    axis.set_xlabel("Age group")
    axis.set_ylabel("F1")
    axis.set_title(title)
    axis.legend()

    figure.tight_layout()
    plt.show()


# =============================================================================
# Task dispatch
# =============================================================================


def _split_model_results_by_task(
    model_results: Mapping[str, ModelTestResults],
) -> tuple[
    dict[str, ModelTestResults],
    dict[str, ModelTestResults],
]:
    """Split model results according to their explicit task."""

    classification_results: dict[
        str,
        ModelTestResults,
    ] = {}

    regression_results: dict[
        str,
        ModelTestResults,
    ] = {}

    for model_name, results in model_results.items():
        if results.task == "classification":
            classification_results[model_name] = results
        elif results.task == "regression":
            regression_results[model_name] = results
        else:
            raise ValueError(
                f"Unsupported model task for '{model_name}': {results.task}"
            )

    return classification_results, regression_results


# =============================================================================
# Complete report
# =============================================================================


def display_complete_test_report(
    model_results: Mapping[str, ModelTestResults],
    classification_target_data_for_test: pd.Series,
    regression_target_data_for_test: pd.Series,
) -> None:
    """Display the complete test-result tables for all model types."""

    if not model_results:
        raise ValueError("model_results must contain at least one model.")

    (
        classification_results,
        regression_results,
    ) = _split_model_results_by_task(model_results)

    # -------------------------------------------------------------------------
    # Classification
    # -------------------------------------------------------------------------

    if classification_results:
        classification_seed_results = prepare_seed_test_results(
            classification_results,
        )

        display_seed_test_results(
            classification_seed_results,
            metric_directions=CLASSIFICATION_TEST_METRICS,
            caption="Classification Test Performance by Seed",
        )

        classification_summary = prepare_test_summary(
            classification_seed_results,
            metric_directions=CLASSIFICATION_TEST_METRICS,
            sort_metric="Macro F1",
        )

        display_test_summary(
            classification_summary,
            metric_directions=CLASSIFICATION_TEST_METRICS,
            caption="Classification Test Performance Across Seeds",
        )

        per_age_group_results = prepare_per_age_group_test_metrics(
            classification_results,
            classification_target_data_for_test,
        )

        per_age_group_summary = prepare_per_age_group_summary(
            per_age_group_results,
        )

        display_per_age_group_summary(
            per_age_group_summary,
        )

        for model_name, results in classification_results.items():
            raw_matrix, normalized_matrix = prepare_mean_confusion_matrix(
                results,
                regression_target_data_for_test,
            )

            display_confusion_matrix_table(
                raw_matrix,
                caption=(f"{model_name} — Mean Confusion Matrix"),
            )

            display_confusion_matrix_table(
                normalized_matrix,
                caption=(f"{model_name} — Mean Row-Normalized Confusion Matrix"),
                percentage=True,
            )

    # -------------------------------------------------------------------------
    # Regression
    # -------------------------------------------------------------------------

    if regression_results:
        regression_seed_results = prepare_seed_test_results(
            regression_results,
        )

        display_seed_test_results(
            regression_seed_results,
            metric_directions=REGRESSION_TEST_METRICS,
            caption="Regression Test Performance by Seed",
        )

        regression_summary = prepare_test_summary(
            regression_seed_results,
            metric_directions=REGRESSION_TEST_METRICS,
            sort_metric="MAE",
        )

        display_test_summary(
            regression_summary,
            metric_directions=REGRESSION_TEST_METRICS,
            caption="Regression Test Performance Across Seeds",
        )

        # Keep the regression target explicit even though the generic
        # summary functions do not need it.
        if regression_target_data_for_test.empty:
            raise ValueError("regression_target_data_for_test must not be empty.")

    # -------------------------------------------------------------------------
    # Feature importance
    # -------------------------------------------------------------------------

    for model_name, results in model_results.items():
        display_feature_importance(
            results,
            caption=f"{model_name} — Feature Importances",
        )


# =============================================================================
# Complete plots
# =============================================================================


def plot_complete_test_report(
    model_results: Mapping[str, ModelTestResults],
    regression_target_data_for_test: pd.Series,
    per_age_group_summary: pd.DataFrame,
) -> None:
    """Plot the main classification test-result figures."""

    for model_name, results in model_results.items():
        plot_mean_confusion_matrix(
            results,
            regression_target_data_for_test,
            title=(f"{model_name} — Mean Row-Normalized Confusion Matrix"),
        )

    plot_per_age_group_f1(
        per_age_group_summary,
        title="Per-Age-Group F1 Across Seeds",
    )

    plot_actual_vs_predicted_distribution(
        model_results,
        regression_target_data_for_test,
    )
