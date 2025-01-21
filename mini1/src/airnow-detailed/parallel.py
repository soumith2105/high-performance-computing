from concurrent.futures import ThreadPoolExecutor
import os
import time

# Define a class to represent each data entry
class DataEntry:
    def __init__(self, latitude, longitude, site_name, parameter, concentration):
        self.latitude = latitude
        self.longitude = longitude
        self.site_name = site_name
        self.parameter = parameter
        self.concentration = float(concentration)

def read_data(thread_count=1):
    # Define the directory path
    directory_path = '../../data/AirNow Fires/data/'
    # List to store all file names
    file_names = []
    # Walk through the directory to get all .csv file names
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.csv'):
                file_names.append(os.path.join(root, file))

    print('Number of files: ', len(file_names))

    # List to store all data entries (objects)
    data_entries = []

    # Function to process each chunk (file)
    def process_chunk(file):
        with open(file, 'r') as f:
            lines = f.readlines()
            print('Processing file: ', file)
            for line in lines[1:]:  # Skip header line
                line = line.strip().replace('"', '').split(',')
                if float(line[7]) > 0:  # Ensure concentration is positive
                    # Create a data entry object and add to the list
                    entry = DataEntry(
                        latitude=line[0],
                        longitude=line[1],
                        site_name=line[9],
                        parameter=line[3],
                        concentration=line[7]
                    )
                    data_entries.append(entry)

    # Process each file concurrently using ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        executor.map(lambda file: process_chunk(file), file_names)

    # Function to calculate the max concentrations
    def calculate_max(entries):
        aggregated_data = {}
        for entry in entries:
            key = f"{entry.site_name} {entry.latitude} {entry.longitude}"
            if key not in aggregated_data:
                aggregated_data[key] = {}
            if entry.parameter not in aggregated_data[key]:
                aggregated_data[key][entry.parameter] = 0
            aggregated_data[key][entry.parameter] += entry.concentration
        
        # Now find the maximum value for each key
        max_data = {}
        for key in aggregated_data:
            max_data[key] = max(aggregated_data[key], key=aggregated_data[key].get)
        return max_data

    # Split data into batches for processing
    def split_into_batches(data, batch_size):
        for i in range(0, len(data), batch_size):
            yield data[i:i + batch_size]

    data_batches = list(split_into_batches(data_entries, len(data_entries) // thread_count + 1))

    # Calculate max for each batch using threads
    max_data_results = []
    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        max_data_results = list(executor.map(calculate_max, data_batches))

    # Combine all max_data results from different batches
    combined_max_data = {}
    for max_data in max_data_results:
        combined_max_data.update(max_data)

    print('Number of unique site-parameter combinations with max data: ', len(combined_max_data))

start = time.time()
read_data(6)
print('Time taken: ', time.time() - start)
