import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd


def main():
    df = pd.read_csv("data/measurements.csv", parse_dates=["day"]).sort_index()

    # Set sunshine duration to 5 minutes for all rows and to 0 for rows where the cloud status is cloudy
    # For "between" cloud status 3 minutes are used
    df.insert(0, "sunshine_duration", 5 / 60)
    df.loc[df["cloud_status"] == "cloudy", "sunshine_duration"] = 0
    df.loc[df["cloud_status"] == "between", "sunshine_duration"] = 3 / 60

    # Plot daily sunshine duration summed up
    estimated_sum = df.groupby(["day"])["sunshine_duration"].sum().values

    # Plot MeteoSwiss sunshine duration in Binningen
    meteoswiss = pd.read_csv("meteoswiss/sunshine_duration/data.csv", sep=";", parse_dates=["time"])

    meteoswiss.insert(0, "Estimated by CloudyAI", estimated_sum[:len(meteoswiss)])
    meteoswiss = meteoswiss.rename(columns={"su2000d0": "Measured by MeteoSwiss in Binningen"})

    max_sunshine = []
    sunrise = pd.read_csv("meteoswiss/sunshine_duration/sunrise.csv", comment="#")
    sunset = pd.read_csv("meteoswiss/sunshine_duration/sunset.csv", comment="#")
    last_rise, last_set = 0, 0

    for date in meteoswiss["time"]:
        try:
            rise = sunrise.loc[int(date.strftime("%d")), date.strftime("%b")]
        except:
            rise = last_rise

        try:
            set = sunset.loc[int(date.strftime("%d")), date.strftime("%b")]
        except:
            set = last_set

        if pd.isna(rise):
            rise = last_rise

        if pd.isna(set):
            set = last_set

        last_set = set
        last_rise = rise

        delta_t = pd.to_datetime(set, format="%H:%M") - pd.to_datetime(rise, format="%H:%M")
        max_sunshine.append(delta_t.seconds / 3600)

    meteoswiss.insert(0, "Daylight hours Seltisberg (gml.noaa.gov)", max_sunshine)

    ax = meteoswiss[["Measured by MeteoSwiss in Binningen", "Estimated by CloudyAI"]].plot.bar()
    meteoswiss[["Daylight hours Seltisberg (gml.noaa.gov)"]].plot.line(linestyle="dashed", color="black", ax=ax)

    # Plot titles
    plt.title("Estimeted sunshine duration with CloudyAI vs MeteoSwiss measurements")
    plt.xlabel("Date")
    plt.ylabel("Sunshine duration [h]")

    # Show exact date on hover
    plt.gca().format_xdata = mdates.DateFormatter('%b %d')

    # x-ticks as months
    x = plt.gca().xaxis
    x.set_major_locator(mdates.MonthLocator())
    x.set_major_formatter(mdates.DateFormatter("%b"))

    plt.show()


if __name__ == "__main__":
    main()
