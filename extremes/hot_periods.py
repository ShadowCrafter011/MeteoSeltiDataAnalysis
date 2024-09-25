import pandas as pd


def main():
    df = pd.read_csv("data/measurements.csv", index_col=0, parse_dates=["day"]).sort_index()
    temperature = df.groupby(["day"])["air_temperature"].max()
    dates = df["day"].unique()

    hot_weeks = []
    start = None
    num = 0
    
    for i in range(len(temperature)):
        temp = temperature.iloc[i]
        day = dates[i]
        if temp < 30:
            if num >= 5:
                hot_weeks.append((start, day, num))

            start = None
            num = 0
            continue

        if not start:
            start = day

        num += 1

    print(hot_weeks)


if __name__ == "__main__":
    main()
