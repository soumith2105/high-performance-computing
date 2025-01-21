import csv
import time
import concurrent.futures
from collections import defaultdict

filename = '../../../data/nyc/parkingviolations/Parking_Violations_Issued_-_Fiscal_Year_2022.csv'  # Replace with your actual file name

def process_batch(rows):
    """Process a batch of rows to count plate violations."""
    plate_violations = defaultdict(int)

    for row in rows:
        plate_id = row['Plate ID']
        if plate_id != 'BLANKPLATE':  # Exclude BLANKPLATE
            plate_violations[plate_id] += 1

    return plate_violations

def calculate_repeat_offenders():
    """Calculate repeat offenders using multithreading."""
    plate_violations = defaultdict(int)
    batch_size = 100000  # Define the size of each batch

    with open(filename, 'r') as file:
        csv_reader = csv.DictReader(file)

        # Create a list to hold batches
        batches = []
        current_batch = []

        # Read the CSV and create batches
        for row in csv_reader:
            current_batch.append(row)
            if len(current_batch) >= batch_size:
                batches.append(current_batch)
                current_batch = []

        # Add any remaining rows as the last batch
        if current_batch:
            batches.append(current_batch)

    # Process batches in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_batch, batch) for batch in batches]

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            for plate_id, count in result.items():
                plate_violations[plate_id] += count

    # Filter repeat offenders
    repeat_offenders = {plate: count for plate, count in plate_violations.items() if count > 1}
    return repeat_offenders

# Measure execution time
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
