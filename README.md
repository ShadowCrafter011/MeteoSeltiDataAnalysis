# MeteoSelti data analysis

All python files are designed to be run from the project root directory.

## Pulling/updating data

Measurement data is keept in the `data` directory. The measurement files are not checked into git as they are quite large.

### Requirements

- Having the required python packages installed: `pip install -r requirements.txt`

Only required for pulling/updating measurements from the database:

- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
- Being [logged in](https://devcenter.heroku.com/articles/heroku-cli#get-started-with-the-heroku-cli) using Heroku CLI
- `.env` file with variable [`DATABSE_URL`](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING) pointing to a local [PostgreSQL](https://www.postgresql.org/) instance

### Update

Simply run [update_measurements.py](update_measurements.py): `python update_measurements.py`

If there is already a measurement snapshot it will be renamed with using the timestamp it was created at. If there is not a snapshot it will just create a new file with the data.

Either way after having run the updater the up to date measurements will be located here: `data/measurements.csv`

## Extremes

This section describes how the extreme weather detectors work in [extremes](extremes).

### [Dry periods](extremes/dry_periods.py)

According to the [drought definition](https://www.meteoschweiz.admin.ch/wetter/wetter-und-klima-von-a-bis-z/duerre.html) from MeteoSwiss droughts last as long as less than 1mm of precipitation are measured at a given station.

The drought detector finds all possible droughts in the dataset, filters out every drought of length of 5 days or less and displays them in descending order.

### [Hot periods](extremes/hot_periods.py)

This extreme weather condition detector looks for periods of seven days or more with a daily maximal temperature of 30 degrees or more.

### [Cold periods](extremes/cold_periods.py)

This extreme weather condition detector looks for periods of seven days or more with a daily maximal temperature of 0 degrees or less.

### [Wind speed](extremes/wind_speed.py)

This detector looks for average hourly wind speeds above a given value. Works in km/h.

## Plotting

This section describes how the different plotters in [plotting](plotting) behave and what they plot.

### [Temperature history](plotting/temperature_history.py)

This plotter uses temperature data from Basel / Binningen which is homogenised for the altitude change using [this guide by MeteoSwiss](https://www.meteoswiss.admin.ch/weather/weather-and-climate-from-a-to-z/temperature/decreases-in-temperature-with-altitude.html). The difference from the norm defined by MeteoSwiss is displayed in red if its positive, in blue otherwise.

I aimed to recreate [this temperature history graph from MeteoSwiss](https://www.meteoschweiz.admin.ch/service-und-publikationen/applikationen/ext/climate-overview-series-public.html).

### [Climate diagram](plotting/temp_precipitation.py)

Plots temperature and precipitation in the same diagram and shades in the areas like [this example](https://de.wikipedia.org/wiki/Klimadiagramm#/media/Datei:Klimadiagramm-deutsch-Bombay-Indien.png).

### [Daily precipitation](plotting/daily_precip.py)

Simply adds up the precipitation for each day and displays it in a graph. Useful to see the drought periods detected by the [drought detector](extremes/dry_periods.py).

### [Temperature wind direction scatter plot](plotting/temp_wind_dir.py)

Plots the average hourly/daily/monthly temperature and wind direction in a scatter plot.

### [Air pressure precipitation scatter plot](plotting/pressure_precipitation.py)

Plots the average hourly/daily/monthly air pressure and the precipitation sum for that period in a scatter plot.

### [Estimated sunshine duration](plotting/estimated_sunshine_duration.py)

Using the data from CloudyAI the estimated sunshine duration per das is calculated and plottet. Data from MeteoSwiss in Binningen is plotted as well as reference.

Because all measurements occur in 5 minute intervals a status of sunny is interpreted as 5 minutes of sun. A status of between is interpreted as 3 minutes and cloudy as 0. If there are measurements missing because of outages or other reasons the estimated sunshine duration will almost certainly be lower than the actual sunshine duration. That with the fact that CloudyAI is not very accurate and sometimes makes false predictions the estimated sunshine duration is higher than daylight hours for that given day.

Daylight hourse are plottet as dashed line and the data comes from https://gml.noaa.gov/grad/solcalc/ for the location of the weather station in Seltisberg. It does not take the horizon and hills into account but it is the best I have found so far. For simplicity data for 2024 is used. This might lead so some minor inaccuracies.
