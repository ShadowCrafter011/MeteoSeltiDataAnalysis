import pandas as pd


def main():
    df = pd.read_csv("data/measurements.csv", parse_dates=["datetime"])
    raindrop_volume = df[df["rain_drop_volume"].notnull()].sort_values("rain_drop_volume").tail(5)
    for i in range(len(raindrop_volume)):
        vol = raindrop_volume.iloc[i]
        print(f"Raindrop volume of {round(vol["rain_drop_volume"])} µl {vol["datetime"].strftime("%Y-%m-%d %H:%M")}")
    
    


if __name__ == "__main__":
    main()
