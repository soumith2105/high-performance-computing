import csv
import time

filename = '../../../data/nyc/parkingviolations/Parking_Violations_Issued_-_Fiscal_Year_2022.csv'  # Replace with your actual file name

def calculate_repeat_offenders():
    plate_violations = {}

    with open(filename, 'r') as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            plate_id = row['Plate ID']
            if plate_id != 'BLANKPLATE':  # Exclude BLANKPLATE
                if plate_id in plate_violations:
                    plate_violations[plate_id] += 1
                else:
                    plate_violations[plate_id] = 1

    repeat_offenders = {plate: count for plate, count in plate_violations.items() if count > 1}
    return repeat_offenders

start_time = time.time()

repeat_offenders = calculate_repeat_offenders()

# Sort repeat offenders by number of violations in descending order
sorted_offenders = sorted(repeat_offenders.items(), key=lambda x: x[1], reverse=True)

# Print results
print("Repeat Offenders (Plate ID: Number of Violations):")
for plate_id, violations in sorted_offenders[:20]:  # Print top 20 repeat offenders
    print(f"{plate_id}: {violations}")

print(f"\nTotal number of repeat offenders: {len(repeat_offenders)}")

end_time = time.time()
execution_time = end_time - start_time

print(f"\nExecution time: {execution_time:.4f} seconds")
# Total number of repeat offenders: 2189069
