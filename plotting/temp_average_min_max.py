import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd


def main():
    df = pd.read_csv("data/measurements.csv", index_col=0, parse_dates=["day"]).sort_index()
    group = df.groupby(["day"])["air_temperature"]
    mean = group.mean()
    min = group.min()
    max = group.max()

    x_locators = df["day"].unique()
    plt.plot(x_locators, mean)
    plt.plot(x_locators, max, color="red", alpha=.2)
    plt.plot(x_locators, min, color="blue", alpha=.2)
    plt.fill_between(x_locators, mean, max, color="red", alpha=.1)
    plt.fill_between(x_locators, mean, min, color="blue", alpha=.1)

    # Show exact date on hover
    plt.gca().format_xdata = mdates.DateFormatter('%Y-%m-%d')

    # x-ticks as months
    x = plt.gca().xaxis
    x.set_major_locator(mdates.MonthLocator())
    x.set_major_formatter(mdates.DateFormatter("%b"))

    # Text
    plt.legend(["Daily average", "Daily maximum", "Daily minimum"])
    plt.grid(linestyle="dotted")
    plt.title(r"Daily temperature average/min/max [$\degree$C]")
    plt.show()


if __name__ == "__main__":
    main()
