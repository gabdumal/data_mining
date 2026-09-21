from imblearn.over_sampling import SMOTENC
from imblearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import (
    train_test_split,
)
from sklearn.preprocessing import FunctionTransformer
from sklearn.tree import DecisionTreeClassifier

from data import (
    df3,
    df3_categorical_features,
    df3_input_features,
    df3_numerical_features,
    df3_target_feature,
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

categorical_features = df3_categorical_features
numerical_features = df3_numerical_features
input_features = df3_input_features
target_feature = df3_target_feature

input_data = df3[input_features].copy()
target_data = df3[target_feature].copy()


def encode_categorical_features(data_frame):
    """Encode categorical features as integer category codes."""
    encoded_data = data_frame.copy()

    for feature in categorical_features:
        encoded_data[feature] = encoded_data[feature].cat.codes

    return encoded_data


categorical_feature_indices = [
    input_features.index(feature) for feature in categorical_features
]


# ---------------------------------------------------------------------------
# Data split
# ---------------------------------------------------------------------------

test_size = 0.2

(
    input_data_for_train,
    input_data_for_test,
    target_data_for_train,
    target_data_for_test,
) = train_test_split(
    input_data,
    target_data,
    test_size=test_size,
    random_state=seed,
    stratify=target_data,
)


# ---------------------------------------------------------------------------
# Decision Tree
# ---------------------------------------------------------------------------


def _build_decision_tree_pipeline(
    random_state,
    use_smote,
):
    """Build a Decision Tree pipeline."""

    encoder = (
        "encoder",
        FunctionTransformer(
            encode_categorical_features,
            validate=False,
        ),
    )

    classifier = (
        "classifier",
        DecisionTreeClassifier(
            random_state=random_state,
        ),
    )

    if use_smote:
        smote = (
            "smote",
            SMOTENC(
                random_state=random_state,
                categorical_features=categorical_feature_indices,
            ),
        )

        return Pipeline(
            [
                encoder,
                smote,
                classifier,
            ]
        )

    return Pipeline(
        [
            encoder,
            classifier,
        ]
    )


# ---------------------------------------------------------------------------
# Random Forest
# ---------------------------------------------------------------------------


def _build_random_forest_pipeline(
    random_state: int,
    use_smote: bool,
):
    """Build a SMOTENC + Random Forest pipeline."""

    encoder = (
        "encoder",
        FunctionTransformer(
            encode_categorical_features,
            validate=False,
        ),
    )

    classifier = (
        "classifier",
        RandomForestClassifier(
            random_state=random_state,
            n_jobs=-1,
        ),
    )

    if use_smote:
        smote = (
            "smote",
            SMOTENC(
                random_state=random_state,
                categorical_features=categorical_feature_indices,
            ),
        )

        return Pipeline(
            [
                encoder,
                smote,
                classifier,
            ]
        )

    return Pipeline(
        [
            encoder,
            classifier,
        ]
    )
