import pandas as pd
from IPython.display import display

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
df.risk_level = df.risk_level.replace(levels_of_risk_renaming)
df.risk_level = pd.Categorical(
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

# Remove duplicates
dd_df = df.drop_duplicates()
