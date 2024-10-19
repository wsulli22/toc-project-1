# THE ACTUAL DPLL ALGORITHM THAT GETS CALLED IN THE IMPLENTATION FILE

#BASED OFF THE INFO ABOUT THE ALGORITHM FROM THE FOLLOWING SOURCES:

#https://en.wikipedia.org/wiki/DPLL_algorithm
#https://stackoverflow.com/questions/12547160/how-does-the-dpll-algorithm-work
#https://cs.stackexchange.com/questions/10932/understanding-dpll-algorithm
#https://csci1710.github.io/book/chapters/solvers/dpll.html

# HOW THE DPLL WORKS:
# 1 - CHECK FOR EMPTY FORMULA (TRUE) OR EMPTY CLAUSE (FALSE)
# 2 - APPLY UNIT PROPAGATION IF POSSIBLE
# 3 - ELIMINATE PURE LITERALS IF PRESENT
# 4 - BRANCH ON A CHOSEN LITERAL, TRYING BOTH ASSIGNMENTS
# 5 - RETURN TRUE IF SATISFIABLE, FALSE OTHERWISE
 
import time

# MAIN DPLL ALGORITHM: TAKES IN A WFF AND RETURNS OUTCOME & TIME TO COMPLETE
def dpll(wff):
    start_time = time.time()
    outcome = dpll_recursive(wff)
    end_time = time.time()
    completion_time = int((end_time - start_time) * 1000000)  
    result = "S" if outcome else "U"
    return result, completion_time

def dpll_recursive(wff): 
    # CHECK EMPTIES AND RETURN ACCORDINGLY
    if not wff: return True                              # IF EMPTY = SATISFIABLE
    if any(not clause for clause in wff): return False   # IF CLAUSE EMPTY = UNSATISFIABLE

    # UNIT PROPAGATION
    for clause in wff:
        if len(clause) == 1: return dpll_recursive(assign_value(wff, clause[0]))

    # PURE LITERAL ELIMINATION
    pure_literal = find_pure_literal(wff)
    if pure_literal: return dpll_recursive(assign_value(wff, pure_literal))

    # SELECT FIRST LITERAL OF FIRST CLAUSE TO BRANCH ON
    branch_literal = abs(wff[0][0]) 
    return dpll_recursive(assign_value(wff, branch_literal)) or dpll_recursive(assign_value(wff, -branch_literal))

# ASSIGN VALUE TO LITERAL AND RETURN THE UDPATED WFF
def assign_value(wff, literal):
    updated_wff = [clause for clause in wff if literal not in clause and -literal not in clause]  # REMOVE CLAUSES WITH LITERAL AND -LITERAL
    updated_wff += [[l for l in clause if l != -literal] for clause in wff if -literal in clause] # REMOVE -LITERAL FROM  CLAUSES WITH -LITERAL
    return updated_wff

# FIND LITERALS THAT ARE PRESENT IN ALL CLAUSES AND RETURN THEM IF PRESENT
def find_pure_literal(wff):
    literals = set(abs(lit) for clause in wff for lit in clause)        # GET ALL LITERALS IN WFF
    for literal in literals:
        if all(literal in clause or -literal not in clause for clause in wff):  # IF LITERAL IS PRESENT IN ALL CLAUSES
            return literal
        if all(-literal in clause or literal not in clause for clause in wff):  # IF -LITERAL IS PRESENT IN ALL CLAUSES
            return -literal
    return None

# FIND ASSIGNMENT TO MAKE IT SATISFIABLE
def find_satisfying_assignment(wff, num_vars):
    assignment = []
    for i in range(1, num_vars + 1):
        if dpll_recursive(assign_value(wff, i)): assignment.append(1)
        else: assignment.append(0)
    return assignment
