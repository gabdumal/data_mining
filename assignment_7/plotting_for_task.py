import pandas as pd
from IPython.display import display


def _build_target_distribution_table(
    train_target,
    test_target,
):
    """Build the train/test target distribution table."""
    train_counts = train_target.value_counts().sort_index()
    test_counts = test_target.value_counts().sort_index()

    distribution = pd.DataFrame(
        {
            "Train N": train_counts,
            "Test N": test_counts,
        }
    ).fillna(0)

    distribution["Total N"] = distribution["Train N"] + distribution["Test N"]

    distribution["Train %"] = distribution["Train N"] / distribution["Total N"] * 100

    distribution["Test %"] = distribution["Test N"] / distribution["Total N"] * 100

    general = pd.DataFrame(
        {
            "Age Group": ["General"],
            "Train N": [train_target.size],
            "Test N": [test_target.size],
            "Total N": [train_target.size + test_target.size],
            "Train %": [
                train_target.size / (train_target.size + test_target.size) * 100
            ],
            "Test %": [test_target.size / (train_target.size + test_target.size) * 100],
        }
    )

    distribution = distribution.reset_index(names="Age Group")

    return pd.concat(
        [distribution, general],
        ignore_index=True,
    )


def _display_target_distribution(
    distribution,
    title="Target Distribution Across Train and Test Sets",
):
    """Display the train/test target distribution."""
    table = distribution.copy()

    for column in ["Train %", "Test %"]:
        table[column] = table[column].map(lambda value: f"{value:.1f}%")

    display(table.style.hide(axis="index").set_caption(title))


def display_train_test_target_distribution(
    train_target,
    test_target,
):
    """Display the target distribution in train and test sets."""
    distribution = _build_target_distribution_table(
        train_target,
        test_target,
    )

    _display_target_distribution(distribution)

    return distribution


def _highlight_better_within_group(
    data_frame,
    group_column,
    metric_columns,
    higher_is_better=True,
):
    """Highlight the better metric value within each group."""

    styles = pd.DataFrame(
        "",
        index=data_frame.index,
        columns=data_frame.columns,
    )

    for _, group in data_frame.groupby(
        group_column,
        sort=False,
        observed=True,
    ):
        for metric in metric_columns:
            if higher_is_better:
                best_value = group[metric].max()
            else:
                best_value = group[metric].min()

            best_rows = group[metric].eq(best_value)

            styles.loc[
                group.index[best_rows],
                metric,
            ] = "font-weight: bold"

    return styles


def display_cross_validation_results(
    results,
    metric_columns,
    caption,
    group_column="Seed",
):
    """Display cross-validation results with better values highlighted."""

    styled_results = (
        results.style.hide(axis="index")
        .format({metric: "{:.3f}" for metric in metric_columns})
        .set_caption(caption)
        .apply(
            _highlight_better_within_group,
            axis=None,
            group_column=group_column,
            metric_columns=metric_columns,
            higher_is_better=True,
        )
    )

    display(styled_results)


def display_cross_validation_summary(
    comparison,
    metric_columns,
    caption,
):
    """Display mean ± standard deviation cross-validation results."""

    display_columns = [
        "Strategy",
        *metric_columns,
    ]

    styled_comparison = (
        comparison[display_columns].style.hide(axis="index").set_caption(caption)
    )

    for metric in metric_columns:
        mean_column = f"{metric} mean"

        maximum = comparison[mean_column].max()

        maximum_strategy = comparison.loc[
            comparison[mean_column].eq(maximum),
            "Strategy",
        ].iloc[0]

        def highlight_strategy(
            row,
            strategy=maximum_strategy,
            metric_name=metric,
        ):
            """Highlight the better strategy for a metric."""

            styles = [""] * len(row)

            if row["Strategy"] == strategy:
                column_index = row.index.get_loc(metric_name)
                styles[column_index] = "font-weight: bold"

            return styles

        styled_comparison = styled_comparison.apply(
            highlight_strategy,
            axis=1,
        )

    display(styled_comparison)
