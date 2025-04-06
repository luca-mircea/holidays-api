"""
Here we keep a function for executing a SQL query
against the mock database
"""

import duckdb
import pandas as pd


class DBFailure(Exception):
    pass


def execute_query(
    query: str, conn: duckdb.DuckDBPyConnection = duckdb.connect(":memory:")
) -> pd.DataFrame:
    """Execute query against the connection"""
    try:
        result = conn.execute(query).fetchdf()
        return result
    except Exception as e:
        raise DBFailure(f"{e}")
