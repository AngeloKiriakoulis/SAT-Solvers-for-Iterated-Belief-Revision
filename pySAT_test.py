from pysat.solvers import Glucose3

# Create a Glucose3 SAT solver instance
solver = Glucose3()

# Define the knowledge base and new evidence as lists of clauses
kb = [[1, -2], [-1, 3], [-3, 4]]
evidence_1 = [[1], [2, -3], [-3]]

#ToDo -> Preordering in propositional atoms needed

#ToDo -> Iterated revision needs new evidence after each revision

# Add the clauses to the solver
for clause in kb + evidence_1:
    solver.add_clause(clause)

# Check if the conjunction of the knowledge base and evidence is satisfiable
is_sat = solver.solve()

if is_sat:
    print("The evidence is consistent with the knowledge base.")
    for model in solver.enum_models():
      print(model)
else:
    print("The evidence contradicts the knowledge base.")
    #ToDo -> Start implementing Revision techniques
