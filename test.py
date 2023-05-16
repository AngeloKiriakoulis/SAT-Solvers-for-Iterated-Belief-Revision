from set import Set
from marco import Marco
from pysat.solvers import Glucose4

class BeliefRevision:
    def __init__(self):
      self.beliefs = Set("sets/kb.cnf")
      self.info = Set("sets/info.cnf")
      self.integrityConstraints = Set("sets/ic.cnf")
      self.query = Set("sets/query.cnf")

      self.K_IC_elements, self.K_IC_language = self.beliefs + self.integrityConstraints
      self.f_IC_elements, self.f_IC_language = self.info + self.integrityConstraints

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

    def implies(self, worlds, query):
      pass

    def query_answering(self):
      flag_f_IC, worlds_f_IC = self.solve_SAT(self.f_IC_elements)
      flag_K_IC, worlds_K_IC = self.solve_SAT(self.K_IC_elements)
      if not flag_f_IC: return True
      if not flag_K_IC:
        return self.implies(worlds_f_IC, self.query)
      if self.query.language.intersection(self.f_IC_language) is None:
        if self.query.language.intersection(self.K_IC_language) is None: return False
        else:
          return self.implies(worlds_K_IC, self.query)
      #BELIEF REVISON to continue
        
    def revise(self):
      #Need to check if f_IC or K_IC are inconsistent first

      cnf = self.K_IC_elements + self.f_IC_elements
      res = []
      [res.append(x) for x in cnf if x not in res] #Remove Duplicates
      cnf = res.copy()
      print(cnf)
      flag, worlds = self.solve_SAT(cnf)
      if not flag:
        Marco(self.K_IC_elements + self.f_IC_elements)
      else: print(worlds)

br = BeliefRevision()
print(br.query_answering())
br.revise()