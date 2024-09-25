import pandas as pd


def main():
    measurement = pd.read_csv("data/measurements.csv", parse_dates=["datetime"])
    measurement = measurement[measurement["precipitation"].notnull()]
    measurement_max = measurement.sort_values(["precipitation"]).tail(5)
    for i in range(len(measurement_max)):
        val = measurement_max.iloc[i]
        print(f"Max 5 min precipitation of {round(val["precipitation"], 1)}mm {val["datetime"].strftime("%Y-%m-%d %H:%M")}")
    print()

    hourly = pd.read_csv("data/measurements.csv", index_col=0, parse_dates=["hour"], date_format="%Y%m%d%H").sort_index()
    hours = hourly["hour"].unique()
    merged_hourly = pd.DataFrame({
        "hour": hours,
        "precipitation": hourly.groupby(["hour"])["precipitation"].sum()
    })
    hourly_max = merged_hourly.sort_values(["precipitation"]).tail(5)
    for i in range(len(hourly_max)):
        val = hourly_max.iloc[i]
        print(f"Max hourly precipitation of {round(val["precipitation"], 1)}mm {val["hour"].strftime("%Y-%m-%d %H:00")}")
    print()

    daily = pd.read_csv("data/measurements.csv", index_col=0, parse_dates=["day"], date_format="%Y%m%d").sort_index()
    days = daily["day"].unique()
    merged_daily = pd.DataFrame({
        "hour": days,
        "precipitation": daily.groupby(["day"])["precipitation"].sum()
    })
    daily_max = merged_daily.sort_values(["precipitation"]).tail(5)
    for i in range(len(daily_max)):
        val = daily_max.iloc[i]
        print(f"Max daily precipitation of {round(val["precipitation"], 1)}mm {val["hour"].strftime("%Y-%m-%d")}")


if __name__ == "__main__":
    main()
