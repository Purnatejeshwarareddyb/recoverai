"""Loads raw payment event data from disk into a pandas DataFrame."""

import pandas as pd
from config import settings


def load_raw_payments(path: str = settings.RAW_DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["event_timestamp"] = pd.to_datetime(df["event_timestamp"])
    return df
