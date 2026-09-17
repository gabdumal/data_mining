from typing import get_args

import pandas as pd
from IPython.display import display

from features import Sex, columns_labels, descriptions_of_columns

# Read data
df = pd.read_csv("data/patients.csv")


# Rename features
if len(df.columns) != len(descriptions_of_columns):
    raise ValueError(
        f"Expected {len(descriptions_of_columns)} columns, but CSV contains {len(df.columns)}"
    )
df.columns = columns_labels()
descriptions_of_columns = dict(descriptions_of_columns)


# Coerce categorical features
df["sex"] = pd.Categorical(
    df.sex,
    categories=get_args(Sex),
    ordered=False,
)

display("Data types:")
display(df.dtypes)

display("\nMissing values:")
display(df.isna().sum())

display("\nDuplicated rows:")
display(df.duplicated().sum())

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
