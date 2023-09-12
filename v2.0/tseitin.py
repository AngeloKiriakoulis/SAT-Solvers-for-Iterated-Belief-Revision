class Tseitin():
  def __init__(self,clauses) -> None:
    self.transformation = list()
    self.max_literal = 100
    for component in clauses:
      result = self.to_cnf(component)
      for clause in result:
        self.transformation.append(clause)
    

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

	
# l1 = Tseitin([[25,82,3], [35], [-55, -68], [-60, 93], [-29, 69], [36, -42], [16, -33], [63, 92], [-63, -89], [34, -55]]).transformation
# print("L1: ", *l1, '\n')

# l2 = Tseitin([[35, 37], [20, -69], [-55, -68], [76, 92], [49, 74], [-60, 93], [-5, 10], [-29, 69], [72, 86], [36, -42], [-63, -89], [26, -96]]).transformation
# print("L2: ", *l2, '\n')

# l3 = Tseitin([[35, 95], [25, 82], [56, 98], [14, -87], [-21, 96], [-78, -83], [-17, 90], [-71, 93], [16, -33], [63, 92], [34, -55]]).transformation
# print("L3: ", *l3, '\n')

# l3 = Tseitin([[[98,99,35, 95], [25, 82], [56, 98], [14, -87], [-21, 96], [-78, -83], [-17, 90], [-71, 93], [16, -33], [63, 92], [34, -55]],[[35, 37], [20, -69], [-55, -68], [76, 92], [49, 74], [-60, 93], [-5, 10], [-29, 69], [72, 86], [36, -42], [-63, -89], [26, -96]],[[25,82,3], [35], [-55, -68], [-60, 93], [-29, 69], [36, -42], [16, -33], [63, 92], [-63, -89], [34, -55]]]).transformation
