import pandas as pd
import time
from multiprocessing import Pool
import numpy as np
import threading
from queue import Queue
import os

filename = '../../../data/nyc/parkingviolations/Parking_Violations_Issued_-_Fiscal_Year_2022.csv'

# Global variable for number of threads
NUM_THREADS = 10  # This is already defined and we'll keep it as is

def process_sub_chunk(sub_chunk, result_queue):
    counts = sub_chunk[sub_chunk['Plate ID'] != 'BLANKPLATE']['Plate ID'].value_counts()
    result_queue.put(counts)

def process_chunk(chunk):
    global NUM_THREADS
    # Split the chunk into smaller sub-chunks for threading
    sub_chunks = np.array_split(chunk, NUM_THREADS)

    threads = []
    result_queue = Queue()

    # Create and start threads
    for sub_chunk in sub_chunks:
        thread = threading.Thread(target=process_sub_chunk, args=(sub_chunk, result_queue))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Combine results from threads
    results = []
    while not result_queue.empty():
        results.append(result_queue.get())

    return pd.concat(results).groupby(level=0).sum()

def calculate_repeat_offenders(num_processes):
    # Read the CSV file in chunks
    chunks = pd.read_csv(filename, usecols=['Plate ID'], chunksize=1000000)

    # Process chunks in parallel using multiprocessing
    with Pool(num_processes) as pool:
        results = pool.map(process_chunk, chunks)

    # Combine results from all processes
    combined_counts = pd.concat(results).groupby(level=0).sum()

    # Filter repeat offenders
    repeat_offenders = combined_counts[combined_counts > 1]

    return repeat_offenders

if __name__ == "__main__":
    num_processes = os.cpu_count()  # This will use all available CPU cores

    start_time = time.time()

    repeat_offenders = calculate_repeat_offenders(num_processes)

    # Sort repeat offenders by number of violations in descending order
    sorted_offenders = repeat_offenders.sort_values(ascending=False)

    # Print results
    print("Repeat Offenders (Plate ID: Number of Violations):")
    for plate_id, violations in sorted_offenders.head(20).items():
        print(f"{plate_id}: {violations}")

    print(f"\nTotal number of repeat offenders: {len(repeat_offenders)}")

    end_time = time.time()
    execution_time = end_time - start_time

    print(f"\nExecution time: {execution_time:.4f} seconds")
    print(f"Number of processes used: {num_processes}")
    print(f"Number of threads per process: {NUM_THREADS}")
