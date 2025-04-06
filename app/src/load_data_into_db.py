"""
Here we load the data from extract_data_from_api into a mock database
that we can then use to "query" from the outside after we dockerize
this project in order to mimmick querying a database
"""

import duckdb
import pandas as pd
from src.extract_data_from_api import get_data_from_local, get_holiday_data_from_api
from src.transform_data import process_data_from_api


class WrongLoadMode(Exception):
    pass


def load_data_into_db(
    conn: duckdb.DuckDBPyConnection = duckdb.connect(":memory:"), mode: str = "local"
) -> None:
    """Load df into DB"""
    if mode == "api":
        holidays = get_holiday_data_from_api()
    elif mode == "local":
        holidays = get_data_from_local()
    else:
        raise WrongLoadMode("mode has to be 'api' or 'local'")

    holidays_df = process_data_from_api(holidays)
    locations_df = pd.read_csv("./src/stored_data/locations.csv")

    # note: the uuid is not unique/a primary key
    # unique values should be checked for the uuid X subdivision combination
    # or alternatively by name/date_string X subdivision combo

    # load into table
    conn.execute("CREATE TABLE holidays AS SELECT * FROM holidays_df")

    # also load the locations table
    conn.execute("CREATE TABLE locations AS SELECT * FROM locations_df")
