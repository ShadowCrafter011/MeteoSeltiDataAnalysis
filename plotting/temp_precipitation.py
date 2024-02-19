import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def main():
    df = pd.read_csv("data/measurements.csv", index_col=0, parse_dates=["month"]).sort_index()
    temperature = df.groupby(["month"])["air_temperature"].mean()
    precipitation = df.groupby(["month"])["precipitation"].sum().div(2)

    # precipitation = np.where(precipitation <= 50, precipitation, (precipitation + 900) / 20)

    x = df["month"].unique()
    _, ax = plt.subplots()
    x_axis = plt.gca().xaxis
    x_axis.set_major_formatter(mdates.DateFormatter("%b"))
    x_axis.set_major_locator(mdates.MonthLocator())

    ax.plot(x, temperature, color="red")
    ax.set_ylabel(r"Temperature [$\degree$C]", color="red")
    ax.tick_params(axis="y", colors="red")

    ax.plot(x, precipitation)

    # Tried to change scale of plot but ticks are only shown above y 50
    # temp2precip = lambda y: np.where(y <= 50, y * 2, y * 20 - 900)
    # precip2temp = lambda y: np.where(y <= 100, y / 2, (y + 900) / 20)

    temp2precip = lambda y: y * 2
    precip2temp = lambda y: y / 2

    secax = ax.secondary_yaxis("right", functions=(temp2precip, precip2temp))
    secax.set_ylabel("Precipitation [mm]", color="blue")
    secax.tick_params(axis="y", colors="blue")

    # Create higher resolution curves for better intersections
    high_res_x = pd.date_range(start=x.min(), end=x.max(), periods=len(x) * 10 * 5)

    # Have to convert datetimes to integers as numpy complains otherwise
    high_res_x_int = high_res_x.array.astype("int64")
    x_int = x.astype("int64")

    np_temp = np.interp(high_res_x_int, x_int, temperature)
    np_precip = np.interp(high_res_x_int, x_int, precipitation)
    total_df = pd.DataFrame({
        "temperature": np_temp,
        "precipitation": np_precip
    })

    ax.fill_between(high_res_x, np_temp, total_df.min(axis=1), color="yellow", alpha=.4)
    ax.fill_between(high_res_x, np_temp, total_df.max(axis=1), color="lightblue", alpha=.8)
    ax.fill_between(high_res_x, np_precip, np.where(np_precip < 50, np_precip, 50), color="royalblue")

    plt.grid(linestyle="dotted")
    plt.show()


if __name__ == "__main__":
    main()
