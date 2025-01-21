import csv
import time
import threading

filename = '../../../data/worldbank population/API_SP.POP.TOTL_DS2_en_csv_v2_3401680/API_SP.POP.TOTL_DS2_en_csv_v2_3401680.csv'
num_threads = 10  # You can change this value to use a different number of threads

def read_population_data():
    data = {
        "country_names": [],
        "country_codes": [],
        "indicator_names": [],
        "indicator_codes": [],
        "years": [],
        "populations": []
    }
    with open(filename, newline='', encoding='utf-8-sig') as fo:
        csv_reader = csv.reader(fo)

        # Skip the first 4 lines
        for _ in range(4):
            next(csv_reader)

        # Read the header row
        headers = next(csv_reader)
        data["years"] = [year for year in headers[4:] if year.strip()]

        # Read the actual data
        for row in csv_reader:
            data["country_names"].append(row[0])
            data["country_codes"].append(row[1])
            data["indicator_names"].append(row[2])
            data["indicator_codes"].append(row[3])
            data["populations"].append([float(value) if value else 0 for value in row[4:]])
    return data

def process_data(data, start_index, end_index, results, index):
    total_population_by_year = {year: 0 for year in data["years"]}
    for i in range(start_index, end_index):
        for j, year in enumerate(data["years"]):
            try:
                if 1960 <= int(year) <= 2023:
                    total_population_by_year[year] += int(data["populations"][i][j])
            except ValueError:
                continue
    results[index] = total_population_by_year

def main():
    start_time = time.time()

    population_data = read_population_data()

    # Split the data into chunks for each thread
    chunk_size = len(population_data["country_names"]) // num_threads
    start_indices = list(range(0, len(population_data["country_names"]), chunk_size))
    end_indices = start_indices[1:] + [len(population_data["country_names"])]

    # Create threads
    threads = []
    results = [None] * num_threads
    for i in range(num_threads):
        thread = threading.Thread(target=process_data, args=(population_data, start_indices[i], end_indices[i], results, i))
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
