import csv
import time

filename = '../../../data/nyc/parkingviolations/Parking_Violations_Issued_-_Fiscal_Year_2022.csv'

def calculate_repeat_offenders():
    data = {
        'Plate ID': [],
        'Violation Count': []
    }

    violations = {}

    with open(filename, 'r') as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            plate_id = row['Plate ID']
            if plate_id != 'BLANKPLATE':  # Exclude BLANKPLATE
                violations[plate_id] = violations.get(plate_id, 0) + 1

    for plate_id, count in violations.items():
        if count > 1:
            data['Plate ID'].append(plate_id)
            data['Violation Count'].append(count)

    return data

start_time = time.time()

repeat_offenders = calculate_repeat_offenders()

# Sort repeat offenders by number of violations in descending order
sorted_indices = sorted(range(len(repeat_offenders['Violation Count'])),
                        key=lambda k: repeat_offenders['Violation Count'][k],
                        reverse=True)

# Print results
print("Repeat Offenders (Plate ID: Number of Violations):")
for i in sorted_indices[:20]:  # Print top 20 repeat offenders
    print(f"{repeat_offenders['Plate ID'][i]}: {repeat_offenders['Violation Count'][i]}")

print(f"\nTotal number of repeat offenders: {len(repeat_offenders['Plate ID'])}")

end_time = time.time()
execution_time = end_time - start_time

print(f"\nExecution time: {execution_time:.4f} seconds")
