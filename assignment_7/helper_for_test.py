from collections.abc import Callable, Mapping
from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from IPython.display import display
from sklearn.base import BaseEstimator
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    precision_recall_fscore_support,
)

from helper_for_analysis import PALETTE

AGE_GROUP_ORDER = [
    "10-19",
    "20-29",
    "30-39",
    "40-49",
    "50-59",
    "60-69",
    "70+",
]

TEST_METRIC_COLUMNS = [
    "Accuracy",
    "Balanced Accuracy",
    "Macro F1",
]


@dataclass
class ModelTestResults:
    """Store predictions, metrics, and feature importances from repeated test runs."""

    model_name: str
    predictions: dict[int, pd.Series]
    seed_metrics: pd.DataFrame
    feature_importances: dict[int, pd.Series]


def run_model_test_evaluation(
    model_name: str,
    model_factory: Callable[[int], BaseEstimator],
    best_parameters: Mapping[str, object],
    input_data_for_train: pd.DataFrame,
    target_data_for_train: pd.Series,
    input_data_for_test: pd.DataFrame,
    target_data_for_test: pd.Series,
    seeds: list[int],
) -> ModelTestResults:
    """Fit a final model for each seed and evaluate it on the fixed test set."""

    predictions = {}
    metric_rows = []
    feature_importances = {}

    for current_seed in seeds:
        model = model_factory(current_seed)

        model.set_params(**best_parameters)

        model.fit(  # type: ignore
            input_data_for_train,
            target_data_for_train,
        )

        predicted_values = model.predict(  # type: ignore
            input_data_for_test,
        )

        predicted_series = pd.Series(
            predicted_values,
            index=target_data_for_test.index,
            name="prediction",
        )

        predictions[current_seed] = predicted_series

        metric_rows.append(
            {
                "Model": model_name,
                "Seed": current_seed,
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
            }
        )

        feature_importances[current_seed] = _extract_feature_importances(
            model,
            feature_names=list(input_data_for_train.columns),
        )

    seed_metrics = pd.DataFrame(metric_rows)

    return ModelTestResults(
        model_name=model_name,
        predictions=predictions,
        seed_metrics=seed_metrics,
        feature_importances=feature_importances,
    )


def prepare_seed_test_results(
    model_results: Mapping[str, ModelTestResults],
) -> pd.DataFrame:
    """Combine seed-level test metrics for all models."""

    data_frames = [results.seed_metrics for results in model_results.values()]

    combined_results = pd.concat(
        data_frames,
        ignore_index=True,
    )

    return combined_results.sort_values(
        by=["Seed", "Model"],
    ).reset_index(drop=True)


def _highlight_seed_metric_winners(
    data_frame: pd.DataFrame,
) -> pd.DataFrame:
    """Highlight the higher metric value within each seed."""

    styles = pd.DataFrame(
        "",
        index=data_frame.index,
        columns=data_frame.columns,
    )

    for seed in data_frame["Seed"].unique():
        seed_mask = data_frame["Seed"] == seed

        for metric in TEST_METRIC_COLUMNS:
            metric_values = data_frame.loc[
                seed_mask,
                metric,
            ]

            if metric_values.empty:  # type: ignore
                continue

            best_index = metric_values.idxmax()  # type: ignore

            styles.at[
                best_index,
                metric,
            ] = "font-weight: bold"

    return styles


def display_seed_test_results(
    data_frame: pd.DataFrame,
    caption: str = "Test Performance by Seed",
) -> None:
    """Display seed-level test metrics."""

    display_data = data_frame.copy()

    styled_data = (
        display_data.style.hide(axis="index")
        .format(
            {
                "Accuracy": "{:.4f}",
                "Balanced Accuracy": "{:.4f}",
                "Macro F1": "{:.4f}",
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
            _highlight_seed_metric_winners,
            axis=None,
        )
    )

    display(styled_data)


def prepare_test_summary(
    seed_test_results: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate mean and standard deviation across test seeds."""

    summary = (
        seed_test_results.groupby("Model", observed=True)[TEST_METRIC_COLUMNS]
        .agg(["mean", "std"])
        .reset_index()
    )

    summary.columns = [
        column[0] if column[1] == "" else f"{column[0]} {column[1]}"
        for column in summary.columns
    ]

    return summary.sort_values(
        by="Macro F1 mean",
        ascending=False,
    ).reset_index(drop=True)


def _format_mean_std(
    mean_value: float,
    std_value: float,
) -> str:
    """Format a mean and standard deviation."""

    return f"{mean_value:.4f} ± {std_value:.4f}"


def prepare_test_summary_display(
    summary: pd.DataFrame,
) -> pd.DataFrame:
    """Prepare a human-readable cross-seed summary table."""

    display_data = pd.DataFrame(
        {
            "Model": summary["Model"],
            "Accuracy": [
                _format_mean_std(
                    mean_value,
                    std_value,
                )
                for mean_value, std_value in zip(
                    summary["Accuracy mean"],
                    summary["Accuracy std"],
                )
            ],
            "Balanced Accuracy": [
                _format_mean_std(
                    mean_value,
                    std_value,
                )
                for mean_value, std_value in zip(
                    summary["Balanced Accuracy mean"],
                    summary["Balanced Accuracy std"],
                )
            ],
            "Macro F1": [
                _format_mean_std(
                    mean_value,
                    std_value,
                )
                for mean_value, std_value in zip(
                    summary["Macro F1 mean"],
                    summary["Macro F1 std"],
                )
            ],
        }
    )

    return display_data


def _highlight_best_summary_metrics(
    data_frame: pd.DataFrame,
    summary: pd.DataFrame,
) -> pd.DataFrame:
    """Highlight the highest mean for each test metric."""

    styles = pd.DataFrame(
        "",
        index=data_frame.index,
        columns=data_frame.columns,
    )

    best_metric_columns = {
        "Accuracy": "Accuracy mean",
        "Balanced Accuracy": "Balanced Accuracy mean",
        "Macro F1": "Macro F1 mean",
    }

    for display_column, numeric_column in best_metric_columns.items():
        best_index = summary[numeric_column].idxmax()

        styles.at[
            best_index,
            display_column,
        ] = "font-weight: bold"

    return styles


def display_test_summary(
    summary: pd.DataFrame,
    caption: str = "Test Performance Across Five Seeds",
) -> None:
    """Display cross-seed model comparison."""

    display_data = prepare_test_summary_display(
        summary,
    )

    styled_data = (
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
            _highlight_best_summary_metrics,
            axis=None,
            summary=summary,
        )
    )

    display(styled_data)


def prepare_per_age_group_test_metrics(
    model_results: Mapping[str, ModelTestResults],
    target_data_for_test: pd.Series,
) -> pd.DataFrame:
    """Calculate per-age-group metrics across all model seeds."""

    rows = []

    for model_name, results in model_results.items():
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
            ):
                rows.append(
                    {
                        "Model": model_name,
                        "Seed": seed,
                        "Age Group": age_group,
                        "Precision": precision_value,
                        "Recall": recall_value,
                        "F1": f1_value,
                        "Support": support_value,
                    }
                )

    return pd.DataFrame(rows)


def prepare_per_age_group_summary(
    per_age_group_results: pd.DataFrame,
) -> pd.DataFrame:
    """Aggregate per-age-group metrics across seeds."""

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
    )

    summary = summary.rename(
        columns={
            "Precision_mean": "Precision mean",
            "Precision_std": "Precision std",
            "Recall_mean": "Recall mean",
            "Recall_std": "Recall std",
            "F1_mean": "F1 mean",
            "F1_std": "F1 std",
        }
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
                    mean_value,
                    std_value,
                )
                for mean_value, std_value in zip(
                    summary["Precision mean"],
                    summary["Precision std"],
                )
            ],
            "Recall": [
                _format_mean_std(
                    mean_value,
                    std_value,
                )
                for mean_value, std_value in zip(
                    summary["Recall mean"],
                    summary["Recall std"],
                )
            ],
            "F1": [
                _format_mean_std(
                    mean_value,
                    std_value,
                )
                for mean_value, std_value in zip(
                    summary["F1 mean"],
                    summary["F1 std"],
                )
            ],
        }
    )


def display_per_age_group_summary(
    summary: pd.DataFrame,
    caption: str = "Per-Age-Group Test Performance Across Five Seeds",
) -> None:
    """Display per-age-group model performance."""

    display_data = prepare_per_age_group_display(
        summary,
    )

    styled_data = (
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
    )

    display(styled_data)


def prepare_mean_confusion_matrix(
    predictions: Mapping[int, pd.Series],
    target_data_for_test: pd.Series,
) -> tuple[np.ndarray, np.ndarray]:
    """Calculate mean raw and row-normalized confusion matrices."""

    raw_matrices = []
    normalized_matrices = []

    for seed in predictions:
        matrix = confusion_matrix(
            target_data_for_test,
            predictions[seed],
            labels=AGE_GROUP_ORDER,
        )

        raw_matrices.append(matrix.astype(float))

        row_sums = matrix.sum(axis=1, keepdims=True)

        normalized_matrix = np.divide(
            matrix,
            row_sums,
            out=np.zeros_like(
                matrix,
                dtype=float,
            ),
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
    matrix: np.ndarray,
) -> pd.DataFrame:
    """Prepare a confusion matrix as a labeled DataFrame."""

    return pd.DataFrame(
        matrix,
        index=AGE_GROUP_ORDER,
        columns=AGE_GROUP_ORDER,
    )


def display_confusion_matrix_table(
    matrix: np.ndarray,
    caption: str,
    percentage: bool = False,
) -> None:
    """Display a confusion matrix as an HTML table."""

    display_data = prepare_confusion_matrix_table(
        matrix,
    ).copy()

    display_data.index.name = "Actual"

    if percentage:
        display_data = display_data.map(lambda value: f"{value:.1f}%")
    else:
        display_data = display_data.map(lambda value: f"{value:.2f}")

    display_data.columns.name = "Predicted"

    styled_data = display_data.style.set_caption(caption).set_table_styles(
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

    display(styled_data)


def plot_mean_confusion_matrix(
    predictions: Mapping[int, pd.Series],
    target_data_for_test: pd.Series,
    title: str,
) -> None:
    """Plot the mean row-normalized confusion matrix."""

    _, normalized_matrix = prepare_mean_confusion_matrix(
        predictions,
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

    axis.set_xticks(
        np.arange(len(AGE_GROUP_ORDER)),
        AGE_GROUP_ORDER,
    )

    axis.set_yticks(
        np.arange(len(AGE_GROUP_ORDER)),
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


def plot_per_age_group_f1(
    per_age_group_summary: pd.DataFrame,
    title: str = "Per-Age-Group F1 Across Five Seeds",
) -> None:
    """Plot mean F1 with standard deviation by age group."""

    models = list(per_age_group_summary["Model"].unique())

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
            color=PALETTE[model_index],
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


def prepare_prediction_distribution(
    predictions: Mapping[int, pd.Series],
    target_data_for_test: pd.Series,
) -> pd.DataFrame:
    """Calculate actual and predicted age-group distributions."""

    actual_counts = target_data_for_test.value_counts().reindex(
        AGE_GROUP_ORDER,
        fill_value=0,
    )

    predicted_counts = []

    for predictions_for_seed in predictions.values():
        counts = predictions_for_seed.value_counts().reindex(
            AGE_GROUP_ORDER,
            fill_value=0,
        )

        predicted_counts.append(counts.to_numpy())

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

    actual_counts = (
        target_data_for_test.value_counts()
        .reindex(
            AGE_GROUP_ORDER,
            fill_value=0,
        )
        .to_numpy()
    )

    model_names = list(model_results.keys())

    x_positions = np.arange(len(AGE_GROUP_ORDER))

    number_of_series = len(model_names) + 1

    bar_width = 0.8 / number_of_series

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
            results.predictions,
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
            color=PALETTE[model_index],
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


def prepare_model_agreement(
    first_model_results: ModelTestResults,
    second_model_results: ModelTestResults,
    target_data_for_test: pd.Series,
) -> pd.DataFrame:
    """Measure prediction agreement between two models."""

    first_model_name = first_model_results.model_name
    second_model_name = second_model_results.model_name

    rows = []

    common_seeds = sorted(
        set(first_model_results.predictions) & set(second_model_results.predictions)
    )

    for age_group in AGE_GROUP_ORDER:
        total_predictions = 0
        same_predictions = 0

        age_mask = target_data_for_test == age_group

        for seed in common_seeds:
            first_predictions = first_model_results.predictions[seed]

            second_predictions = second_model_results.predictions[seed]

            same_mask = first_predictions == second_predictions

            combined_mask = age_mask & same_mask

            same_predictions += int(combined_mask.sum())

            total_predictions += int(age_mask.sum())

        agreement_percentage = (
            same_predictions / total_predictions * 100 if total_predictions > 0 else 0.0
        )

        rows.append(
            {
                "Age Group": age_group,
                "Support": int(age_mask.sum()),
                "Same Prediction (%)": (agreement_percentage),
                "Different Prediction (%)": (100 - agreement_percentage),
            }
        )

    result = pd.DataFrame(rows)

    result.attrs["first_model"] = first_model_name
    result.attrs["second_model"] = second_model_name

    return result


def display_model_agreement(
    agreement: pd.DataFrame,
    caption: str = "Decision Tree vs Random Forest Prediction Agreement",
) -> None:
    """Display model prediction agreement."""

    styled_data = (
        agreement.style.hide(axis="index")
        .format(
            {
                "Same Prediction (%)": "{:.1f}",
                "Different Prediction (%)": "{:.1f}",
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
    )

    display(styled_data)


def _extract_feature_importances(
    model: BaseEstimator,
    feature_names: list[str],
) -> pd.Series:
    """Extract feature importances from a fitted model or pipeline."""

    estimator = model

    # Your models use a pipeline with a classifier step.
    if hasattr(model, "named_steps") and "classifier" in model.named_steps:  # type: ignore
        estimator = model.named_steps["classifier"]  # type: ignore

    if not hasattr(estimator, "feature_importances_"):
        raise ValueError(
            f"{type(estimator).__name__} does not provide `feature_importances_`."
        )

    importances = np.asarray(
        estimator.feature_importances_,  # type: ignore
        dtype=float,
    )

    if len(importances) != len(feature_names):
        raise ValueError(
            "The number of feature names does not match the number "
            f"of feature importances: {len(feature_names)} != {len(importances)}."
        )

    return pd.Series(
        importances,
        index=feature_names,
        name="Importance",
    ).sort_values(ascending=False)


def display_feature_importance(
    results: ModelTestResults,
    caption: str = "Feature Importance Across Five Seeds",
) -> None:
    """Display mean feature importance across model seeds."""

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

    display_data = pd.DataFrame(
        {
            "Feature": summary["Feature"],
            "Importance": [
                _format_mean_std(
                    mean_value,
                    std_value,
                )
                for mean_value, std_value in zip(
                    summary["Importance mean"],
                    summary["Importance std"],
                )
            ],
        }
    )

    styled_data = (
        display_data.style.hide(axis="index")
        .set_caption(
            caption,
        )
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
    )

    display(styled_data)


def display_complete_test_report(
    model_results: Mapping[str, ModelTestResults],
    target_data_for_test: pd.Series,
) -> None:
    """Display the complete test-result table set."""

    seed_results = prepare_seed_test_results(
        model_results,
    )

    display_seed_test_results(
        seed_results,
    )

    summary = prepare_test_summary(
        seed_results,
    )

    display_test_summary(
        summary,
    )

    per_age_group_results = prepare_per_age_group_test_metrics(
        model_results,
        target_data_for_test,
    )

    per_age_group_summary = prepare_per_age_group_summary(
        per_age_group_results,
    )

    display_per_age_group_summary(
        per_age_group_summary,
    )

    for model_name, results in model_results.items():
        raw_matrix, normalized_matrix = prepare_mean_confusion_matrix(
            results.predictions,
            target_data_for_test,
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

        display_feature_importance(
            results,
            caption=f"{model_name} — Feature Importances",
        )


def plot_complete_test_report(
    model_results: Mapping[str, ModelTestResults],
    target_data_for_test: pd.Series,
    per_age_group_summary: pd.DataFrame,
) -> None:
    """Plot the main test-result figures."""

    for model_name, results in model_results.items():
        plot_mean_confusion_matrix(
            results.predictions,
            target_data_for_test,
            title=(f"{model_name} — Mean Row-Normalized Confusion Matrix"),
        )

    plot_per_age_group_f1(
        per_age_group_summary,
        title="Per-Age-Group F1 Across Five Seeds",
    )

    plot_actual_vs_predicted_distribution(
        model_results,
        target_data_for_test,
    )
