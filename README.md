# MeteoSelti data analysis

All python files are designed to be run from the project root directory.

## Pulling/updating data

Measurement data is keept in the `data` directory. The measurement files are not checked into git as they are quite large.

### Requirements

- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
- Being [logged in](https://devcenter.heroku.com/articles/heroku-cli#get-started-with-the-heroku-cli) using Heroku CLI
- Having the required python packages installed: `pip install -r requirements.txt`
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

### [Average min max](plotting/temp_average_min_max.py)

This plotter uses months as major ticks and displays the daily average, minimum and maximum temperature.

### [Climate diagram](plotting/temp_precipitation.py)

Plots temperature and precipitation in the same diagram and shades in the areas like [this example](https://de.wikipedia.org/wiki/Klimadiagramm#/media/Datei:Klimadiagramm-deutsch-Bombay-Indien.png).

### [Daily precipitation](plotting/daily_precip.py)

Simply adds up the precipitation for each day and displays it in a graph. Useful to see the drought periods detected by the [drought detector](extremes/dry_periods.py).

### [Temperature wind direction scatter plot](plotting/temp_wind_dir.py)

Plots the average hourly/daily/monthly temperature and wind direction in a scatter plot.

### [Air pressure precipitation scatter plot](plotting/pressure_precipitation.py)

Plots the average hourly/daily/monthly air pressure and the precipitation sum for that period in a scatter plot.
