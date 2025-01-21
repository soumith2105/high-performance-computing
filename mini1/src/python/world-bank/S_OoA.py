import csv
import time

filename = '../../../data/worldbank population/API_SP.POP.TOTL_DS2_en_csv_v2_3401680/API_SP.POP.TOTL_DS2_en_csv_v2_3401680.csv'
def read_population_data_as_object_of_arrays():
    data = {
        'Country Name': [],
        'Country Code': [],
        'Indicator Name': [],
        'Indicator Code': [],
        'Years': {}
    }
    with open(filename, newline='', encoding='utf-8-sig') as fo:
        csv_reader = csv.reader(fo)

        # Skip the first 4 lines
        for _ in range(4):
            next(csv_reader)

        # Read the header row
        headers = next(csv_reader)
        years = headers[4:]

        # Initialize Years dictionary
        for year in years:
            if year.strip():
                data['Years'][year] = []

        # Read the actual data
        for row in csv_reader:
            data['Country Name'].append(row[0])
            data['Country Code'].append(row[1])
            data['Indicator Name'].append(row[2])
            data['Indicator Code'].append(row[3])

            for year, value in zip(years, row[4:]):
                if year.strip():
                    data['Years'][year].append(value if value else None)
    return data

start_time = time.time()

population_data = read_population_data_as_object_of_arrays()

total_population_by_year = {}
for year, populations in population_data['Years'].items():
    try:
        if 1960 <= int(year) <= 2023:
            total = sum(int(float(pop)) for pop in populations if pop and pop != '')
            total_population_by_year[year] = total
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
