from concurrent.futures import ThreadPoolExecutor
import os
from threading import Thread


def read_data(thread_count=1):
    # Define the directory path
    directory_path = '../../../data/AirNow Fires/data/'
    # List to store all file names
    file_names = []
    # Walk through the directory
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.csv'):
                file_names.append(os.path.join(root, file))

    print('Number of files: ', len(file_names))
    # columns = ['Latitude', 'Longitude', 'UTC', 'Parameter', 'Concentration', 'Unit', 'Raw Concentration', 'AQI', 'Category', 'Site Name', 'Site Agency', 'AQS ID', 'Full AQS ID' ]
    data = {}
    max_data = {}

    def process_chunk(file):
        with open(file, 'r') as f:
            lines = f.readlines()
            print('Processing file: ', file)
            for line in lines[1:]:
                line = line.strip().replace('"', '').split(',')
                key = line[9]+" "+line[0]+" "+line[1]
                if key not in data:
                    data[key] = {}
                if line[3] not in data[key]:
                    data[key][line[3]] = 0

                data[key][line[3]] += float(line[7])

    def calculate_max(data):
        for key in data:
            max_data[key] = max(data[key], key=data[key].get)

    if thread_count == 1:
        for file in file_names:
            process_chunk(file)

        calculate_max(data)
    else:
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            executor.map(lambda file: process_chunk(file), file_names)

        def split_into_batches(data, batch_size):
            keys = list(data.keys())
            for i in range(0, len(keys), batch_size):
                yield {k: data[k] for k in keys[i:i + batch_size]}

        data_batches = list(split_into_batches(data, len(data) // thread_count + 1))
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            executor.map(calculate_max, data_batches)

    print(len(max_data))


import time

start = time.time()
read_data(1)
print('Time taken: ', time.time()-start)

start = time.time()
read_data(6)
print('Time taken: ', time.time()-start)
