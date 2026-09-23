from sklearn.model_selection import (
    GridSearchCV,
    KFold,
    StratifiedKFold,
)

from helper_for_validation import save_grid_searches
from pipelines import (
    _build_decision_tree_pipeline,
    _build_gradient_boost_pipeline,
    _build_random_forest_pipeline,
    classification_input_data_for_train,
    classification_target_data_for_train,
    regression_input_data_for_train,
    regression_target_data_for_train,
    seeds,
)

# ---------------------------------------------------------------------------
# Decision Tree
# ---------------------------------------------------------------------------


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


param_grid_of_decision_tree = {
    "classifier__criterion": ["gini", "entropy"],
    "classifier__max_depth": [7, 10, None],
    "classifier__min_samples_split": [2, 5, 10],
    "classifier__min_samples_leaf": [1, 2, 5],
}

grid_searches_for_decision_tree_without_smote = run_grid_searches_for_decision_tree(
    classification_input_data_for_train,
    classification_target_data_for_train,
    seeds=seeds,
    param_grid=param_grid_of_decision_tree,
    use_smote=False,
)

save_grid_searches(
    grid_searches_for_decision_tree_without_smote,
    "validation/grid_searches_for_decision_tree_without_smote.joblib",
)

grid_searches_for_decision_tree_with_smote = run_grid_searches_for_decision_tree(
    classification_input_data_for_train,
    classification_target_data_for_train,
    seeds=seeds,
    param_grid=param_grid_of_decision_tree,
    use_smote=True,
)

save_grid_searches(
    grid_searches_for_decision_tree_with_smote,
    "validation/grid_searches_for_decision_tree_with_smote.joblib",
)


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


param_grid_of_random_forest = {
    "classifier__n_estimators": [100, 200, 300],
    "classifier__criterion": ["gini", "entropy"],
    "classifier__max_depth": [3, 5, 7],
    "classifier__min_samples_split": [2, 5, 10],
    "classifier__min_samples_leaf": [1, 2, 3],
    "classifier__max_features": ["sqrt", "log2"],
}

grid_searches_for_random_forest_without_smote = run_grid_searches_for_random_forest(
    classification_input_data_for_train,
    classification_target_data_for_train,
    seeds=seeds,
    param_grid=param_grid_of_random_forest,
    use_smote=False,
)

save_grid_searches(
    grid_searches_for_random_forest_without_smote,
    "validation/grid_searches_for_random_forest_without_smote.joblib",
)

grid_searches_for_random_forest_with_smote = run_grid_searches_for_random_forest(
    classification_input_data_for_train,
    classification_target_data_for_train,
    seeds=seeds,
    param_grid=param_grid_of_random_forest,
    use_smote=True,
)

save_grid_searches(
    grid_searches_for_random_forest_with_smote,
    "validation/grid_searches_for_random_forest_with_smote.joblib",
)


# ---------------------------------------------------------------------------
# Gradient Boost
# ---------------------------------------------------------------------------


def _build_grid_search_for_gradient_boost(
    random_state: int,
    param_grid,
):
    """Build a GridSearchCV for the Gradient Boosting regression pipeline."""

    pipeline = _build_gradient_boost_pipeline(
        random_state=random_state,
    )

    cross_validation = KFold(
        n_splits=5,
        shuffle=True,
        random_state=random_state,
    )

    scoring = {
        "mae": "neg_mean_absolute_error",
        "rmse": "neg_root_mean_squared_error",
        "r2": "r2",
    }

    return GridSearchCV(
        estimator=pipeline,
        param_grid=param_grid,
        scoring=scoring,
        refit="mae",
        cv=cross_validation,
        n_jobs=-1,
        return_train_score=False,
        error_score="raise",
    )


def run_grid_searches_for_gradient_boost(
    input_data,
    target_data,
    seeds,
    param_grid,
):
    """Run Gradient Boosting GridSearchCV for multiple CV seeds."""

    grid_searches = {}

    for current_seed in seeds:
        grid_search = _build_grid_search_for_gradient_boost(
            random_state=current_seed,
            param_grid=param_grid,
        )

        grid_search.fit(
            input_data,
            target_data,
        )

        grid_searches[current_seed] = grid_search

    return grid_searches


param_grid_of_gradient_boost = {
    "regressor__n_estimators": [100, 200, 300],
    "regressor__learning_rate": [0.01, 0.05, 0.1],
    "regressor__max_depth": [2, 3, 5],
    "regressor__min_samples_leaf": [1, 3, 5, 10],
    "regressor__loss": [
        "squared_error",
        "huber",
        "absolute_error",
    ],
}

grid_searches_for_gradient_boost = run_grid_searches_for_gradient_boost(
    regression_input_data_for_train,
    regression_target_data_for_train,
    seeds=seeds,
    param_grid=param_grid_of_gradient_boost,
)

save_grid_searches(
    grid_searches_for_gradient_boost,
    "validation/grid_searches_for_gradient_boost.joblib",
)
