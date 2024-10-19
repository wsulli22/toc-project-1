import sys
import csv

# READ CSV FILE
def read_csv(file_path):
    data = {}
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 5:
                problem_id, _, _, _, outcome = row[:5]  # EXTRACT PROBLEM ID AND OUTCOME
                data[int(problem_id)] = outcome
    return data

# COMPARE OUTPUTS
def compare_outputs(generated_file, expected_file):
    generated_data = read_csv(generated_file)
    expected_data = read_csv(expected_file)

    correct_count = 0
    total_count = 0

    # PRINT COMPARISION RESULTS
    print("\nCOMPARISON RESULTS:\n")
    for problem_id in generated_data:
        generated_outcome = generated_data[problem_id]
        expected_outcome = expected_data.get(problem_id)

        if expected_outcome:
            total_count += 1
            if generated_outcome == expected_outcome:
                print(f"{problem_id}: Correct   ({expected_outcome})")
                correct_count += 1
            else:
                print(f"{problem_id}: Incorrect ({expected_outcome} expected, got {generated_outcome})")
        else:
            print(f"{problem_id}: No expected outcome to compare with")
            print("[further comparison stopped]")
            break

    # CALC ACCURACY 
    accuracy = (correct_count / total_count) * 100 if total_count > 0 else 0
    print("------------------------------------------")
    print(f"Accuracy: {accuracy:.2f}%\n")

if len(sys.argv) != 3:
    print("Usage: python check.py [generated] [expected]")
    sys.exit(1)

generated_file = sys.argv[1]
expected_file = sys.argv[2]

compare_outputs(generated_file, expected_file)
