from sklearn.model_selection import (
    GridSearchCV,
    StratifiedKFold,
)

from pipelines import (
    _build_decision_tree_pipeline,
    _build_random_forest_pipeline,
    seed,
)

# ---------------------------------------------------------------------------
# Decision Tree
# ---------------------------------------------------------------------------

decision_tree_pipeline = _build_decision_tree_pipeline(
    random_state=seed,
    use_smote=True,
)


def _build_grid_search_for_decision_tree(random_state, param_grid, use_smote: bool):
    """Build a GridSearchCV for the SMOTENC + Decision Tree pipeline."""

    pipeline = _build_decision_tree_pipeline(
        random_state=random_state,
        use_smote=use_smote,
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
    input_data, target_data, seeds, param_grid, use_smote: bool
):
    """Run Decision Tree GridSearchCV for multiple CV seeds."""

    grid_searches = {}

    for current_seed in seeds:
        grid_search = _build_grid_search_for_decision_tree(
            random_state=current_seed, param_grid=param_grid, use_smote=use_smote
        )

        grid_search.fit(
            input_data,
            target_data,
        )

        grid_searches[current_seed] = grid_search

    return grid_searches


# ---------------------------------------------------------------------------
# Random Forest
# ---------------------------------------------------------------------------
def _build_grid_search_for_random_forest(
    random_state: int,
    param_grid,
    use_smote: bool,
):
    """Build a GridSearchCV for the SMOTENC + Random Forest pipeline."""

    pipeline = _build_random_forest_pipeline(
        random_state=random_state,
        use_smote=use_smote,
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


def run_grid_searches_for_random_forest(
    input_data,
    target_data,
    seeds,
    param_grid,
    use_smote: bool,
):
    """Run Random Forest GridSearchCV for multiple CV seeds."""

    grid_searches = {}

    for current_seed in seeds:
        grid_search = _build_grid_search_for_random_forest(
            random_state=current_seed,
            param_grid=param_grid,
            use_smote=use_smote,
        )

        grid_search.fit(
            input_data,
            target_data,
        )

        grid_searches[current_seed] = grid_search

    return grid_searches
