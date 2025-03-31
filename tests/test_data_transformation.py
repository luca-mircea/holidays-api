"""
Note: I wrote this with ChatGPT to show that I know the principles.
IRL I'd be more critical with my tests. I would test above all
for the data types to ensure they comply with the columns in the tables
"""


import unittest
import pandas as pd
from datetime import datetime

# Assuming the function is defined in a module named `data_processing_module`
from src.transform_data import process_data_from_api


class TestProcessDataFromApi(unittest.TestCase):

    def test_process_data_from_api(self):
        data = {
            "uuid": ["123", "456"],
            "name": ["Holiday1", "Holiday2"],
            "date": ["2023-01-01", "2023-01-02"],
            "observed": ["2023-01-01", "2023-01-03"],
            "public": [True, False],
            "country": ["US", "CA"],
            "subdivisions": [["NY", "NJ"], ["ON"]],
            "weekday_date_name": ["Sunday", "Monday"],
            "weekday_date_numeric": [0, 1],
            "weekday_observed_name": ["Sunday", "Tuesday"],
            "weekday_observed_numeric": [0, 2]
        }
        # we could add more edge cases if any

        df = pd.DataFrame(data)

        # Call the function
        result_df = process_data_from_api(df)

        # Check if the result is a DataFrame
        self.assertIsInstance(result_df, pd.DataFrame)

        # Check if the 'public' column is converted to integers
        self.assertTrue(sum([True if value in [0, 1] else False for value in result_df["public"]]) == 3)

        # Check if the date columns are converted to Unix timestamps
        self.assertEqual(result_df["date_unix"].iloc[0], int(datetime.strptime("2023-01-01", "%Y-%m-%d").timestamp()))
        self.assertEqual(result_df["observed_unix"].iloc[1], int(datetime.strptime("2023-01-01", "%Y-%m-%d").timestamp()))

        # Check if the columns are rearranged correctly
        expected_columns = [
            "uuid", "name", "date_string", "date_unix", "observed_string",
            "observed_unix", "public", "country", "subdivisions",
            "weekday_date_name", "weekday_date_numeric",
            "weekday_observed_name", "weekday_observed_numeric"
        ]
        self.assertListEqual(list(result_df.columns), expected_columns)

        # Check if the 'subdivisions' column is exploded
        self.assertEqual(len(result_df), 3)  # 2 original rows, 1 with 2 subdivisions
        self.assertListEqual(result_df["subdivisions"].tolist(), ["NY", "NJ", "ON"])

        # note: ChatGPT is seriously amazing for unit tests


if __name__ == '__main__':
    unittest.main()
