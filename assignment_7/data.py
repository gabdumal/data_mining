import pandas as pd

from features import (
    age_groups,
    format_mouth_condition,
    format_sex,
    mouth_conditions,
    sexes,
)

# Read data
df = pd.read_csv("data/patients.csv")


# Coerce categorical features
df["sex"] = pd.Categorical(
    df["sex"].map(format_sex),
    categories=[format_sex(sex) for sex in sexes],
    ordered=False,
)
df["mouth_condition"] = pd.Categorical(
    df["mouth_condition"].map(format_mouth_condition),
    categories=[format_mouth_condition(condition) for condition in mouth_conditions],
    ordered=False,
)

# Transform age into ranges
df["age_group"] = pd.cut(
    df["age"],
    bins=[
        10,
        20,
        30,
        40,
        50,
        60,
        70,
        float("inf"),
    ],
    labels=age_groups,
    right=False,
    include_lowest=True,
)
df["age_group"] = pd.Categorical(
    df["age_group"],
    categories=age_groups,
    ordered=True,
)


# Remove features that do not have relevant amount of values different from 0
df2_features = [
    "age",
    "age_group",
    "sex",
    "mouth_condition",
    "amount_of_im",
    "amount_of_p",
    "amount_of_h",
    "amount_of_rr",
    "amount_of_m3i",
    "amount_of_m3f",
    "amount_of_te",
    "amount_of_dc",
    "amount_of_di",
    "amount_of_c",
    "amount_of_r",
    "amount_of_cpum",
]
df2 = df[df2_features].copy()


# Remove features that do not have significative differences between age groups
classification_target_feature = "age_group"
regression_target_feature = "age"

categorical_features = [
    "mouth_condition",
]
numerical_features = [
    "amount_of_im",
    "amount_of_p",
    "amount_of_h",
    "amount_of_m3i",
    "amount_of_m3f",
    "amount_of_te",
    "amount_of_di",
    "amount_of_c",
    "amount_of_r",
    "amount_of_cpum",
]
input_features = categorical_features + numerical_features

t_df = df2[
    input_features + [classification_target_feature] + [regression_target_feature]
].copy()

classification_features = input_features + [classification_target_feature]
regression_features = input_features + [regression_target_feature]
