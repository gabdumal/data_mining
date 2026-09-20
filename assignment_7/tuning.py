from sklearn.model_selection import (
    GridSearchCV,
    StratifiedKFold,
)

from helper_for_task import get_best_grid_search_parameters
from pipelines import (
    _build_decision_tree_pipeline,
    input_data_for_train,
    seed,
    seeds,
    target_data_for_train,
)

# ---------------------------------------------------------------------------
# Decision tree
# ---------------------------------------------------------------------------

decision_tree_pipeline = _build_decision_tree_pipeline(
    random_state=seed,
    use_smote=True,
)


def _build_grid_search_for_decision_tree(
    random_state,
    param_grid,
):
    """Build a GridSearchCV for the SMOTENC + Decision Tree pipeline."""

    pipeline = _build_decision_tree_pipeline(
        random_state=random_state,
        use_smote=True,
    )

    stratified_cross_validation = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=random_state,
    )

    scoring = {
        "f1_macro": "f1_macro",
        "balanced_accuracy": "balanced_accuracy",
        "accuracy": "accuracy",
    }

    return GridSearchCV(
        estimator=pipeline,
        param_grid=param_grid,
        scoring=scoring,
        refit="f1_macro",
        cv=stratified_cross_validation,
        n_jobs=-1,
        return_train_score=False,
        error_score="raise",
    )


def run_grid_searches_for_decision_tree(
    input_data,
    target_data,
    seeds,
    param_grid,
):
    """Run Decision Tree GridSearchCV for multiple CV seeds."""

    grid_searches = {}

    for current_seed in seeds:
        grid_search = _build_grid_search_for_decision_tree(
            random_state=current_seed,
            param_grid=param_grid,
        )

        grid_search.fit(
            input_data,
            target_data,
        )

        grid_searches[current_seed] = grid_search

    return grid_searches


param_grid_of_decision_tree = {
    "classifier__criterion": ["gini", "entropy"],
    "classifier__max_depth": [3, 5, 7, 10, None],
    "classifier__min_samples_split": [2, 5, 10],
    "classifier__min_samples_leaf": [1, 2, 5],
}

grid_searches_for_decision_tree = run_grid_searches_for_decision_tree(
    input_data_for_train,
    target_data_for_train,
    seeds=seeds,
    param_grid=param_grid_of_decision_tree,
)

best_parameters_for_decision_tree = get_best_grid_search_parameters(
    grid_searches_for_decision_tree
)
