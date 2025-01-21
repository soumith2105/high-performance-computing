import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

def read_csv_file(file_path, columns):
    return pd.read_csv(file_path, header=None, names=columns)

def most_problematic_pollutant(thread_count=1):
    data_path = '../../../data/AirNow Fires/data/'
    columns = ['Latitude', 'Longitude', 'UTC', 'Parameter', 'Concentration', 'Unit',
               'Raw Concentration', 'AQI', 'Category', 'Site Name', 'Site Agency',
               'AQS ID', 'Full AQS ID']

    csv_files = [os.path.join(root, file)
                 for root, _, files in os.walk(data_path)
                 for file in files if file.endswith('.csv')]

    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        dataframes = list(executor.map(lambda file: read_csv_file(file, columns), csv_files))

    full_data = pd.concat(dataframes, ignore_index=True)
    full_data['AQI'] = pd.to_numeric(full_data['AQI'])
    full_data = full_data.dropna(subset=['AQI'])

    grouped_data = full_data.groupby(['Latitude', 'Longitude', 'Parameter'])['AQI'].mean().reset_index()
    most_problematic = grouped_data.loc[grouped_data.groupby(['Latitude', 'Longitude'])['AQI'].idxmax()]

    print(most_problematic)

import time
start = time.time()
most_problematic_pollutant(6)
print(f"Execution Time: {time.time() - start}")
