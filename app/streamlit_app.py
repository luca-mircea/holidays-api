"""
Here we keep the code for the streamlit app - a very basic one
where we simply provide a cute web interface for running
the query against our mock database
"""

import duckdb
import streamlit as st
from pandas import DataFrame
from src.load_data_into_db import load_data_into_db
from src.query_execution import execute_query


class BadInput(Exception):
    pass


def main():
    default_query = """
    WITH holiday_location_selection AS (
        SELECT
            *
        FROM holidays
        LEFT JOIN locations
        ON holidays.country = locations.country_code
        UNION ALL
        SELECT
            *
        FROM holidays
        LEFT JOIN locations
        ON holidays.subdivisions = locations.subdivision_code
    )
    
    SELECT *
    FROM holiday_location_selection
    WHERE location_id = '9415913d-fffa-41f9-9323-6d62e6100a31'
    AND observed_string >= '2024-01-01'
    AND observed_string <= '2024-02-01'
    """

    # run the app
    st.title("Database User Interface")

    user_input = st.text_area(
        "Please write your query below",
        value=default_query,
        placeholder="Type your query here...",
        height=300,
    )

    if st.button("Run Query"):
        try:
            # set up the db
            conn = duckdb.connect(":memory:")
            load_data_into_db(conn)

            result = execute_query(user_input, conn)
            if isinstance(result, DataFrame):
                st.write("Query Results:")
                st.dataframe(result)
            else:
                raise BadInput(
                    "The query you submitted could not be executed. Please try again"
                )
        except Exception as e:
            # normally we'd catch each possible exception individually
            st.write(f"Your query could not be run. The error was: \n\n{e}")


if __name__ == "__main__":
    main()
