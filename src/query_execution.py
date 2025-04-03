"""
Here we keep a function for executing a SQL query
against the mock database
"""

import sqlite3
import pandas as pd


class DBFailure(Exception):
    pass


def execute_query(query: str, conn: sqlite3.Connection = sqlite3.connect(":memory:")) -> pd.DataFrame:
    """Execute query against the connection"""

    cursor = conn.cursor()

    # cursor.execute(query)

    try:
        result = pd.read_sql_query(query, conn)
        return result
    except Exception as e:
        raise DBFailure(f"{e}")
