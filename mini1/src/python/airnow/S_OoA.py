import csv
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import os

global directory_path
directory_path = '../../../data/AirNow Fires/data/'

class ObjectOfArrays():
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
        data = {
            "Latitude": [],
            "Longitude": [],
            "Parameter": [],
            "AQI": [],
            "Site Name": [],
        }

        def read_air_quality_data(file_names):
            data = {
                "Latitude": [],
                "Longitude": [],
                "Parameter": [],
                "AQI": [],
                "Site Name": [],
            }
            for file_path in file_names:
                with open(file_path, 'r') as fo:
                    csv_reader = csv.reader(fo)

                    # Ensure that the header matches expected columns in the 'data' dictionary
                    for row in csv_reader:
                        data["Latitude"].append(row[0])
                        data["Longitude"].append(row[1])
                        data["Parameter"].append(row[3])
                        data["AQI"].append(int(row[7]) if row[7] else 0)
                        data["Site Name"].append(row[9])

            return data

        pollutant_data = defaultdict(lambda: defaultdict(int))  # Aggregating AQI per pollutant in each site/area

        # Function to aggregate AQI data based on site and pollutant
        def aggregate_pollutant_data(start_idx, end_idx):
            for i in range(start_idx, end_idx):
                site = f"{data['Site Name'][i]} ({data['Latitude'][i]}, {data['Longitude'][i]})" if data["Site Name"][i] else f"{data["Latitude"][i], data["Longitude"][i]}"
                pollutant_data[site][data['Parameter'][i]] += data['AQI'][i]

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
            data = read_air_quality_data(file_names)
            aggregate_pollutant_data(0, len(data["Latitude"]))
            identify_problematic_pollutants(pollutant_data)

        else:
            break_point = len(file_names) // thread_count + 1
            batches = [file_names[i:i+break_point] for i in range(0, len(file_names), break_point)]

            with ThreadPoolExecutor(max_workers=thread_count) as executor:
                data_batch = executor.map(read_air_quality_data, batches)

            for data_item in data_batch:
                data["Latitude"].extend(data_item["Latitude"])
                data["Longitude"].extend(data_item["Longitude"])
                data["Parameter"].extend(data_item["Parameter"])
                data["AQI"].extend(data_item["AQI"])
                data["Site Name"].extend(data_item["Site Name"])

            break_point = len(data["Latitude"]) // thread_count + 1
            batches = [(i, i+break_point if i+break_point < len(data["Latitude"]) else len(data["Latitude"])) for i in range(0, len(data["Latitude"]), break_point)]
            with ThreadPoolExecutor(max_workers=thread_count) as executor:
                executor.map(lambda batch: aggregate_pollutant_data(*batch), batches)

            data_batches = list(split_into_batches(pollutant_data, len(pollutant_data) // thread_count + 1))
            with ThreadPoolExecutor(max_workers=thread_count) as executor:
                executor.map(identify_problematic_pollutants, data_batches)

        # Output the results
        print(len(problematic_pollutants))

# Example usage
import time

start = time.time()
ObjectOfArrays.most_problematic_pollutant()
print('Time taken with 1 thread: ', time.time() - start)

start = time.time()
ObjectOfArrays.most_problematic_pollutant(6)
print('Time taken with 4 threads: ', time.time() - start)
