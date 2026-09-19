import pandas as pd
from IPython.display import display

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


# Display statistics
display("Data types:")
display(df.dtypes)

display("Missing values:")
display(df.isna().sum())

display(f"Duplicated rows: {df.duplicated().sum()}")


# # Treat outliers
# def treat_outliers_through_iqr(
#     data_frame: pd.DataFrame,
#     column_label: str,
# ):
#     first_quartile = data_frame[column_label].quantile(0.25)
#     third_quartile = data_frame[column_label].quantile(0.75)
#     iqr = third_quartile - first_quartile
#     lower = first_quartile - 1.5 * iqr
#     upper = third_quartile + 1.5 * iqr
#     data_frame[column_label] = data_frame[column_label].clip(
#         lower=lower,
#         upper=upper,
#     )
#     return data_frame


# for column_label in [
#     "age",
#     "systolic_bp",
#     "diastolic_bp",
#     "blood_sugar",
#     "heart_rate",
# ]:
#     a_df = treat_outliers_through_iqr(
#         data_frame=a_df,
#         column_label=column_label,
#     )
