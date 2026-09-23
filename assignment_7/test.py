from helper_for_test import (
    run_classification_model_test_evaluation,
    run_regression_model_test_evaluation,
)
from pipelines import (
    _build_decision_tree_pipeline,
    _build_gradient_boost_pipeline,
    _build_random_forest_pipeline,
    classification_input_data_for_test,
    classification_input_data_for_train,
    classification_target_data_for_test,
    classification_target_data_for_train,
    regression_input_data_for_test,
    regression_input_data_for_train,
    regression_target_data_for_test,
    regression_target_data_for_train,
    seeds,
)
from validation_import import (
    best_parameters_for_decision_tree_with_smote,
    best_parameters_for_decision_tree_without_smote,
    best_parameters_for_gradient_boost,
    best_parameters_for_random_forest_with_smote,
    best_parameters_for_random_forest_without_smote,
)

# ---------------------------------------------------------------------------
# Decision Tree
# ---------------------------------------------------------------------------

decision_tree_without_smote_test_results = run_classification_model_test_evaluation(
    model_name="Decision Tree without SMOTE",
    model_factory=lambda random_state: _build_decision_tree_pipeline(
        random_state=random_state,
        use_smote=False,
    ),
    best_parameters=best_parameters_for_decision_tree_without_smote,
    input_data_for_train=classification_input_data_for_train,
    target_data_for_train=classification_target_data_for_train,
    input_data_for_test=classification_input_data_for_test,
    target_data_for_test=classification_target_data_for_test,
    seeds=seeds,
)

decision_tree_with_smote_test_results = run_classification_model_test_evaluation(
    model_name="Decision Tree with SMOTE",
    model_factory=lambda random_state: _build_decision_tree_pipeline(
        random_state=random_state,
        use_smote=True,
    ),
    best_parameters=best_parameters_for_decision_tree_with_smote,
    input_data_for_train=classification_input_data_for_train,
    target_data_for_train=classification_target_data_for_train,
    input_data_for_test=classification_input_data_for_test,
    target_data_for_test=classification_target_data_for_test,
    seeds=seeds,
)


# ---------------------------------------------------------------------------
# Random Forest
# ---------------------------------------------------------------------------

random_forest_without_smote_test_results = run_classification_model_test_evaluation(
    model_name="Random Forest without SMOTE",
    model_factory=lambda random_state: _build_random_forest_pipeline(
        random_state=random_state,
        use_smote=False,
    ),
    best_parameters=best_parameters_for_random_forest_without_smote,
    input_data_for_train=classification_input_data_for_train,
    target_data_for_train=classification_target_data_for_train,
    input_data_for_test=classification_input_data_for_test,
    target_data_for_test=classification_target_data_for_test,
    seeds=seeds,
)

random_forest_with_smote_test_results = run_classification_model_test_evaluation(
    model_name="Random Forest with SMOTE",
    model_factory=lambda random_state: _build_random_forest_pipeline(
        random_state=random_state,
        use_smote=True,
    ),
    best_parameters=best_parameters_for_random_forest_with_smote,
    input_data_for_train=classification_input_data_for_train,
    target_data_for_train=classification_target_data_for_train,
    input_data_for_test=classification_input_data_for_test,
    target_data_for_test=classification_target_data_for_test,
    seeds=seeds,
)


# ---------------------------------------------------------------------------
# Gradient Boost
# ---------------------------------------------------------------------------

gradient_boost_test_results = run_regression_model_test_evaluation(
    model_name="Gradient Boost",
    model_factory=lambda random_state: _build_gradient_boost_pipeline(
        random_state=random_state,
    ),
    best_parameters=best_parameters_for_gradient_boost,
    input_data_for_train=regression_input_data_for_train,
    target_data_for_train=regression_target_data_for_train,
    input_data_for_test=regression_input_data_for_test,
    target_data_for_test=regression_target_data_for_test,
    seeds=seeds,
)


# ---------------------------------------------------------------------------
# Comparison
# ---------------------------------------------------------------------------

classification_model_results = {
    "Decision Tree without SMOTE": decision_tree_without_smote_test_results,
    "Decision Tree with SMOTE": decision_tree_with_smote_test_results,
    "Random Forest without SMOTE": random_forest_without_smote_test_results,
    "Random Forest with SMOTE": random_forest_with_smote_test_results,
}
regression_model_results = {
    "Gradient Boost": gradient_boost_test_results,
}
model_results = {**classification_model_results, **regression_model_results}
