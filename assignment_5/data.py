import pandas as pd
from IPython.display import display
from sklearn.preprocessing import StandardScaler

from categorical import levels_of_risk, levels_of_risk_renaming
from columns import columns_labels, descriptions_of_columns

# Read data
df = pd.read_csv("data/maternal_health_risk_subbase_1.csv")


# Rename features
if len(df.columns) != len(descriptions_of_columns):
    raise ValueError(
        f"Expected {len(descriptions_of_columns)} columns, but CSV contains {len(df.columns)}"
    )
df.columns = columns_labels()
descriptions_of_columns = dict(descriptions_of_columns)


# Coerce categorical features
df["risk_level"] = df.risk_level.replace(levels_of_risk_renaming)
df["risk_level"] = pd.Categorical(
    df.risk_level,
    categories=levels_of_risk,
    ordered=False,
)

display("Data types:")
display(df.dtypes)

display("\nMissing values:")
display(df.isna().sum())

display("\nDuplicated rows:")
display(df.duplicated().sum())

a_df = df.copy()


# Remove duplicates
a_df = df.drop_duplicates()


# Treat outliers
def treat_outliers_through_iqr(
    data_frame: pd.DataFrame,
    column_label: str,
):
    first_quartile = data_frame[column_label].quantile(0.25)
    third_quartile = data_frame[column_label].quantile(0.75)
    iqr = third_quartile - first_quartile
    lower = first_quartile - 1.5 * iqr
    upper = third_quartile + 1.5 * iqr
    data_frame[column_label] = data_frame[column_label].clip(
        lower=lower,
        upper=upper,
    )
    return data_frame


for column_label in [
    "age",
    "systolic_bp",
    "diastolic_bp",
    "blood_sugar",
    "heart_rate",
]:
    a_df = treat_outliers_through_iqr(
        data_frame=a_df,
        column_label=column_label,
    )


# Normalize features
standard_scaler = StandardScaler()


numerical_columns = [
    "age",
    "systolic_bp",
    "diastolic_bp",
    "blood_sugar",
    "body_temperature",
    "heart_rate",
]

categorical_columns = ["risk_level"]


def normalize_features(
    data_frame: pd.DataFrame,
    numerical_columns: list[str],
):
    data_frame = data_frame.copy()
    data_frame[numerical_columns] = standard_scaler.fit_transform(
        data_frame[numerical_columns]
    )
    return data_frame
