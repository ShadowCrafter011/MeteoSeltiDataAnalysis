import pandas as pd


def main():
    best = {"deviation": 1e12}
    values = [i / 120 for i in range(11)]
    print(values)
    x, y = 0, 0
    for _ in range(len(values) ** 2):
        df = pd.read_csv("data/measurements.csv", parse_dates=["day"]).sort_index()

        # Set sunshine duration to 5 minutes for all rows and to 0 for rows where the cloud status is cloudy
        # For "between" cloud status 3 minutes are used
        x_val, y_val = values[x], values[y]
        df.insert(0, "sunshine_duration", x_val)
        df.loc[df["cloud_status"] == "cloudy", "sunshine_duration"] = y_val
        df.loc[df["cloud_status"] == "between", "sunshine_duration"] = 0
        
        x += 1
        if x >= len(values):
            x = 0
            y += 1

        # Plot daily sunshine duration summed up
        estimated_sum = df.groupby(["day"])["sunshine_duration"].sum().values

        # Plot MeteoSwiss sunshine duration in Binningen
        meteoswiss = pd.read_csv("meteoswiss/sunshine_duration/data.csv", sep=";", parse_dates=["time"])

        meteoswiss.insert(0, "Estimated by CloudyAI", estimated_sum[:len(meteoswiss)])
        meteoswiss = meteoswiss.rename(columns={"su2000d0": "Measured by MeteoSwiss in Binningen"})

        deviation = (meteoswiss["Measured by MeteoSwiss in Binningen"] - meteoswiss["Estimated by CloudyAI"]).abs().sum()
        if deviation < best["deviation"]:
            best = {
                "deviation": deviation,
                "daily_deviation": deviation / len(meteoswiss),
                "sunny": x_val,
                "sunny_index": x,
                "between": y_val,
                "between_index": y
            }
        
        print(f"Testing sunny {round(x_val, 3)}, between {round(y_val, 3)} and cloudy 0: deviation {round(deviation, 3)}, daily deviation: {round(deviation / len(meteoswiss), 3)}")

    print(best)


if __name__ == "__main__":
    main()
