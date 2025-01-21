import csv
import time
import numpy as np
from numba import njit

filename = '../../../data/nyc/parkingviolations/Parking_Violations_Issued_-_Fiscal_Year_2022.csv'

def read_parking_data():
    plate_ids = []

    with open(filename, 'r') as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            plate_id = row['Plate ID']
            if plate_id != 'BLANKPLATE':
                plate_ids.append(plate_id)

    return np.array(plate_ids)

@njit
def count_violations(plate_ids, unique_plates):
    counts = np.zeros(len(unique_plates), dtype=np.int64)
    for plate_id in plate_ids:
        idx = np.searchsorted(unique_plates, plate_id)
        if unique_plates[idx] == plate_id:
            counts[idx] += 1
    return counts

def main():
    start_time = time.time()

    plate_ids = read_parking_data()
    unique_plates = np.unique(plate_ids)

    violation_counts = count_violations(plate_ids, unique_plates)
    repeat_offenders = violation_counts[violation_counts > 1]
    repeat_offender_plates = unique_plates[violation_counts > 1]

    # Sort repeat offenders by number of violations in descending order
    sorted_indices = np.argsort(repeat_offenders)[::-1]
    sorted_offenders = list(zip(repeat_offender_plates[sorted_indices], repeat_offenders[sorted_indices]))

    # Print results
    print("Repeat Offenders (Plate ID: Number of Violations):")
    for plate_id, violations in sorted_offenders[:20]:  # Print top 20 repeat offenders
        print(f"{plate_id}: {violations}")

    print(f"\nTotal number of repeat offenders: {len(repeat_offenders)}")

    execution_time = time.time() - start_time
    print(f"\nExecution time: {execution_time:.4f} seconds")

if __name__ == "__main__":
    main()
