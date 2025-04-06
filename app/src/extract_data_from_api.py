"""
Here we extract the data from the API

I assume the holidays to be static and known well in advance
so we will need to query them very rarely, which is why I think
it makes little sense to invest a lot of time into making this part
ultra high-performance.

I would query the API depending on how often we onboard new partners
and how close together they are + the granularity of the holidays.
For example, if holidays are the same in all of Austria, I will
only get that data once per year and use it for all the partners.

If/when we expand to a new country, I would set that up to trigger
an update to the list of countries in the constants file of the project

Because this app will run very rarely and the data quantity is quite small,
I will use pandas for convenience. I would not do so if I were worried about
having a lean build or if I wanted super high performance
"""

import holidayapi
import pandas as pd

from src.constants import API_KEY, COUNTRIES, YEAR


class ApiError(Exception):
    pass


def get_holiday_data_from_api() -> pd.DataFrame:
    """Get data from API for countries, return flattened DF"""
    try:
        hapi = holidayapi.v1(API_KEY)
        # note: normally instantiate client outside function
        # and then pass into here to make more efficient
        # but in this case it's overkill

        holidays = hapi.holidays(
            {"country": COUNTRIES, "year": YEAR, "subdivisions": True}
        )

        # make it nice
        holiday_data = holidays["holidays"]

        holidays_df = pd.json_normalize(holiday_data, sep="_")

        return holidays_df

    except Exception as e:
        (
            print(
                ApiError(
                    "There was a problem when retrieving" f"the data from the API: {e}"
                )
            )
        )
        # note: here we'd tackle different kinds of exceptions
        # such as one for having exceeded the quota
        # one for no-network
        # maybe another for an API error (codes 5xx)
        # but I opted for a generic one since it's a demo


def get_data_from_local() -> pd.DataFrame:
    """Also keep a copy locally since small & quota, useful for tests"""
    holidays_df = pd.read_csv("./src/stored_data/holidays.csv")

    return holidays_df
