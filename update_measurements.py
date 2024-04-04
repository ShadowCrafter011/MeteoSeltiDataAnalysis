from dotenv import load_dotenv
from datetime import datetime
from pytz import timezone
import pandas as pd
import json
import os


def main():
    load_dotenv()
    
    # Check if previous file exists if so rename it
    if os.path.isfile("data/latest.json") and os.path.isfile("data/measurements.csv"):
        with open("data/latest.json") as f:
            time_str = json.loads(f.read())["time"]

        os.rename("data/measurements.csv", f"data/{time_str}.csv")

    # Persist current datetime
    now = datetime.now(timezone("Europe/Zurich"))
    with open("data/latest.json", "w") as f:
        f.write(json.dumps({
            "time": now.strftime("%d.%m.%Y %H-%M-%S")
        }))

    # Get measurements from database
    capture_cmd = r"\COPY measurements TO 'data/measurements.csv' WITH (FORMAT csv, DELIMITER ',',  HEADER true);"
    os.system(f"heroku pg:psql -a meteoselti -c \"{capture_cmd}\"")

    # Format csv file
    df = pd.read_csv("data/measurements.csv")
    df.insert(0, "datetime", pd.to_datetime(df["measured_at"]))
    df = df.set_index("datetime")
    df = df.tz_localize("utc")
    df = df.tz_convert("Europe/Zurich")
    df = df.drop(["id", "measured_at", "created_at", "updated_at"], axis="columns")
    df.insert(0, "month", df.index.strftime("%Y%m01"))
    df.insert(1, "day", df.index.strftime("%Y%m%d"))
    df.insert(2, "hour", df.index.strftime("%Y%m%d%H"))
    df.to_csv("data/measurements.csv")


if __name__ == "__main__":
    main()
