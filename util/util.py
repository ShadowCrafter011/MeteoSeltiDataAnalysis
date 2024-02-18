import pandas as pd


def get_dataframe() -> pd.DataFrame:
    df = pd.read_csv("data/measurements.csv")
    df["measured_at"] = pd.to_datetime(df["measured_at"])
    df = df.set_index("measured_at")
    return df.sort_index()
