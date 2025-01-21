from concurrent.futures import ThreadPoolExecutor
import csv
import time
import threading
from collections import defaultdict
import os

directory_path = "data/AirNow Fires/data/"


class ArrayOfObjects:
    global directory_path

    @classmethod
    def _get_file_names(cls):
        file_names = []
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith(".csv"):
                    file_names.append(os.path.join(root, file))
        return file_names  # [: len(file_names) // 2]

    @classmethod
    def read_dataset(self):
        file_names = self._get_file_names()
        data = []

        for file in file_names:
            with open(file, "r") as fo:
                csv_reader = csv.reader(fo)

                # Read the header row
                _ = next(csv_reader)

                # Read the actual data
                for row in csv_reader:
                    country_data = {
                        "latitude": row[0],
                        "longitude": row[1],
                        "parameter": row[3],
                        "aqi": int(row[7]),
                        "sitename": row[9],
                    }
                    data.append(country_data)

        return data
