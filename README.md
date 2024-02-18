# MeteoSelti data analysis

All python files are designed to be run from the project root directory.

## Util package

Since access to the measurement data is frequent and parsing the `measurements.csv` file is not perfect out of the box there exists a util package in this project. It must be installed in the used pip environment: `pip install -e util`

If you are using a virtual environment (which is recommended) the command most likely is `venv/Scripts/pip.exe install -e util` (Windows).

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
