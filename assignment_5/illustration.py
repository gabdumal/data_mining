import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import StratifiedKFold

from columns import get_name_of_column

seed = 24


def train_test_split_table(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
) -> pd.io.formats.style.Styler:
    data = pd.DataFrame(
        {
            "dataset": ["train", "test"],
            "samples": [
                len(X_train),
                len(X_test),
            ],
            "percentage": [
                len(X_train) / (len(X_train) + len(X_test)) * 100,
                len(X_test) / (len(X_train) + len(X_test)) * 100,
            ],
            "features": [
                X_train.shape[1],
                X_test.shape[1],
            ],
        }
    )

    return data.style.format(
        {
            "samples": "{:,.0f}",
            "percentage": "{:.2f}%",
            "features": "{:,.0f}",
        }
    ).set_caption("Divisão entre treinamento e teste")


def class_distribution_table(
    target: pd.Series,
    caption: str = "Distribuição das classes",
) -> pd.io.formats.style.Styler:
    distribution = target.value_counts().rename("count").to_frame()
    distribution["percentage"] = distribution["count"] / len(target) * 100

    column_name = target.name
    if not isinstance(column_name, str):
        raise TypeError("The series must have a string column name.")
    distribution.index.name = get_name_of_column(column_name)

    return distribution.style.format(
        {
            "count": "{:,.0f}",
            "percentage": "{:.2f}%",
        }
    ).set_caption(caption)


def stratified_fold_table(
    X: pd.DataFrame,
    y: pd.Series,
    n_splits: int = 5,
    random_state: int = seed,
) -> pd.io.formats.style.Styler:
    stratified_kfold = StratifiedKFold(
        n_splits=n_splits,
        shuffle=True,
        random_state=random_state,
    )

    rows = []

    for fold_number, (_, validation_indices) in enumerate(
        stratified_kfold.split(X, y),
        start=1,
    ):
        validation_target = y.iloc[validation_indices]

        class_counts = validation_target.value_counts()

        row = {
            "fold": fold_number,
            "validation_samples": len(validation_indices),
        }

        for class_name in sorted(y.unique()):
            row[f"{class_name}_samples"] = class_counts.get(
                class_name,
                0,
            )

        rows.append(row)

    data = pd.DataFrame(rows)

    return data.style.format(
        {column: "{:,.0f}" for column in data.columns}
    ).set_caption("Distribuição das classes nos folds de validação")


def fold_size_table(
    X: pd.DataFrame,
    y: pd.Series,
    n_splits: int = 5,
    random_state: int = seed,
) -> pd.io.formats.style.Styler:
    stratified_kfold = StratifiedKFold(
        n_splits=n_splits,
        shuffle=True,
        random_state=random_state,
    )

    rows = []

    for fold_number, (train_indices, validation_indices) in enumerate(
        stratified_kfold.split(X, y),
        start=1,
    ):
        rows.append(
            {
                "fold": fold_number,
                "training_samples": len(train_indices),
                "validation_samples": len(validation_indices),
                "total_samples": len(train_indices) + len(validation_indices),
            }
        )

    data = pd.DataFrame(rows)

    return data.style.format(
        {
            "training_samples": "{:,.0f}",
            "validation_samples": "{:,.0f}",
            "total_samples": "{:,.0f}",
        }
    ).set_caption("Tamanho dos conjuntos em cada fold")


def grid_search_results_table(
    grid_search,
) -> pd.io.formats.style.Styler:
    results = pd.DataFrame(grid_search.cv_results_).copy()

    parameter_columns = [
        column for column in results.columns if column.startswith("param_")
    ]

    columns = (
        ["rank_test_score"]
        + parameter_columns
        + [
            "mean_test_score",
            "std_test_score",
        ]
    )

    data = results[columns].copy()

    data = data.sort_values("rank_test_score")

    data = data.rename(
        columns={
            "rank_test_score": "rank",
            "mean_test_score": "mean_f1_macro",
            "std_test_score": "std_f1_macro",
        }
    )

    data.columns = [column.replace("param_classifier__", "") for column in data.columns]

    return data.style.format(
        {
            "mean_f1_macro": "{:.4f}",
            "std_f1_macro": "{:.4f}",
        }
    ).set_caption("Resultados do Grid Search")


def best_parameters_table(
    grid_search,
) -> pd.io.formats.style.Styler:
    data = pd.DataFrame(
        list(grid_search.best_params_.items()),
        columns=["parameter", "value"],
    )

    data.loc[len(data)] = [
        "best_f1_macro",
        grid_search.best_score_,
    ]

    return data.style.format(
        {
            "value": lambda value: (
                f"{value:.4f}" if isinstance(value, float) else str(value)
            ),
        }
    ).set_caption("Melhores hiperparâmetros")


def calculate_classification_metrics(
    y_true,
    y_pred,
) -> dict:
    return {
        "accuracy": accuracy_score(
            y_true,
            y_pred,
        ),
        "precision_macro": precision_score(
            y_true,
            y_pred,
            average="macro",
            zero_division=0,
        ),
        "recall_macro": recall_score(
            y_true,
            y_pred,
            average="macro",
            zero_division=0,
        ),
        "f1_macro": f1_score(
            y_true,
            y_pred,
            average="macro",
            zero_division=0,
        ),
    }


def classification_metrics_comparison_table(
    model_metrics: dict,
) -> pd.io.formats.style.Styler:
    data = pd.DataFrame(model_metrics).T

    data.index.name = "model"

    return data.style.format(
        {
            "accuracy": "{:.4f}",
            "precision_macro": "{:.4f}",
            "recall_macro": "{:.4f}",
            "f1_macro": "{:.4f}",
        }
    ).set_caption("Desempenho dos modelos no conjunto de teste")
