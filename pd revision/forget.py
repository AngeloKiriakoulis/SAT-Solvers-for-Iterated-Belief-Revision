import itertools
from cnf_converter import convert_to_cnf

def forget(V, P):
  """This function replaces the values in V based on P. It generates all combinations of True and False
  values for the variables in P using binary representation. For each combination, it iterates over V 
  and replaces the values based on the condition. If a value in the sublist (clause) matches a value in
  P, it assigns the corresponding combination value. If the value is negative, it flips the combination
  value. The function then checks for clauses (represented as CNF clauses in V) with only one True
  occurrence and removes them. Finally, it removes any False occurrences from the remaining clauses.
  The function returns a list of different result lists based on the combinations of True and False
  values in the condition list. That list represent the disjunction of non-empty clauses created by
  "forgotten" variables, from each T/F combination"""

  # Generate all combinations of True and False values for the P list
  combinations = list(itertools.product([False, True], repeat=len(P)))
  print(combinations)
  result_lists = []
  for combination in combinations:
    result_list = []
    for clause in V:
      clause_result = []
      for i in range(len(clause)):
        # Check if the clause value is present in the P list or its negation
        if abs(clause[i]) in P:
          value_index = P.index(abs(clause[i]))
          value = combination[value_index]
          # Handle negative values in the clause
          if clause[i] < 0:
            value = not value
          clause_result.append(value)
        else:
            clause_result.append(clause[i])

      # Check if the clause has only one True occurrence
      if clause_result.count(True) < 1:
        result_list.append(clause_result)
    # Check if any False occurrence should be removed from the result list
    result_list = [[value for value in clause if value is not False] for clause in result_list]
    if any(result_list):  # Only add non-empty result lists
      result_lists.append(result_list)
  return result_lists

# Example V
V = [[1, 2], [-1, 3], [-3, -2, -4]]
# Example P list
P = [1,4]

# Call the function to replace values in V based on P and get different lists
result_lists = forget(V, P)
# Print the different result lists
for i, result_list in enumerate(result_lists):
    print(f"Result List {i+1}:")
    print(result_list)

print(convert_to_cnf(result_lists))
