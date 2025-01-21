import csv
import time

filename = '../../../data/nyc/parkingviolations/Parking_Violations_Issued_-_Fiscal_Year_2022.csv'

class ParkingViolation:
    def __init__(self, plate_id, violation_count):
        self.plate_id = plate_id
        self.violation_count = violation_count

def calculate_repeat_offenders():
    violations = {}

    with open(filename, 'r') as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            plate_id = row['Plate ID']
            if plate_id != 'BLANKPLATE':  # Exclude BLANKPLATE
                violations[plate_id] = violations.get(plate_id, 0) + 1

    repeat_offenders = [ParkingViolation(plate, count) for plate, count in violations.items() if count > 1]
    return repeat_offenders

start_time = time.time()

repeat_offenders = calculate_repeat_offenders()

# Sort repeat offenders by number of violations in descending order
sorted_offenders = sorted(repeat_offenders, key=lambda x: x.violation_count, reverse=True)

# Print results
print("Repeat Offenders (Plate ID: Number of Violations):")
for offender in sorted_offenders[:20]:  # Print top 20 repeat offenders
    print(f"{offender.plate_id}: {offender.violation_count}")

print(f"\nTotal number of repeat offenders: {len(repeat_offenders)}")

end_time = time.time()
execution_time = end_time - start_time

print(f"\nExecution time: {execution_time:.4f} seconds")
