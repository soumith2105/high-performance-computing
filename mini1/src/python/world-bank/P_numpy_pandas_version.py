import time
import numpy as np
import pandas as pd
import threading
from queue import Queue

filename = '../../../data/worldbank population/API_SP.POP.TOTL_DS2_en_csv_v2_3401680/API_SP.POP.TOTL_DS2_en_csv_v2_3401680.csv'
num_threads = 10  # You can adjust this number based on your system's capabilities

def read_population_data():
    # Read CSV file using pandas, skipping the first 4 rows
    df = pd.read_csv(filename, skiprows=4)

    # Extract years and convert to integers, filtering out non-numeric columns
    year_columns = [col for col in df.columns[4:] if col.isdigit()]
    years = np.array(year_columns, dtype=int)

    # Convert population data to a 2D numpy array, using only the year columns
    population_data = df[year_columns].values.astype(np.float64)

    return years, population_data

def process_chunk(start, end, population_data, result_queue):
    chunk_sum = np.nansum(population_data[:, start:end], axis=0)
    result_queue.put((start, chunk_sum))

def main():
    start_time = time.time()

    years, population_data = read_population_data()

    # Filter years between 1960 and 2023
    mask = (years >= 1960) & (years <= 2023)
    years = years[mask]
    population_data = population_data[:, mask]

    # Split the data for threading
    chunk_size = len(years) // num_threads
    threads = []
    result_queue = Queue()

    # Create and start threads
    for i in range(num_threads):
        start = i * chunk_size
        end = start + chunk_size if i < num_threads - 1 else len(years)
        thread = threading.Thread(target=process_chunk, args=(start, end, population_data, result_queue))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Combine results from all threads
    total_population = np.zeros(len(years))
    while not result_queue.empty():
        start, chunk_sum = result_queue.get()
        end = start + len(chunk_sum)
        total_population[start:end] = chunk_sum

    # Create a sorted list of total populations by year
    sorted_total_population = sorted(zip(years, total_population))

    # Print the results
    print("Total population by year:")
    for year, population in sorted_total_population:
        print(f"{year}: {int(population):,}")

    execution_time = time.time() - start_time
    print(f"\nExecution time: {execution_time:.10f} seconds")
    print(f"Number of threads used: {num_threads}")

if __name__ == "__main__":
    main()
