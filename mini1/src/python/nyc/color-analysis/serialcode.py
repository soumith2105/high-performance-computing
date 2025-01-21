import csv
import time

filename = '../../../data/nyc/parkingviolations/Parking_Violations_Issued_-_Fiscal_Year_2022.csv'

def color_analysis():
    color_counts = {}

    with open(filename, 'r') as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            color = row['Vehicle Body Type'].strip().upper()
            if color:
                if color in color_counts:
                    color_counts[color] += 1
                else:
                    color_counts[color] = 1

    return color_counts

start_time = time.time()

color_counts = color_analysis()

# Sort colors by count in descending order
sorted_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)

# Print results
print("Vehicle Color Analysis:")
for color, count in sorted_colors:
    print(f"{color}: {count}")

print(sorted_colors[0:5], " get most tickets")
end_time = time.time()
execution_time = end_time - start_time

print(f"\nExecution time: {execution_time:.4f} seconds")
