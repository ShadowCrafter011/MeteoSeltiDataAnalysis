from dotenv import load_dotenv
from datetime import datetime
from pytz import timezone
import json
import os


def main():
    load_dotenv()
    
    if os.path.isfile("data/latest.json") and os.path.isfile("data/measurements.csv"):
        with open("data/latest.json") as f:
            time_str = json.loads(f.read())["time"]

        os.rename("data/measurements.csv", f"data/{time_str}.csv")

    now = datetime.now(timezone("Europe/Zurich"))
    with open("data/latest.json", "w") as f:
        f.write(json.dumps({
            "time": now.strftime("%d.%m.%Y %H-%M-%S")
        }))

    capture_cmd = r"\COPY measurements TO 'data/measurements.csv' WITH (FORMAT csv, DELIMITER ',',  HEADER true);"
    os.system(f"heroku pg:psql -a meteoselti -c \"{capture_cmd}\"")

if __name__ == "__main__":
    main()
