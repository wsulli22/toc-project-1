#WHAT THIS FILE DOES:
# 1. READS CSV FILE
# 2. EXTRACT RELEVANT INFO FROM EACH LINE
# 3. CALL DPLL ALGORITHM ON EACH PROBLEM
# 4. USES BACKTRACKING TO FIND ASSIGNMENT VALS IF SATISFIABLE
# 5. OUTPUT RESULTS TO CSV FILE

import csv
from dpll_algorithm_wsulli22 import dpll, find_satisfying_assignment
import sys
import shutil

# TAKE IN CSV FROM COMMAND LINE
if len(sys.argv) != 2:
    print("Usage: python algorithm.py [csv file]")
    sys.exit(1)
input_file = sys.argv[1]
output_file = 'data_generated_output_from_' + input_file.split('.')[0] + '_wsulli22.csv'

data = {} # DICTIONARY TO STORE PROBLEMS

print("\n")
# PROCESS THE CSV FILE
def process_csv(input_file):
    current_problem = None
    with open(input_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or all(cell.strip() == '' for cell in row): continue

            # EXTRACT IMPORTANT INFO FROM COMMENT LINE
            if row[0] == 'c':                                       
                if current_problem:
                    data[current_problem['id']] = current_problem
                current_problem = {
                    'id': int(row[1]),
                    'wff': []
                }
            
            # EXTRACT IMPORTANT INFO FROM PROBLEM LINE
            elif row[0] == 'p':                                   
                current_problem['num_variables'] = int(row[2])
                current_problem['num_clauses'] = int(row[3])
            
            # EXTRACT IMPORTANT INFO FROM CLAUSE LINE
            else:
                valid_entries = [x for x in row if x.strip().isdigit() 
                                 or (x.strip().startswith('-') and x.strip()[1:].isdigit())]
                clause = [int(x) for x in valid_entries]
                if clause: current_problem['wff'].append(clause[:-1])  #REMOVE TRAILING 0

    # ADD LAST PROBLEM TO DATA
    if current_problem: data[current_problem['id']] = current_problem
    return data
data = process_csv(input_file)

# COMPARE OUTPUTS TO EXPECTED OUTPUT
satisfiable_count = 0
total_problems = len(data)

with open(output_file, 'w') as f:
    for problem_id, problem_data in data.items():
        outcome, completion_time = dpll(problem_data['wff'])
        problem_data['outcome'] = outcome
        problem_data['completion_time'] = completion_time
        
        # IF SATISFIABLE, FIND ASSIGNMENT
        if outcome == 'S':
            satisfiable_count += 1
            assignment = find_satisfying_assignment(problem_data['wff'], problem_data['num_variables'])
            problem_data['assignment'] = assignment
        else: problem_data['assignment'] = []

        # WRITE OUTPUTS TO OUTPUT FILE
        output_line = f"{problem_id},{problem_data['num_variables']},{problem_data['num_clauses']},{problem_data['completion_time']},{problem_data['outcome']}\n"
        print(output_line.strip()) 
        f.write(output_line)

    #CALC ACCURACY 
    accuracy = (satisfiable_count / total_problems) * 100
    print("-------------------")
    print(f"Satisfiable: {accuracy:.2f}%")

#MAKE A COPY OF THE OUTPUT FILE (B/C DIRECTIONS SAY WANT A "DATA" FILE)
output_file_out = 'output_generated_output_from_' + input_file.split('.')[0] + '_wsulli22.csv'
shutil.copy2(output_file, output_file_out)

print(f"\nOutput saved to {output_file}\n")
print(f"And copy saved as {output_file_out}\n")
