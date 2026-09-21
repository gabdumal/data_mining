from helper_for_test import (
    prepare_model_agreement,
    prepare_per_age_group_summary,
    prepare_per_age_group_test_metrics,
    prepare_seed_test_results,
    prepare_test_summary,
    run_model_test_evaluation,
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

# ---------------------------------------------------------------------------
# Decision Tree
# ---------------------------------------------------------------------------

best_parameters_for_decision_tree_without_smote = {
    "classifier__criterion": "entropy",
    "classifier__max_depth": None,
    "classifier__min_samples_leaf": 1,
    "classifier__min_samples_split": 10,
}
decision_tree_without_smote_test_results = run_model_test_evaluation(
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

best_parameters_for_decision_tree_with_smote = {
    "classifier__criterion": "gini",
    "classifier__max_depth": 7,
    "classifier__min_samples_leaf": 2,
    "classifier__min_samples_split": 10,
}

decision_tree_with_smote_test_results = run_model_test_evaluation(
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

best_parameters_for_random_forest_without_smote = {
    "classifier__criterion": "entropy",
    "classifier__max_depth": 10,
    "classifier__max_features": "log2",
    "classifier__min_samples_leaf": 1,
    "classifier__min_samples_split": 5,
    "classifier__n_estimators": 300,
}
random_forest_without_smote_test_results = run_model_test_evaluation(
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

best_parameters_for_random_forest_with_smote = {
    "classifier__criterion": "entropy",
    "classifier__max_depth": None,
    "classifier__max_features": "log2",
    "classifier__min_samples_leaf": 2,
    "classifier__min_samples_split": 2,
    "classifier__n_estimators": 200,
}
random_forest_with_smote_test_results = run_model_test_evaluation(
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

best_parameters_for_gradient_boost = {
    "classifier__criterion": "entropy",
    "classifier__max_depth": 10,
    "classifier__max_features": "log2",
    "classifier__min_samples_leaf": 1,
    "classifier__min_samples_split": 5,
    "classifier__n_estimators": 300,
}
gradient_boost_test_results = run_model_test_evaluation(
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

model_results = {
    "Decision Tree without SMOTE": decision_tree_without_smote_test_results,
    "Decision Tree with SMOTE": decision_tree_with_smote_test_results,
    "Random Forest without SMOTE": random_forest_without_smote_test_results,
    "Random Forest with SMOTE": random_forest_with_smote_test_results,
    "Gradient Boost": gradient_boost_test_results,
}

seed_test_results = prepare_seed_test_results(
    model_results,
)

test_summary = prepare_test_summary(seed_test_results)

per_age_group_results = prepare_per_age_group_test_metrics(
    model_results,
    classification_target_data_for_test,
)

per_age_group_summary = prepare_per_age_group_summary(
    per_age_group_results,
)

# # Model-agreement analysis.

agreement_between_models = prepare_model_agreement(
    decision_tree_with_smote_test_results,
    random_forest_with_smote_test_results,
    classification_target_data_for_test,
)
