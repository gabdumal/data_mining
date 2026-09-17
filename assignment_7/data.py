import pandas as pd
from IPython.display import display

from features import age_ranges, sexes

# Read data
df = pd.read_csv("data/patients.csv")


# Coerce categorical features
df["sex"] = pd.Categorical(
    df.sex,
    categories=sexes,
    ordered=False,
)


# Transform age into ranges
df["age_range"] = pd.cut(
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
    labels=age_ranges,
    right=False,
    include_lowest=True,
)
df["age_range"] = pd.Categorical(
    df["age_range"],
    categories=age_ranges,
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
