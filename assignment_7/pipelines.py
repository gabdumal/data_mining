from __future__ import annotations

from typing import TypeAlias

import pandas as pd
from imblearn.over_sampling import SMOTENC
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import (
    GradientBoostingRegressor,
    RandomForestClassifier,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier

from data import (
    categorical_features,
    classification_target_feature,
    input_features,
    numerical_features,
    regression_target_feature,
    t_df,
)

# =============================================================================
# Types
# =============================================================================

ClassificationPipeline: TypeAlias = Pipeline | ImbPipeline

ClassificationEstimator: TypeAlias = DecisionTreeClassifier | RandomForestClassifier


# =============================================================================
# Reproducibility
# =============================================================================

seeds: tuple[int, ...] = (
    27,
    32,
    59,
    74,
    93,
)

seed = seeds[0]

test_size = 0.2


# =============================================================================
# Data
# =============================================================================

input_data = t_df.loc[:, input_features].copy()

classification_target_data = t_df.loc[
    :,
    classification_target_feature,
].copy()

regression_target_data = t_df.loc[
    :,
    regression_target_feature,
].copy()


# =============================================================================
# Validation
# =============================================================================


def _validate_feature_configuration() -> None:
    """Validate the feature configuration used by the pipelines."""

    configured_features = list(categorical_features) + list(numerical_features)

    if set(configured_features) != set(input_features):
        raise ValueError(
            "categorical_features and numerical_features must contain "
            "exactly the columns in input_features."
        )

    if len(configured_features) != len(set(configured_features)):
        raise ValueError(
            "A feature appears more than once in the feature configuration."
        )


_validate_feature_configuration()


# =============================================================================
# Data split
# =============================================================================


def _split_data(
    input_data: pd.DataFrame,
    classification_target_data: pd.Series,
    regression_target_data: pd.Series,
    test_size: float,
    random_state: int,
) -> tuple[
    pd.DataFrame,
    pd.DataFrame,
    pd.Series,
    pd.Series,
    pd.Series,
    pd.Series,
]:
    """
    Create one stratified train/test split and reuse its indices
    for both classification and regression.
    """

    if not 0 < test_size < 1:
        raise ValueError("test_size must be strictly between 0 and 1.")

    if not (
        input_data.index.equals(classification_target_data.index)
        and input_data.index.equals(regression_target_data.index)
    ):
        raise ValueError(
            "Input data and both target Series must have identical indices."
        )

    train_indices, test_indices = train_test_split(
        input_data.index,
        test_size=test_size,
        random_state=random_state,
        stratify=classification_target_data,
    )

    classification_input_data_for_train = input_data.loc[train_indices].copy()

    classification_input_data_for_test = input_data.loc[test_indices].copy()

    classification_target_data_for_train = classification_target_data.loc[
        train_indices
    ].copy()

    classification_target_data_for_test = classification_target_data.loc[
        test_indices
    ].copy()

    regression_target_data_for_train = regression_target_data.loc[train_indices].copy()

    regression_target_data_for_test = regression_target_data.loc[test_indices].copy()

    return (
        classification_input_data_for_train,
        classification_input_data_for_test,
        classification_target_data_for_train,
        classification_target_data_for_test,
        regression_target_data_for_train,
        regression_target_data_for_test,
    )


(
    classification_input_data_for_train,
    classification_input_data_for_test,
    classification_target_data_for_train,
    classification_target_data_for_test,
    regression_target_data_for_train,
    regression_target_data_for_test,
) = _split_data(
    input_data=input_data,
    classification_target_data=classification_target_data,
    regression_target_data=regression_target_data,
    test_size=test_size,
    random_state=seed,
)

regression_input_data_for_train = classification_input_data_for_train.copy()
regression_input_data_for_test = classification_input_data_for_test.copy()


# =============================================================================
# Preprocessing
# =============================================================================


def _build_one_hot_preprocessor() -> ColumnTransformer:
    """Build the shared preprocessing transformer."""

    return ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=False,
                ),
                list(categorical_features),
            ),
            (
                "numerical",
                "passthrough",
                list(numerical_features),
            ),
        ],
        verbose_feature_names_out=False,
    )


# =============================================================================
# Generic classification pipeline
# =============================================================================


def _build_classification_pipeline(
    classifier: ClassificationEstimator,
    random_state: int,
    use_smote: bool,
) -> ClassificationPipeline:
    """Build a classification pipeline with optional SMOTENC."""

    preprocessor = _build_one_hot_preprocessor()

    if use_smote:
        smote = SMOTENC(
            categorical_features=list(categorical_features),
            random_state=random_state,
        )

        return ImbPipeline(
            steps=[
                ("smote", smote),
                ("preprocessor", preprocessor),
                ("classifier", classifier),
            ]
        )

    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", classifier),
        ]
    )


# =============================================================================
# Decision Tree
# =============================================================================


def _build_decision_tree_pipeline(
    random_state: int,
    use_smote: bool,
) -> ClassificationPipeline:
    """Build a Decision Tree classification pipeline."""

    classifier = DecisionTreeClassifier(
        random_state=random_state,
    )

    return _build_classification_pipeline(
        classifier=classifier,
        random_state=random_state,
        use_smote=use_smote,
    )


# =============================================================================
# Random Forest
# =============================================================================


def _build_random_forest_pipeline(
    random_state: int,
    use_smote: bool,
) -> ClassificationPipeline:
    """Build a Random Forest classification pipeline."""

    classifier = RandomForestClassifier(
        random_state=random_state,
    )

    return _build_classification_pipeline(
        classifier=classifier,
        random_state=random_state,
        use_smote=use_smote,
    )


# =============================================================================
# Gradient Boosting Regression
# =============================================================================


def _build_gradient_boost_pipeline(
    random_state: int,
) -> Pipeline:
    """Build a Gradient Boosting regression pipeline."""

    preprocessor = _build_one_hot_preprocessor()

    regressor = GradientBoostingRegressor(
        random_state=random_state,
    )

    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("regressor", regressor),
        ]
    )
