import pandas as pd


def main():
    df = pd.read_csv("data/measurements.csv", index_col=0, parse_dates=["day"]).sort_index()
    precip = df.groupby(["day"])["precipitation"].sum()
    dates = df["day"].unique()
    
    dry_periods = []

    start_date, counter = None, 0
    for i in range(len(precip)):
        if precip.iloc[i] > 1:
            if start_date:
                dry_periods.append({
                    "start": start_date,
                    "end": dates[i - 1],
                    "length": counter
                })  
                start_date = None
                counter = 0          
            continue

        if not start_date:
            counter = 1
            start_date = dates[i]
        else:
            counter += 1

    dry_periods = list(filter(lambda x: x["length"] > 5, dry_periods))
    dry_periods = list(sorted(dry_periods, key=lambda x: x["length"], reverse=True))
    
    for dry_period in dry_periods:
        print(f"Dry period from {dry_period['start']} to {dry_period['end']} with a length of {dry_period['length']} days")


if __name__ == "__main__":
    main()
