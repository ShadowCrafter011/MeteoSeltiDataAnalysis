import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from math import ceil
import pandas as pd
import numpy as np


def main():
    df = pd.read_csv("data/measurements.csv", index_col=0, parse_dates=["month"]).sort_index()
    temperature = df.groupby(["month"])["air_temperature"].mean()
    precipitation = df.groupby(["month"])["precipitation"].sum()
    max_precip = precipitation.max()
    max_temp = temperature.max()

    precipitation = np.where(precipitation <= 100, precipitation / 2, (precipitation + 900) / 20)

    x = df["month"].unique()
    _, ax = plt.subplots()
    x_axis = plt.gca().xaxis
    x_axis.set_major_formatter(mdates.DateFormatter("%b"))
    x_axis.set_major_locator(mdates.MonthLocator())

    ax.plot(x, temperature, color="red")
    ax.set_ylabel(r"Temperature [$\degree$C]", color="red")
    ax.tick_params(axis="y", colors="red")

    ax.plot(x, precipitation)

    tick_inverval = 10
    max_plot_val = max(max_precip, max_temp)
    num_ticks = ceil(max_plot_val / tick_inverval)
    max_tick_val = num_ticks * tick_inverval
    ticks = np.arange(0, max_tick_val, tick_inverval)

    secax = ax.secondary_yaxis("right")
    secax.set_ylabel("Precipitation [mm]", color="blue")
    secax.tick_params(axis="y", colors="blue")

    # Set ticks
    ax.yaxis.set_ticks(ticks)
    secax.yaxis.set_ticks(ticks)
    sexax_tick_labels = []
    tick = 0
    for _ in range(num_ticks):
        sexax_tick_labels.append(tick)
        tick += tick_inverval * 2 * (tick < 100) + 200 * (tick >= 100)
    secax.yaxis.set_ticklabels(sexax_tick_labels)

    # Create higher resolution curves for better intersections
    high_res_x = pd.date_range(start=x.min(), end=x.max(), periods=len(x) * 50)

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
