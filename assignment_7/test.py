from helper_for_test import (
    prepare_per_age_group_summary,
    prepare_per_age_group_test_metrics,
    prepare_seed_test_results,
    prepare_test_summary,
    run_model_test_evaluation,
)
from pipelines import (
    _build_decision_tree_pipeline,
    input_data_for_test,
    input_data_for_train,
    seeds,
    target_data_for_test,
    target_data_for_train,
)
from tuning import (
    best_parameters_for_decision_tree_with_smote,
    best_parameters_for_decision_tree_without_smote,
)

# ---------------------------------------------------------------------------
# Decision tree
# ---------------------------------------------------------------------------

decision_tree_without_smote_test_results = run_model_test_evaluation(
    model_name="Decision Tree without SMOTE",
    model_factory=lambda random_state: _build_decision_tree_pipeline(
        random_state=random_state,
        use_smote=False,
    ),
    best_parameters=best_parameters_for_decision_tree_without_smote,
    input_data_for_train=input_data_for_train,
    target_data_for_train=target_data_for_train,
    input_data_for_test=input_data_for_test,
    target_data_for_test=target_data_for_test,
    seeds=seeds,
)

decision_tree_with_smote_test_results = run_model_test_evaluation(
    model_name="Decision Tree with SMOTE",
    model_factory=lambda random_state: _build_decision_tree_pipeline(
        random_state=random_state,
        use_smote=True,
    ),
    best_parameters=best_parameters_for_decision_tree_with_smote,
    input_data_for_train=input_data_for_train,
    target_data_for_train=target_data_for_train,
    input_data_for_test=input_data_for_test,
    target_data_for_test=target_data_for_test,
    seeds=seeds,
)


# ---------------------------------------------------------------------------
# Random forest
# ---------------------------------------------------------------------------

# random_forest_test_results = run_model_test_evaluation(
#     model_name="Random Forest",
#     model_factory=lambda random_state: _build_random_forest_pipeline(
#         random_state=random_state,
#         use_smote=True,
#     ),
#     best_parameters=best_random_forest_parameters,
#     input_data_for_train=input_data_for_train,
#     target_data_for_train=output_data_for_train,
#     input_data_for_test=input_data_for_test,
#     target_data_for_test=output_data_for_test,
#     seeds=[1, 2, 3, 4, 5],
# )


# ---------------------------------------------------------------------------
# Comparison
# ---------------------------------------------------------------------------

model_results = {
    "Decision Tree without SMOTE": decision_tree_without_smote_test_results,
    "Decision Tree with SMOTE": decision_tree_with_smote_test_results,
    # "Random Forest": random_forest_test_results,
}

seed_test_results = prepare_seed_test_results(
    model_results,
)

test_summary = prepare_test_summary(seed_test_results)

per_age_group_results = prepare_per_age_group_test_metrics(
    model_results,
    target_data_for_test,
)

per_age_group_summary = prepare_per_age_group_summary(
    per_age_group_results,
)

# # Model-agreement analysis.

# agreement = prepare_model_agreement(
#     decision_tree_test_results,
#     random_forest_test_results,
#     target_data_for_test,
# )

# display_model_agreement(agreement)
