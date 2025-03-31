"""
Here we load the data from extract_data_from_api into a mock database
that we can then use to "query" from the outside after we dockerize
this project in order to mimmick querying a database
"""

import sqlite3

import pandas as pd

from extract_data_from_api import (get_data_from_local,
                                   get_holiday_data_from_api)
from transform_data import process_data_from_api


class WrongLoadMode(Exception):
    pass


def load_data_into_db(mode: bool = "local") -> None:
    """Load df into DB"""
    if mode == "api":
        holidays = get_holiday_data_from_api()
    elif mode == "local":
        holidays = get_data_from_local()
    else:
        raise WrongLoadMode("mode has to be 'api' or 'local'")

    holidays_df = process_data_from_api(holidays)
    locations_df = pd.read_csv("../stored_data/locations.csv")

    # note: normally client instantiated outside, passed as argument
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # note: the uuid is not unique/a primary key
    # unique values should be checked for the uuid X subdivision combination
    # or alternatively by name/date_string X subdivision combo

    # load into table
    holidays_df.to_sql("holidays", conn, if_exists="replace", index=False)
    conn.commit()

    # also load the locations table
    locations_df.to_sql("locations", conn, if_exists="replace", index=False)
    conn.commit()

    # query example
    cursor.execute("SELECT * FROM holidays")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    cursor.execute("SELECT * FROM locations")
    rows = cursor.fetchall()

    for row in rows:
        print(row)
