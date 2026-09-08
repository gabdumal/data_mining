import pandas as pd

from columns import columns_labels, descriptions_of_columns

# Read data
df = pd.read_csv("data/trabalho4_dados_1.csv")
df = df.astype(bool)

# Rename features
if len(df.columns) != len(descriptions_of_columns):
    raise ValueError(
        f"Expected {len(descriptions_of_columns)} columns, but CSV contains {len(df.columns)}"
    )
df.columns = columns_labels()
descriptions_of_columns = dict(descriptions_of_columns)
