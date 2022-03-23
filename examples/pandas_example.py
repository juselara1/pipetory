import pandas as pd
import datetime as dt
from pipetory import factory
import logging

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
if __name__ == "__main__":
    logging.basicConfig()
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    preprocess_pipe = (
            factory("sequential", "df1", log)
            .register(assign_types, "types")
            .register(transform_dates, "dates")
            .register(transform_names, "names")
            .compile()
            )

    print(preprocess_pipe(df))
