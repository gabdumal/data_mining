from imblearn.over_sampling import SMOTENC
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor, RandomForestClassifier
from sklearn.model_selection import (
    train_test_split,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.tree import DecisionTreeClassifier

from data import (
    categorical_features,
    classification_target_feature,
    input_features,
    numerical_features,
    regression_target_feature,
    t_df,
)

# ---------------------------------------------------------------------------
# Definitions
# ---------------------------------------------------------------------------

seeds = [
    27,
    32,
    59,
    74,
    93,
]
seed = seeds[0]


input_data = t_df[input_features].copy()
classification_target_data = t_df[classification_target_feature].copy()
regression_target_data = t_df[regression_target_feature].copy()


# ---------------------------------------------------------------------------
# Data split
# ---------------------------------------------------------------------------

test_size = 0.2

(
    classification_input_data_for_train,
    classification_input_data_for_test,
    classification_target_data_for_train,
    classification_target_data_for_test,
) = train_test_split(
    input_data,
    classification_target_data,
    test_size=test_size,
    random_state=seed,
    stratify=classification_target_data,
)

(
    regression_input_data_for_train,
    regression_input_data_for_test,
    regression_target_data_for_train,
    regression_target_data_for_test,
) = train_test_split(
    input_data,
    regression_target_data,
    test_size=test_size,
    random_state=seed,
    stratify=classification_target_data,
)


# ---------------------------------------------------------------------------
# Decision Tree
# ---------------------------------------------------------------------------


def _build_decision_tree_pipeline(
    random_state,
    use_smote,
):
    """Build a Decision Tree pipeline."""

    classifier = DecisionTreeClassifier(random_state=random_state)

    if use_smote:
        smote_encoder = ColumnTransformer(
            transformers=[
                ("categorical", OrdinalEncoder(), categorical_features),
                ("numerical", "passthrough", numerical_features),
            ]
        )

        final_encoder = ColumnTransformer(
            transformers=[
                (
                    "categorical",
                    OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                    [0, 1],
                ),
                ("numerical", "passthrough", list(range(2, len(input_features)))),
            ]
        )

        smote = SMOTENC(categorical_features=[0, 1], random_state=random_state)

        return ImbPipeline(
            [
                ("smote_encoder", smote_encoder),
                ("smote", smote),
                ("onehot", final_encoder),
                ("classifier", classifier),
            ]
        )

    else:
        normal_encoder = ColumnTransformer(
            transformers=[
                (
                    "categorical",
                    OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                    categorical_features,
                ),
                ("numerical", "passthrough", numerical_features),
            ]
        )

        return Pipeline([("encoder", normal_encoder), ("classifier", classifier)])


# ---------------------------------------------------------------------------
# Random Forest
# ---------------------------------------------------------------------------


def _build_random_forest_pipeline(
    random_state: int,
    use_smote: bool,
):
    """Build a SMOTENC + Random Forest pipeline."""

    classifier = RandomForestClassifier(random_state=random_state)

    if use_smote:
        smote_encoder = ColumnTransformer(
            transformers=[
                ("categorical", OrdinalEncoder(), categorical_features),
                ("numerical", "passthrough", numerical_features),
            ]
        )

        final_encoder = ColumnTransformer(
            transformers=[
                (
                    "categorical",
                    OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                    [0, 1],
                ),
                ("numerical", "passthrough", list(range(2, len(input_features)))),
            ]
        )

        smote = SMOTENC(categorical_features=[0, 1], random_state=random_state)

        return ImbPipeline(
            [
                ("smote_encoder", smote_encoder),
                ("smote", smote),
                ("onehot", final_encoder),
                ("classifier", classifier),
            ]
        )

    else:
        normal_encoder = ColumnTransformer(
            transformers=[
                (
                    "categorical",
                    OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                    categorical_features,
                ),
                ("numerical", "passthrough", numerical_features),
            ]
        )

        return Pipeline([("encoder", normal_encoder), ("classifier", classifier)])


# ---------------------------------------------------------------------------
# Gradient Boost
# ---------------------------------------------------------------------------


def _build_gradient_boost_pipeline(
    random_state: int,
):
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                categorical_features,
            ),
            ("numerical", "passthrough", numerical_features),
        ]
    )

    regressor = GradientBoostingRegressor(random_state=random_state)

    return Pipeline([("preprocessor", preprocessor), ("regressor", regressor)])
