import pandas as pd
from sklearn.preprocessing import StandardScaler

from categorical import (
    nursery_modes,
    types_of_agriblock,
    types_of_soil,
    varieties,
    wind_directions,
)
from columns import (
    names_of_columns,
    numeric_columns,
)

# Read data
df = pd.read_csv("data/trabalho3_dados_1.csv")


# Rename features
if len(df.columns) != len(names_of_columns):
    raise ValueError(
        f"Expected {len(names_of_columns)} columns, but CSV contains {len(df.columns)}"
    )
df.columns = [code for code, _ in names_of_columns]
names_of_columns = dict(names_of_columns)


# Coerce categorical features
df.agriblock = pd.Categorical(
    df.agriblock,
    categories=types_of_agriblock,
    ordered=False,
)
df.variety = pd.Categorical(
    df.variety,
    categories=varieties,
    ordered=False,
)
df.soil_type = pd.Categorical(
    df.soil_type,
    categories=types_of_soil,
    ordered=False,
)
df.nursery = pd.Categorical(
    df.nursery,
    categories=nursery_modes,
    ordered=False,
)
df.wind_direction_d1_d30 = pd.Categorical(
    df.wind_direction_d1_d30,
    categories=wind_directions,
    ordered=False,
)
df.wind_direction_d31_d60 = pd.Categorical(
    df.wind_direction_d31_d60,
    categories=wind_directions,
    ordered=False,
)
df.wind_direction_d61_d90 = pd.Categorical(
    df.wind_direction_d61_d90,
    categories=wind_directions,
    ordered=False,
)
df.wind_direction_d91_d120 = pd.Categorical(
    df.wind_direction_d91_d120,
    categories=wind_directions,
    ordered=False,
)


# Scale features
scaler = StandardScaler()

scaled_df = df.copy()
scaled_df[numeric_columns] = scaler.fit_transform(df[numeric_columns])
