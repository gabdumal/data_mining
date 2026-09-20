from imblearn.pipeline import Pipeline

from pipelines import (
    _build_decision_tree_pipeline,
    input_data_for_test,
    input_data_for_train,
    seed,
    target_data_for_train,
)
from tuning import best_parameters_for_decision_tree

# ---------------------------------------------------------------------------
# Decision tree
# ---------------------------------------------------------------------------


def build_best_decision_tree_model(
    best_parameters: dict[str, object],
    random_state: int,
) -> Pipeline:
    """Build the final Decision Tree pipeline."""

    model = _build_decision_tree_pipeline(
        random_state=random_state,
        use_smote=True,
    )

    model.set_params(**best_parameters)

    return model


decision_tree_best_model = build_best_decision_tree_model(
    best_parameters=best_parameters_for_decision_tree,
    random_state=seed,
)


decision_tree_best_model.fit(
    input_data_for_train,
    target_data_for_train,
)


decision_tree_predictions = decision_tree_best_model.predict(input_data_for_test)
