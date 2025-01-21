import time
import numpy as np
import pandas as pd

filename = '../../../data/worldbank population/API_SP.POP.TOTL_DS2_en_csv_v2_3401680/API_SP.POP.TOTL_DS2_en_csv_v2_3401680.csv'

def read_population_data():
    # Read CSV file using pandas, skipping the first 4 rows
    df = pd.read_csv(filename, skiprows=4)

    # Extract years and convert to integers, filtering out non-numeric columns
    year_columns = [col for col in df.columns[4:] if col.isdigit()]
    years = np.array(year_columns, dtype=int)

    # Convert population data to a 2D numpy array, using only the year columns
    population_data = df[year_columns].values.astype(np.float64)

    return years, population_data

def main():
    start_time = time.time()

    years, population_data = read_population_data()

    # Filter years between 1960 and 2023
    mask = (years >= 1960) & (years <= 2023)
    years = years[mask]
    population_data = population_data[:, mask]

    # Calculate total population for each year
    total_population = np.nansum(population_data, axis=0)

    # Create a sorted list of total populations by year
    sorted_total_population = sorted(zip(years, total_population))

    # Print the results
    print("Total population by year:")
    for year, population in sorted_total_population:
        print(f"{year}: {int(population):,}")

    execution_time = time.time() - start_time
    print(f"\nExecution time: {execution_time:.10f} seconds")

if __name__ == "__main__":
    main()
