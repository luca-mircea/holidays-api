"""
Here we keep the code for the streamlit app - a very basic one
where we simply provide a cute web interface for running
the query against our mock database
"""

import sqlite3
import streamlit as st
from pandas import DataFrame
from src.load_data_into_db import load_data_into_db
from src.query_execution import execute_query


class BadInput(Exception):
    pass


def main():
    conn = sqlite3.connect(":memory:")
    load_data_into_db(conn)
    print("main is running")
    st.title("Database User Interface")

    user_input = st.text_input(
        "Please write your query below",
        value="SELECT * FROM locations",
        placeholder="Type your query here...",
    )

    if st.button("Run Query"):
        try:
            result = execute_query(user_input)
            if isinstance(result, DataFrame):
                st.write("Query Results:")
                st.dataframe(result)
            else:
                raise BadInput(
                    "The query you submitted could " "not be executed. Please try again"
                )
        except Exception as e:
            # normally we'd catch each possible exception individually
            print(f"Your query could not be run. The error was: \n\n{e}")


if __name__ == "__main__":
    main()
