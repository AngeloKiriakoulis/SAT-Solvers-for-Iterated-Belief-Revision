from pysat.solvers import Glucose3

class Marco:
  def __init__(self,cnf) -> None:
    self.cnf = cnf
    self.Map=[[i+1 for i in range(len(self.cnf))]]
    self.mus_list = [] 
    self.mss_list = []
    self.find_subsets()
  
  def shrink(self, seed):
    for c in seed[:]:
      seed_copy = seed.copy()
      seed.remove(c)
      solver = Glucose3()
      for clause in seed:
        solver.add_clause(clause)
      if solver.solve():
        seed = seed_copy
    solver.delete()
    return seed
  
  def grow(self, seed):
    for c in self.cnf:
      while True:
        if c not in seed:
          solver = Glucose3()
          for clause in seed:
            solver.add_clause(clause)
          solver.add_clause(c)
          if solver.solve():
            seed += [c]
          else: break
        else:break
        solver.delete()
    return seed
  
  def block_up(self, mus):
    block_up_list = []
    for i in mus:
      block_up_list.append(-self.cnf.index(i) - 1)
    return block_up_list
  
  def block_down(self, mss):
    block_down_list = []
    for i in self.cnf:
      if i not in mss:
        block_down_list.append(self.cnf.index(i) + 1)
    return block_down_list

  def get_unexplored(self, Map):
    solver = Glucose3()
    highest_num_positives = 0
    lists_with_highest_num_positives = []
    f = []
    for clause in Map:
      solver.add_clause(clause)
    solver.solve()
    for formula in solver.enum_models():
      num_positives = len(list(filter(lambda x: x > 0, formula)))
      if num_positives > highest_num_positives:
        highest_num_positives = num_positives
        lists_with_highest_num_positives = [formula]
      elif num_positives == highest_num_positives:
        lists_with_highest_num_positives.append(formula)
      break
    for formula in lists_with_highest_num_positives:
      s = []
      for i in formula:
        if i > 0: s.append(self.cnf[i - 1])
      f.append(s)
    return f
  
  def is_satisfiable(self, problem):
    solver = Glucose3()
    for clause in problem:
      solver.add_clause(clause)
    flag = solver.solve()
    return flag
  
  def find_subsets(self):
    while True:
      seed_list = self.get_unexplored(self.Map)
      for seed in seed_list:
        if self.is_satisfiable(seed):
          mss = self.grow(seed)
          if mss not in self.mss_list:
            self.mss_list.append(mss)
            self.Map.append(self.block_down(mss))
        else:
          mus = self.shrink(seed)
          if mus not in self.mus_list:
            self.mus_list.append(mus)
            self.Map.append(self.block_up(mus))
        seed_list.remove(seed)
      if not self.is_satisfiable(self.Map):
        break
    print("Maximum Satisfiable Subsets:")
    for i in self.mss_list:
      print(i)
    print("Minimum Unsatisfiable Subsets:")
    for i in self.mus_list:
      print(i)


cnf = [[1],[2],[-1,-2]]
marco = Marco(cnf)