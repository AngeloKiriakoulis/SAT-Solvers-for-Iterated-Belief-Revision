from set import Set
from marco import Marco
from pysat.solvers import Glucose4

class BeliefRevision:
  """This class represents an algorithm designed to perform belief revision in a knowledge base.
  Belief revision is the process of updating or modifying a set of beliefs (knowledge base) based
  on new information or evidence."""

  def __init__(self):
    #The initial set of beliefs or knowledge base.
    self.beliefs = Set("sets/kb.cnf")
    #The new information or evidence to be incorporated into the knowledge base.
    self.info = Set("sets/info.cnf")
    #The integrity constraints of a domain
    self.integrityConstraints = Set("sets/ic.cnf")
    #The given query that need to be checked 
    self.query = Set("sets/query.cnf")

    self.K_IC = self.beliefs + self.integrityConstraints
    self.f_IC = self.info + self.integrityConstraints

  def solve_SAT(self, cnf):
    worlds = []
    solver = Glucose4()
    for clause in cnf:
      solver.add_clause(clause)
    flag = solver.solve()
    for world in solver.enum_models():
      worlds.append(world)
    solver.delete()
    return flag, worlds

  def implies(self, source, query):
    #Need to check cases where query are sub-lists of the source
    query_flag, query_worlds = self.solve_SAT(query)
    print(source, query)
    solver = Glucose4()
    for clause in source:
      solver.add_clause(clause)
    for q in query_worlds:
      if not solver.solve(assumptions=q): return False
    return True
  
  def query_answering(self):
    f_IC_flag, f_IC_worlds = self.solve_SAT(self.f_IC.elements)
    K_IC_flag, K_IC_worlds = self.solve_SAT(self.K_IC.elements)
    if not f_IC_flag: return True
    if not K_IC_flag: return self.implies(self.f_IC.elements, self.query.elements)
    if len(self.query.language.intersection(self.f_IC.language)) == 0:
      print(1)
      if len(self.query.language.intersection(self.K_IC.language)) == 0: 
        print(2)
        return False
      else: 
        print(3)
        return self.implies(self.K_IC.elements, self.query.elements)
    self.revise()

  def revise(self):
    #Need to check if f_IC or K_IC are inconsistent first
    f_IC_flag, f_IC_worlds = self.solve_SAT(self.f_IC.elements)
    K_IC_flag, K_IC_worlds = self.solve_SAT(self.K_IC.elements)
    if not f_IC_flag:
      K_R_worlds = []
    if not K_IC_flag:
      K_R_worlds = f_IC_worlds
    #Need to find the "effective" portion of f_IC

    #Need to find the Minimum Unsatisfiable or Maximum Satisfiable subsets.
    #Need to check if the constraint initial belief set and the effective portion is consistent
    #If it is, the revised belief set is the intersection of their worlds. If not, distance between worlds need to be calculated.
    cnf = self.K_IC + self.f_IC
    print(cnf.elements)
    flag, worlds = self.solve_SAT(cnf.elements)
    if not flag:
      Marco(cnf.elements)
    else: print(worlds)

br = BeliefRevision()
print(br.query_answering())