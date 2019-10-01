import pandas as pd

LOGGER = None

def null_step(df:pd.DataFrame) -> pd.DataFrame:
    return df

def add_empty_column(column_name):
    def _add_empty_column(df:pd.DataFrame) -> pd.DataFrame:
        df[column_name] = ''
        return df
    return _add_empty_column