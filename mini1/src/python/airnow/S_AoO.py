from concurrent.futures import ThreadPoolExecutor
import csv
import time
import threading
from collections import defaultdict
import os

global directory_path
directory_path = '../../../data/AirNow Fires/data/'
class ArrayOfObjects():
    @classmethod
    def _get_file_names(cls):
        file_names = []
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith('.csv'):
                    file_names.append(os.path.join(root, file))
        return file_names


    @classmethod
    def most_problematic_pollutant(self, thread_count=1):
        file_names = self._get_file_names()
        data = []

        def read_air_quality_data(file_names):
            for file in file_names:
                with open(file, 'r') as fo:
                    csv_reader = csv.reader(fo)

                    # Read the header row
                    _ = next(csv_reader)

                    # Read the actual data
                    for row in csv_reader:
                        country_data = {
                            "Latitude": row[0],
                            "Longitude": row[1],
                            "Parameter": row[3],
                            "AQI": int(row[7]),
                            "Site Name": row[9],
                        }
                        data.append(country_data)

        pollutant_data = defaultdict(lambda: defaultdict(int))

        def aggregate_pollutant_data(data):
            for entry in data:
                area = f"{entry["Site Name"]} ({entry["Latitude"], entry["Longitude"]}" if entry["Site Name"] else f"{entry["Latitude"], entry["Longitude"]}"
                pollutant_data[area][entry["Parameter"]]+=entry["AQI"]


        problematic_pollutants = {}
        def identify_problematic_pollutants(pollutant_data):

            for area, pollutants in pollutant_data.items():
                max_val = (0, '')
                for pollutant, aqis in pollutants.items():
                    max_val = max((aqis, pollutant), max_val)

                problematic_pollutants[area] = max_val[1]

        def split_into_batches(data, batch_size):
            keys = list(data.keys())
            for i in range(0, len(keys), batch_size):
                yield {k: data[k] for k in keys[i:i + batch_size]}

        if thread_count == 1:
            read_air_quality_data(file_names)
            aggregate_pollutant_data(data)
            identify_problematic_pollutants(pollutant_data)


        else:
            break_point = len(file_names) // thread_count + 1
            batches = [file_names[i:i+break_point] for i in range(0, len(file_names), break_point)]

            with ThreadPoolExecutor(max_workers=thread_count) as executor:
                executor.map(read_air_quality_data, batches)

            break_point = len(data) // thread_count + 1
            batches = [data[i:i+break_point] for i in range(0, len(data), break_point)]
            with ThreadPoolExecutor(max_workers=thread_count) as executor:
                executor.map(aggregate_pollutant_data, batches)

            data_batches = list(split_into_batches(pollutant_data, len(pollutant_data) // thread_count + 1))
            with ThreadPoolExecutor(max_workers=thread_count) as executor:
                executor.map(identify_problematic_pollutants, data_batches)

        # for area, pollutant in problematic_pollutants.items():
        #     print(f"{area} => Most Problematic Pollutant: {pollutant}")

        print(len(problematic_pollutants))



import time
start = time.time()
ArrayOfObjects.most_problematic_pollutant()
print('Time taken: ', time.time()-start)


import time
start = time.time()
ArrayOfObjects.most_problematic_pollutant(6)
print('Time taken: ', time.time()-start)
