import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def main():
    df = pd.read_csv("data/measurements.csv", index_col=0, parse_dates=["dayinyear"], date_format="%m%d").sort_index()
    temps_meteoswiss = pd.read_csv("meteoswiss/1864_temp/data.csv", sep=";", index_col=1, parse_dates=["time"])
    
    # https://www.meteoswiss.admin.ch/weather/weather-and-climate-from-a-to-z/temperature/decreases-in-temperature-with-altitude.html
    # Estimate temperature change for elevation change
    temps_meteoswiss["tre200d0"].sub(0.65 * (475 - 315) / 100)
    temps_meteoswiss.insert(0, "dayinyear", temps_meteoswiss.index.strftime("%m%d"))
    norm_meteoswiss = temps_meteoswiss[
        (temps_meteoswiss.index > np.datetime64("1991-01-01", "ns")) &
        (temps_meteoswiss.index < np.datetime64("2020-12-31", "ns"))
    ]
    mean = df.groupby(["day"])["air_temperature"].mean()

    # Get only daily average for days of the last year. Duplicates are discarded
    mean = pd.DataFrame({
        "dayinyear": pd.to_datetime(mean.index, format="%Y%m%d").strftime("%m%d"),
        "air_temperature": mean
    })
    mean = mean.groupby("dayinyear").last()["air_temperature"]

    x_locators = df["dayinyear"].unique()

    # Plot mean for each day since 1864
    norm_group = grouped_meteoswiss(norm_meteoswiss, x_locators)
    mean_meteoswiss = norm_group.mean()
    plt.plot(x_locators, mean_meteoswiss, color="black")

    # Fill difference between mean since 1864 and own measurements
    full_df = pd.DataFrame([mean, mean_meteoswiss])
    plt.fill_between(x_locators, mean_meteoswiss, full_df.max(axis=0), color="red")
    plt.fill_between(x_locators, full_df.min(axis=0), mean_meteoswiss, color="blue")

    # Plot max and min daily values since 1864
    all_group = grouped_meteoswiss(temps_meteoswiss, x_locators)
    plt.plot(x_locators, all_group.max(), color="gray", linewidth=.5)
    plt.plot(x_locators, all_group.min(), color="gray", linewidth=.5)

    # Plot standart deviation from average 1864 - June 2024
    plt.plot(x_locators, mean_meteoswiss + norm_group.std(), color="black", linestyle="dotted")
    plt.plot(x_locators, mean_meteoswiss - norm_group.std(), color="black", linestyle="dotted")

    # Show exact date on hover
    plt.gca().format_xdata = mdates.DateFormatter('%m-%d')

    # x-ticks as months
    x = plt.gca().xaxis
    x.set_major_locator(mdates.MonthLocator())
    x.set_major_formatter(mdates.DateFormatter("%b"))

    # Text
    plt.legend([
        "Täglicher Durschnitt der Norm in Binningen 1991 - 2020",
        "Abweichung über der Norm dieses Jahr",
        "Abweichung unter der Norm dieses Jahr",
        "Maximum seit 1864 in Binningen",
        "Minimum seit 1864 in Binningen",
        "Standardabweichung der Norm"
    ])
    plt.grid(linestyle="dotted")
    plt.title(r"Daily temperature average/min/max [$\degree$C]")
    plt.show()


def grouped_meteoswiss(df, x_locators):
    return df[df["dayinyear"].isin(x_locators)].groupby(["dayinyear"])["tre200d0"]


if __name__ == "__main__":
    main()
