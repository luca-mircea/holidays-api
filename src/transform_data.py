"""
Here we keep the function for transforming the data from the API
"""

from datetime import datetime

import pandas as pd


def process_data_from_api(data: pd.DataFrame) -> pd.DataFrame:
    """Process the data into the shape of the DB table"""
    # note: need to convert boolean to 1/0 for sqlite database
    data["public"] = [1 if flag else 0 for flag in data["public"]]

    # we also convert dates from string to unix
    # I expect unix to be high performance for
    # querying the DB thousands of times a day
    data.rename(
        columns={"date": "date_string", "observed": "observed_string"}, inplace=True
    )

    data["date_unix"] = [
        int(datetime.strptime(date_string, "%Y-%m-%d").timestamp())
        for date_string in data["date_string"]
    ]

    data["observed_unix"] = [
        int(datetime.strptime(date_string, "%Y-%m-%d").timestamp())
        for date_string in data["observed_string"]
    ]

    # rearrange columns

    data = data[
        [
            "uuid",
            "name",
            "date_string",
            "date_unix",
            "observed_string",
            "observed_unix",
            "public",
            "country",
            "subdivisions",
            "weekday_date_name",
            "weekday_date_numeric",
            "weekday_observed_name",
            "weekday_observed_numeric",
        ]
    ]

    # note: we need to join on the subdivision, so we
    # "flatten" the table longitudinally

    # this is because of sqllite, but real life databases
    # like BigQuery support joining with/ checking in an array

    data = data.explode("subdivisions")

    # note to self: not sure yet what to do with NaN,
    # it depends on the logic of the eventual query

    return data
