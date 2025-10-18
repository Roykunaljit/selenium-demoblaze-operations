# utilities/csv_utils.py

import csv
import pandas as pd
import os


class CSVUtils:
    @staticmethod
    def read_csv_data(file_path):
        """
        Read data from a CSV file using Python's built-in csv module.
        Returns a list of dictionaries, where each dictionary represents a row.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"CSV file not found: {file_path}")

        data = []
        with open(file_path, 'r', newline='', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                data.append(row)
        return data

    @staticmethod
    def write_csv_data(file_path, data, headers=None):
        """
        Write a list of dictionaries to a CSV file using Python's csv module.
        Parameters:
            file_path (str): Path to the output CSV file.
            data (list of dict): Data to write.
            headers (list, optional): Column headers. If not provided, inferred from the first row.
        """
        if not data:
            raise ValueError("No data provided to write to CSV.")

        # Infer headers if not provided
        if headers is None and isinstance(data[0], dict):
            headers = list(data[0].keys())

        # Ensure output directory exists
        os.makedirs(os.path.dirname(file_path) if os.path.dirname(file_path) else '.', exist_ok=True)

        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)

    @staticmethod
    def read_with_pandas(file_path):
        """
        Read a CSV file using pandas for advanced data handling.
        Returns a list of dictionaries.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"CSV file not found: {file_path}")

        df = pd.read_csv(file_path)
        return df.to_dict('records')