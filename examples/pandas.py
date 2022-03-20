import pandas as pd
import datetime as dt
from pipetory import factory

# %%
# Create a dataframe with 4 columns: name, birth date, and height

df = pd.DataFrame(
    data=[
        ["John", "1980-01-01", "180", "male"],
        ["Jane", "1979-01-01", "170", "female"],
        ["Lucal", "1945-01-01", "180", "male"],
        ["Mary", "1990-01-01", "170", "female"],
    ],
    columns=["name", "birth_date", "height", "gender"],
)

# %%
def assign_types(df):
    tdf = (
            df
            .astype({"height": "int64"})
            )
    return tdf

def transform_dates(df):
    tdf = (
            df
            .assign(birth_date = pd.to_datetime(df.birth_date))
            .assign(age = lambda x: (dt.datetime.now() - x.birth_date).dt.days / 365)
            )
    return tdf

def transform_names(df):
    tdf = (
            df
            .assign(name_length = lambda df: df.name.apply(len))
            .assign(name_first_letter = lambda df: df.name.apply(lambda x: x[0]))
            )
    return tdf

# %%
preprocess_pipe = (
        factory("sequential", "df1")
        .register(assign_types, "types")
        .register(transform_dates, "dates")
        .register(transform_names, "names")
        .compile()
        )

# %%
preprocess_pipe(df)

# %%
preprocess_pipe(df, step="types")

# %%
preprocess_pipe(df, step="dates")

# %%
preprocess_pipe(df, step="names")
