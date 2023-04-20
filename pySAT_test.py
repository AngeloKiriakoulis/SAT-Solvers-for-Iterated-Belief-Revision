from pysat.solvers import Glucose3
from belief_set import BeliefSet, Evidences

# Create a Glucose3 SAT solver instance
solver = Glucose3()

# Check if the conjunction of the knowledge base and evidence is satisfiable
def check() -> None:
    is_sat = solver.solve()

    if is_sat:
        print("The evidence is consistent with the knowledge base.")
        for model in solver.enum_models():
            print(model)
    else:
        print("The evidence contradicts the knowledge base.")
        #ToDo -> Start implementing Revision techniques

# Define the knowledge base and new evidence as lists of clauses
kb = [[1, -2], [-1, 3], [-3, 4]]

#ToDo -> Iterated revision needs new evidence after each revision

# Define the new evidence for each revision step
evidence = [
    [1, 2],     # First revision step
    [-2, 3],    # Second revision step
    [4],        # Third revision step
    [-1, -3],   # Fourth revision step
    [5]         # Fifth revision step
]

#ToDo -> Preordering in propositional atoms needed

# Add the clauses to the solver
for clause in kb + [_ for _ in evidence]:
    solver.add_clause(clause)
    check()

