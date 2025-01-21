import csv
import time
import threading

filename = '../../../data/worldbank population/API_SP.POP.TOTL_DS2_en_csv_v2_3401680/API_SP.POP.TOTL_DS2_en_csv_v2_3401680.csv'
num_threads = 8  # You can change this value to use a different number of threads

def read_population_data():
    data = []
    with open(filename, newline='', encoding='utf-8-sig') as fo:
        csv_reader = csv.reader(fo)

        # Skip the first 4 lines
        for _ in range(4):
            next(csv_reader)

        # Read the header row
        headers = next(csv_reader)

        # Read the actual data
        for row in csv_reader:
            country_data = {
                "Country Name": row[0],
                "Country Code": row[1],
                "Indicator Name": row[2],
                "Indicator Code": row[3],
                "Years": {year: value for year, value in zip(headers[4:], row[4:]) if year.strip()}
            }
            data.append(country_data)
    return data

def process_data(data_chunk, results, index):
    total_population_by_year = {}
    for country in data_chunk:
        for year, population in country['Years'].items():
            try:
                if 1960 <= int(year) <= 2023:
                    if year not in total_population_by_year:
                        total_population_by_year[year] = 0
                    if population and population != '':
                        total_population_by_year[year] += int(float(population))
            except ValueError:
                # Skip years that can't be converted to integers
                continue
    results[index] = total_population_by_year

def main():
    start_time = time.time()

    population_data = read_population_data()

    # Split the data into chunks for each thread
    chunk_size = len(population_data) // num_threads
    data_chunks = [population_data[i:i + chunk_size] for i in range(0, len(population_data), chunk_size)]

    # Create threads
    threads = []
    results = [None] * num_threads
    for i in range(num_threads):
        thread = threading.Thread(target=process_data, args=(data_chunks[i], results, i))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Combine results from all threads
    total_population_by_year = {}
    for partial_result in results:
        for year, population in partial_result.items():
            if year not in total_population_by_year:
                total_population_by_year[year] = 0
            total_population_by_year[year] += population

    # Create a sorted list of total populations by year
    sorted_total_population = sorted(total_population_by_year.items(), key=lambda x: int(x[0]))

    # Print the results
    print("Total population by year:")
    for year, population in sorted_total_population:
        print(f"{year}: {population:,}")

    execution_time = time.time() - start_time
    print(f"\nExecution time: {execution_time:.10f} seconds")
    print(f"Number of threads used: {num_threads}")

if __name__ == "__main__":
    main()
