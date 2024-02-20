import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd


def main():
    df = pd.read_csv("data/measurements.csv", index_col=0, parse_dates=["day"]).sort_index()
    precip = df.groupby(["day"])["precipitation"].sum()

    x_axis = plt.gca().xaxis
    x_axis.set_major_formatter(mdates.DateFormatter("%b"))
    x_axis.set_major_locator(mdates.MonthLocator())
    plt.gca().format_xdata = mdates.DateFormatter('%Y-%m-%d')

    precip.plot()
    plt.show()


if __name__ == "__main__":
    main()
