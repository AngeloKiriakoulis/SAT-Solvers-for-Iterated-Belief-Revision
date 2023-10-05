class Tseitin():
  """The class performs the Tseitin transformation on OR clauses."""
  def __init__(self, clauses, max) -> None:
    self.transformation = list()  # Initialize an empty list to store the transformed clauses.
    self.max_literal = max  # Initialize the maximum literal value.
    self.aux_var_dict = dict()  # Initialize a dictionary to store auxiliary variables and their associated clauses.

    for component in clauses:
      self.aux_vars = list()  # Initialize a list to store auxiliary variables for each component.
      result = self.to_cnf(component)  # Perform the Tseitin transformation on the component.
      
      # Append the resulting CNF clauses to the 'transformation' list.
      for clause in result:
        self.transformation.append(clause)
      
      self.max_literal += 1  # Increment the maximum literal value.
      self.aux_var_dict[self.max_literal] = self.aux_vars  # Store auxiliary variables in the dictionary.
    
    aux_result = self.aux_part()  # Generate auxiliary clauses.
    
    # Append the auxiliary clauses to the 'transformation' list.
    for result in aux_result:
        if result in self.transformation:
          self.transformation.remove(result)
          self.transformation.append(result)
        else:
          self.transformation.append(result)

  # Function to perform Tseitin transformation on a component.
  def to_cnf(self, component):
    literals = set()  # Initialize a set to store literals in the component.

    # Iterate through clauses in the component and collect literals.
    for clause in component:
      literals.update((abs(l) for l in clause))
    
    # Iterate through clauses in the component again.
    for clause in component:
      clause_copy = list(sorted(clause, key=abs))  # Create a sorted copy of the clause.
      clause = list(sorted(clause, key=abs))  # Sort the original clause by absolute value.
      next_clause = list()
      self.max_literal += 1  # Increment the maximum literal value.
      
      # Yield the first clause, which appends the negation of the new auxiliary variable.
      yield [*clause, -self.max_literal]
      
      for i in range(0, len(clause)):
          next_clause.append(clause[i])  # Append literals from the original clause.
      
      next_clause.append(self.max_literal)  # Append the new auxiliary variable.
      clause = next_clause
      
      # Yield clauses that connect the new auxiliary variable to the literals in the original clause.
      for i in clause_copy:
          yield [-i, clause[-1]]
      
      yield [self.max_literal]  # Yield the clause containing the new auxiliary variable.
      self.aux_vars.append(self.max_literal)  # Add the new auxiliary variable to the list.

# Function to generate auxiliary clauses based on the 'aux_var_dict.'
  def aux_part(self):
    for item in self.aux_var_dict.items():
      aux = item[0]  # Get the auxiliary variable.
      clauses = item[1]  # Get the list of clauses associated with the auxiliary variable.
      
      # Yield clauses that connect the auxiliary variable to its associated clauses.
      for clause in clauses:
          yield [clause, -aux]
      
      # Yield a clause that connects all clauses associated with the auxiliary variable to the variable itself.
      yield [-i for i in clauses] + [aux]
      yield [aux]  # Yield a clause containing only the auxiliary variable.
      
      aux = self.max_literal + 1
      or_clauses = list(self.aux_var_dict.keys())
      yield [*or_clauses]  # Yield a clause containing all auxiliary variables in 'aux_var_dict.'


