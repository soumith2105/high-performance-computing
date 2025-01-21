from concurrent.futures import ThreadPoolExecutor
import os
import time

# Define a class to represent the data entries for clarity
class AirQualityDataEntry:
    def __init__(self, latitude, longitude, parameter, concentration, site_name):
        self.latitude = latitude
        self.longitude = longitude
        self.parameter = parameter
        self.concentration = float(concentration)
        self.site_name = site_name

def read_data():
    # Define the directory path
    directory_path = '../../data/AirNow Fires/data/'
    # List to store all file names
    file_names = []

    # Walk through the directory and collect file names
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.csv'):
                file_names.append(os.path.join(root, file))

    print('Number of files: ', len(file_names))

    # List to store all data entries
    data_entries = []

    def process_chunk(file):
        with open(file, 'r') as f:
            lines = f.readlines()
            print('Processing file: ', file)
            for line in lines[1:]:  # Skip the header
                line = line.strip().replace('"', '').split(',')
                # Create a new data entry and append it to the list
                entry = AirQualityDataEntry(
                    latitude=line[0],
                    longitude=line[1],
                    parameter=line[3],
                    concentration=line[4],
                    site_name=line[9],
                )
                data_entries.append(entry)

    # Process each file to collect data entries
    for file in file_names:
        process_chunk(file)

    # Dictionary to hold aggregated data for max calculation
    aggregated_data = {}

    # Aggregate data from the list of entries
    for entry in data_entries:
        key = f"{entry.site_name} {entry.latitude} {entry.longitude}"
        if key not in aggregated_data:
            aggregated_data[key] = {}
        if entry.parameter not in aggregated_data[key]:
            aggregated_data[key][entry.parameter] = 0

        aggregated_data[key][entry.parameter] += entry.concentration

    # Dictionary to hold maximum values
    max_data = {}

    # Calculate max values for each key
    for key in aggregated_data:
        max_data[key] = max(aggregated_data[key], key=aggregated_data[key].get)

    print('Number of unique entries with max data: ', len(max_data))

start = time.time()
read_data()
print('Time taken: ', time.time() - start)
