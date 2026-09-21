import pandas as pd
from sklearn.model_selection import (
    StratifiedKFold,
    cross_validate,
)


def compare_smote(
    build_pipeline,
    input_data,
    target_data,
    seeds,
    n_splits=5,
):
    """Compare a model pipeline with and without SMOTE."""

    scoring = {
        "accuracy": "accuracy",
        "balanced_accuracy": "balanced_accuracy",
        "f1_macro": "f1_macro",
    }

    results = []

    for current_seed in seeds:
        stratified_cross_validation = StratifiedKFold(
            n_splits=n_splits,
            shuffle=True,
            random_state=current_seed,
        )

        pipelines = {
            "Without SMOTE": build_pipeline(
                random_state=current_seed,
                use_smote=False,
            ),
            "With SMOTE": build_pipeline(
                random_state=current_seed,
                use_smote=True,
            ),
        }

        for strategy, pipeline in pipelines.items():
            cross_validation_results = cross_validate(
                pipeline,
                input_data,
                target_data,
                cv=stratified_cross_validation,
                scoring=scoring,
                n_jobs=-1,
                return_train_score=False,
                error_score="raise",
            )

            results.append(
                {
                    "Seed": current_seed,
                    "Strategy": strategy,
                    "Accuracy": (cross_validation_results["test_accuracy"].mean()),
                    "Balanced Accuracy": (
                        cross_validation_results["test_balanced_accuracy"].mean()
                    ),
                    "Macro F1": (cross_validation_results["test_f1_macro"].mean()),
                }
            )

    results = pd.DataFrame(results)

    comparison = results.groupby(
        "Strategy",
        observed=True,
    ).agg(
        {
            "Accuracy": ["mean", "std"],
            "Balanced Accuracy": ["mean", "std"],
            "Macro F1": ["mean", "std"],
        }
    )

    comparison.columns = [f"{metric} {stat}" for metric, stat in comparison.columns]

    comparison = comparison.reset_index()

    metrics = [
        "Accuracy",
        "Balanced Accuracy",
        "Macro F1",
    ]

    for metric in metrics:
        comparison[metric] = (
            comparison[f"{metric} mean"].map(lambda value: f"{value:.3f}")
            + " ± "
            + comparison[f"{metric} std"].map(lambda value: f"{value:.3f}")
        )

    return comparison, results
