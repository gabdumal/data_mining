from helper_for_validation import (
    CLASSIFICATION_GRID_SEARCH_METRICS,
    REGRESSION_GRID_SEARCH_METRICS,
    get_best_grid_search_parameters,
    load_grid_searches,
)

grid_searches_for_decision_tree_without_smote = load_grid_searches(
    "validation/grid_searches_for_decision_tree_without_smote.joblib",
)

best_parameters_for_decision_tree_without_smote = get_best_grid_search_parameters(
    grid_searches=grid_searches_for_decision_tree_without_smote,
    metrics=CLASSIFICATION_GRID_SEARCH_METRICS,
    selection_metric="F1 Macro",
)


grid_searches_for_decision_tree_with_smote = load_grid_searches(
    "validation/grid_searches_for_decision_tree_with_smote.joblib",
)

best_parameters_for_decision_tree_with_smote = get_best_grid_search_parameters(
    grid_searches=grid_searches_for_decision_tree_with_smote,
    metrics=CLASSIFICATION_GRID_SEARCH_METRICS,
    selection_metric="F1 Macro",
)


grid_searches_for_random_forest_without_smote = load_grid_searches(
    "validation/grid_searches_for_random_forest_without_smote.joblib",
)

best_parameters_for_random_forest_without_smote = get_best_grid_search_parameters(
    grid_searches=grid_searches_for_random_forest_without_smote,
    metrics=CLASSIFICATION_GRID_SEARCH_METRICS,
    selection_metric="F1 Macro",
)


grid_searches_for_random_forest_with_smote = load_grid_searches(
    "validation/grid_searches_for_random_forest_with_smote.joblib",
)

best_parameters_for_random_forest_with_smote = get_best_grid_search_parameters(
    grid_searches=grid_searches_for_random_forest_with_smote,
    metrics=CLASSIFICATION_GRID_SEARCH_METRICS,
    selection_metric="F1 Macro",
)


grid_searches_for_gradient_boost = load_grid_searches(
    "validation/grid_searches_for_gradient_boost.joblib",
)

best_parameters_for_gradient_boost = get_best_grid_search_parameters(
    grid_searches=grid_searches_for_gradient_boost,
    metrics=REGRESSION_GRID_SEARCH_METRICS,
    selection_metric="MAE",
)
