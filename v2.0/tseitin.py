import numpy as np
from revision.negation import negate

class Tseitin():
  def __init__(self,clauses,max) -> None:
    self.transformation = list()
    self.max_literal = max
    self.aux_var_dict = dict()
    for component in clauses:
      self.aux_vars = list()
      result = self.to_cnf(component)
      for clause in result:
        self.transformation.append(clause)
      self.max_literal += 1
      self.aux_var_dict[self.max_literal] = self.aux_vars
    aux_result = self.aux_part()
    for result in aux_result:
      self.transformation.append(result)
    
    # for aux_var in range(len(clauses)):
    #   self.max_literal+=1
    #   self.aux_vars.append(self.max_literal)
    # self.transformation.append(self.aux_vars)
      
  def to_cnf(self,component):
    literals = set()

    for clause in component:
      literals.update((abs(l) for l in clause))
    
    for clause in component:
      clause_copy = list(sorted(clause, key=abs))
      clause = list(sorted(clause, key=abs))
      next_clause = list()
      self.max_literal += 1
      yield [*clause, -self.max_literal]
      for i in range(0,len(clause)):
        next_clause.append(clause[i])
      next_clause.append(self.max_literal) 
      clause = next_clause
      for i in clause_copy:
        yield [-i,clause[-1]]
      yield [self.max_literal]
      self.aux_vars.append(self.max_literal)

  def aux_part(self):
    for item in self.aux_var_dict.items():
      aux = item[0]
      clauses = item[1]
      for clause in clauses:
        yield [clause,-aux]
      yield [-i for i in clauses] + [aux]
      yield [aux]
    aux = self.max_literal + 1
    or_clauses = list(self.aux_var_dict.keys())
    yield [*or_clauses]
# ts = Tseitin([[[1,2],[3]],[[4,5],[6,7,8]]],8)
# print(ts.transformation)
# ts = Tseitin([[[3,4]],[[-5]]],5)
# print(ts.transformation)
    