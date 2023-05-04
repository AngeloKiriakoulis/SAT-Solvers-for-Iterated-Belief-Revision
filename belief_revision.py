from pysat.formula import CNF
from pysat.solvers import Glucose4

class BeliefRevision:
    def __init__(self, initial_kb):
        self.initial_kb = initial_kb
        self.revised_kb = initial_kb.copy()
    
    # Function to convert a list of propositional clauses to CNF form
    def convert_to_cnf(self, clauses):
        cnf = CNF()
        for clause in clauses:
            cnf.append(clause)
        return cnf

    # Function to perform Iterated Belief Revision
    def belief_revision(self, new_info_list):
        for new_info in new_info_list:
            # Convert the revised KB and new information to CNF
            cnf = self.convert_to_cnf(self.revised_kb + new_info)
            # Solve the CNF formula using PySAT's Glucose4 solver
            with Glucose4(bootstrap_with=cnf.clauses) as solver:
                # If the formula is unsatisfiable, find the subset of the clauses in the formula which are actually responsible for the conflict and return the revised KB.
                # When a conflict is detected in the formula, it's often the case that only a small subset of the clauses in the formula are actually responsible for the conflict.
                # Extract the non-conflicting clauses from the belief-revision process.
                
                if not solver.solve():
                    conflicting_clauses = []
                    for clause in cnf.clauses:
                        for literal in clause:
                            if True:
                                conflicting_clauses.append(clause)
                    #print(conflicting_clauses)            
                    # if len(conflicting_clauses) == 0:
                    #     break
                    self.revised_kb = [clause for clause in self.revised_kb if clause not in conflicting_clauses]
                    continue
                #REVISION FUNCTION HERE

                # Otherwise, expand the initial knowlegde base with the new info.
                self.revised_kb = self.revised_kb + new_info
                print(self.revised_kb)

    # Function to check if a query stands in the revised knowledge base
    def check_query(self, query):
        cnf = self.convert_to_cnf(self.revised_kb + [query])
        with Glucose4(bootstrap_with=cnf.clauses) as solver:
            if solver.solve():
                return True
            else:
                return False


initial_kb = [[1, 2], [-1, 3], [-2, -3]]
new_info_list = [[[1]],[[2]]]
br_solver = BeliefRevision(initial_kb)
br_solver.belief_revision(new_info_list)