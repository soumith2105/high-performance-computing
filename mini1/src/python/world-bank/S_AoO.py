import csv
import time

filename = '../../../data/worldbank population/API_SP.POP.TOTL_DS2_en_csv_v2_3401680/API_SP.POP.TOTL_DS2_en_csv_v2_3401680.csv'

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
                "Years": {}
            }
            for year, value in zip(headers[4:], row[4:]):
                if year.strip():  # Only add non-empty year keys
                    country_data["Years"][year] = value if value else None

            data.append(country_data)
    return data

start_time = time.time()

population_data = read_population_data()

total_population_by_year = {}
for country in population_data:
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

# Create a sorted list of total populations by year
sorted_total_population = sorted(total_population_by_year.items(), key=lambda x: int(x[0]))

# Print the results
print("Total population by year:")
for year, population in sorted_total_population:
    print(f"{year}: {population:,}")

execution_time = time.time() - start_time
print(f"\nExecution time: {execution_time:.10f} seconds")
