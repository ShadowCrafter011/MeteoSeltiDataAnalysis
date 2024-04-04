import matplotlib.pyplot as plt
import pandas as pd


def main():
    df = pd.read_csv("data/measurements.csv", index_col=0, parse_dates=["day"]).sort_index()
    groupby = ["hour"]
    temperature = df.groupby(groupby)["air_temperature"].mean()
    wind_direction = df.groupby(groupby)["wind_direction"].mean()

    plt.scatter(wind_direction, temperature)
    plt.show()


if __name__ == "__main__":
    main()
