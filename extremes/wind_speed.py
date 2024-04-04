from datetime import timedelta
import pandas as pd


def main():
    df = pd.read_csv("data/measurements.csv", index_col=0, parse_dates=["hour"], date_format="%Y%m%d%H").sort_index()
    wind = df.groupby(["hour"])["wind_speed"].mean().mul(3.6)
    dates = df["hour"].unique()
    print(f"Max hourly average wind speed for measurement period: {round(wind.max(), 1)} km/h")

    for i in range(len(wind)):
        if (s := wind.iloc[i]) >= 30:
            first_date_str = dates[i].strftime("%Y-%m-%d %H:00")
            second_date_str = (dates[i] + timedelta(hours=1)).strftime("%H:00")
            print(f"High wind speed of {round(s, 1)} km/h on the {first_date_str} - {second_date_str}")


if __name__ == "__main__":
    main()
