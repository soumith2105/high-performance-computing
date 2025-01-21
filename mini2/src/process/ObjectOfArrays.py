import csv
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import os

directory_path = "data/AirNow Fires/data/"


class ObjectOfArrays:
    global directory_path

    @classmethod
    def _get_file_names(cls):
        file_names = []
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith(".csv"):
                    file_names.append(os.path.join(root, file))
        return file_names

    @classmethod
    def read_dataset(self):
        file_names = self._get_file_names()
        data = {
            "latitude": [],
            "longitude": [],
            "parameter": [],
            "aqi": [],
            "sitename": [],
        }

        for file_path in file_names:
            with open(file_path, "r") as fo:
                csv_reader = csv.reader(fo)

                # Ensure that the header matches expected columns in the 'data' dictionary
                for row in csv_reader:
                    data["latitude"].append(row[0])
                    data["longitude"].append(row[1])
                    data["parameter"].append(row[3])
                    data["aqi"].append(int(row[7]) if row[7] else 0)
                    data["sitename"].append(row[9])

        return data
