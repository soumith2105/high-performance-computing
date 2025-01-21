import csv
import time
import numpy as np
from numba import njit

filename = '../../../../data/worldbank population/API_SP.POP.TOTL_DS2_en_csv_v2_3401680/API_SP.POP.TOTL_DS2_en_csv_v2_3401680.csv'

def read_population_data():
    years = []
    population_data = []
    with open(filename, newline='', encoding='utf-8-sig') as fo:
        csv_reader = csv.reader(fo)

        # Skip the first 4 lines
        for _ in range(4):
            next(csv_reader)

        # Read the header row
        headers = next(csv_reader)
        years = [int(year) for year in headers[4:] if year.strip() and year.isdigit()]

        # Read the actual data
        for row in csv_reader:
            population_data.append([float(value) if value.strip() else 0 for value in row[4:]])

    return np.array(years), np.array(population_data)

@njit
def calculate_total_population(population_data):
    return np.sum(population_data, axis=0)

start_time = time.time()

years, population_data = read_population_data()
total_population = calculate_total_population(population_data)

# Create a sorted list of total populations by year
sorted_total_population = sorted(zip(years, total_population))

# Print the results
print("Total population by year:")
for year, population in sorted_total_population:
    if 1960 <= year <= 2023:
        print(f"{year}: {int(population):,}")

execution_time = time.time() - start_time
print(f"\nExecution time: {execution_time:.10f} seconds")
