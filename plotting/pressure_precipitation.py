import matplotlib.pyplot as plt
import pandas as pd


def main():
    df = pd.read_csv("data/measurements.csv", index_col=0, parse_dates=["day"]).sort_index()
    groupby = ["day"]
    air_pressure = df.groupby(groupby)["absolute_air_pressure"].mean()
    precipitation = df.groupby(groupby)["precipitation"].sum()

    plt.scatter(air_pressure, precipitation)
    plt.show()


if __name__ == "__main__":
    main()
